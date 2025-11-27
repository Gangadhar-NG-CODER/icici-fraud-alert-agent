# Agent Starter for React

🎙️ **This is part of the AI Voice Agents Challenge by murf.ai**

This frontend is designed to work with the Murf Falcon-powered backend for ultra-fast voice interactions. See the main README for complete setup instructions and challenge details.

This is a starter template for LiveKit Agents that provides a voice interface for the ICICI Bank Fraud Alert Agent using the LiveKit JavaScript SDK. It supports voice interaction, real-time transcriptions, and a professional banking UI.

Based on: [livekit-examples/agent-starter-react](https://github.com/livekit-examples/agent-starter-react)

Also available for: Android • Flutter • Swift • React Native

## Features

- Real-time voice interaction with LiveKit Agents
- Audio visualization and level monitoring
- Light/dark theme switching with system preference detection
- Customizable branding, colors, and UI text via configuration
- ICICI Bank branded UI with security-focused design
- Fraud alert badge and trust indicators
- Enhanced animations and visual effects
- Responsive design for desktop and mobile

This template is built with Next.js and is free for you to use or modify as you see fit.

## Project structure

```
agent-starter-react/
├── app/
│   ├── (app)/
│   ├── api/
│   ├── components/
│   ├── fonts/
│   ├── globals.css
│   └── layout.tsx
├── components/
│   ├── livekit/
│   ├── ui/
│   ├── app.tsx
│   ├── session-view.tsx
│   └── welcome.tsx
├── hooks/
├── lib/
├── public/
└── package.json
```

## Getting started

> **Tip**  
> If you'd like to try this application without modification, you can deploy an instance in just a few clicks with LiveKit Cloud Sandbox.

Run the following command to automatically clone this template:

```bash
lk app create --template agent-starter-react
```

Then run the app with:

```bash
pnpm install
pnpm dev
```

And open http://localhost:3000 in your browser.

You'll also need an agent to speak with. Try our starter agent for Python, Node.js, or create your own from scratch.

## Configuration

This starter is designed to be flexible so you can adapt it to your specific agent use case. You can easily configure it to work with different types of inputs and outputs:

### Example: App configuration (app-config.ts)

```typescript
export const APP_CONFIG_DEFAULTS: AppConfig = {
  companyName: 'ICICI Bank',
  pageTitle: 'ICICI Bank Fraud Alert - AI Fraud Detection',
  pageDescription: 'Verify suspicious transactions with our AI fraud detection agent',
  
  supportsChatInput: true,
  supportsVideoInput: false,
  supportsScreenShare: false,
  isPreConnectBufferEnabled: true,
  
  logo: '/lk-logo.svg',
  accent: '#f97316',
  logoDark: '/lk-logo-dark.svg',
  accentDark: '#3b82f6',
  startButtonText: 'Connect to Fraud Alert',
  
  // for LiveKit Cloud Sandbox
  sandboxId: undefined,
  agentName: undefined,
};
```

You can update these values in `app-config.ts` to customize branding, features, and UI text for your deployment.

> **Note**  
> The `sandboxId` and `agentName` are for the LiveKit Cloud Sandbox environment. They are not used for local development.

## Environment Variables

You'll also need to configure your LiveKit credentials in `.env.local` (copy `.env.example` if you don't have one):

```env
LIVEKIT_API_KEY=your_livekit_api_key
LIVEKIT_API_SECRET=your_livekit_api_secret
LIVEKIT_URL=https://your-livekit-server-url
```

These are required for the voice agent functionality to work with your LiveKit project.

## Contributing

This template is open source and we welcome contributions! Please open a PR or issue through GitHub, and don't forget to join us in the LiveKit Community Slack!
