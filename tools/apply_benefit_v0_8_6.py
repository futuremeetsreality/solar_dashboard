#!/usr/bin/env python3
# File: tools/apply_benefit_v0_8_6.py
# Timestamp: 2026-08-10 18:05 +0200

"""Add the responsive PV benefit module for v0.8.6-alpha.

The module supports small, large and max layouts and uses Solar Yield Calculator
values by default. Power Flux remains outside the configurable module system.

Das Modul unterstützt small, large und max und verwendet standardmäßig Werte des
Solar Yield Calculators. Power Flux bleibt außerhalb des konfigurierbaren Systems.
"""

from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DASHBOARD = ROOT / "dashboard.yaml"
SOURCE_CONFIG = ROOT / "src" / "config.js"


def extract_object(text: str, key: str) -> str:
    match = re.search(rf"\b{re.escape(key)}\s*:\s*\{{", text)
    if not match:
        raise SystemExit(f"Could not find object {key} in src/config.js")
    start = text.find("{", match.start())
    depth = 0
    quote = None
    escaped = False
    for i in range(start, len(text)):
        ch = text[i]
        if quote:
            if escaped:
                escaped = False
            elif ch == "\\":
                escaped = True
            elif ch == quote:
                quote = None
            continue
        if ch in ("'", '"', "`"):
            quote = ch
            continue
        if ch == "{":
            depth += 1
        elif ch == "}":
            depth -= 1
            if depth == 0:
                return text[start:i + 1]
    raise SystemExit(f"Unclosed object {key}")


def indent_object_for_yaml_block(source: str, base_spaces: int = 12) -> str:
    lines = source.splitlines()
    if len(lines) <= 1:
        return source
    prefix = " " * base_spaces
    return lines[0] + "\n" + "\n".join(prefix + line for line in lines[1:])


