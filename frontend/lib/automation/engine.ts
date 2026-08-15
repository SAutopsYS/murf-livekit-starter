export type TriggerKind =
  | 'VoiceCompleted'
  | 'LearningFinished'
  | 'DocumentCreated'
  | 'AgentFinished'
  | 'PluginInstalled'
  | 'ScheduleTriggered';

export type AutomationWorkflow = {
  id: string;
  owner: string;
  organization: string | null;
  trigger: TriggerKind;
  nodes: string[];
};

export function createAutomation(owner: string, trigger: TriggerKind): AutomationWorkflow {
  return {
    id: `wf:${trigger.toLowerCase()}`,
    owner,
    organization: null,
    trigger,
    nodes: ['trigger', 'condition', 'ai_action'],
  };
}
