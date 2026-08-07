# Solar Dashboard für Home Assistant

[English](README.md) | [Deutsch](README_DE.md)

Ein responsives PV- und Batterie-Dashboard für Home Assistant mit Power-Flux-Ansicht, dynamischen MPPT-Gauges, Tageswerten, Netzfluss, Batterie, Einspeisevergütung, adaptivem Hell-/Dunkelmodus, zweisprachiger Oberfläche und eigenem Wall-Display-Profil.

Aktuelle Version: **v0.8.2-alpha**

> Alpha bedeutet: Das Dashboard ist bereits nutzbar, wird aber noch auf unterschiedlichen Home-Assistant-Systemen hinsichtlich Konfiguration, Kompatibilität und Darstellung getestet.

## Highlights

- automatischer Home-Assistant-Hell-/Dunkelmodus
- adaptive Glows und Verläufe in beiden Modi
- dynamische Unterstützung für 1, 2, 3 oder mehr MPPT-/PV-Tracker
- automatische PV-Maximalleistung aus allen `maxKw`-Werten
- dynamisch geteilter PV-Total-Balken
- Live- und Tageswerte für Batterie, Haus und Netz
- Dashboard-Sprachen `auto`, `de` und `en`
- sprachabhängige Zahlenformatierung
- herstellerunabhängige Sensor-Zuordnung
- eigener `wall`-Modus für dauerhaft montierte Tablets
- automatischer Kompatibilitätsmodus für ältere Safari-/iPadOS-Geräte
- modulare Quellcode-Struktur mit automatisch erzeugter `dashboard.yaml`

## Voraussetzungen

Über HACS → Frontend installieren:

- `Button Card` (`custom:button-card`)
- `Power Flux Card` (`custom:power-flux-card`)
- `card-mod`

Danach Home Assistant bzw. den Browser neu laden.

## Schnelltest

[`dashboard.yaml`](dashboard.yaml) ist eine vollständige Lovelace-Kartenkonfiguration.

In Home Assistant:

1. Dashboard bearbeiten.
2. Karte hinzufügen.
3. **Manuell** auswählen.
4. Den vollständigen Inhalt von `dashboard.yaml` einfügen.
5. Speichern.

Nicht direkt in den Rohkonfigurationseditor des gesamten Dashboards einfügen.

## Sprache

```js
language: 'auto',
```

Unterstützt: `auto`, `de`, `en`. Auch die Zahlenformatierung folgt der ausgewählten Sprache.

## Display- und Performance-Profile

```js
displayMode: 'auto',
performanceMode: 'auto',
```

`displayMode`: `auto`, `desktop`, `tablet`, `wall`

`performanceMode`: `auto`, `high`, `balanced`, `low`

Ältere Safari-/iPadOS-Versionen ohne `color-mix()` fallen automatisch auf `low` zurück. Für ein älteres, dauerhaft montiertes iPad empfiehlt sich zunächst:

```js
displayMode: 'wall',
performanceMode: 'auto',
```

## MPPT-/Tracker-Konfiguration

Die Tracker werden in `CONFIG.trackers` definiert. Für einen Tracker bleibt nur ein Objekt stehen. Für weitere Tracker werden zusätzliche Objekte ergänzt. Raster, Gauges und PV-Total-Balken passen sich automatisch an.

## Beispielkonfiguration im Repository

- MPPT 1: 9,10 kW
- MPPT 2: 6,37 kW
- automatisch berechnete PV-Gesamtleistung: 15,47 kW
- Batterie: 12,50 kWh

## Modulare Quellcode-Architektur

Ab **v0.8.2-alpha** ist `dashboard.yaml` eine generierte Datei. Neue Entwicklung wird aufgeteilt in:

```text
src/
├── config.js
├── i18n.js
├── layout.js
├── logic.js
├── styles.css
└── README.md

tools/
└── build_dashboard.py
```

Lokaler Build:

```bash
python tools/build_dashboard.py
```

GitHub Actions führt denselben Builder automatisch aus, sobald sich Quellcode oder Build-Werkzeuge ändern. Normale Home-Assistant-Nutzer benötigen weiterhin nur `dashboard.yaml`.

Die bewährte V7-Basis bleibt während der v0.8.x-Migration vorübergehend im Build-Prozess. Einzelne Bereiche werden schrittweise nach `src/` verschoben, ohne das funktionierende Dashboard komplett neu zu schreiben.

## Sensor-Zuordnung

Die enthaltenen SolaX-Entity-IDs sind nur Beispiele. Andere Wechselrichter-, Batterie- oder Messsysteme funktionieren ebenfalls, sofern die verknüpften Sensoren den erwarteten Messwert liefern.

Siehe:

- [Entity-Referenz](docs/ENTITY_REFERENCE_DE.md)
- [Home-Assistant-Testanleitung](docs/TESTING_DE.md)
- [Quellcode-Architektur](src/README.md)
- [Changelog](CHANGELOG.md)

## Versionierung

- `v0.8.x-alpha` — aktive Funktionsentwicklung und Kompatibilitätstests
- `v0.9.x-beta` — weitgehend vollständiger Funktionsumfang, breite Tests
- `v1.0.0` — erste stabile Version
