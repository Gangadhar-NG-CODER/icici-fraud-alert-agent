import logging
import json
from pathlib import Path
from typing import Optional
from dataclasses import dataclass, field
from datetime import datetime

from dotenv import load_dotenv
from livekit.agents import (
    Agent,
    AgentSession,
    JobContext,
    JobProcess,
    MetricsCollectedEvent,
    RoomInputOptions,
    WorkerOptions,
    cli,
    metrics,
    tokenize,
    function_tool,
    RunContext,
)
from livekit.plugins import murf, silero, google, noise_cancellation, assemblyai
from livekit.plugins.turn_detector.multilingual import MultilingualModel

logger = logging.getLogger("agent")

load_dotenv(".env.local")

# Load company info and FAQ
company_info_path = Path(__file__).parent.parent / "shared-data" / "zerodha_company_info.json"
faq_path = Path(__file__).parent.parent / "shared-data" / "zerodha_faq.json"

with open(company_info_path, "r") as f:
    COMPANY_INFO = json.load(f)

with open(faq_path, "r") as f:
    FAQ_DATA = json.load(f)["faqs"]

# Create leads directory if it doesn't exist
leads_dir = Path(__file__).parent.parent / "leads"
leads_dir.mkdir(exist_ok=True)


@dataclass
class LeadInfo:
    """Store lead information collected during conversation"""
    name: Optional[str] = None
    company: Optional[str] = None
    email: Optional[str] = None
    role: Optional[str] = None
    use_case: Optional[str] = None
    team_size: Optional[str] = None
    timeline: Optional[str] = None  # now / soon / later
    
    def to_dict(self):
        return {
            "name": self.name,
            "company": self.company,
            "email": self.email,
            "role": self.role,
            "use_case": self.use_case,
            "team_size": self.team_size,
            "timeline": self.timeline
        }
    
    def is_complete(self):
        """Check if all essential fields are collected"""
        return all([
            self.name,
            self.email,
            self.use_case
        ])
    
    def get_missing_fields(self):
        """Return list of missing essential fields"""
        missing = []
        if not self.name:
            missing.append("name")
        if not self.email:
            missing.append("email")
        if not self.use_case:
            missing.append("use case")
        return missing


@dataclass
class Userdata:
    agent_session: Optional[AgentSession] = None
    lead_info: LeadInfo = field(default_factory=LeadInfo)
    conversation_started: bool = False


def prewarm(proc: JobProcess):
    """Prewarm function to load models before agent starts"""
    proc.userdata["vad"] = silero.VAD.load()
    logger.info("Prewarmed VAD model and loaded FAQ data")


def search_faq(query: str, top_k: int = 3) -> list:
    """Simple keyword-based FAQ search"""
    query_lower = query.lower()
    scored_faqs = []
    
    for faq in FAQ_DATA:
        score = 0
        # Check keywords
        for keyword in faq["keywords"]:
            if keyword in query_lower:
                score += 2
        
        # Check question
        question_words = faq["question"].lower().split()
        for word in query_lower.split():
            if len(word) > 3 and word in question_words:
                score += 1
        
        # Check answer
        answer_words = faq["answer"].lower().split()
        for word in query_lower.split():
            if len(word) > 3 and word in answer_words:
                score += 0.5
        
        if score > 0:
            scored_faqs.append((score, faq))
    
    # Sort by score and return top_k
    scored_faqs.sort(reverse=True, key=lambda x: x[0])
    return [faq for score, faq in scored_faqs[:top_k]]


