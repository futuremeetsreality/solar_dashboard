#!/usr/bin/env python3
# File: tools/build_dashboard.py
# Timestamp: 2026-08-10 18:10 +0200

"""Build the generated Home Assistant dashboard.

Build pipeline / Build-Pipeline:
1. Decode the proven legacy V7 base.
2. Apply the existing compatibility/theme/i18n/display migrations.
3. Replace migrated sections with modular sources from src/.
4. Apply configurable module visibility/order/size and prepared tracker slots.
5. Apply MPPT presentation polish.
6. Apply responsive PV benefit module.
7. Write the single user-facing dashboard.yaml.
"""

from __future__ import annotations

import base64
import gzip
import re
import runpy
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DASHBOARD = ROOT / "dashboard.yaml"
BASE = ROOT / "tools" / "dashboard_v7.yaml.gz.b64"
SRC = ROOT / "src"

LEGACY_PATCHES = [
    ROOT / "tools" / "apply_theme_v7_1.py",
    ROOT / "tools" / "apply_v72_theme.py",
    ROOT / "tools" / "apply_i18n_v0_8.py",
    ROOT / "tools" / "apply_display_v0_8_1.py",
]

MODULE_PATCH = ROOT / "tools" / "apply_modules_v0_8_3.py"
BENEFIT_PATCH = ROOT / "tools" / "apply_benefit_v0_8_6.py"


def decode_base() -> None:
    encoded = BASE.read_text(encoding="utf-8")
    raw = gzip.decompress(base64.b64decode(encoded))
    DASHBOARD.write_bytes(raw)


def run_legacy_patches() -> None:
    for patch in LEGACY_PATCHES:
        if not patch.exists():
            raise SystemExit(f"Missing legacy patch: {patch}")
        runpy.run_path(str(patch), run_name="__main__")


def read_source_object(path: Path, variable: str) -> str:
    text = path.read_text(encoding="utf-8")
    match = re.search(rf"const\s+{re.escape(variable)}\s*=\s*(\{{.*\}})\s*;", text, re.S)
    if not match:
        raise SystemExit(f"Could not read {variable} from {path}")
    return match.group(1)


def source_setting(name: str, default: str) -> str:
    text = (SRC / "config.js").read_text(encoding="utf-8")
    match = re.search(rf"\b{re.escape(name)}\s*:\s*'([^']+)'", text)
    return match.group(1) if match else default


def indent_source(text: str, spaces: int) -> str:
    prefix = " " * spaces
    return "\n".join(prefix + line if line else "" for line in text.strip().splitlines())