def main() -> None:
    text = DASHBOARD.read_text(encoding="utf-8")
    config_source = SOURCE_CONFIG.read_text(encoding="utf-8")

    text = re.sub(
        r"# solar_dashboard .*? - dashboard\.yaml",
        "# solar_dashboard v0.8.6-alpha - dashboard.yaml",
        text,
        count=1,
    )

    # Insert the user-facing benefit entity mapping before limits.
    benefit_source = indent_object_for_yaml_block(
        extract_object(config_source, "benefitEntities")
    )
    if "benefitEntities:" not in text:
        marker = "            limits: {"
        if marker not in text:
            raise SystemExit("CONFIG.limits marker not found")
        block = (
            "            /*\n"
            "             * PV BENEFIT / PV-NUTZEN\n"
            "             * Default entity names target Solar Yield Calculator.\n"
            "             * Standard-Entity-Namen verwenden Solar Yield Calculator.\n"
            "             */\n"
            f"            benefitEntities: {benefit_source},\n\n"
        )
        text = text.replace(marker, block + marker, 1)

    # Enable the new module id in the module resolver.
    text = text.replace(
        "'mppt', 'pvTotal', 'battery', 'live', 'payment', 'runtime'",
        "'mppt', 'pvTotal', 'battery', 'live', 'benefit', 'runtime'",
        1,
    )

    # Financial calculations and unit-aware rates.
    old_values = """          const compensation = getNumber(\n            CONFIG.entities.compensationToday\n          );"""
    new_values = r'''          function benefitNumber(entityId) {
            if (!entityId) return 0;
            return getNumber(entityId);
          }

          function benefitRate(entityId) {
            const sensor = getSensor(entityId);
            if (!sensor) return { value: 0, text: '–' };

            const raw = Number.parseFloat(sensor.state);
            if (!Number.isFinite(raw)) return { value: 0, text: '–' };

            const unit = String(sensor.attributes?.unit_of_measurement || '').trim();
            const normalizedUnit = unit.toLowerCase();

            if (
              normalizedUnit.includes('eur/kwh') ||
              normalizedUnit.includes('€/kwh')
            ) {
              const ct = raw * 100;
              return {
                value: ct,
                text: `${formatNumber(ct, 2, 2)} ct/kWh`
              };
            }

            if (normalizedUnit.includes('ct/kwh')) {
              return {
                value: raw,
                text: `${formatNumber(raw, 2, 2)} ct/kWh`
              };
            }

            return {
              value: raw,
              text: `${formatNumber(raw, 2, 2)}${unit ? ` ${unit}` : ''}`
            };
          }

          const exportRevenueToday = benefitNumber(
            CONFIG.benefitEntities?.exportRevenueToday
          );

          const selfConsumptionSavingToday = benefitNumber(
            CONFIG.benefitEntities?.selfConsumptionSavingToday
          );

          const configuredTotalBenefit = benefitNumber(
            CONFIG.benefitEntities?.totalBenefitToday
          );

          const totalBenefitToday = configuredTotalBenefit > 0
            ? configuredTotalBenefit
            : exportRevenueToday + selfConsumptionSavingToday;

          const exportRevenueRate = benefitRate(
            CONFIG.benefitEntities?.exportRevenueRate
          );

          const selfConsumptionSavingRate = benefitRate(
            CONFIG.benefitEntities?.selfConsumptionSavingRate
          );

          const configuredSelfSupplyToday = CONFIG.benefitEntities?.selfSupplyEnergyToday
            ? getEnergy(CONFIG.benefitEntities.selfSupplyEnergyToday)
            : 0;

          const selfSupplyToday = configuredSelfSupplyToday > 0
            ? configuredSelfSupplyToday
            : Math.max(solarToday - exportToday, 0);

          const exportBenefitShare = totalBenefitToday > 0
            ? Math.min(Math.max((exportRevenueToday / totalBenefitToday) * 100, 0), 100)
            : 0;

          const savingBenefitShare = totalBenefitToday > 0
            ? Math.min(Math.max((selfConsumptionSavingToday / totalBenefitToday) * 100, 0), 100)
            : 0;'''

    if old_values not in text:
        raise SystemExit("Legacy compensation calculation not found")
    text = text.replace(old_values, new_values, 1)

    # Replace legacy payment tile with the adaptive benefit tile.
    old_payment = re.search(
        r"              <!-- =============================================== -->\n"
        r"              <!-- VERGÜTUNG -->\n"
        r"              <!-- =============================================== -->\n\n"
        r"              <div class=\"panel information-panel payment-panel.*?"
        r"              </div>\n\n"
        r"              <!-- =============================================== -->\n"
        r"              <!-- RESTLAUFZEIT -->",
        text,
        re.S,
    )
    if not old_payment:
        raise SystemExit("Legacy payment module not found")

    benefit_html = r'''              <!-- =============================================== -->
              <!-- PV BENEFIT / PV-NUTZEN -->
              <!-- =============================================== -->

              <div class="panel benefit-panel module-item module-benefit${moduleClass('benefit')}" style="--module-order:${moduleOrder('benefit')};">

                <div class="benefit-title">${t.pvBenefitToday}</div>

                <div class="benefit-main-grid">
                  <div class="benefit-part benefit-export">
                    <ha-icon icon="mdi:transmission-tower-export"></ha-icon>
                    <div class="benefit-part-label">${t.feedInRevenue}</div>
                    <div class="benefit-part-value">${formatNumber(exportRevenueToday, 2, 2)} €</div>
                    <div class="benefit-energy">${formatEnergy(exportToday)} kWh</div>
                    <div class="benefit-rate">${exportRevenueRate.text}</div>
                  </div>

                  <div class="benefit-part benefit-saving">
                    <ha-icon icon="mdi:home-lightning-bolt"></ha-icon>
                    <div class="benefit-part-label">${t.saving}</div>
                    <div class="benefit-part-value">${formatNumber(selfConsumptionSavingToday, 2, 2)} €</div>
                    <div class="benefit-energy">${formatEnergy(selfSupplyToday)} kWh</div>
                    <div class="benefit-rate">${selfConsumptionSavingRate.text}</div>
                  </div>
                </div>

                <div class="benefit-total">
                  <span class="benefit-total-value">${formatNumber(totalBenefitToday, 2, 2)} €</span>
                  <span class="benefit-total-label">${t.totalBenefit}</span>
                </div>

                <div class="benefit-share-wrap">
                  <div class="benefit-share-bar">
                    <div class="benefit-share-export" style="width:${exportBenefitShare}%;"></div>
                    <div class="benefit-share-saving" style="width:${savingBenefitShare}%;"></div>
                  </div>
                  <div class="benefit-share-labels">
                    <span>${t.export} ${formatNumber(exportBenefitShare, 0, 0)} %</span>
                    <span>${t.saving} ${formatNumber(savingBenefitShare, 0, 0)} %</span>
                  </div>
                </div>

              </div>

              <!-- =============================================== -->
              <!-- RESTLAUFZEIT -->'''
    text = text[:old_payment.start()] + benefit_html + text[old_payment.end():]

    css_marker = "    extra_styles: |\n"
    css = r'''
      /* ==========================================================
       * v0.8.6-alpha PV BENEFIT / PV-NUTZEN
       * small = compact, large = split detail, max = full economics
       * ========================================================== */
      .benefit-panel {
        min-width: 0;
        padding: 14px 16px;
        display: grid;
        grid-template-columns: 1fr;
        gap: 8px;
        background:
          radial-gradient(circle at 12% 110%, rgba(38,198,218,0.10), transparent 45%),
          radial-gradient(circle at 88% 110%, rgba(255,193,7,0.10), transparent 45%),
          var(--solar-surface-strong) !important;
      }

      .benefit-title {
        text-align: center;
        font-size: 12px;
        font-weight: 800;
        letter-spacing: 0.04em;
        color: var(--primary-text-color);
      }

      .benefit-main-grid {
        display: grid;
        grid-template-columns: 1fr 1fr;
        gap: 8px;
      }

      .benefit-part {
        min-width: 0;
        display: grid;
        grid-template-columns: auto 1fr;
        grid-template-areas:
          "icon label"
          "icon value"
          "icon energy"
          "icon rate";
        column-gap: 7px;
        align-items: center;
      }

      .benefit-part ha-icon {
        grid-area: icon;
        width: 26px;
        height: 26px;
      }

      .benefit-export,
      .benefit-export ha-icon { color: #26c6da; }
      .benefit-saving,
      .benefit-saving ha-icon { color: #ffd740; }

      .benefit-part-label {
        grid-area: label;
        font-size: 9px;
        font-weight: 800;
        opacity: 0.82;
        white-space: nowrap;
        overflow: hidden;
        text-overflow: ellipsis;
      }

      .benefit-part-value {
        grid-area: value;
        font-size: 21px;
        line-height: 1.05;
        font-weight: 900;
      }

      .benefit-energy,
      .benefit-rate {
        font-size: 9px;
        color: var(--secondary-text-color);
      }
      .benefit-energy { grid-area: energy; }
      .benefit-rate { grid-area: rate; }

      .benefit-total {
        display: flex;
        justify-content: center;
        align-items: baseline;
        gap: 7px;
        color: var(--primary-text-color);
      }

      .benefit-total-value {
        font-size: 25px;
        font-weight: 900;
      }

      .benefit-total-label {
        font-size: 9px;
        font-weight: 800;
        color: var(--secondary-text-color);
      }

      .benefit-share-wrap { display: none; }

      .module-benefit.module-size-small {
        align-content: center;
      }
      .module-benefit.module-size-small .benefit-title {
        font-size: 10px;
      }
      .module-benefit.module-size-small .benefit-total {
        order: 1;
      }
      .module-benefit.module-size-small .benefit-main-grid {
        order: 2;
        gap: 4px;
      }
      .module-benefit.module-size-small .benefit-part {
        display: block;
        text-align: center;
      }
      .module-benefit.module-size-small .benefit-part ha-icon,
      .module-benefit.module-size-small .benefit-energy,
      .module-benefit.module-size-small .benefit-rate {
        display: none;
      }
      .module-benefit.module-size-small .benefit-part-label {
        font-size: 8px;
      }
      .module-benefit.module-size-small .benefit-part-value {
        font-size: 14px;
      }
      .module-benefit.module-size-small .benefit-total-value {
        font-size: 24px;
      }

      .module-benefit.module-size-large .benefit-rate,
      .module-benefit.module-size-large .benefit-share-wrap {
        display: none;
      }

      .module-benefit.module-size-max {
        grid-template-columns: 1fr auto;
        grid-template-areas:
          "title title"
          "parts total"
          "share share";
        column-gap: 20px;
        padding: 15px 20px;
      }
      .module-benefit.module-size-max .benefit-title { grid-area: title; }
      .module-benefit.module-size-max .benefit-main-grid { grid-area: parts; gap: 24px; }
      .module-benefit.module-size-max .benefit-total {
        grid-area: total;
        min-width: 150px;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        gap: 0;
      }
      .module-benefit.module-size-max .benefit-total-value { font-size: 32px; }
      .module-benefit.module-size-max .benefit-share-wrap {
        grid-area: share;
        display: block;
      }
      .benefit-share-bar {
        display: flex;
        width: 100%;
        height: 8px;
        overflow: hidden;
        border-radius: 999px;
        background: var(--solar-track);
      }
      .benefit-share-export {
        background: linear-gradient(90deg, #00acc1, #26c6da);
      }
      .benefit-share-saving {
        background: linear-gradient(90deg, #ffb300, #ffd740);
      }
      .benefit-share-labels {
        display: flex;
        justify-content: space-between;
        margin-top: 4px;
        font-size: 8px;
        color: var(--secondary-text-color);
      }

      @media screen and (max-width: 699px) {
        .benefit-panel {
          padding: 11px 12px;
        }
        .benefit-part-value { font-size: 18px; }
        .benefit-total-value { font-size: 22px; }
        .module-benefit.module-size-max {
          grid-template-columns: 1fr;
          grid-template-areas:
            "title"
            "parts"
            "total"
            "share";
          gap: 7px;
        }
      }
'''
    if css_marker not in text:
        raise SystemExit("extra_styles block not found")
    text = text.replace(css_marker, css_marker + css, 1)

    DASHBOARD.write_text(text, encoding="utf-8")


if __name__ == "__main__":
    main()
