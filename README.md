# 🎙️ Zerodha SDR Voice Agent

An AI-powered Sales Development Representative (SDR) voice agent for Zerodha that answers FAQ questions and captures lead information through natural conversation. Built to demonstrate intelligent lead qualification and data collection in voice interactions.

**Built for the Murf AI Voice Agents Challenge - Day 5**

[![GitHub](https://img.shields.io/badge/GitHub-zerodha--sdr--voice--agent-blue?logo=github)](https://github.com/Gangadhar-NG-CODER/zerodha-sdr-voice-agent)

---

## ✨ Features

### Primary Goal - Simple FAQ SDR + Lead Capture

✅ **Company**: Zerodha (India's largest stock broker)

✅ **SDR Persona**: 
- Warm and professional greeting
- Natural conversation flow
- Focused on understanding user needs
- Intelligent lead qualification

✅ **FAQ System**: 
- 25 comprehensive FAQs covering all aspects of Zerodha
- Keyword-based search for accurate answers
- Products: Kite, Coin, Console, Kite Connect, Varsity
- Pricing, account opening, trading capabilities
- No hallucination - answers only from FAQ database

✅ **Lead Capture**:
Naturally collects during conversation:
- Name
- Company
- Email
- Role/Designation
- Use case (what they need Zerodha for)
- Team size
- Timeline (now/soon/later)

✅ **End-of-Call Summary**:
- Verbal summary of the lead
- JSON file with complete lead data
- Stored in `backend/leads/` directory
- Timestamp-based file naming

---

## 🛠️ Tech Stack

- **TTS**: Murf Falcon (fastest text-to-speech API)
- **STT**: AssemblyAI (high-accuracy speech recognition)
- **LLM**: Google Gemini 2.5 Flash
- **Framework**: LiveKit Agents
- **Frontend**: Next.js 15 + React 19
- **Backend**: Python 3.12
- **Styling**: Tailwind CSS

---

## 🚀 Quick Start

### Prerequisites

- Python 3.9+ with [uv](https://docs.astral.sh/uv/) package manager
- Node.js 18+ with pnpm
- [LiveKit Server](https://github.com/livekit/livekit/releases)

### 1. Clone Repository

```bash
git clone https://github.com/Gangadhar-NG-CODER/zerodha-sdr-voice-agent.git
cd zerodha-sdr-voice-agent
```

### 2. Get API Keys

You'll need free API keys from:
- **Murf Falcon**: https://murf.ai/api
- **Google Gemini**: https://ai.google.dev/
- **AssemblyAI**: https://www.assemblyai.com/

### 3. Backend Setup

```bash
cd backend

# Install dependencies
uv sync

# Copy and configure environment
cp .env.example .env.local

# Edit .env.local with your API keys:
# LIVEKIT_URL=ws://127.0.0.1:7880
# LIVEKIT_API_KEY=devkey
# LIVEKIT_API_SECRET=secret
# MURF_API_KEY=your_murf_api_key
# GOOGLE_API_KEY=your_google_api_key
# ASSEMBLYAI_API_KEY=your_assemblyai_api_key

# Download required models
uv run python src/agent.py download-files
```

### 4. Frontend Setup

```bash
cd frontend

# Install dependencies
pnpm install

# Copy and configure environment
cp .env.example .env.local

# Edit .env.local:
# LIVEKIT_API_KEY=devkey
# LIVEKIT_API_SECRET=secret
# LIVEKIT_URL=ws://127.0.0.1:7880
```

### 5. Run the Application

**Terminal 1 - LiveKit Server:**
```bash
# Download from: https://github.com/livekit/livekit/releases
livekit-server --dev
```

**Terminal 2 - Backend:**
```bash
cd backend
uv run python src/agent.py dev
```

**Terminal 3 - Frontend:**
```bash
cd frontend
pnpm dev
```

Open **http://localhost:3000** in your browser! 🎉

---

## 💡 How to Use

1. Click "Talk to SDR" to start the conversation
2. The SDR will greet you warmly and ask what brought you here
3. Have a natural conversation:
   - Ask about Zerodha products: "What is Kite?"
   - Ask about pricing: "What are your charges?"
   - Ask about use cases: "Can I do algo trading?"
4. The agent will naturally ask for your details during conversation
5. When you're done, say "That's all" or "Thanks" to end the call
6. The agent will provide a summary and save your lead information

---

## 📁 Project Structure

```
zerodha-sdr-voice-agent/
├── backend/
│   ├── shared-data/
│   │   ├── zerodha_company_info.json  # Company details
│   │   └── zerodha_faq.json           # 25 FAQ entries
│   ├── leads/                          # Generated lead files
│   │   └── lead_TIMESTAMP.json        # Individual leads
│   ├── src/
│   │   ├── agent.py                   # Main SDR agent
│   │   └── __init__.py
│   ├── .env.example
│   ├── pyproject.toml
│   └── README.md
├── frontend/
│   ├── app/
│   ├── components/
│   ├── styles/
│   ├── .env.example
│   ├── package.json
│   └── README.md
├── DEMO_SCRIPT.md                      # Video recording guide
├── TESTING_GUIDE.md                    # Testing scenarios
├── .gitignore
└── README.md
```

---

## 🎯 Agent Tools

The SDR agent has 3 function tools:

### 1. search_faq(query)
Searches the FAQ database using keyword matching to find relevant answers.

**Example usage:**
- User: "What does Zerodha do?"
- Agent calls: `search_faq("what does zerodha do")`
- Returns: Relevant FAQ answer

### 2. save_lead_field(field_name, field_value)
Stores lead information as it's collected during conversation.

**Supported fields:**
- name, company, email, role
- use_case, team_size, timeline

**Example usage:**
- User: "My name is Rahul"
- Agent calls: `save_lead_field("name", "Rahul")`

### 3. end_call_summary()
Generates verbal summary and saves lead to JSON file.

**Triggered when user says:**
- "That's all", "Thanks", "Goodbye", "I'm done"

**Output:**
- Verbal summary of the conversation
- JSON file in `backend/leads/` directory

---

## 📊 Lead Data Format

```json
{
  "timestamp": "2025-11-26T10:30:00",
  "lead_info": {
    "name": "Rahul Sharma",
    "company": "TechCorp",
    "email": "rahul@techcorp.com",
    "role": "Algo Trader",
    "use_case": "Algorithmic trading using Kite Connect API",
    "team_size": "5-10 people",
    "timeline": "now"
  },
  "status": "complete"
}
```

---

## 🏢 About Zerodha

**Company**: Zerodha  
**Founded**: 2010  
**Headquarters**: Bangalore, India  
**Founders**: Nithin Kamath, Nikhil Kamath

**Products**:
- **Kite**: Trading platform (web, mobile, desktop)
- **Coin**: Direct mutual fund investment platform
- **Console**: Back-office and reports
- **Kite Connect**: Trading APIs for developers
- **Varsity**: Free educational content

**Pricing Highlights**:
- Zero brokerage on equity delivery
- Flat ₹20 per order for intraday/F&O
- Zero commission on mutual funds
- ₹2000/month for Kite Connect API

---

## 🔧 Technical Implementation

### FAQ Search Algorithm
Simple but effective keyword-based search:
1. Matches keywords in FAQ entries
2. Scores based on question and answer relevance
3. Returns top 2 most relevant FAQs
4. Combines answers for comprehensive response

### Lead State Management
Uses dataclass to track lead information:
- Stores in agent context during conversation
- Validates completeness before saving
- Generates timestamp-based filenames
- Saves to JSON with proper formatting

### Conversation Flow
1. **Greeting** → Warm introduction
2. **Discovery** → Understand needs
3. **FAQ Answering** → Use search_faq tool
4. **Lead Collection** → Use save_lead_field tool
5. **Summary** → Use end_call_summary tool

---

## 📝 Testing

See `TESTING_GUIDE.md` for detailed testing scenarios and verification checklist.

---

## 🎬 Demo Recording

See `DEMO_SCRIPT.md` for a complete guide on recording your demo video.

---

## 📝 License

MIT License - See LICENSE file for details

---

## 🙏 Acknowledgments

- Built for the **Murf AI Voice Agents Challenge - Day 5**
- Powered by **Murf Falcon TTS** - The fastest text-to-speech API
- Based on [LiveKit Agents](https://docs.livekit.io/agents)
- Company data: Zerodha (India's largest stock broker)

---

## 🔗 Links

- **GitHub Repository**: https://github.com/Gangadhar-NG-CODER/zerodha-sdr-voice-agent
- [Murf Falcon Documentation](https://murf.ai/api/docs/text-to-speech/streaming)
- [LiveKit Agents Documentation](https://docs.livekit.io/agents)
- [AssemblyAI Documentation](https://www.assemblyai.com/docs)

---

## 📱 Social Media

Part of the **#MurfAIVoiceAgentsChallenge** • **#10DaysofAIVoiceAgents**

---

**Built with ❤️ by Gangadhar for the Murf AI Voice Agents Challenge**