class ZerodhaSdrAgent(Agent):
    def __init__(self) -> None:
        # Create company overview for context
        products_list = "\n".join([
            f"- {p['name']}: {p['description']}"
            for p in COMPANY_INFO["products"]
        ])
        
        pricing_summary = f"""
Pricing:
- Account Opening: {COMPANY_INFO['pricing']['account_opening']}
- Annual Maintenance: {COMPANY_INFO['pricing']['account_maintenance']}
- Equity Delivery: {COMPANY_INFO['pricing']['equity_delivery']}
- Intraday/F&O: {COMPANY_INFO['pricing']['equity_intraday']}
- Mutual Funds: {COMPANY_INFO['pricing']['mutual_funds']}
- Kite Connect API: {COMPANY_INFO['pricing']['kite_connect_api']}
"""
        
        super().__init__(
            instructions=f"""You are a friendly and professional Sales Development Representative (SDR) for Zerodha, India's largest stock broker.

**ABOUT ZERODHA:**
{COMPANY_INFO['overview']}

**OUR PRODUCTS:**
{products_list}

{pricing_summary}

**YOUR ROLE AS AN SDR:**

1. **WARM GREETING:**
   - Greet the visitor warmly and professionally
   - Simply say you're an SDR at Zerodha (don't use placeholder names)
   - Ask what brought them here today and what they're working on

2. **UNDERSTAND THEIR NEEDS:**
   - Listen carefully to understand their trading/investing needs
   - Ask clarifying questions about their use case
   - Keep the conversation focused and natural

3. **ANSWER QUESTIONS USING FAQ:**
   - When they ask about products, pricing, or features, use the search_faq tool
   - Answer based ONLY on the FAQ content - never make up information
   - If you don't find relevant information in FAQ, be honest and offer to connect them with the team

4. **COLLECT LEAD INFORMATION (VERY IMPORTANT):**
   - After answering their questions, ALWAYS ask for their contact information
   - You MUST collect these essential fields:
     * Name - Ask: "By the way, what's your name?"
     * Email - Ask: "What's the best email to reach you at?"
     * Use case - Ask: "What specifically are you looking to use Zerodha for?"
   - Also try to collect (if relevant):
     * Company - Ask: "Which company are you with?"
     * Role - Ask: "What's your role there?"
     * Team size - Ask: "How big is your team?"
     * Timeline - Ask: "When are you looking to get started?"
   - Use the save_lead_field tool IMMEDIATELY after they provide each piece of information
   - Be friendly and conversational, not like filling a form
   - Example: "That's great! By the way, what's your name?" then use save_lead_field("name", "their answer")

5. **DETECT CONVERSATION END:**
   - Listen for signals that the user is done: "that's all", "thanks", "goodbye", "I'm done", etc.
   - When you detect they're wrapping up, use the end_call_summary tool
   - This will generate a summary and save the lead information

**CONVERSATION STYLE:**
- Be warm, friendly, and professional
- Speak naturally - you're having a conversation, not reading a script
- Show genuine interest in helping them
- Be concise but informative
- If they seem interested, gently guide them toward next steps (account opening, demo, etc.)

**IMPORTANT RULES:**
- NEVER make up information not in the FAQ
- ALWAYS use search_faq tool when answering product/pricing questions
- ALWAYS ask for at least name, email, and use case - this is mandatory
- Use save_lead_field tool IMMEDIATELY after they provide each piece of information
- When conversation ends, use end_call_summary tool

**MANDATORY CONVERSATION FLOW:**
1. Greet and ask what brought them here
2. Answer their FAQ questions using search_faq tool
3. After answering 2-3 questions, YOU MUST ask for ALL these fields IN ORDER:
   - "By the way, what's your name?" → use save_lead_field("name", answer)
   - "What's the best email to reach you at?" → use save_lead_field("email", answer)
   - "Which company are you with?" → use save_lead_field("company", answer)
   - "What's your role there?" → use save_lead_field("role", answer)
   - "What specifically are you looking to use Zerodha for?" → use save_lead_field("use_case", answer)
   - "How big is your team?" → use save_lead_field("team_size", answer)
   - "When are you looking to get started?" → use save_lead_field("timeline", answer)
4. After collecting ALL 7 fields, wait for them to say "that's all" or "thanks"
5. Then use end_call_summary tool

CRITICAL: You MUST ask for ALL 7 fields - name, email, company, role, use_case, team_size, timeline. Do NOT skip any!"""
        )

    @function_tool
    async def search_faq(
        self,
        context: RunContext[Userdata],
        query: str
    ) -> str:
        """Search the FAQ database for relevant answers to user questions.
        
        Use this tool whenever the user asks about:
        - What Zerodha does
        - Products (Kite, Coin, Console, Kite Connect, Varsity)
        - Pricing and charges
        - Account opening process
        - Trading capabilities
        - Technical requirements
        - Any other product or service questions
        
        Args:
            query: The user's question or topic they're asking about
        """
        logger.info(f"Searching FAQ for: {query}")
        
        results = search_faq(query, top_k=2)
        
        if not results:
            return "I don't have specific information about that in my knowledge base. Let me connect you with our team who can provide detailed information. Could you share your email so we can follow up?"
        
        # Format the answer
        answer_parts = []
        for faq in results:
            answer_parts.append(faq["answer"])
        
        combined_answer = " ".join(answer_parts)
        logger.info(f"Found {len(results)} relevant FAQ entries")
        
        return combined_answer

    @function_tool
    async def save_lead_field(
        self,
        context: RunContext[Userdata],
        field_name: str,
        field_value: str
    ) -> str:
        """Save a piece of lead information that you've collected during the conversation.
        
        Use this tool to store lead details as you learn them naturally during conversation.
        
        Args:
            field_name: The type of information (must be one of: name, company, email, role, use_case, team_size, timeline)
            field_value: The actual value/information provided by the user
        """
        lead_info = context.userdata.lead_info
        
        field_name = field_name.lower().strip()
        
        # Map field names to LeadInfo attributes
        if field_name in ["name", "full name", "your name"]:
            lead_info.name = field_value
            logger.info(f"Saved lead name: {field_value}")
            return f"Got it, {field_value}!"
            
        elif field_name in ["company", "organization", "firm"]:
            lead_info.company = field_value
            logger.info(f"Saved lead company: {field_value}")
            return f"Great, {field_value}."
            
        elif field_name in ["email", "email address", "email id"]:
            lead_info.email = field_value
            logger.info(f"Saved lead email: {field_value}")
            return f"Perfect, I've noted down {field_value}."
            
        elif field_name in ["role", "designation", "position", "job title"]:
            lead_info.role = field_value
            logger.info(f"Saved lead role: {field_value}")
            return f"Understood, you're a {field_value}."
            
        elif field_name in ["use_case", "use case", "purpose", "need", "requirement"]:
            lead_info.use_case = field_value
            logger.info(f"Saved lead use case: {field_value}")
            return "That's helpful context, thank you."
            
        elif field_name in ["team_size", "team size", "team", "size"]:
            lead_info.team_size = field_value
            logger.info(f"Saved lead team size: {field_value}")
            return "Got it."
            
        elif field_name in ["timeline", "when", "timeframe", "urgency"]:
            # Normalize timeline to now/soon/later
            value_lower = field_value.lower()
            if any(word in value_lower for word in ["now", "immediate", "asap", "today", "this week"]):
                lead_info.timeline = "now"
            elif any(word in value_lower for word in ["soon", "next week", "next month", "couple weeks"]):
                lead_info.timeline = "soon"
            else:
                lead_info.timeline = "later"
            logger.info(f"Saved lead timeline: {lead_info.timeline}")
            return "Understood."
        
        else:
            return f"I've noted that information."

    @function_tool
    async def end_call_summary(
        self,
        context: RunContext[Userdata]
    ) -> str:
        """Generate end-of-call summary and save lead information.
        
        Use this tool when you detect the conversation is ending, such as when the user says:
        - "That's all"
        - "Thanks"
        - "Goodbye"
        - "I'm done"
        - "That's it"
        - Or any other closing statement
        """
        lead_info = context.userdata.lead_info
        
        # Generate timestamp for filename
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        lead_filename = leads_dir / f"lead_{timestamp}.json"
        
        # Prepare lead data
        lead_data = {
            "timestamp": datetime.now().isoformat(),
            "lead_info": lead_info.to_dict(),
            "status": "complete" if lead_info.is_complete() else "partial"
        }
        
        # Save to JSON file
        with open(lead_filename, "w") as f:
            json.dump(lead_data, f, indent=2)
        
        logger.info(f"Saved lead to {lead_filename}")
        
        # Generate verbal summary
        summary_parts = []
        
        if lead_info.name:
            summary_parts.append(f"I've been speaking with {lead_info.name}")
        
        if lead_info.role and lead_info.company:
            summary_parts.append(f"who is a {lead_info.role} at {lead_info.company}")
        elif lead_info.role:
            summary_parts.append(f"who is a {lead_info.role}")
        elif lead_info.company:
            summary_parts.append(f"from {lead_info.company}")
        
        if lead_info.use_case:
            summary_parts.append(f"They're interested in {lead_info.use_case}")
        
        if lead_info.timeline:
            if lead_info.timeline == "now":
                summary_parts.append("and they're looking to get started right away")
            elif lead_info.timeline == "soon":
                summary_parts.append("and they're planning to start soon")
            else:
                summary_parts.append("and they're in the exploration phase")
        
        if summary_parts:
            verbal_summary = ". ".join(summary_parts) + "."
        else:
            verbal_summary = "Thank you for your interest in Zerodha."
        
        # Add closing message
        closing = " Our team will reach out to you shortly"
        if lead_info.email:
            closing += f" at {lead_info.email}"
        closing += ". Have a great day!"
        
        full_summary = verbal_summary + closing
        
        logger.info(f"Generated summary: {full_summary}")
        
        return full_summary


