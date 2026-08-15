import { NextResponse } from 'next/server';
import { AccessToken, type AccessTokenOptions, type VideoGrant } from 'livekit-server-sdk';
import { RoomConfiguration } from '@livekit/protocol';
import { getPlatformConfig } from '@/lib/platform/config';
import { platformError, reportError } from '@/lib/platform/errors';
import { platformRoute } from '@/lib/platform/http';
import { recordMetric } from '@/lib/platform/observability';

type ConnectionDetails = {
  serverUrl: string;
  roomName: string;
  participantName: string;
  participantToken: string;
};

export const revalidate = 0;

export async function POST(req: Request) {
  return platformRoute(req, { rateLimit: 'token', csrf: true, metric: 'voice.token' }, async () => {
    const config = getPlatformConfig();
    if (!config.livekit.url || !config.livekit.apiKey || !config.livekit.apiSecret) {
      const error = platformError('CONFIG_MISSING');
      return new NextResponse(error.userMessage, { status: error.status });
    }

    try {
      const body = await req.json().catch(() => ({}));
      let roomConfig: RoomConfiguration | undefined;
      if (body?.room_config) {
        roomConfig = RoomConfiguration.fromJson(body.room_config, { ignoreUnknownFields: true });
      } else if (config.livekit.agentName) {
        roomConfig = RoomConfiguration.fromJson(
          { agents: [{ agentName: config.livekit.agentName }] },
          { ignoreUnknownFields: true }
        );
      }

      const participantName = 'user';
      const participantIdentity = `voice_assistant_user_${Math.floor(Math.random() * 10_000)}`;
      const roomName = `voice_assistant_room_${Math.floor(Math.random() * 10_000)}`;

      const participantToken = await createParticipantToken(
        { identity: participantIdentity, name: participantName },
        roomName,
        roomConfig,
        config.livekit.apiKey,
        config.livekit.apiSecret
      );

      const data: ConnectionDetails = {
        serverUrl: config.livekit.url,
        roomName,
        participantName,
        participantToken,
      };
      recordMetric('voice.session.start', 1);
      return NextResponse.json(data, {
        headers: { 'Cache-Control': 'no-store' },
      });
    } catch (error) {
      reportError(error, { route: 'voice.token' });
      if (error instanceof Error) {
        return new NextResponse(error.message, { status: 500 });
      }
      return new NextResponse('Unable to create a voice session.', { status: 500 });
    }
  });
}

function createParticipantToken(
  userInfo: AccessTokenOptions,
  roomName: string,
  roomConfig: RoomConfiguration | undefined,
  apiKey: string,
  apiSecret: string
): Promise<string> {
  const at = new AccessToken(apiKey, apiSecret, {
    ...userInfo,
    ttl: '15m',
  });
  const grant: VideoGrant = {
    room: roomName,
    roomJoin: true,
    canPublish: true,
    canPublishData: true,
    canSubscribe: true,
  };
  at.addGrant(grant);

  if (roomConfig) {
    at.roomConfig = roomConfig;
  }

  return at.toJwt();
}
