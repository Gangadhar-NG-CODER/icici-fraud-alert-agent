import logging
import json
from pathlib import Path
from typing import Optional
from dataclasses import dataclass
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

# Load fraud cases database
fraud_cases_path = Path(__file__).parent.parent / "fraud-data" / "fraud_cases.json"

with open(fraud_cases_path, "r") as f:
    FRAUD_DATABASE = json.load(f)

# Create fraud-data directory if it doesn't exist
fraud_data_dir = Path(__file__).parent.parent / "fraud-data"
fraud_data_dir.mkdir(exist_ok=True)


@dataclass
class FraudCase:
    """Store fraud case information"""
    userName: str
    securityIdentifier: str
    securityQuestion: str
    securityAnswer: str
    cardEnding: str
    case: str
    transactionAmount: str
    transactionName: str
    transactionTime: str
    transactionCategory: str
    transactionSource: str
    transactionLocation: str
    verification_status: Optional[str] = None
    outcome_note: Optional[str] = None
    
    def to_dict(self):
        return {
            "userName": self.userName,
            "securityIdentifier": self.securityIdentifier,
            "securityQuestion": self.securityQuestion,
            "securityAnswer": self.securityAnswer,
            "cardEnding": self.cardEnding,
            "case": self.case,
            "transactionAmount": self.transactionAmount,
            "transactionName": self.transactionName,
            "transactionTime": self.transactionTime,
            "transactionCategory": self.transactionCategory,
            "transactionSource": self.transactionSource,
            "transactionLocation": self.transactionLocation,
            "verification_status": self.verification_status,
            "outcome_note": self.outcome_note
        }


@dataclass
class Userdata:
    agent_session: Optional[AgentSession] = None
    fraud_case: Optional[FraudCase] = None
    conversation_started: bool = False
    verification_passed: bool = False


def prewarm(proc: JobProcess):
    """Prewarm function to load models before agent starts"""
    proc.userdata["vad"] = silero.VAD.load()
    logger.info("Prewarmed VAD model and loaded fraud cases database")


def load_fraud_case(username: str) -> Optional[dict]:
    """Load fraud case from database by username"""
    for case in FRAUD_DATABASE["cases"]:
        if case["userName"].lower() == username.lower():
            return case
    return None


def save_fraud_database():
    """Save updated fraud database back to JSON file"""
    with open(fraud_cases_path, "w") as f:
        json.dump(FRAUD_DATABASE, f, indent=2)
    logger.info("Saved updated fraud database")