async def entrypoint(ctx: JobContext):
    # Logging setup
    ctx.log_context_fields = {
        "room": ctx.room,
    }

    # Initialize userdata
    userdata = Userdata()

    # Create session
    session = AgentSession(
        stt=assemblyai.STT(),
        llm=google.LLM(model="gemini-2.5-flash"),
        tts=murf.TTS(
            voice="en-US-matthew",
            style="Conversation",
            tokenizer=tokenize.basic.SentenceTokenizer(min_sentence_len=2),
            text_pacing=True
        ),
        turn_detection=MultilingualModel(),
        vad=ctx.proc.userdata["vad"],
        preemptive_generation=True,
        userdata=userdata,
    )

    # Store session in userdata
    userdata.agent_session = session

    # Metrics collection
    usage_collector = metrics.UsageCollector()

    @session.on("metrics_collected")
    def _on_metrics_collected(ev: MetricsCollectedEvent):
        metrics.log_metrics(ev.metrics)
        usage_collector.collect(ev.metrics)

    async def log_usage():
        summary = usage_collector.get_summary()
        logger.info(f"Usage: {summary}")

    ctx.add_shutdown_callback(log_usage)

    # Start session
    await session.start(
        agent=ZerodhaSdrAgent(),
        room=ctx.room,
        room_input_options=RoomInputOptions(
            noise_cancellation=noise_cancellation.BVC(),
        ),
    )

    # Join the room
    await ctx.connect()


if __name__ == "__main__":
    cli.run_app(WorkerOptions(entrypoint_fnc=entrypoint, prewarm_fnc=prewarm))
