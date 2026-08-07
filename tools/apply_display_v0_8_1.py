from pathlib import Path

path = Path('dashboard.yaml')
text = path.read_text(encoding='utf-8')

# -----------------------------------------------------------------------------
# Version
# -----------------------------------------------------------------------------
text = text.replace(
    '# solar_dashboard v0.8.0-alpha - dashboard.yaml',
    '# solar_dashboard v0.8.1-alpha - dashboard.yaml',
    1,
)

# -----------------------------------------------------------------------------
# User configuration
# -----------------------------------------------------------------------------
language_block = """            language: 'auto',\n"""
config_extension = """            language: 'auto',\n\n            // Display profile: 'auto', 'desktop', 'tablet' or 'wall'.\n            // 'wall' is optimized for permanently mounted tablets.\n            displayMode: 'auto',\n\n            // Rendering profile: 'auto', 'high', 'balanced' or 'low'.\n            // 'auto' selects a safe profile from browser capabilities.\n            performanceMode: 'auto',\n"""

if "displayMode: 'auto'" not in text:
    if language_block not in text:
        raise SystemExit('language config entry not found')
    text = text.replace(language_block, config_extension, 1)

# -----------------------------------------------------------------------------
# Display/performance resolver
# -----------------------------------------------------------------------------
resolver_marker = """          const t = I18N[language] || I18N.en;\n          const locale = language === 'de' ? 'de-AT' : 'en-US';\n"""

resolver = r'''          const t = I18N[language] || I18N.en;
          const locale = language === 'de' ? 'de-AT' : 'en-US';

          /*
           * ========================================================
           * DISPLAY / PERFORMANCE PROFILE
           * ========================================================
           */

          const configuredDisplayMode =
            String(CONFIG.displayMode || 'auto').toLowerCase();

          const configuredPerformanceMode =
            String(CONFIG.performanceMode || 'auto').toLowerCase();

          const viewportWidth =
            Number(window?.innerWidth || 0);

          const touchPoints =
            Number(window?.navigator?.maxTouchPoints || 0);

          const userAgent =
            String(window?.navigator?.userAgent || '');

          const isTouchDevice = touchPoints > 0;
          const isTabletLike =
            isTouchDevice && viewportWidth >= 700;

          const validDisplayModes =
            ['auto', 'desktop', 'tablet', 'wall'];

          let displayMode =
            validDisplayModes.includes(configuredDisplayMode)
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

          const iosVersionMatch =
            userAgent.match(/OS (\d+)[_.]/i);

          const iosMajorVersion =
            iosVersionMatch
              ? Number.parseInt(iosVersionMatch[1], 10)
              : null;

          const isOldIOS =
            Number.isFinite(iosMajorVersion) &&
            iosMajorVersion <= 15;

          const supportsColorMix =
            Boolean(
              window?.CSS?.supports?.(
                'color',
                'color-mix(in srgb, red 50%, blue)'
              )
            );

          const validPerformanceModes =
            ['auto', 'high', 'balanced', 'low'];

          let performanceMode =
            validPerformanceModes.includes(configuredPerformanceMode)
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
'''

if 'const configuredDisplayMode =' not in text:
    if resolver_marker not in text:
        raise SystemExit('i18n locale resolver not found')
    text = text.replace(resolver_marker, resolver, 1)

# -----------------------------------------------------------------------------
# Add runtime classes to the dashboard root
# -----------------------------------------------------------------------------
root_old = '<div class="solar-dashboard">'
root_new = '<div class="solar-dashboard display-${displayMode} perf-${performanceMode}">'
if root_new not in text:
    if root_old not in text:
        raise SystemExit('dashboard root not found')
    text = text.replace(root_old, root_new, 1)

# -----------------------------------------------------------------------------
# CSS compatibility + wall mode
# -----------------------------------------------------------------------------
css_anchor = """      /*\n       * ==========================================================\n       * GRUNDLAYOUT\n       * ==========================================================\n       */\n"""

