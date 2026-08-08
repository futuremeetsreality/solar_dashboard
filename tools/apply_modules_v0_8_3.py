#!/usr/bin/env python3
# File: tools/apply_modules_v0_8_3.py
# Timestamp: 2026-08-08 08:05 +0200

"""Apply v0.8.3-alpha configurable module visibility/order.

The user controls modules from CONFIG.modules. Only known module IDs are accepted.
Power Flux intentionally stays outside this system as the separate first Lovelace card.

Der Benutzer steuert die Module über CONFIG.modules. Es werden nur bekannte Modul-IDs
akzeptiert. Power Flux bleibt absichtlich außerhalb dieses Systems als separate erste
Lovelace-Karte.
"""

from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DASHBOARD = ROOT / "dashboard.yaml"
SOURCE_CONFIG = ROOT / "src" / "config.js"


def extract_array(text: str, key: str) -> str:
    """Return the complete JS array expression assigned to key."""
    match = re.search(rf"\b{re.escape(key)}\s*:\s*\[", text)
    if not match:
        raise SystemExit(f"Could not find array {key} in src/config.js")

    start = text.find("[", match.start())
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
        if ch == "[":
            depth += 1
        elif ch == "]":
            depth -= 1
            if depth == 0:
                return text[start : i + 1]

    raise SystemExit(f"Unclosed array {key} in src/config.js")


def replace_js_array(text: str, key: str, array_source: str, occurrence: int = 1) -> str:
    """Replace the nth JS array assigned to key while respecting nested brackets."""
    matches = list(re.finditer(rf"\b{re.escape(key)}\s*:\s*\[", text))
    if len(matches) < occurrence:
        raise SystemExit(f"Could not find target array {key} occurrence {occurrence}")

    match = matches[occurrence - 1]
    start = text.find("[", match.start())
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
        if ch == "[":
            depth += 1
        elif ch == "]":
            depth -= 1
            if depth == 0:
                return text[:start] + array_source + text[i + 1 :]

    raise SystemExit(f"Unclosed target array {key}")


