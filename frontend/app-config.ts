export interface AppConfig {
  pageTitle: string;
  pageDescription: string;
  companyName: string;

  supportsChatInput: boolean;
  supportsVideoInput: boolean;
  supportsScreenShare: boolean;
  isPreConnectBufferEnabled: boolean;

  logo: string;
  startButtonText: string;
  accent?: string;
  logoDark?: string;
  accentDark?: string;

  // for LiveKit Cloud Sandbox
  sandboxId?: string;
  agentName?: string;
}

export const APP_CONFIG_DEFAULTS: AppConfig = {
  companyName: 'Zerodha',
  pageTitle: 'Zerodha SDR Agent - AI Sales Representative',
  pageDescription: 'Talk to our AI SDR to learn about Zerodha products, pricing, and services',

  supportsChatInput: true,
  supportsVideoInput: false,
  supportsScreenShare: false,
  isPreConnectBufferEnabled: true,

  logo: '/lk-logo.svg',
  accent: '#06b6d4',
  logoDark: '/lk-logo-dark.svg',
  accentDark: '#22d3ee',
  startButtonText: 'Talk to SDR',

  // for LiveKit Cloud Sandbox
  sandboxId: undefined,
  agentName: undefined,
};
