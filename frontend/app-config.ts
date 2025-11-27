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
