import { MediaDeviceFailure, Track } from 'livekit-client';

/** Detect microphone permission / device failures from LiveKit or browser errors. */
export function isMicrophonePermissionError(error: unknown, source?: Track.Source): boolean {
  if (source && source !== Track.Source.Microphone) {
    return false;
  }

  if (!(error instanceof Error) && typeof error !== 'object') {
    return false;
  }

  const err = error as Error;
  const failure = MediaDeviceFailure.getFailure(err);
  if (
    failure === MediaDeviceFailure.PermissionDenied ||
    failure === MediaDeviceFailure.NotFound ||
    failure === MediaDeviceFailure.DeviceInUse
  ) {
    return true;
  }

  const name = err.name?.toLowerCase?.() ?? '';
  const message = err.message?.toLowerCase?.() ?? '';

  return (
    name === 'notallowederror' ||
    name === 'permissiondeniederror' ||
    message.includes('permission') ||
    message.includes('not allowed') ||
    message.includes('microphone')
  );
}
