# Backend - Zerodha SDR Voice Agent

Python-based LiveKit agent that acts as a Sales Development Representative (SDR) for Zerodha, answering FAQ questions and capturing lead information.

**Part of**: [zerodha-sdr-voice-agent](https://github.com/Gangadhar-NG-CODER/zerodha-sdr-voice-agent)

---

## Quick Start

```bash
# Install dependencies
uv sync

# Configure environment
cp .env.example .env.local
# Edit .env.local with your API keys

# Download models
uv run python src/agent.py download-files

# Run agent
uv run python src/agent.py dev
```

---

## Environment Variables

Required in `.env.local`:

```bash
LIVEKIT_URL=ws://127.0.0.1:7880
LIVEKIT_API_KEY=devkey
LIVEKIT_API_SECRET=secret
MURF_API_KEY=your_murf_api_key
GOOGLE_API_KEY=your_google_api_key
ASSEMBLYAI_API_KEY=your_assemblyai_api_key
```

---

## Project Structure

```
backend/
├── shared-data/
│   ├── zerodha_company_info.json  # Company details
│   └── zerodha_faq.json           # FAQ database (25 entries)
├── leads/                          # Generated lead files
│   └── lead_TIMESTAMP.json        # Individual lead data
├── src/
│   ├── agent.py                   # Main SDR agent
│   └── __init__.py
├── .env.example                   # Environment template
└── pyproject.toml                 # Dependencies
```

---

## Features

### Primary Goal - Simple FAQ SDR + Lead Capture

✅ **Company**: Zerodha (India's largest stock broker)

✅ **SDR Persona**: Warm, professional sales representative

✅ **FAQ System**: 25 comprehensive FAQs covering:
  - Products (Kite, Coin, Console, Kite Connect, Varsity)
  - Pricing and charges
  - Account opening
  - Trading capabilities
  - Use cases and comparisons

✅ **Lead Capture**: Naturally collects:
  - Name
  - Company
  - Email
  - Role
  - Use case
  - Team size
  - Timeline (now/soon/later)

✅ **End-of-Call Summary**: 
  - Verbal summary of the conversation
  - JSON file with complete lead data
  - Stored in `leads/` directory

---

## How It Works

1. **Greeting**: Agent warmly greets visitor and asks what brought them
2. **Discovery**: Understands user needs through conversation
3. **FAQ Answering**: Uses `search_faq` tool to answer questions accurately
4. **Lead Collection**: Naturally collects information using `save_lead_field` tool
5. **Summary**: Detects conversation end and generates summary with `end_call_summary` tool

---

## Tools

The agent has 3 function tools:

### 1. search_faq(query)
Searches FAQ database using keyword matching

**Example:**
```python
search_faq("what are your charges")
# Returns: FAQ answer about Zerodha pricing
```

### 2. save_lead_field(field_name, field_value)
Stores lead information

**Supported fields:**
- name, company, email, role
- use_case, team_size, timeline

**Example:**
```python
save_lead_field("name", "Rahul Sharma")
save_lead_field("email", "rahul@techcorp.com")
```

### 3. end_call_summary()
Generates summary and saves lead to JSON

**Triggered by:** "That's all", "Thanks", "Goodbye"

**Output:** JSON file in `leads/` directory

---

## Lead Data Format

```json
{
  "timestamp": "2025-11-26T10:30:00",
  "lead_info": {
    "name": "Rahul Sharma",
    "company": "TechCorp",
    "email": "rahul@techcorp.com",
    "role": "Trader",
    "use_case": "Algorithmic trading using Kite Connect API",
    "team_size": "5-10",
    "timeline": "now"
  },
  "status": "complete"
}
```

---

## API Keys

Get free API keys from:
- **Murf Falcon**: https://murf.ai/api
- **Google Gemini**: https://ai.google.dev/
- **AssemblyAI**: https://www.assemblyai.com/

---

## Tech Stack

- Python 3.12
- LiveKit Agents 1.3.2
- Murf Falcon TTS (Matthew voice)
- AssemblyAI STT
- Google Gemini 2.5 Flash LLM
- Silero VAD

---

## Documentation

See the [main README](../README.md) for complete setup instructions.

---

**Part of the Murf AI Voice Agents Challenge - Day 5**

**GitHub**: https://github.com/Gangadhar-NG-CODER/zerodha-sdr-voice-agent
