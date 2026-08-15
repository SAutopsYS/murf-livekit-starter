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

  audioVisualizerType?: 'bar' | 'wave' | 'grid' | 'radial' | 'aura';
  audioVisualizerColor?: `#${string}`;
  audioVisualizerColorDark?: `#${string}`;
  audioVisualizerColorShift?: number;
  audioVisualizerBarCount?: number;
  audioVisualizerGridRowCount?: number;
  audioVisualizerGridColumnCount?: number;
  audioVisualizerRadialBarCount?: number;
  audioVisualizerRadialRadius?: number;
  audioVisualizerWaveLineWidth?: number;

  // agent dispatch configuration
  agentName?: string;

  // LiveKit Cloud Sandbox configuration
  sandboxId?: string;
}

export const APP_CONFIG_DEFAULTS: AppConfig = {
  companyName: 'SALORA AI',
  pageTitle: 'SALORA OS',
  pageDescription:
    'Voice-first learning. Practice in Hindi, English, or Hinglish. Learning that stays on the line.',

  supportsChatInput: true,
  supportsVideoInput: true,
  supportsScreenShare: true,
  isPreConnectBufferEnabled: true,

  logo: '/salora-mark.svg',
  accent: '#2F6F5E',
  logoDark: '/salora-mark-dark.svg',
  accentDark: '#6FBF9A',
  startButtonText: 'Enter the hall',

  // Voice experience uses the existing LiveKit wave visualizer.
  audioVisualizerType: 'wave',
  audioVisualizerColor: '#2F6F5E',
  audioVisualizerColorDark: '#6FBF9A',
  audioVisualizerColorShift: 0.28,
  audioVisualizerWaveLineWidth: 4,

  // agent dispatch configuration
  agentName: process.env.AGENT_NAME ?? undefined,

  // LiveKit Cloud Sandbox configuration
  sandboxId: undefined,
};
