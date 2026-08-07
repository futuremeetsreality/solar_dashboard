# apply_v72_theme.py
# Zeitstempel: 2026-08-07 21:35

from pathlib import Path

path = Path("dashboard.yaml")
text = path.read_text(encoding="utf-8")

text = text.replace(
    "# solar_dashboard V7.1 - dashboard.yaml",
    "# solar_dashboard V7.2 - dashboard.yaml",
    1,
)
text = text.replace(
    "# solar_dashboard V7 - dashboard.yaml",
    "# solar_dashboard V7.2 - dashboard.yaml",
    1,
)

# Tracker-Footer nicht mehr mit einer festen hellen Farbe ausgeben.
# Stattdessen werden die Trackerfarben als CSS-Variablen übergeben und
# danach theme-adaptiv mit der jeweiligen HA-Textfarbe gemischt.
text = text.replace(
    'style="color:${tracker.colorEnd};"',
    'style="--tracker-start:${tracker.colorStart}; --tracker-end:${tracker.colorEnd};"',
)

marker = "      /* V7.2 ADAPTIVE THEME MANAGER */"
if marker not in text:
    theme_css = r'''

      /* V7.2 ADAPTIVE THEME MANAGER */
      /*
       * Die Oberflächen basieren auf den aktiven Home-Assistant-Themefarben.
       * Dadurch funktioniert derselbe Code in Hell- und Dunkelmodus sowie
       * mit benutzerdefinierten HA-Themes. Farbakzente werden mit der
       * aktuellen Text-/Kartenfarbe gemischt, damit der Kontrast erhalten bleibt.
       */

      .solar-dashboard {
        --solar-pv: color-mix(in srgb, #ffb300 82%, var(--solar-text) 18%);
        --solar-house: color-mix(in srgb, #42a5f5 82%, var(--solar-text) 18%);
        --solar-grid: color-mix(in srgb, #00b8d4 82%, var(--solar-text) 18%);
        --solar-battery: color-mix(in srgb, #43a047 82%, var(--solar-text) 18%);
        --solar-payment: color-mix(in srgb, #42a5f5 78%, var(--solar-text) 22%);
        --solar-runtime: color-mix(in srgb, #8e5cff 78%, var(--solar-text) 22%);

        --solar-glow-pv: color-mix(in srgb, #ffb300 15%, transparent);
        --solar-glow-house: color-mix(in srgb, #42a5f5 11%, transparent);
        --solar-glow-grid: color-mix(in srgb, #00b8d4 10%, transparent);
        --solar-glow-battery: color-mix(in srgb, #43a047 13%, transparent);
        --solar-glow-payment: color-mix(in srgb, #42a5f5 12%, transparent);
        --solar-glow-runtime: color-mix(in srgb, #8e5cff 12%, transparent);

        --solar-glass-top:
          color-mix(in srgb, var(--solar-surface) 96%, var(--solar-text) 4%);
        --solar-glass-bottom:
          color-mix(in srgb, var(--solar-surface) 99%, var(--solar-text) 1%);

        --solar-track:
          color-mix(in srgb, var(--solar-text) 9%, transparent);
        --solar-inset:
          color-mix(in srgb, var(--solar-text) 5%, transparent);
        --solar-gauge-track:
          color-mix(in srgb, var(--solar-text) 14%, transparent);
        --solar-border:
          color-mix(in srgb, var(--solar-text) 13%, transparent);
        --solar-divider:
          color-mix(in srgb, var(--solar-text) 15%, transparent);

        --solar-shadow:
          0 7px 22px rgba(0, 0, 0, 0.13);
      }

      .panel {
        background:
          linear-gradient(
            145deg,
            var(--solar-glass-top),
            var(--solar-glass-bottom)
          );
        border-color: var(--solar-border);
        box-shadow: var(--solar-shadow);
      }

      /* MPPT: jeder Tracker erhält einen Glow aus seinen eigenen Farben. */
      .mppt-panel {
        background:
          radial-gradient(
            circle at 12% 115%,
            color-mix(in srgb, var(--tracker-start) 14%, transparent),
            transparent 48%
          ),
          radial-gradient(
            circle at 92% -10%,
            color-mix(in srgb, var(--tracker-end) 8%, transparent),
            transparent 46%
          ),
          linear-gradient(
            145deg,
            var(--solar-glass-top),
            var(--solar-glass-bottom)
          );
      }

      .mppt-daily-box {
        background:
          linear-gradient(
            145deg,
            color-mix(in srgb, var(--solar-inset) 86%, var(--tracker-end) 14%),
            var(--solar-inset)
          );
        border-color:
          color-mix(in srgb, var(--solar-border) 78%, var(--tracker-start) 22%);
      }

      /* Live-Leiste: dezente Farbzonen für PV / Haus / Netz / Batterie. */
      .live-panel {
        background:
          radial-gradient(circle at 10% 115%, var(--solar-glow-pv), transparent 34%),
          radial-gradient(circle at 38% 115%, var(--solar-glow-house), transparent 34%),
          radial-gradient(circle at 66% 115%, var(--solar-glow-grid), transparent 34%),
          radial-gradient(circle at 92% 115%, var(--solar-glow-battery), transparent 34%),
          linear-gradient(145deg, var(--solar-glass-top), var(--solar-glass-bottom));
      }

      .live-pv ha-icon,
      .live-pv .live-current {
        color: var(--solar-pv);
      }

      .live-house ha-icon,
      .live-house .live-current {
        color: var(--solar-house);
      }

      .live-grid-value ha-icon,
      .live-grid-value .live-current {
        color: var(--solar-grid);
      }

      .live-battery ha-icon,
      .live-battery .live-current {
        color: var(--solar-battery);
      }

      /* PV Total: stärkerer Orange-/Grün-Verlauf, aber weiterhin Theme-basiert. */
      .pv-total-panel.v5-bar-panel {
        background:
          radial-gradient(
            circle at 10% 115%,
            color-mix(in srgb, #ff9800 18%, transparent),
            transparent 46%
          ),
          radial-gradient(
            circle at 92% 115%,
            color-mix(in srgb, #43a047 16%, transparent),
            transparent 46%
          ),
          radial-gradient(
            circle at 52% -25%,
            color-mix(in srgb, #64b5f6 6%, transparent),
            transparent 52%
          ),
          linear-gradient(
            145deg,
            var(--solar-glass-top),
            var(--solar-glass-bottom)
          );
      }

      .pv-percent {
        color: var(--solar-pv) !important;
      }

      .tracker-footer-values span {
        color:
          color-mix(
            in srgb,
            var(--tracker-end) 76%,
            var(--solar-text) 24%
          ) !important;
        text-shadow:
          0 0 7px color-mix(in srgb, var(--tracker-start) 18%, transparent);
      }

      .pv-split-track,
      .battery-horizontal-track {
        background:
          linear-gradient(
            180deg,
            color-mix(in srgb, var(--solar-track) 88%, var(--solar-text) 12%),
            var(--solar-track)
          );
        border-color: var(--solar-border);
      }

      /* Batterie: Grün plus warmer Lade-/Entlade-Akzent. */
      .battery-panel.v5-bar-panel {
        background:
          radial-gradient(
            circle at 10% 115%,
            color-mix(in srgb, #43a047 15%, transparent),
            transparent 48%
          ),
          radial-gradient(
            circle at 92% 115%,
            color-mix(in srgb, #ffb300 8%, transparent),
            transparent 48%
          ),
          linear-gradient(
            145deg,
            var(--solar-glass-top),
            var(--solar-glass-bottom)
          );
      }

      /* Vergütung und Restlaufzeit erhalten eigene dezente Glows. */
      .payment-panel {
        background:
          radial-gradient(circle at 8% 110%, var(--solar-glow-payment), transparent 48%),
          radial-gradient(circle at 94% -20%, color-mix(in srgb, #26c6da 6%, transparent), transparent 44%),
          linear-gradient(145deg, var(--solar-glass-top), var(--solar-glass-bottom));
      }

      .runtime-panel {
        background:
          radial-gradient(circle at 10% 110%, var(--solar-glow-runtime), transparent 48%),
          radial-gradient(circle at 94% -20%, color-mix(in srgb, #b388ff 7%, transparent), transparent 44%),
          linear-gradient(145deg, var(--solar-glass-top), var(--solar-glass-bottom));
      }

      .payment-panel ha-icon,
      .payment-panel .information-title {
        color: var(--solar-payment);
      }

      .runtime-panel ha-icon,
      .runtime-panel .information-title {
        color: var(--solar-runtime);
      }

      /* Kleine Texte erhalten etwas mehr Kontrast, besonders im Hellmodus. */
      .v5-bar-footer,
      .v7-pv-footer,
      .live-double-value,
      .information-subtitle,
      .small-label {
        color:
          color-mix(
            in srgb,
            var(--solar-text-secondary) 86%,
            var(--solar-text) 14%
          );
      }
'''

    # dashboard.yaml endet innerhalb von extra_styles: |.
    # Daher kann der Theme-Block direkt mit derselben Einrückung angehängt werden.
    text = text.rstrip() + theme_css + "\n"

path.write_text(text, encoding="utf-8")
