export type DesktopSnapshot = {
  platforms: readonly ['windows', 'macos', 'linux'];
  electron: false;
  installer: false;
  multiWindow: true;
};

export function buildDesktop(): DesktopSnapshot {
  return {
    platforms: ['windows', 'macos', 'linux'],
    electron: false,
    installer: false,
    multiWindow: true,
  };
}
