import type { NextConfig } from 'next';
import { productionSecurityHeaders } from './lib/platform/headers';

const profile = process.env.SALORA_PROFILE || process.env.NODE_ENV || 'development';

const nextConfig: NextConfig = {
  output: 'standalone',
  poweredByHeader: false,
  compress: true,
  eslint: {
    // These warnings come from upstream LiveKit/AI UI components, not our code.
    ignoreDuringBuilds: true,
  },
  images: {
    formats: ['image/avif', 'image/webp'],
  },
  experimental: {
    optimizePackageImports: ['@phosphor-icons/react', 'lucide-react'],
  },
  async headers() {
    const headers = productionSecurityHeaders(profile);
    return [
      {
        source: '/:path*',
        headers: Object.entries(headers).map(([key, value]) => ({ key, value })),
      },
    ];
  },
};

export default nextConfig;