class FraudAlertAgent(Agent):
    def __init__(self) -> None:
        super().__init__(
            instructions="""You are a professional Fraud Detection Representative for ICICI Bank, calling customers about suspicious transactions on their accounts.

**YOUR ROLE:**

You are contacting customers about potentially fraudulent transactions. Your job is to:
1. Introduce yourself professionally
2. Ask for the customer's name to load their case
3. Verify their identity using a security question
4. Inform them about the suspicious transaction
5. Ask if they authorized it
6. Take appropriate action based on their response

**CONVERSATION FLOW:**

**STEP 1 - INTRODUCTION:**
- Greet professionally: "Hello, this is the ICICI Bank Fraud Detection Department."
- Explain purpose: "We're calling about a suspicious transaction on your account."
- Ask for their name: "May I have your name please?"
- Use load_fraud_case tool with their name

**STEP 2 - VERIFICATION:**
- Once case is loaded, say: "For security purposes, I need to verify your identity."
- Ask the security question from the loaded case
- Use verify_customer tool with their answer
- If verification fails: Politely end the call saying you cannot proceed without verification
- If verification passes: Continue to transaction details

**STEP 3 - TRANSACTION DETAILS:**
- Read out the suspicious transaction clearly:
  * "We detected a transaction on your card ending in [cardEnding]"
  * "Amount: [transactionAmount]"
  * "Merchant: [transactionName]"
  * "Location: [transactionLocation]"
  * "Time: [transactionTime]"
  * "Source: [transactionSource]"

**STEP 4 - CONFIRMATION:**
- Ask directly: "Did you authorize this transaction?"
- Listen for clear yes or no
- Use mark_transaction tool with their response:
  * If they say YES → mark as "safe"
  * If they say NO → mark as "fraudulent"

**STEP 5 - RESOLUTION:**
- If marked safe: "Thank you for confirming. We've marked this transaction as legitimate. Your card remains active."
- If marked fraudulent: "I understand. We've immediately blocked your card ending in [cardEnding] and will issue a replacement. A dispute has been filed and you will not be charged for this transaction."
- End professionally: "Is there anything else I can help you with regarding this matter?"
- When they're done, use end_fraud_call tool

**IMPORTANT RULES:**
- NEVER ask for full card numbers, PINs, or passwords
- Be calm, professional, and reassuring
- Speak clearly when reading transaction details
- Wait for clear confirmation before marking the case
- Always use the tools in the correct order
- Keep the conversation focused on the fraud case

**SECURITY:**
- Only verify using the security question from the database
- Never ask for sensitive information
- If customer seems confused or uncertain, offer to call back

**TONE:**
- Professional but warm
- Calm and reassuring
- Clear and direct
- Patient and understanding"""
        )

    @function_tool
    async def load_fraud_case(
        self,
        context: RunContext[Userdata],
        username: str
    ) -> str:
        """Load a fraud case from the database using the customer's name.
        
        Use this tool immediately after the customer provides their name.
        This will load their fraud case details into memory.
        
        Args:
            username: The customer's name as they provided it
        """
        logger.info(f"Loading fraud case for: {username}")
        
        case_data = load_fraud_case(username)
        
        if not case_data:
            logger.warning(f"No fraud case found for username: {username}")
            return f"I apologize, but I don't see any fraud alert for the name {username}. Could you please verify the name on the account?"
        
        # Create FraudCase object and store in context
        fraud_case = FraudCase(**case_data)
        context.userdata.fraud_case = fraud_case
        
        logger.info(f"Loaded fraud case for {username}: Card ending {fraud_case.cardEnding}")
        
        return f"Thank you, {username}. I have your account information here. For security purposes, I need to verify your identity before we proceed. {fraud_case.securityQuestion}"

    @function_tool
    async def verify_customer(
        self,
        context: RunContext[Userdata],
        answer: str
    ) -> str:
        """Verify the customer's identity using their answer to the security question.
        
        Use this tool after asking the security question from the loaded fraud case.
        This will check if their answer matches the expected answer.
        
        Args:
            answer: The customer's answer to the security question
        """
        fraud_case = context.userdata.fraud_case
        
        if not fraud_case:
            return "I apologize, but I need to load your case first. Could you please provide your name?"
        
        logger.info(f"Verifying customer answer for {fraud_case.userName}")
        
        # Simple case-insensitive comparison
        if answer.lower().strip() == fraud_case.securityAnswer.lower().strip():
            context.userdata.verification_passed = True
            logger.info(f"Verification PASSED for {fraud_case.userName}")
            return "Thank you for verifying your identity. Now, let me tell you about the suspicious transaction we detected."
        else:
            context.userdata.verification_passed = False
            logger.warning(f"Verification FAILED for {fraud_case.userName}")
            return "I'm sorry, but that answer doesn't match our records. For your security, I cannot proceed without proper verification. Please contact ICICI Bank directly at 1-800-ICICI-BANK. Goodbye."

    @function_tool
    async def mark_transaction(
        self,
        context: RunContext[Userdata],
        status: str
    ) -> str:
        """Mark the transaction as safe or fraudulent based on customer confirmation.
        
        Use this tool after the customer clearly confirms whether they made the transaction.
        
        Args:
            status: Either "safe" (customer confirmed they made it) or "fraudulent" (customer denies making it)
        """
        fraud_case = context.userdata.fraud_case
        
        if not fraud_case:
            return "I apologize, but I don't have a case loaded. Please provide your name first."
        
        if not context.userdata.verification_passed:
            return "I cannot update the case without proper verification."
        
        status = status.lower().strip()
        
        if status == "safe":
            fraud_case.case = "confirmed_safe"
            fraud_case.verification_status = "verified"
            fraud_case.outcome_note = f"Customer {fraud_case.userName} confirmed the transaction as legitimate on {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
            
            # Update database
            for case in FRAUD_DATABASE["cases"]:
                if case["userName"] == fraud_case.userName:
                    case["case"] = fraud_case.case
                    case["verification_status"] = fraud_case.verification_status
                    case["outcome_note"] = fraud_case.outcome_note
                    break
            
            save_fraud_database()
            logger.info(f"Marked transaction as SAFE for {fraud_case.userName}")
            
            return f"Thank you for confirming. I've marked this transaction as legitimate in our system. Your card ending in {fraud_case.cardEnding} remains active and no further action is needed."
            
        elif status == "fraudulent":
            fraud_case.case = "confirmed_fraud"
            fraud_case.verification_status = "verified"
            fraud_case.outcome_note = f"Customer {fraud_case.userName} denied the transaction. Card blocked and dispute filed on {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
            
            # Update database
            for case in FRAUD_DATABASE["cases"]:
                if case["userName"] == fraud_case.userName:
                    case["case"] = fraud_case.case
                    case["verification_status"] = fraud_case.verification_status
                    case["outcome_note"] = fraud_case.outcome_note
                    break
            
            save_fraud_database()
            logger.info(f"Marked transaction as FRAUDULENT for {fraud_case.userName}")
            
            return f"I understand. I've immediately blocked your card ending in {fraud_case.cardEnding}. A replacement card will be mailed to you within 5-7 business days. We've also filed a dispute for the {fraud_case.transactionAmount} charge, and you will not be held responsible for this fraudulent transaction."
        
        else:
            return "I need a clear confirmation. Did you make this transaction - yes or no?"

    @function_tool
    async def end_fraud_call(
        self,
        context: RunContext[Userdata]
    ) -> str:
        """End the fraud alert call with a professional closing.
        
        Use this tool when the customer indicates they're done or have no more questions.
        """
        fraud_case = context.userdata.fraud_case
        
        if fraud_case:
            logger.info(f"Ending fraud call for {fraud_case.userName}. Final status: {fraud_case.case}")
            
            if fraud_case.case == "confirmed_safe":
                return "You're all set. Thank you for your time, and have a great day. Goodbye."
            elif fraud_case.case == "confirmed_fraud":
                return "We've taken care of everything. You're protected. If you have any questions, please call our fraud department at 1-800-SECURE-BANK. Have a great day. Goodbye."
            else:
                return "Thank you for your time. If you have any concerns, please contact us at 1-800-ICICI-BANK. Goodbye."
        else:
            return "Thank you for calling ICICI Bank. Goodbye."


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
        agent=FraudAlertAgent(),
        room=ctx.room,
        room_input_options=RoomInputOptions(
            noise_cancellation=noise_cancellation.BVC(),
        ),
    )

    # Join the room
    await ctx.connect()


if __name__ == "__main__":
    cli.run_app(WorkerOptions(entrypoint_fnc=entrypoint, prewarm_fnc=prewarm))
