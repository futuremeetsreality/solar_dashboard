#!/usr/bin/env python3
# File: tools/apply_modules_v0_8_3.py
# Timestamp: 2026-08-08 08:14 +0200

"""Apply v0.8.4-alpha configurable module visibility/order/size.

CONFIG.modules accepts objects with id + size. Supported sizes are small, large,
and max. Power Flux intentionally stays outside this system.

CONFIG.modules akzeptiert Objekte mit id + size. Unterstützt werden small, large
und max. Power Flux bleibt absichtlich außerhalb dieses Systems.
"""

from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DASHBOARD = ROOT / "dashboard.yaml"
SOURCE_CONFIG = ROOT / "src" / "config.js"


def extract_array(text: str, key: str) -> str:
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
                return text[start:i + 1]
    raise SystemExit(f"Unclosed array {key} in src/config.js")


def indent_array_for_yaml_block(array_source: str, base_spaces: int = 12) -> str:
    lines = array_source.splitlines()
    if len(lines) <= 1:
        return array_source
    prefix = " " * base_spaces
    return lines[0] + "\n" + "\n".join(prefix + line for line in lines[1:])


def replace_js_array(text: str, key: str, array_source: str, occurrence: int = 1) -> str:
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
                return text[:start] + array_source + text[i + 1:]
    raise SystemExit(f"Unclosed target array {key}")


def main() -> None:
    text = DASHBOARD.read_text(encoding="utf-8")
    config_source = SOURCE_CONFIG.read_text(encoding="utf-8")

    text = re.sub(
        r"# solar_dashboard .*? - dashboard\.yaml",
        "# solar_dashboard v0.8.4-alpha - dashboard.yaml",
        text,
        count=1,
    )

    modules_array = indent_array_for_yaml_block(extract_array(config_source, "modules"))
    trackers_array = indent_array_for_yaml_block(extract_array(config_source, "trackers"))

    if "modules: [" not in text:
        marker = "            trackers: ["
        pos = text.find(marker)
        if pos < 0:
            raise SystemExit("Generated CONFIG.trackers not found")
        modules_block = (
            "            /*\n"
            "             * MODULE VISIBILITY, ORDER AND SIZE / MODUL-SICHTBARKEIT, REIHENFOLGE UND GRÖSSE\n"
            "             *\n"
            "             * id: mppt | pvTotal | battery | live | payment | runtime\n"
            "             * size: small = 1/4, large = 1/2, max = full row\n"
            "             * size: small = 1/4, large = 1/2, max = ganze Zeile\n"
            "             * Remove an object to hide the module. Reorder objects to change display order.\n"
            "             * Block entfernen = Modul ausblenden. Blöcke verschieben = Reihenfolge ändern.\n"
            "             * Power Flux remains the separate first Lovelace card.\n"
            "             */\n"
            f"            modules: {modules_array},\n\n"
        )
        text = text[:pos] + modules_block + text[pos:]
    else:
        text = replace_js_array(text, "modules", modules_array)

    text = replace_js_array(text, "trackers", trackers_array)

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
    if old_filter in text:
        text = text.replace(old_filter, new_filter, 1)

    resolver_marker = "          /*\n           * ========================================================\n           * OUTPUT / AUSGABE"
    resolver = r'''          /*
           * ========================================================
           * MODULE VISIBILITY / ORDER / SIZE
           * MODUL-SICHTBARKEIT / REIHENFOLGE / GRÖSSE
           * ========================================================
           */

          const availableModules = [
            'mppt', 'pvTotal', 'battery', 'live', 'payment', 'runtime'
          ];
          const validModuleSizes = ['small', 'large', 'max'];

          const configuredModules = (Array.isArray(CONFIG.modules)
            ? CONFIG.modules
            : availableModules.map((id) => ({ id, size: 'max' })))
            .map((entry) =>
              typeof entry === 'string'
                ? { id: entry, size: 'max' }
                : entry
            )
            .filter((entry) => entry && availableModules.includes(entry.id))
            .filter((entry, index, array) =>
              array.findIndex((candidate) => candidate.id === entry.id) === index
            )
            .map((entry) => ({
              id: entry.id,
              size: validModuleSizes.includes(entry.size) ? entry.size : 'large'
            }));

          const moduleConfig = (moduleId) =>
            configuredModules.find((entry) => entry.id === moduleId);

          const moduleEnabled = (moduleId) => Boolean(moduleConfig(moduleId));

          const moduleOrder = (moduleId) => {
            const index = configuredModules.findIndex((entry) => entry.id === moduleId);
            return index >= 0 ? index : 999;
          };

          const moduleSize = (moduleId) =>
            moduleConfig(moduleId)?.size || 'large';

          const moduleClass = (moduleId) =>
            moduleEnabled(moduleId)
              ? ` module-size-${moduleSize(moduleId)}`
              : ' module-hidden';

'''

    existing_resolver = re.search(
        r"          /\*\n           \* ========================================================\n"
        r"           \* MODULE VISIBILITY / ORDER.*?"
        r"          const moduleClass = \(moduleId\) =>.*?;\n\n",
        text,
        re.S,
    )
    if existing_resolver:
        text = text[:existing_resolver.start()] + resolver + text[existing_resolver.end():]
    elif resolver_marker in text:
        text = text.replace(resolver_marker, resolver + resolver_marker, 1)

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
        if old in text:
            text = text.replace(old, new, 1)

    css_marker = "    extra_styles: |\n"
    module_css = r'''      /*
       * ==========================================================
       * v0.8.4-alpha MODULE SIZE / MODULGRÖSSE
       * ==========================================================
       */

      .solar-dashboard.modules-custom {
        grid-template-areas: none !important;
        grid-template-columns: repeat(4, minmax(0, 1fr)) !important;
        grid-auto-flow: row dense;
      }

      .solar-dashboard.modules-custom > .module-item {
        grid-area: auto !important;
        order: var(--module-order, 0);
      }

      .solar-dashboard.modules-custom > .module-size-small {
        grid-column: span 1 !important;
      }

      .solar-dashboard.modules-custom > .module-size-large {
        grid-column: span 2 !important;
      }

      .solar-dashboard.modules-custom > .module-size-max {
        grid-column: 1 / -1 !important;
      }

      .solar-dashboard.modules-custom > .module-hidden {
        display: none !important;
      }

      @media screen and (max-width: 699px) {
        .solar-dashboard.modules-custom > .module-size-small,
        .solar-dashboard.modules-custom > .module-size-large {
          grid-column: span 2 !important;
        }

        .solar-dashboard.modules-custom > .module-size-max {
          grid-column: 1 / -1 !important;
        }
      }

      @media screen and (max-width: 420px) {
        .solar-dashboard.modules-custom > .module-size-small {
          grid-column: span 2 !important;
        }
      }

'''

    old_css = re.search(
        r"      /\*\n       \* ==========================================================\n"
        r"       \* v0\.8\.3-alpha MODULE ORDER.*?"
        r"(?=      /\*\n       \* ==========================================================)",
        text,
        re.S,
    )
    if old_css:
        text = text[:old_css.start()] + module_css + text[old_css.end():]
    elif "v0.8.4-alpha MODULE SIZE" not in text:
        if css_marker not in text:
            raise SystemExit("extra_styles block not found")
        text = text.replace(css_marker, css_marker + module_css, 1)

    DASHBOARD.write_text(text, encoding="utf-8")


if __name__ == "__main__":
    main()