def main() -> None:
    text = DASHBOARD.read_text(encoding="utf-8")
    config_source = SOURCE_CONFIG.read_text(encoding="utf-8")

    # Version / Version
    text = re.sub(
        r"# solar_dashboard .*? - dashboard\.yaml",
        "# solar_dashboard v0.8.3-alpha - dashboard.yaml",
        text,
        count=1,
    )

    modules_array = extract_array(config_source, "modules")
    trackers_array = extract_array(config_source, "trackers")

    # Inject the module list immediately before trackers in the generated CONFIG.
    # Modulliste direkt vor trackers in CONFIG einfügen.
    if "modules: [" not in text:
        marker = "            trackers: ["
        pos = text.find(marker)
        if pos < 0:
            raise SystemExit("Generated CONFIG.trackers not found")
        modules_block = (
            "            /*\n"
            "             * MODULE VISIBILITY AND ORDER / MODUL-SICHTBARKEIT UND REIHENFOLGE\n"
            "             *\n"
            "             * Available / Verfügbar:\n"
            "             * mppt    = tracker gauges / Tracker-Gauges\n"
            "             * pvTotal = total PV + tracker split bar / PV Gesamt + Tracker-Balken\n"
            "             * battery = SoC, remaining energy, power/status / SoC, Restenergie, Leistung/Status\n"
            "             * live    = PV, house, grid, battery live overview / PV-, Haus-, Netz-, Batterie-Liveübersicht\n"
            "             * payment = today's feed-in revenue / heutiger Einspeiseerlös\n"
            "             * runtime = estimated battery runtime / geschätzte Batterie-Restlaufzeit\n"
            "             *\n"
            "             * Remove an ID to hide a module. Reorder IDs to change display order.\n"
            "             * ID entfernen = Modul ausblenden. IDs verschieben = Reihenfolge ändern.\n"
            "             * Power Flux remains the separate first Lovelace card.\n"
            "             * Power Flux bleibt die separate erste Lovelace-Karte.\n"
            "             */\n"
            f"            modules: {modules_array},\n\n"
        )
        text = text[:pos] + modules_block + text[pos:]
    else:
        text = replace_js_array(text, "modules", modules_array)

    # Replace the generated tracker list with the four prepared source slots.
    # Generierte Tracker-Liste durch die vier vorbereiteten Quell-Slots ersetzen.
    text = replace_js_array(text, "trackers", trackers_array)

    # Disabled trackers must not contribute to gauges, totals or split bars.
    old_filter = """            .filter((tracker) =>
              tracker &&
              tracker.power &&
              Number(tracker.maxKw) > 0
            )"""
    new_filter = """            .filter((tracker) =>
              tracker &&
              tracker.enabled !== false &&
              tracker.power &&
              Number(tracker.maxKw) > 0
            )"""
    if old_filter not in text:
        raise SystemExit("Tracker filter block not found")
    text = text.replace(old_filter, new_filter, 1)

    # Module resolver. Unknown IDs and duplicates are ignored safely.
    # Modul-Resolver. Unbekannte IDs und Duplikate werden sicher ignoriert.
    resolver_marker = "          /*\n           * ========================================================\n           * OUTPUT / AUSGABE"
    resolver = r'''          /*
           * ========================================================
           * MODULE VISIBILITY / ORDER
           * MODUL-SICHTBARKEIT / REIHENFOLGE
           * ========================================================
           */

          const availableModules = [
            'mppt',
            'pvTotal',
            'battery',
            'live',
            'payment',
            'runtime'
          ];

          const configuredModules = Array.from(
            new Set(
              (Array.isArray(CONFIG.modules)
                ? CONFIG.modules
                : availableModules
              ).filter((moduleId) => availableModules.includes(moduleId))
            )
          );

          const moduleEnabled = (moduleId) =>
            configuredModules.includes(moduleId);

          const moduleOrder = (moduleId) => {
            const index = configuredModules.indexOf(moduleId);
            return index >= 0 ? index : 999;
          };

          const moduleClass = (moduleId) =>
            moduleEnabled(moduleId) ? '' : ' module-hidden';

'''
    if "const availableModules = [" not in text:
        if resolver_marker not in text:
            raise SystemExit("Output marker not found")
        text = text.replace(resolver_marker, resolver + resolver_marker, 1)

    # Make the root use auto-placement instead of fixed grid-template-areas.
    text = text.replace(
        '<div class="solar-dashboard display-${displayMode} perf-${performanceMode}">',
        '<div class="solar-dashboard modules-custom display-${displayMode} perf-${performanceMode}">',
        1,
    )

    wrapper_replacements = {
        'class="mppt-grid"\n                style="--mppt-count:${Math.max(trackers.length, 1)};"':
            'class="mppt-grid module-item module-mppt${moduleClass(\'mppt\')}"\n                style="--mppt-count:${Math.max(trackers.length, 1)}; --module-order:${moduleOrder(\'mppt\')};"',
        'class="panel live-panel"':
            'class="panel live-panel module-item module-live${moduleClass(\'live\')}" style="--module-order:${moduleOrder(\'live\')};"',
        'class="panel pv-total-panel v5-bar-panel"':
            'class="panel pv-total-panel v5-bar-panel module-item module-pv-total${moduleClass(\'pvTotal\')}" style="--module-order:${moduleOrder(\'pvTotal\')};"',
        'class="panel battery-panel v5-bar-panel"':
            'class="panel battery-panel v5-bar-panel module-item module-battery${moduleClass(\'battery\')}" style="--module-order:${moduleOrder(\'battery\')};"',
        'class="panel information-panel payment-panel"':
            'class="panel information-panel payment-panel module-item module-payment${moduleClass(\'payment\')}" style="--module-order:${moduleOrder(\'payment\')};"',
        'class="panel information-panel runtime-panel"':
            'class="panel information-panel runtime-panel module-item module-runtime${moduleClass(\'runtime\')}" style="--module-order:${moduleOrder(\'runtime\')};"',
    }
    for old, new in wrapper_replacements.items():
        if old not in text:
            raise SystemExit(f"Module wrapper not found: {old[:45]}")
        text = text.replace(old, new, 1)

    # CSS grid auto-placement. Full-width modules span both columns, compact modules pair naturally.
    # CSS-Raster mit Auto-Platzierung. Breite Module belegen beide Spalten, kompakte Module paaren sich automatisch.
    css_marker = "    extra_styles: |\n"
    module_css = r'''      /*
       * ==========================================================
       * v0.8.3-alpha MODULE ORDER / MODULE REIHENFOLGE
       * ==========================================================
       */

      .solar-dashboard.modules-custom {
        grid-template-areas: none !important;
        grid-auto-flow: row dense;
      }

      .solar-dashboard.modules-custom > .module-item {
        grid-area: auto !important;
        order: var(--module-order, 0);
      }

      .solar-dashboard.modules-custom > .module-mppt,
      .solar-dashboard.modules-custom > .module-live {
        grid-column: 1 / -1 !important;
      }

      .solar-dashboard.modules-custom > .module-pv-total,
      .solar-dashboard.modules-custom > .module-battery,
      .solar-dashboard.modules-custom > .module-payment,
      .solar-dashboard.modules-custom > .module-runtime {
        grid-column: span 1 !important;
      }

      .solar-dashboard.modules-custom > .module-hidden {
        display: none !important;
      }

      @media screen and (max-width: 699px) {
        .solar-dashboard.modules-custom {
          grid-template-columns: repeat(2, minmax(0, 1fr)) !important;
        }
      }

      @media screen and (min-width: 700px) {
        .solar-dashboard.modules-custom.display-wall {
          grid-template-areas: none !important;
          grid-auto-flow: row dense !important;
        }
      }

'''
    if "v0.8.3-alpha MODULE ORDER" not in text:
        if css_marker not in text:
            raise SystemExit("extra_styles marker not found")
        text = text.replace(css_marker, css_marker + module_css, 1)

    DASHBOARD.write_text(text, encoding="utf-8")
    print("Applied v0.8.3-alpha module visibility/order and four MPPT slots")


if __name__ == "__main__":
    main()
