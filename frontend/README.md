# Frontend - Zerodha SDR Voice Agent

Next.js 15 + React 19 frontend for the Zerodha SDR voice agent with modern UI and smooth animations.

**Part of**: [zerodha-sdr-voice-agent](https://github.com/Gangadhar-NG-CODER/zerodha-sdr-voice-agent)

---

## Quick Start

```bash
# Install dependencies
pnpm install

# Configure environment
cp .env.example .env.local
# Edit .env.local with LiveKit credentials

# Run development server
pnpm dev
```

Open [http://localhost:3000](http://localhost:3000) in your browser.

---

## Environment Variables

Required in `.env.local`:

```bash
LIVEKIT_API_KEY=devkey
LIVEKIT_API_SECRET=secret
LIVEKIT_URL=ws://127.0.0.1:7880
```

---

## Features

### UI Design

- **Blue/Cyan Theme**: Professional business-oriented color scheme
- **Animated Elements**: 
  - Rotating rings around icon
  - Bouncing briefcase icon
  - Pinging background particles
  - Glowing button effects
  - Interactive title words
- **Responsive**: Works on desktop and mobile
- **Smooth Transitions**: All interactions have smooth animations

### Components

- **Welcome View**: Landing page with "Talk to SDR" button
- **Session View**: Active conversation interface
- **Voice Controls**: Mute, volume, chat toggle
- **End Call**: Clean disconnect with summary

---

## Project Structure

```
frontend/
├── app/
│   ├── (app)/
│   │   └── page.tsx              # Main page
│   ├── api/
│   │   └── connection-details/   # LiveKit connection API
│   ├── layout.tsx                # Root layout
│   └── ui/                       # UI components
├── components/
│   ├── app/
│   │   ├── app.tsx              # Main app component
│   │   ├── welcome-view.tsx     # Landing page
│   │   ├── session-view.tsx     # Conversation UI
│   │   └── session-provider.tsx # State management
│   └── livekit/                 # LiveKit UI components
├── styles/
│   └── globals.css              # Global styles
├── app-config.ts                # App configuration
├── package.json
└── README.md
```

---

## UI Customization

### Colors

The app uses a blue/cyan/teal gradient theme. To customize:

**File**: `app-config.ts`
```typescript
accent: '#06b6d4',      // Cyan
accentDark: '#22d3ee',  // Light cyan
```

**File**: `components/app/welcome-view.tsx`
```typescript
// Gradient colors
from-blue-500 via-cyan-500 to-teal-500
```

### Animations

**Rotating Rings**: Around the icon
```typescript
animationDuration: '8s'  // Adjust speed
```

**Bouncing Icon**: Briefcase animation
```typescript
animationDuration: '3s'  // Adjust bounce speed
```

**Button Hover**: Scale and glow effects
```typescript
hover:scale-110          // Adjust scale
hover:shadow-cyan-500/50 // Adjust glow color
```

---

## Tech Stack

- **Framework**: Next.js 15.5.2 (Turbopack)
- **React**: 19.2.0
- **LiveKit**: Components React 2.9.16
- **Styling**: Tailwind CSS 4.1.17
- **Animations**: Motion 12.23.24
- **UI Components**: Radix UI
- **TypeScript**: 5.9.3

---

## Development

```bash
# Install dependencies
pnpm install

# Run development server
pnpm dev

# Build for production
pnpm build

# Start production server
pnpm start

# Lint code
pnpm lint
```

---

## API Routes

### POST /api/connection-details

Generates LiveKit connection details for the voice session.

**Request Body:**
```json
{
  "room_config": {
    "agents": [
      {
        "agent_name": ""
      }
    ]
  }
}
```

**Response:**
```json
{
  "serverUrl": "ws://127.0.0.1:7880",
  "roomName": "voice_assistant_room_1234",
  "participantToken": "eyJhbGc...",
  "participantName": "user"
}
```

---

## Troubleshooting

### Port Already in Use

If port 3000 is in use:
```bash
# The app will automatically use port 3001
# Or specify a different port:
PORT=3001 pnpm dev
```

### Environment Variables Not Loading

1. Ensure `.env.local` exists
2. Restart the development server
3. Clear `.next` cache:
```bash
rm -rf .next
pnpm dev
```

### Connection Issues

1. Verify LiveKit server is running on port 7880
2. Check backend agent is connected
3. Verify environment variables match across all services

---

## Documentation

See the [main README](../README.md) for complete setup instructions.

---

**Part of the Murf AI Voice Agents Challenge - Day 5**

**GitHub**: https://github.com/Gangadhar-NG-CODER/zerodha-sdr-voice-agent
