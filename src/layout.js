/*
 * Display and performance resolver
 * Display- und Performance-Erkennung
 */

const configuredDisplayMode =
  String(CONFIG.displayMode || 'auto').toLowerCase();

const configuredPerformanceMode =
  String(CONFIG.performanceMode || 'auto').toLowerCase();

const viewportWidth = Number(window?.innerWidth || 0);
const touchPoints = Number(window?.navigator?.maxTouchPoints || 0);
const userAgent = String(window?.navigator?.userAgent || '');

const isTouchDevice = touchPoints > 0;
const isTabletLike = isTouchDevice && viewportWidth >= 700;

const validDisplayModes = ['auto', 'desktop', 'tablet', 'wall'];
let displayMode = validDisplayModes.includes(configuredDisplayMode)
  ? configuredDisplayMode
  : 'auto';

if (displayMode === 'auto') {
  if (isTabletLike) {
    displayMode = 'tablet';
  } else if (viewportWidth >= 1000) {
    displayMode = 'desktop';
  } else {
    displayMode = 'auto';
  }
}

const iosVersionMatch = userAgent.match(/OS (\d+)[_.]/i);
const iosMajorVersion = iosVersionMatch
  ? Number.parseInt(iosVersionMatch[1], 10)
  : null;

const isOldIOS =
  Number.isFinite(iosMajorVersion) && iosMajorVersion <= 15;

const supportsColorMix = Boolean(
  window?.CSS?.supports?.(
    'color',
    'color-mix(in srgb, red 50%, blue)'
  )
);

const validPerformanceModes = ['auto', 'high', 'balanced', 'low'];
let performanceMode = validPerformanceModes.includes(configuredPerformanceMode)
  ? configuredPerformanceMode
  : 'auto';

if (performanceMode === 'auto') {
  if (isOldIOS || !supportsColorMix) {
    performanceMode = 'low';
  } else if (isTabletLike) {
    performanceMode = 'balanced';
  } else {
    performanceMode = 'high';
  }
}
