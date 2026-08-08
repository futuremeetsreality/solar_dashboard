# Changelog

## v0.8.3-alpha - 2026-08-08

- Added configurable dashboard module visibility and ordering through `CONFIG.modules`.
- Supported module IDs: `mppt`, `pvTotal`, `battery`, `live`, `payment`, `runtime`.
- Removing a module ID hides that module; changing the list order changes its dashboard position.
- Power Flux intentionally remains the separate first Lovelace card and is not part of the internal module ordering.
- Added bilingual EN/DE descriptions in the user configuration explaining every available module and what it displays.
- Added four prepared MPPT tracker slots.
- MPPT 1 and MPPT 2 remain enabled with the example SolaX configuration.
- MPPT 3 and MPPT 4 are prepared but disabled by default.
- Added `enabled` per tracker. Disabled trackers are ignored by MPPT gauges, PV maximum calculation and the PV Total split bar.
- Unknown module IDs and duplicate module IDs are ignored safely.
- Added automatic grid placement so full-width modules (`mppt`, `live`) and compact modules can be reordered without fixed grid-template areas.

## v0.8.2-alpha - 2026-08-07

- Introduced a modular source architecture under `src/`.
- Added `src/config.js`, `src/i18n.js`, `src/layout.js`, `src/logic.js` and `src/styles.css`.
- Added `tools/build_dashboard.py` as the single dashboard builder.
- GitHub Actions now runs the modular builder and regenerates `dashboard.yaml` automatically.
- `dashboard.yaml` is now explicitly marked as a generated file.
- Kept the proven legacy V7 base temporarily during the v0.8.x migration to avoid a risky full rewrite.
- Migrated language data, display/performance resolver, runtime helper and compatibility styles into modular source files.
- Added unit-aware battery runtime display: Home Assistant sensor units are used when available; numeric runtime falls back to hours (`h`).
- Started converting generated YAML comments to bilingual English/German documentation.
- Added bilingual source-architecture documentation in `src/README.md`.

## v0.8.1-alpha - 2026-08-07

- Added `displayMode`: `auto`, `desktop`, `tablet`, `wall`.
- Added `performanceMode`: `auto`, `high`, `balanced`, `low`.
- Added a dedicated wall-display layout with larger values, thicker bars and increased viewing-distance readability.
- Added automatic tablet detection for the `auto` display profile.
- Added browser capability detection for `performanceMode: auto`.
- Added automatic low-performance fallback for older iPadOS/Safari versions and browsers without `color-mix()` support.
- Added Safari 15-compatible fallback surfaces that avoid `color-mix()` dependent rendering.
- Low mode disables expensive SVG filters, glow shadows, animations and transitions while retaining lightweight gradients.
- Balanced mode keeps the visual design while reducing GPU-heavy effects.
- Documented recommended settings for older permanently mounted iPads: `displayMode: 'wall'`, `performanceMode: 'auto'`.

## v0.8.0-alpha - 2026-08-07

- Switched project versioning from V-number milestones to semantic pre-release versioning.
- Added dashboard UI languages `auto`, `de` and `en`.
- `auto` follows the Home Assistant language; German uses `de`, all other languages currently fall back to English.
- Added locale-aware number formatting (`de-AT` / `en-US`).
- Translated live labels, PV Total, battery labels/status, revenue, runtime and unknown-state text.
- Added English as the primary GitHub documentation language.
- Added `README_DE.md` for German documentation.
- Added English/German entity reference documentation.
- Added English/German Home Assistant testing guides.
- Kept the V7.2 adaptive light/dark glow and gradient design.
- Kept dynamic support for any number of MPPT/PV trackers.

## V7.2 - 2026-08-07

- Adaptives Glow- und Verlaufsdesign für Hell- und Dunkelmodus.
- Oberflächen basieren auf den aktiven Home-Assistant-Themefarben.
- MPPT-Karten erhalten Tracker-spezifische Glows aus `colorStart` und `colorEnd`.
- PV Total erhält einen adaptiven Orange-/Grün-Verlauf mit verbessertem Kontrast.
- Batterie erhält einen adaptiven Grün-/Warmton-Glow.
- Live-Leiste erhält dezente Farbzonen für PV, Haus, Netz und Batterie.
- Vergütung erhält einen blauen Glow.
- Restlaufzeit erhält einen violetten Glow.
- Kleine Tracker- und Prozenttexte werden theme-adaptiv mit der aktuellen Textfarbe gemischt.
- Rahmen, Track-Hintergründe, Inset-Flächen und neutrale Texte reagieren automatisch auf das HA-Theme.
- Power Flux Card behält ihr eigenes automatisches Theme-Verhalten.

## V7.1 - 2026-08-07

- Vollständige Unterstützung für Home-Assistant-Hell- und Dunkelmodus ergänzt.
- Kartenflächen verwenden nun die aktiven Home-Assistant-Theme-Variablen statt fest verdrahteter dunkler Farben.
- Primär- und Sekundärtexte folgen automatisch dem aktiven Theme.
- Rahmen, Trenner, MPPT-Hintergrundbögen und neutrale Balkenhintergründe passen sich automatisch an.
- PV- und Batterie-Karten behalten ihre farbigen Akzente, verwenden aber eine themeabhängige Grundfläche.
- Vergütungs- und Restlaufzeitkarten verwenden im Hell- und Dunkelmodus nur noch einen dezenten Blau-/Violett-Farbstich.
- Power Flux Card erzwingt keinen dunklen Hintergrund mehr und folgt dem Home-Assistant-Theme.
- Wechsel zwischen Hell und Dunkel erfordert keine zweite Dashboard-Konfiguration.

## V7 - 2026-08-07

- MPPT-/PV-Tracker vollständig dynamisch gemacht.
- Beliebige Anzahl von Trackern über `CONFIG.trackers` möglich.
- 1, 2, 3 oder mehr Tracker ohne Änderungen am eigentlichen Dashboard-Code.
- Jede Tracker-Konfiguration enthält Beschreibung, Leistungs-Entity, Tagesenergie, Maximalleistung und Farben.
- MPPT-Gauges werden automatisch aus der Tracker-Liste erzeugt.
- Responsive MPPT-Anordnung wird automatisch erzeugt.
- PV-Total-Balken wird automatisch in farbige Tracker-Segmente aufgeteilt.
- PV-Gesamtmaximum wird nicht mehr separat gepflegt, sondern aus der Summe aller `maxKw`-Werte berechnet.
- Beispielkonfiguration weiterhin mit 9,10 kW für MPPT 1 und 6,37 kW für MPPT 2; daraus ergeben sich automatisch 15,47 kW PV max.
- V6-Sensorstruktur für Haus, Netz und Batterie beibehalten.
