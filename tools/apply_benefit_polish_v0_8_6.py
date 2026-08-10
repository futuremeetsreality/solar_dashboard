#!/usr/bin/env python3
# File: tools/apply_benefit_polish_v0_8_6.py
# Timestamp: 2026-08-10 18:29 +0200

"""Polish the v0.8.6 PV benefit card, especially the large phone layout.

Large uses a calm 50/50 upper split and a full-width total benefit footer.
Small and max keep their dedicated information density.
"""

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DASHBOARD = ROOT / "dashboard.yaml"


def main() -> None:
    text = DASHBOARD.read_text(encoding="utf-8")

    # Append late CSS overrides so they intentionally win over the base benefit styles.
    css = r'''

      /* ==========================================================
       * v0.8.6-alpha BENEFIT POLISH
       * Large: quiet 50/50 split + full-width total footer
       * ========================================================== */
      .module-benefit.module-size-large {
        padding: 12px 14px !important;
        gap: 7px !important;
        align-content: center;
      }

      .module-benefit.module-size-large .benefit-title {
        font-size: 10px !important;
        line-height: 1.1;
        letter-spacing: 0.08em;
        text-transform: uppercase;
        color: var(--secondary-text-color) !important;
        opacity: 0.92;
      }

      .module-benefit.module-size-large .benefit-main-grid {
        grid-template-columns: minmax(0, 1fr) minmax(0, 1fr) !important;
        gap: 0 !important;
        align-items: start;
      }

      .module-benefit.module-size-large .benefit-part {
        display: flex !important;
        min-width: 0;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        gap: 1px;
        text-align: center;
        padding: 1px 7px 4px;
      }

      .module-benefit.module-size-large .benefit-part + .benefit-part {
        border-left: 1px solid var(--solar-divider);
      }

      .module-benefit.module-size-large .benefit-part ha-icon {
        display: none !important;
      }

      .module-benefit.module-size-large .benefit-part-label {
        width: 100%;
        font-size: 8px !important;
        line-height: 1.15;
        font-weight: 800;
        letter-spacing: 0.03em;
        text-transform: uppercase;
        white-space: nowrap;
        overflow: hidden;
        text-overflow: ellipsis;
      }

      .module-benefit.module-size-large .benefit-part-value {
        font-size: 20px !important;
        line-height: 1.05;
        font-weight: 900;
      }

      .module-benefit.module-size-large .benefit-energy {
        display: block !important;
        font-size: 8px !important;
        line-height: 1.15;
        color: var(--secondary-text-color) !important;
      }

      .module-benefit.module-size-large .benefit-rate,
      .module-benefit.module-size-large .benefit-share-wrap {
        display: none !important;
      }

      .module-benefit.module-size-large .benefit-total {
        display: flex !important;
        flex-direction: column;
        justify-content: center;
        align-items: center;
        gap: 0;
        padding-top: 7px;
        border-top: 1px solid var(--solar-divider);
        color: var(--primary-text-color);
      }

      .module-benefit.module-size-large .benefit-total-label {
        order: 1;
        font-size: 8px !important;
        line-height: 1.1;
        font-weight: 800;
        letter-spacing: 0.06em;
        text-transform: uppercase;
        color: var(--secondary-text-color) !important;
      }

      .module-benefit.module-size-large .benefit-total-value {
        order: 2;
        font-size: 25px !important;
        line-height: 1.05;
        font-weight: 900;
      }

      @media screen and (max-width: 699px) {
        .module-benefit.module-size-large {
          padding: 10px 11px !important;
          gap: 5px !important;
        }

        .module-benefit.module-size-large .benefit-part {
          padding-left: 5px;
          padding-right: 5px;
        }

        .module-benefit.module-size-large .benefit-part-value {
          font-size: 18px !important;
        }

        .module-benefit.module-size-large .benefit-total {
          padding-top: 5px;
        }

        .module-benefit.module-size-large .benefit-total-value {
          font-size: 22px !important;
        }
      }
'''

    if "v0.8.6-alpha BENEFIT POLISH" not in text:
        text = text.rstrip() + "\n" + css + "\n"

    DASHBOARD.write_text(text, encoding="utf-8")


if __name__ == "__main__":
    main()
