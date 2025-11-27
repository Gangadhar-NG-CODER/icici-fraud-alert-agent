# ICICI Bank Fraud Alert Agent - Backend (Python with Murf Falcon TTS)

🎙️ **This is part of the AI Voice Agents Challenge by murf.ai - Day 6**

This backend is configured to use **Murf Falcon** - the consistently fastest TTS API - for ultra-fast voice synthesis in fraud detection scenarios.

A complete fraud detection voice agent built with LiveKit Agents for Python and LiveKit Cloud.

## 🎯 What This Agent Does

The ICICI Bank Fraud Alert Agent:
- **Loads fraud cases** by customer name from a JSON database
- **Verifies customer identity** using security questions
- **Reads suspicious transaction details** clearly and professionally
- **Confirms or denies fraud** based on customer response
- **Updates the database** in real-time with case outcomes
- **Handles three scenarios**: confirmed_safe, confirmed_fraud, verification_failed

## 🛠️ Tech Stack

- **TTS**: Murf Falcon (fastest text-to-speech API)
- **STT**: AssemblyAI (high-accuracy speech recognition)
- **LLM**: Google Gemini 2.5 Flash
- **Framework**: LiveKit Agents
- **Database**: JSON file storage
- **VAD**: Silero VAD
- **Turn Detection**: LiveKit Multilingual Turn Detector

## 📁 Project Structure

```
backend/
├── src/
│   ├── agent.py              # Main fraud detection agent
│   └── __init__.py
├── fraud-data/
│   └── fraud_cases.json      # Fraud cases database (5 test cases)
├── .env.example              # Environment template
├── .env.local                # Your API keys (not tracked)
├── pyproject.toml            # Python dependencies
└── README.md                 # This file
```

## 🚀 Dev Setup

### 1. Install Dependencies

```bash
cd backend
uv sync
```

### 2. Set Up Environment

Copy `.env.example` to `.env.local` and fill in your API keys:

```bash
cp .env.example .env.local
```

