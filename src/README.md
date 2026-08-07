# Source architecture / Quellcode-Architektur

Starting with **v0.8.2-alpha**, new development is moved out of the generated `dashboard.yaml` and into modular files under `src/`.

Ab **v0.8.2-alpha** wird neue Entwicklung aus der generierten `dashboard.yaml` in modulare Dateien unter `src/` verschoben.

## Files / Dateien

- `config.js` — user-facing defaults and tracker model / Benutzer-Defaults und Tracker-Modell
- `i18n.js` — German and English UI strings / deutsche und englische UI-Texte
- `layout.js` — display and performance detection / Display- und Performance-Erkennung
- `logic.js` — reusable logic helpers / wiederverwendbare Logik-Helfer
- `styles.css` — wall-display and compatibility styles / Wall-Display- und Kompatibilitäts-Styles

## Build

Run locally:

```bash
python tools/build_dashboard.py
```

The builder creates the single Home Assistant file:

```text
dashboard.yaml
```

GitHub Actions runs the same builder automatically whenever `src/` or the build tooling changes.

GitHub Actions führt denselben Builder automatisch aus, wenn sich `src/` oder die Build-Werkzeuge ändern.

## Migration note / Migrationshinweis

The proven V7 base and the existing patch scripts are still used internally during the v0.8.x migration. This avoids a risky complete rewrite of the working dashboard. Migrated sections are then replaced by the modular `src/` files.

Die bewährte V7-Basis und bestehende Patch-Skripte werden während der v0.8.x-Migration intern noch verwendet. Dadurch vermeiden wir einen riskanten Komplettumbau des funktionierenden Dashboards. Bereits migrierte Bereiche werden anschließend durch die modularen `src/`-Dateien ersetzt.