def apply_modular_sources() -> None:
    text = DASHBOARD.read_text(encoding="utf-8")
    text = re.sub(r"# solar_dashboard .*? - dashboard\.yaml", "# solar_dashboard v0.8.6-alpha - dashboard.yaml", text, count=1)

    notice = (
        "# GENERATED FILE - edit src/ and tools/build_dashboard.py instead.\n"
        "# GENERIERTE DATEI - Änderungen bitte in src/ und tools/build_dashboard.py vornehmen.\n"
    )
    if notice not in text:
        first_newline = text.find("\n") + 1
        text = text[:first_newline] + notice + text[first_newline:]

    defaults = {
        "language": source_setting("language", "auto"),
        "displayMode": source_setting("displayMode", "auto"),
        "performanceMode": source_setting("performanceMode", "auto"),
    }
    for key, value in defaults.items():
        text = re.sub(rf"({re.escape(key)}\s*:\s*)'[^']+'", rf"\1'{value}'", text, count=1)

    i18n = read_source_object(SRC / "i18n.js", "I18N_SOURCE")
    i18n_match = re.search(r"const I18N = \{.*?\n          \};", text, re.S)
    if not i18n_match:
        raise SystemExit("Generated dashboard I18N block not found")
    indented_i18n = "const I18N = " + i18n.replace("\n", "\n          ") + ";"
    text = text[:i18n_match.start()] + indented_i18n + text[i18n_match.end():]

    layout_source = (SRC / "layout.js").read_text(encoding="utf-8")
    layout_body = re.sub(r"^/\*.*?\*/\s*", "", layout_source, count=1, flags=re.S).strip()
    layout_match = re.search(r"          const configuredDisplayMode =.*?          if \(performanceMode === 'auto'\) \{.*?\n          \}", text, re.S)
    if not layout_match:
        raise SystemExit("Display/performance resolver not found")
    text = text[:layout_match.start()] + indent_source(layout_body, 10) + text[layout_match.end():]

    old_runtime = """          const runtimeRaw =
            runtimeSensor?.state || t.unknown;

          const runtime =
            runtimeRaw === 'unknown' ||
            runtimeRaw === 'unavailable'
              ? t.unknown
              : runtimeRaw;"""
    new_runtime = """          const runtime = formatRuntimeSensor(
            runtimeSensor,
            t.unknown
          );"""
    if old_runtime not in text:
        raise SystemExit("Battery runtime block not found")
    text = text.replace(old_runtime, new_runtime, 1)

    logic_source = (SRC / "logic.js").read_text(encoding="utf-8")
    helper_match = re.search(r"function formatRuntimeSensor\(.*?\n\}", logic_source, re.S)
    if not helper_match:
        raise SystemExit("formatRuntimeSensor helper not found in src/logic.js")
    helper = indent_source(helper_match.group(0), 10)
    marker = "          /*\n           * ========================================================\n           * AKTUELLE LEISTUNGEN"
    if "function formatRuntimeSensor(" not in text:
        text = text.replace(marker, helper + "\n\n" + marker, 1)

    styles = (SRC / "styles.css").read_text(encoding="utf-8").strip()
    styles = indent_source(styles, 6)
    css_match = re.search(
        r"      /\*\n       \* ==========================================================\n       \* v0\.8\.1-alpha .*?DISPLAY / PERFORMANCE PROFILES.*?(?=      /\*\n       \* ==========================================================\n       \* GRUNDLAYOUT)",
        text,
        re.S,
    )
    if not css_match:
        raise SystemExit("Legacy display/performance CSS block not found")
    text = text[:css_match.start()] + styles + "\n\n" + text[css_match.end():]

    replacements = {
        "BENUTZERKONFIGURATION – NUR DIESEN BLOCK ANPASSEN": "USER CONFIGURATION / BENUTZERKONFIGURATION – ONLY EDIT THIS BLOCK / NUR DIESEN BLOCK ANPASSEN",
        "HILFSFUNKTIONEN": "HELPER FUNCTIONS / HILFSFUNKTIONEN",
        "AKTUELLE LEISTUNGEN": "CURRENT POWER / AKTUELLE LEISTUNGEN",
        "TAGESENERGIEN": "DAILY ENERGY / TAGESENERGIEN",
        "BATTERIEWERTE": "BATTERY VALUES / BATTERIEWERTE",
        "NETZSTATUS": "GRID STATUS / NETZSTATUS",
        "WEITERE WERTE": "ADDITIONAL VALUES / WEITERE WERTE",
        "AUSGABE": "OUTPUT / AUSGABE",
        "GRUNDLAYOUT": "BASE LAYOUT / GRUNDLAYOUT",
        "LIVE-ENERGIEFLUSS": "LIVE ENERGY FLOW / LIVE-ENERGIEFLUSS",
        "VERGÜTUNG UND RESTLAUFZEIT": "REVENUE AND RUNTIME / VERGÜTUNG UND RESTLAUFZEIT",
    }
    for old, new in replacements.items():
        text = text.replace(old, new)

    DASHBOARD.write_text(text, encoding="utf-8")


def apply_module_patch() -> None:
    if not MODULE_PATCH.exists():
        raise SystemExit(f"Missing module patch: {MODULE_PATCH}")
    runpy.run_path(str(MODULE_PATCH), run_name="__main__")


