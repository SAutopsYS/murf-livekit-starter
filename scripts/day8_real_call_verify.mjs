/**
 * Day 8 real-browser verification:
 * Start Talking → chat exercise flow → disconnect → check analytics API.
 */
import { chromium } from 'playwright';

const BASE = process.env.APP_URL || 'http://localhost:3000';

async function getMetrics() {
  const res = await fetch(`${BASE}/api/analytics?preset=all`);
  if (!res.ok) throw new Error(`analytics API ${res.status}`);
  return res.json();
}

async function sendChat(page, text) {
  const box = page.locator('textarea').first();
  await box.waitFor({ state: 'visible', timeout: 60000 });
  await box.fill(text);
  await box.press('Enter');
}

async function main() {
  const before = await getMetrics();
  console.log('BEFORE', JSON.stringify({
    total_calls: before.total_calls,
    successful_calls: before.successful_calls,
    failed_calls: before.failed_calls,
  }));

  const browser = await chromium.launch({
    headless: true,
    args: [
      '--use-fake-ui-for-media-stream',
      '--use-fake-device-for-media-stream',
      '--allow-anonymous-microphone',
    ],
  });
  const context = await browser.newContext({
    permissions: ['microphone'],
  });
  const page = await context.newPage();
  page.on('console', (msg) => {
    if (msg.type() === 'error') console.log('PAGE_ERROR', msg.text());
  });

  await page.goto(BASE, { waitUntil: 'networkidle', timeout: 120000 });
  await page.getByRole('button', { name: /start talking/i }).click({ timeout: 30000 });

  // Wait for connected session controls / chat.
  await page.waitForTimeout(8000);
  const disconnect = page.getByRole('button', { name: /disconnect|leave|end/i }).first();
  await disconnect.waitFor({ state: 'visible', timeout: 90000 }).catch(() => null);

  // Learning exercise via existing chat toolchain.
  await sendChat(page, 'Give me a beginner speaking exercise.');
  await page.waitForTimeout(12000);
  await sendChat(
    page,
    'Hello, my name is Asha. I am a student. I like learning English every day. Thank you for helping me practice speaking.'
  );
  await page.waitForTimeout(15000);
  await sendChat(page, 'Please score my answer. I am beginner level.');
  await page.waitForTimeout(20000);

  // End session so analytics completion runs.
  if (await disconnect.count()) {
    await disconnect.click({ timeout: 10000 }).catch(() => null);
  } else {
    // Fallback: close page/context to force disconnect.
    await page.close({ runBeforeUnload: true }).catch(() => null);
  }

  await page.waitForTimeout(8000);
  await browser.close();

  // Poll analytics for success bump.
  let after = before;
  for (let i = 0; i < 12; i++) {
    await new Promise((r) => setTimeout(r, 2500));
    after = await getMetrics();
    if (
      after.total_calls >= before.total_calls + 1 &&
      after.successful_calls >= before.successful_calls + 1
    ) {
      break;
    }
  }

  console.log('AFTER', JSON.stringify({
    total_calls: after.total_calls,
    successful_calls: after.successful_calls,
    failed_calls: after.failed_calls,
    success_rate: after.success_rate,
    recent_calls: (after.recent_calls || []).slice(0, 3),
    performance: after.performance,
    language_breakdown: after.language_breakdown,
    channel_breakdown: after.channel_breakdown,
  }));

  const ok =
    after.total_calls === before.total_calls + 1 &&
    after.successful_calls === before.successful_calls + 1 &&
    after.failed_calls === before.failed_calls;

  console.log('PROOF', JSON.stringify({
    total_plus_1: after.total_calls === before.total_calls + 1,
    success_plus_1: after.successful_calls === before.successful_calls + 1,
    failed_unchanged: after.failed_calls === before.failed_calls,
    ok,
  }));
  process.exit(ok ? 0 : 2);
}

main().catch((err) => {
  console.error('VERIFY_FAILED', err);
  process.exit(1);
});
