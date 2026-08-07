#!/usr/bin/env python3
# File: tools/build_dashboard.py
# Timestamp: 2026-08-07 22:46 +0200

"""Build the generated Home Assistant dashboard.

Build-Pipeline / Build-Pipeline:
1. Decode the proven legacy V7 base.
2. Apply the existing compatibility/theme/i18n/display migrations.
3. Apply modular v0.8.2-alpha sources from src/.
4. Write the single user-facing dashboard.yaml.

The legacy base is intentionally kept during the v0.8.x migration so the working
layout is not rewritten in one risky step. New development moves into src/.

Die Legacy-Basis bleibt während der v0.8.x-Migration absichtlich erhalten, damit
das funktionierende Layout nicht in einem riskanten Schritt neu geschrieben wird.
Neue Entwicklung wandert ab jetzt nach src/.
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
    match = re.search(
        rf"const\s+{re.escape(variable)}\s*=\s*(\{{.*\}})\s*;",
        text,
        re.S,
    )
    if not match:
        raise SystemExit(f"Could not read {variable} from {path}")
    return match.group(1)


def source_setting(name: str, default: str) -> str:
    text = (SRC / "config.js").read_text(encoding="utf-8")
    match = re.search(rf"\b{re.escape(name)}\s*:\s*'([^']+)'", text)
    return match.group(1) if match else default


def apply_modular_sources() -> None:
    text = DASHBOARD.read_text(encoding="utf-8")

    # Version header / Versionskopf
    text = re.sub(
        r"# solar_dashboard .*? - dashboard\.yaml",
        "# solar_dashboard v0.8.2-alpha - dashboard.yaml",
        text,
        count=1,
    )

    # Bilingual generated-file notice / Zweisprachiger Hinweis zur generierten Datei
    notice = (
        "# GENERATED FILE - edit src/ and tools/build_dashboard.py instead.\n"
        "# GENERIERTE DATEI - Änderungen bitte in src/ und tools/build_dashboard.py vornehmen.\n"
    )
    if notice not in text:
        first_newline = text.find("\n") + 1
        text = text[:first_newline] + notice + text[first_newline:]

    # Central defaults from src/config.js / Zentrale Defaults aus src/config.js
    defaults = {
        "language": source_setting("language", "auto"),
        "displayMode": source_setting("displayMode", "auto"),
        "performanceMode": source_setting("performanceMode", "auto"),
    }
    for key, value in defaults.items():
        text = re.sub(
            rf"({re.escape(key)}\s*:\s*)'[^']+'",
            rf"\1'{value}'",
            text,
            count=1,
        )

    # Replace I18N table from the modular source.
    # I18N-Tabelle aus der modularen Quelle ersetzen.
    i18n = read_source_object(SRC / "i18n.js", "I18N_SOURCE")
    i18n_match = re.search(r"const I18N = \{.*?\n          \};", text, re.S)
    if not i18n_match:
        raise SystemExit("Generated dashboard I18N block not found")
    indented_i18n = "const I18N = " + i18n.replace("\n", "\n          ") + ";"
    text = text[: i18n_match.start()] + indented_i18n + text[i18n_match.end() :]

    # Unit-aware battery runtime / Restlaufzeit mit Einheit
    old_runtime = """          const runtimeRaw =\n            runtimeSensor?.state || t.unknown;\n\n          const runtime =\n            runtimeRaw === 'unknown' ||\n            runtimeRaw === 'unavailable'\n              ? t.unknown\n              : runtimeRaw;"""
    new_runtime = """          const runtime = formatRuntimeSensor(\n            runtimeSensor,\n            t.unknown\n          );"""
    if old_runtime not in text:
        raise SystemExit("Battery runtime block not found")
    text = text.replace(old_runtime, new_runtime, 1)

    # Inject modular runtime helper before the current-power section.
    # Modularen Laufzeit-Helfer vor dem Leistungsbereich einfügen.
    logic_source = (SRC / "logic.js").read_text(encoding="utf-8")
    helper_match = re.search(
        r"function formatRuntimeSensor\(.*?\n\}", logic_source, re.S
    )
    if not helper_match:
        raise SystemExit("formatRuntimeSensor helper not found in src/logic.js")
    helper = helper_match.group(0)
    helper = "\n".join("          " + line if line else "" for line in helper.splitlines())
    marker = "          /*\n           * ========================================================\n           * AKTUELLE LEISTUNGEN"
    if "function formatRuntimeSensor(" not in text:
        if marker not in text:
            raise SystemExit("Current-power marker not found")
        text = text.replace(marker, helper + "\n\n" + marker, 1)

    # Bilingual user-facing code comments. We intentionally focus on the configuration
    # and main sections; old historical CSS comments are migrated gradually.
    # Zweisprachige Nutzer-Kommentare. Historische CSS-Kommentare werden schrittweise migriert.
    replacements = {
        "BENUTZERKONFIGURATION – NUR DIESEN BLOCK ANPASSEN":
            "USER CONFIGURATION / BENUTZERKONFIGURATION – ONLY EDIT THIS BLOCK / NUR DIESEN BLOCK ANPASSEN",
        "HILFSFUNKTIONEN": "HELPER FUNCTIONS / HILFSFUNKTIONEN",
        "AKTUELLE LEISTUNGEN": "CURRENT POWER / AKTUELLE LEISTUNGEN",
        "TAGESENERGIEN": "DAILY ENERGY / TAGESENERGIEN",
        "BATTERIEWERTE": "BATTERY VALUES / BATTERIEWERTE",
        "NETZSTATUS": "GRID STATUS / NETZSTATUS",
        "WEITERE WERTE": "ADDITIONAL VALUES / WEITERE WERTE",
        "AUSGABE": "OUTPUT / AUSGABE",
        "GRUNDLAYOUT": "BASE LAYOUT / GRUNDLAYOUT",
        "LIVE-ENERGIEFLUSS": "LIVE ENERGY FLOW / LIVE-ENERGIEFLUSS",
        "BATTERIE": "BATTERY / BATTERIE",
        "VERGÜTUNG UND RESTLAUFZEIT": "REVENUE AND RUNTIME / VERGÜTUNG UND RESTLAUFZEIT",
    }
    for old, new in replacements.items():
        text = text.replace(old, new)

    DASHBOARD.write_text(text, encoding="utf-8")


def sanity_check() -> None:
    text = DASHBOARD.read_text(encoding="utf-8")
    required = [
        "type: vertical-stack",
        "custom:power-flux-card",
        "custom:button-card",
        "v0.8.2-alpha",
        "language: 'auto'",
        "displayMode: 'auto'",
        "performanceMode: 'auto'",
        "function formatRuntimeSensor(",
        "const I18N = {",
    ]
    missing = [item for item in required if item not in text]
    if missing:
        raise SystemExit(f"Build sanity check failed, missing: {missing}")


if __name__ == "__main__":
    decode_base()
    run_legacy_patches()
    apply_modular_sources()
    sanity_check()
    print("Built dashboard.yaml v0.8.2-alpha from modular sources")
