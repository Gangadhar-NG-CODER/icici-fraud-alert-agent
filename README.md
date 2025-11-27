# 🔒 ICICI Bank Fraud Alert Voice Agent

![CHALLENGE](https://img.shields.io/badge/CHALLENGE-10%20DAYS%20OF%20AI%20VOICE%20AGENTS-blue?style=for-the-badge)
![TTS](https://img.shields.io/badge/TTS-MURF%20FALCON-orange?style=for-the-badge)
![FRAMEWORK](https://img.shields.io/badge/FRAMEWORK-LIVEKIT-green?style=for-the-badge)
![PYTHON](https://img.shields.io/badge/PYTHON-3.9+-yellow?style=for-the-badge&logo=python)
![NEXT.JS](https://img.shields.io/badge/NEXT.JS-15-black?style=for-the-badge&logo=next.js)
![DAY](https://img.shields.io/badge/DAY-6-blueviolet?style=for-the-badge)

**Building 10 AI Voice Agents in 10 Days** using Murf Falcon TTS - the consistently fastest text-to-speech API in the world.

---

## About the Challenge

We just launched Murf Falcon – the consistently fastest TTS API, and you're going to be among the first to test it out in ways never thought before!

Build 10 AI Voice Agents over the course of 10 Days along with help from our devs and the community champs, and win rewards!

## About This Project

This is Day 6 of the 10-day AI Voice Agents Challenge. The task was to build a fraud alert voice agent that:
- Loads fraud cases from a database
- Verifies customer identity with security questions
- Reads suspicious transaction details
- Confirms or denies fraud based on customer response
- Updates the database with case outcomes

An AI-powered fraud detection voice agent for ICICI Bank that verifies suspicious transactions through natural conversation and updates a fraud case database in real-time.

## Repository Structure

This is a monorepo that contains both the backend and frontend for the ICICI Bank Fraud Alert Voice Agent.

```
icici-fraud-alert-agent/
├── backend/          # LiveKit Agents backend with Murf Falcon TTS
├── frontend/         # React/Next.js frontend for voice interaction
└── README.md         # This file
```

## Backend

The backend is based on LiveKit's agent-starter-python with modifications to integrate Murf Falcon TTS for ultra-fast, high-quality voice synthesis in fraud detection scenarios.

**Features:**
- Complete voice AI agent framework using LiveKit Agents
- Murf Falcon TTS integration for fastest text-to-speech
- AssemblyAI STT for high-accuracy speech recognition
- Google Gemini 2.5 Flash for LLM
- JSON-based fraud case database
- Real-time database updates
- Security question verification
- Professional fraud detection persona

→ [Backend Documentation](backend/README.md)

## Frontend

The frontend is based on LiveKit's agent-starter-react, providing a modern, beautiful UI for interacting with the ICICI Bank Fraud Alert Agent.

**Features:**
- Real-time voice interaction with LiveKit Agents
- ICICI Bank branded UI with security-focused design
- Audio visualization and level monitoring
- Light/dark theme switching
- Fraud alert badge and trust indicators
- Enhanced animations and visual effects
- Responsive design for desktop and mobile

→ [Frontend Documentation](frontend/README.md)

## Quick Start

### Prerequisites

Make sure you have the following installed:
- Python 3.9+ with [uv](https://docs.astral.sh/uv/) package manager
- Node.js 18+ with pnpm
- LiveKit CLI (optional but recommended)
- [LiveKit Server](https://github.com/livekit/livekit/releases) for local development

### 1. Clone the Repository

```bash
git clone https://github.com/Gangadhar-NG-CODER/icici-fraud-alert-agent.git
cd icici-fraud-alert-agent
```

### 2. Backend Setup

```bash
cd backend

# Install dependencies
uv sync

# Copy environment file and configure
cp .env.example .env.local

# Edit .env.local with your credentials:
# - LIVEKIT_URL
# - LIVEKIT_API_KEY
# - LIVEKIT_API_SECRET
# - MURF_API_KEY (for Falcon TTS)
# - GOOGLE_API_KEY (for Gemini LLM)
# - ASSEMBLYAI_API_KEY (for AssemblyAI STT)

# Download required models
uv run python src/agent.py download-files
```

For LiveKit Cloud users, you can automatically populate credentials:

```bash
lk cloud auth
lk app env -w -d .env.local
```

### 3. Frontend Setup

```bash
cd frontend

# Install dependencies
pnpm install

# Copy environment file and configure
cp .env.example .env.local

# Edit .env.local with the same LiveKit credentials
```

### 4. Run the Application

**Install LiveKit Server:**

```bash
brew install livekit
```

You have two options:

**Option A: Run services individually**

```bash
# Terminal 1 - LiveKit Server
livekit-server --dev

# Terminal 2 - Backend Agent
cd backend
uv run python src/agent.py dev

# Terminal 3 - Frontend
cd frontend
pnpm dev
```

Then open **http://localhost:3000** in your browser!

## How to Use

### Test Scenarios

The database includes 5 test cases. Try these scenarios:

#### Scenario 1: Confirmed Safe (John)
1. Click "Connect to Fraud Alert"
2. Agent: "May I have your name please?"
3. You: "John"
4. Agent: "What is your mother's maiden name?"
5. You: "Smith"
6. Agent reads transaction details
7. Agent: "Did you authorize this transaction?"
8. You: "Yes"
9. Result: Transaction marked as `confirmed_safe`

#### Scenario 2: Confirmed Fraud (Sarah)
1. Start call
2. You: "Sarah"
3. Security question: "What city were you born in?"
4. You: "Boston"
5. Agent reads transaction details
6. You: "No, I didn't make that transaction"
7. Result: Card blocked, transaction marked as `confirmed_fraud`

#### Scenario 3: Verification Failed (Michael)
1. Start call
2. You: "Michael"
3. Security question: "What was your first pet's name?"
4. You: "Wrong answer"
5. Result: Call ends, marked as `verification_failed`

### Available Test Users

| Username | Security Question | Answer | Card Ending |
|----------|------------------|---------|-------------|
| John | Mother's maiden name? | Smith | 4242 |
| Sarah | City you were born in? | Boston | 8765 |
| Michael | First pet's name? | Buddy | 1357 |
| Emily | Favorite color? | Blue | 9876 |
| David | Street you grew up on? | Oak Street | 5432 |

## Agent Tools

The fraud detection agent has 4 function tools:

### 1. load_fraud_case(username)
Loads a fraud case from the database using the customer's name.

**Example:**
- User: "My name is John"
- Agent calls: `load_fraud_case("John")`
- Returns: Case loaded with transaction details

### 2. verify_customer(answer)
Verifies customer identity using their security question answer.

**Example:**
- Agent asks: "What is your mother's maiden name?"
- User: "Smith"
- Agent calls: `verify_customer("Smith")`
- Returns: Verification passed/failed

### 3. mark_transaction(status)
Marks the transaction as safe or fraudulent.

**Parameters:**
- `"safe"` - Customer confirmed they made the transaction
- `"fraudulent"` - Customer denied making the transaction

**Example:**
- User: "No, I didn't make that purchase"
- Agent calls: `mark_transaction("fraudulent")`
- Updates database and blocks card

### 4. end_fraud_call()
Ends the call professionally with appropriate closing message.

## Fraud Case Data Format

```json
{
  "userName": "John",
  "securityIdentifier": "12345",
  "securityQuestion": "What is your mother's maiden name?",
  "securityAnswer": "Smith",
  "cardEnding": "4242",
  "case": "confirmed_safe",
  "transactionAmount": "$1,247.99",
  "transactionName": "ABC Industry",
  "transactionTime": "November 26, 2025 at 11:45 PM",
  "transactionCategory": "e-commerce",
  "transactionSource": "alibaba.com",
  "transactionLocation": "Shanghai, China",
  "verification_status": "verified",
  "outcome_note": "Customer John confirmed the transaction as legitimate on 2025-11-27 10:30:00"
}
```

## Technical Implementation

### Fraud Detection Flow
1. **Name Collection** → Load case from database
2. **Security Verification** → Ask security question
3. **Transaction Disclosure** → Read all details clearly
4. **Confirmation** → Get yes/no answer
5. **Action** → Update database and take appropriate action

### Database Operations
- **Load**: Read fraud_cases.json on startup
- **Query**: Find case by username (case-insensitive)
- **Update**: Modify case status and outcome
- **Save**: Write updated database back to JSON file

### Security Features
- Never asks for full card numbers or PINs
- Uses non-sensitive security questions
- Verification required before disclosure
- Clear audit trail in database

## Testing

Test all three scenarios:

1. **Confirmed Safe**: Customer authorizes transaction
2. **Confirmed Fraud**: Customer denies transaction
3. **Verification Failed**: Wrong security answer

Check the database file after each test to verify updates.

## Documentation & Resources

- [Murf Falcon TTS Documentation](https://murf.ai/api/docs/text-to-speech/streaming)
- [LiveKit Agents Documentation](https://docs.livekit.io/agents)
- [AssemblyAI Documentation](https://www.assemblyai.com/docs)
- [Backend Documentation](backend/README.md)
- [Frontend Documentation](frontend/README.md)

## Contributing & Community

This is a challenge repository, but we encourage collaboration and knowledge sharing!

- Share your solutions and learnings on GitHub
- Post about your progress on LinkedIn
- Join the LiveKit Community Slack
- Connect with other challenge participants

## License

This project is based on MIT-licensed templates from LiveKit and includes integration with Murf Falcon. See individual LICENSE files in backend and frontend directories for details.

---

**Built for the AI Voice Agents Challenge by murf.ai**

Part of the **#MurfAIVoiceAgentsChallenge** • **#10DaysofAIVoiceAgents**