compat_css = r'''      /*
       * ==========================================================
       * v0.8.1-alpha – DISPLAY / PERFORMANCE PROFILES
       * ==========================================================
       *
       * displayMode:
       *   auto | desktop | tablet | wall
       *
       * performanceMode:
       *   auto | high | balanced | low
       *
       * The low profile intentionally avoids color-mix dependent
       * surfaces and expensive filters. This keeps older Safari /
       * iPadOS devices usable as permanent Home Assistant displays.
       */

      /* Balanced: keep the design, reduce GPU-heavy effects. */
      .solar-dashboard.perf-balanced .panel {
        box-shadow: 0 5px 16px rgba(0,0,0,0.13);
      }

      .solar-dashboard.perf-balanced .mppt-panel,
      .solar-dashboard.perf-balanced .pv-total-panel,
      .solar-dashboard.perf-balanced .battery-panel,
      .solar-dashboard.perf-balanced .live-panel {
        background-size: 100% 100%;
      }

      .solar-dashboard.perf-balanced .gauge-svg path,
      .solar-dashboard.perf-balanced .gauge-svg circle {
        filter: none;
      }

      /* Low: Safari 15 / old tablet compatibility layer. */
      .solar-dashboard.perf-low {
        --solar-surface-soft: var(--solar-surface);
        --solar-surface-strong: var(--solar-surface);
        --solar-border: var(--divider-color, rgba(128,128,128,0.25));
        --solar-divider: var(--divider-color, rgba(128,128,128,0.22));
        --solar-gauge-track: rgba(128,128,128,0.22);
        --solar-inset: rgba(128,128,128,0.08);
        --solar-track: rgba(128,128,128,0.13);
        --solar-shadow: 0 3px 10px rgba(0,0,0,0.12);
      }

      .solar-dashboard.perf-low .panel {
        background: var(--solar-surface) !important;
        box-shadow: var(--solar-shadow) !important;
      }

      .solar-dashboard.perf-low .mppt-panel {
        background:
          radial-gradient(
            circle at 50% 110%,
            rgba(255, 180, 40, 0.08),
            transparent 52%
          ),
          var(--solar-surface) !important;
      }

      .solar-dashboard.perf-low .pv-total-panel {
        background:
          radial-gradient(
            circle at 12% 110%,
            rgba(255, 152, 0, 0.11),
            transparent 48%
          ),
          radial-gradient(
            circle at 88% 110%,
            rgba(67, 160, 71, 0.10),
            transparent 48%
          ),
          var(--solar-surface) !important;
      }

      .solar-dashboard.perf-low .battery-panel {
        background:
          radial-gradient(
            circle at 55% 115%,
            rgba(76, 175, 80, 0.10),
            transparent 52%
          ),
          var(--solar-surface) !important;
      }

      .solar-dashboard.perf-low .live-panel {
        background:
          linear-gradient(
            90deg,
            rgba(255,193,7,0.035) 0%,
            rgba(33,150,243,0.035) 34%,
            rgba(38,198,218,0.035) 67%,
            rgba(76,175,80,0.035) 100%
          ),
          var(--solar-surface) !important;
      }

      .solar-dashboard.perf-low .payment-panel {
        background:
          linear-gradient(
            145deg,
            rgba(66,165,245,0.08),
            transparent 65%
          ),
          var(--solar-surface) !important;
      }

      .solar-dashboard.perf-low .runtime-panel {
        background:
          linear-gradient(
            145deg,
            rgba(142,92,255,0.08),
            transparent 65%
          ),
          var(--solar-surface) !important;
      }

      .solar-dashboard.perf-low *,
      .solar-dashboard.perf-low *::before,
      .solar-dashboard.perf-low *::after {
        transition-duration: 0s !important;
        animation-duration: 0s !important;
      }

      .solar-dashboard.perf-low .gauge-svg path,
      .solar-dashboard.perf-low .gauge-svg circle,
      .solar-dashboard.perf-low ha-icon {
        filter: none !important;
      }

      .solar-dashboard.perf-low .pv-segment,
      .solar-dashboard.perf-low .battery-horizontal-fill {
        box-shadow: none !important;
      }

      /* Wall display: larger and easier to read from a distance. */
      @media screen and (min-width: 700px) {
        .solar-dashboard.display-wall {
          gap: 12px !important;
          grid-template-columns:
            repeat(2, minmax(0, 1fr)) !important;
          grid-template-areas:
            "pv battery"
            "live live"
            "mppt mppt"
            "payment runtime" !important;
        }

        .solar-dashboard.display-wall .mppt-grid {
          grid-template-columns:
            repeat(var(--mppt-count), minmax(0, 1fr)) !important;
          gap: 10px;
        }

        .solar-dashboard.display-wall .pv-total-panel,
        .solar-dashboard.display-wall .battery-panel {
          height: 112px !important;
        }

        .solar-dashboard.display-wall .live-panel {
          height: 132px !important;
        }

        .solar-dashboard.display-wall .mppt-panel {
          height: 190px !important;
        }

        .solar-dashboard.display-wall .information-panel {
          height: 100px !important;
        }

        .solar-dashboard.display-wall .v5-bar-main {
          font-size: 26px !important;
        }

        .solar-dashboard.display-wall .v5-bar-title {
          font-size: 10px !important;
        }

        .solar-dashboard.display-wall .pv-split-track,
        .solar-dashboard.display-wall .battery-horizontal-track {
          height: 16px !important;
        }

        .solar-dashboard.display-wall .live-item ha-icon {
          width: 31px !important;
          height: 31px !important;
        }

        .solar-dashboard.display-wall .live-title {
          font-size: 9px !important;
        }

        .solar-dashboard.display-wall .live-current {
          font-size: 22px !important;
        }

        .solar-dashboard.display-wall .live-double-value {
          font-size: 9px !important;
          line-height: 1.35 !important;
        }

        .solar-dashboard.display-wall .mppt-title {
          font-size: 17px !important;
        }

        .solar-dashboard.display-wall .mppt-current-value {
          font-size: 28px !important;
        }

        .solar-dashboard.display-wall .mppt-daily-value {
          font-size: 13px !important;
        }

        .solar-dashboard.display-wall .information-title {
          font-size: 11px !important;
        }

        .solar-dashboard.display-wall .information-value {
          font-size: 22px !important;
        }
      }

'''

if 'v0.8.1-alpha – DISPLAY / PERFORMANCE PROFILES' not in text:
    if css_anchor not in text:
        raise SystemExit('CSS anchor not found')
    text = text.replace(css_anchor, compat_css + css_anchor, 1)

path.write_text(text, encoding='utf-8')
print('Applied v0.8.1-alpha display/performance profiles')