Required keys:
- `LIVEKIT_URL` - LiveKit server URL (default: ws://127.0.0.1:7880)
- `LIVEKIT_API_KEY` - LiveKit API key (default: devkey)
- `LIVEKIT_API_SECRET` - LiveKit API secret (default: secret)
- `MURF_API_KEY` - Your Murf Falcon API key
- `GOOGLE_API_KEY` - Your Google Gemini API key
- `ASSEMBLYAI_API_KEY` - Your AssemblyAI API key

**Get API Keys:**
- Murf Falcon: https://murf.ai/api
- Google Gemini: https://ai.google.dev/
- AssemblyAI: https://www.assemblyai.com/

### 3. Download Required Models

Before your first run, download models like Silero VAD:

```bash
uv run python src/agent.py download-files
```

## 🎤 Run the Agent

### Development Mode (with auto-reload)

```bash
uv run python src/agent.py dev
```

This will:
- Start the agent
- Watch for file changes
- Auto-reload on code updates
- Connect to LiveKit server at ws://127.0.0.1:7880

### Console Mode (terminal testing)

```bash
uv run python src/agent.py console
```

Speak to your agent directly in the terminal for quick testing.

### Production Mode

```bash
uv run python src/agent.py start
```

## 🗄️ Fraud Cases Database

Located at `fraud-data/fraud_cases.json`

### Structure

```json
{
  "cases": [
    {
      "userName": "John",
      "securityIdentifier": "12345",
      "securityQuestion": "What is your mother's maiden name?",
      "securityAnswer": "Smith",
      "cardEnding": "4242",
      "case": "pending_review",
      "transactionAmount": "$1,247.99",
      "transactionName": "ABC Industry",
      "transactionTime": "November 26, 2025 at 11:45 PM",
      "transactionCategory": "e-commerce",
      "transactionSource": "alibaba.com",
      "transactionLocation": "Shanghai, China"
    }
  ]
}
```

### Test Users

| Username | Security Answer | Card Ending |
|----------|----------------|-------------|
| John | Smith | 4242 |
| Sarah | Boston | 8765 |
| Michael | Buddy | 1357 |
| Emily | Blue | 9876 |
| David | Oak Street | 5432 |

### Case Statuses

- `pending_review` - Initial state
- `confirmed_safe` - Customer authorized the transaction
- `confirmed_fraud` - Customer denied, card blocked
- `verification_failed` - Security verification failed

## 🔧 Agent Tools

The fraud detection agent has 4 function tools:

### 1. load_fraud_case(username)
Loads a fraud case from the database by customer name.

### 2. verify_customer(answer)
Verifies customer identity using their security question answer.

### 3. mark_transaction(status)
Marks the transaction as "safe" or "fraudulent" and updates the database.

### 4. end_fraud_call()
Ends the call with appropriate closing message.

## 🎯 Conversation Flow

1. **Introduction** → "Hello, this is the ICICI Bank Fraud Detection Department"
2. **Name Collection** → "May I have your name please?"
3. **Load Case** → `load_fraud_case(username)`
4. **Security Question** → Ask question from database
5. **Verification** → `verify_customer(answer)`
6. **Transaction Details** → Read all details clearly
7. **Confirmation** → "Did you authorize this transaction?"
8. **Mark Status** → `mark_transaction("safe" or "fraudulent")`
9. **Resolution** → Explain action taken
10. **End Call** → `end_fraud_call()`

## 🧪 Testing

Test all three scenarios:

### Scenario 1: Confirmed Safe
- User: "John"
- Security: "Smith"
- Response: "Yes"
- Result: `confirmed_safe`

### Scenario 2: Confirmed Fraud
- User: "Sarah"
- Security: "Boston"
- Response: "No"
- Result: `confirmed_fraud`, card blocked

### Scenario 3: Verification Failed
- User: "Michael"
- Wrong security answer
- Result: Call ends, no disclosure

## 📊 Database Updates

The agent automatically updates `fraud_cases.json` when:
- Transaction is marked as safe or fraudulent
- Adds `verification_status` field
- Adds `outcome_note` with timestamp and details

Check the file after each test to verify updates.

## 🔒 Security Features

- Never asks for full card numbers or PINs
- Uses non-sensitive security questions
- Verification required before disclosure
- Clear audit trail in database
- Professional handling of failed verification

## 🌐 Frontend Integration

This backend works with the Next.js frontend in the `frontend/` folder.

To connect:
1. Start LiveKit server: `livekit-server --dev`
2. Start this backend: `uv run python src/agent.py dev`
3. Start frontend: `cd ../frontend && pnpm dev`
4. Open http://localhost:3000

## 📚 Documentation

- [LiveKit Agents Documentation](https://docs.livekit.io/agents)
- [Murf Falcon API Docs](https://murf.ai/api/docs/text-to-speech/streaming)
- [AssemblyAI Documentation](https://www.assemblyai.com/docs)
- [Google Gemini Documentation](https://ai.google.dev/)

## 🐛 Troubleshooting

### Agent won't start
- Check all API keys in `.env.local`
- Verify LiveKit server is running
- Run `uv run python src/agent.py download-files`

### Can't connect to LiveKit
- Ensure LiveKit server is running on port 7880
- Check `LIVEKIT_URL` in `.env.local`
- Try: `livekit-server --dev`

### Database not updating
- Check file permissions on `fraud-data/fraud_cases.json`
- Verify JSON syntax is valid
- Check backend console for errors

### Wrong security question
- The agent should ask the question from the database
- If not, check that `load_fraud_case` tool is being called
- Verify the fraud case was loaded successfully

## 🚀 Deploying to Production

This project is production-ready and includes a working Dockerfile.

To deploy to LiveKit Cloud or another environment, see the [deploying to production guide](https://docs.livekit.io/agents/deployment/).

## 📝 License

This project is licensed under the MIT License - see the LICENSE file for details.

---

**Built with ❤️ for the Murf AI Voice Agents Challenge - Day 6**

**Powered by Murf Falcon TTS** 🎙️
