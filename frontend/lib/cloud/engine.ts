export type CloudSnapshot = {
  regions: readonly string[];
  rollback: 'previous_image_and_env';
  speechLake: false;
};

export function buildCloud(): CloudSnapshot {
  return {
    regions: ['local', 'staging', 'production'],
    rollback: 'previous_image_and_env',
    speechLake: false,
  };
}
