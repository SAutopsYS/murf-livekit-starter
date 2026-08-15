export type MobileSnapshot = {
  offline: true;
  push: true;
  nativeUi: false;
  modules: readonly string[];
};

export function buildMobile(): MobileSnapshot {
  return {
    offline: true,
    push: true,
    nativeUi: false,
    modules: ['voice', 'learning', 'studio', 'whiteboard', 'knowledge'],
  };
}