def apply_mppt_polish() -> None:
    text = DASHBOARD.read_text(encoding="utf-8")
    text = re.sub(r"# solar_dashboard .*? - dashboard\.yaml", "# solar_dashboard v0.8.6-alpha - dashboard.yaml", text, count=1)

    old_return = """                energyToday,
                colorStart,
                colorEnd,
                gauge"""
    new_return = """                energyToday,
                currentPercent: maxKw > 0
                  ? Math.min(Math.max((power / maxKw) * 100, 0), 999)
                  : 0,
                colorStart,
                colorEnd,
                gauge"""
    if old_return not in text:
        raise SystemExit("MPPT tracker return block not found")
    text = text.replace(old_return, new_return, 1)

    old_box = """                <div class=\"mppt-daily-box\">\n\n                  <ha-icon\n                    icon=\"mdi:lightning-bolt\"\n                  ></ha-icon>\n\n                  <div>\n\n                    <div class=\"mppt-daily-value\">\n                      ${formatEnergy(tracker.energyToday)}\n                      kWh\n                    </div>\n\n                    <div class=\"small-label\">\n                      ${t.todayUpper} · ${t.maxUpper} ${formatNumber(\n                        tracker.maxKw,\n                        2,\n                        2\n                      )} kW\n                    </div>\n\n                  </div>\n\n                </div>"""

    new_box = """                <div class=\"mppt-daily-box\">\n\n                  <div class=\"mppt-percent\">\n                    <ha-icon icon=\"mdi:lightning-bolt\"></ha-icon>\n                    <span>${formatNumber(tracker.currentPercent, 0, 0)} %</span>\n                  </div>\n\n                  <div class=\"mppt-daily-data\">\n                    <div class=\"mppt-daily-value\">\n                      ${formatEnergy(tracker.energyToday)} kWh\n                    </div>\n                    <div class=\"small-label\">\n                      ${t.maxUpper} ${formatNumber(tracker.maxKw, 2, 2)} kW\n                    </div>\n                  </div>\n\n                </div>"""

    if old_box not in text:
        raise SystemExit("MPPT daily box not found")
    text = text.replace(old_box, new_box, 1)

    css = """
      /* v0.8.5-alpha MPPT footer: current percentage + daily energy */
      .mppt-daily-box {
        justify-content: space-between !important;
      }

      .mppt-percent {
        display: flex;
        align-items: center;
        gap: 5px;
        color: var(--tracker-end);
        font-weight: 800;
        white-space: nowrap;
      }

      .mppt-percent ha-icon {
        color: var(--tracker-end);
      }

      .mppt-daily-data {
        text-align: right;
        min-width: 0;
      }
"""
    marker = "    extra_styles: |\n"
    if marker not in text:
        raise SystemExit("extra_styles block not found for MPPT CSS")
    text = text.replace(marker, marker + css, 1)

    DASHBOARD.write_text(text, encoding="utf-8")


def apply_benefit_patch() -> None:
    if not BENEFIT_PATCH.exists():
        raise SystemExit(f"Missing benefit patch: {BENEFIT_PATCH}")
    runpy.run_path(str(BENEFIT_PATCH), run_name="__main__")


def sanity_check() -> None:
    text = DASHBOARD.read_text(encoding="utf-8")
    required = [
        "type: vertical-stack",
        "custom:power-flux-card",
        "custom:button-card",
        "v0.8.6-alpha",
        "language: 'auto'",
        "displayMode: 'auto'",
        "performanceMode: 'auto'",
        "modules: [",
        "size: 'large'",
        "module-size-small",
        "module-size-large",
        "module-size-max",
        "enabled: false",
        "MPPT 4",
        "function formatRuntimeSensor(",
        "const I18N = {",
        "currentPercent:",
        "class=\"mppt-percent\"",
        "benefitEntities:",
        "class=\"panel benefit-panel",
        "module-benefit",
        "pvBenefitToday",
        "totalBenefitToday",
    ]
    missing = [item for item in required if item not in text]
    if missing:
        raise SystemExit(f"Build sanity check failed, missing: {missing}")


if __name__ == "__main__":
    decode_base()
    run_legacy_patches()
    apply_modular_sources()
    apply_module_patch()
    apply_mppt_polish()
    apply_benefit_patch()
    sanity_check()
    print("Built dashboard.yaml v0.8.6-alpha from modular sources")
