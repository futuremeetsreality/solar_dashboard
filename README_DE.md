# Solar Dashboard für Home Assistant

[English](README.md) | [Deutsch](README_DE.md)

Ein responsives PV- und Batterie-Dashboard für Home Assistant mit Power-Flux-Ansicht, dynamischen MPPT-Gauges, Tageswerten, Netzfluss, Batterie, Einspeisevergütung, adaptivem Hell-/Dunkelmodus, zweisprachiger Oberfläche und eigenem Wall-Display-Profil.

Aktuelle Version: **v0.8.3-alpha**

> Alpha bedeutet: Das Dashboard ist bereits nutzbar, wird aber noch auf unterschiedlichen Home-Assistant-Systemen hinsichtlich Konfiguration, Kompatibilität und Darstellung getestet.

## Highlights

- automatischer Home-Assistant-Hell-/Dunkelmodus
- adaptive Glows und Verläufe in beiden Modi
- dynamische Unterstützung für 1, 2, 3 oder mehr MPPT-/PV-Tracker
- vier vorbereitete MPPT-Konfigurationsslots
- automatische PV-Maximalleistung aus allen aktivierten `maxKw`-Werten
- dynamisch geteilter PV-Total-Balken für alle aktivierten Tracker
- frei konfigurierbare Modul-Sichtbarkeit und Modul-Reihenfolge
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

## Modul-Sichtbarkeit und Reihenfolge

v0.8.3-alpha ergänzt `CONFIG.modules`:

```js
modules: [
  'mppt',
  'pvTotal',
  'battery',
  'live',
  'payment',
  'runtime'
],
```

Nur eingetragene Module werden angezeigt. Die Reihenfolge im Array ist gleichzeitig die Reihenfolge im Dashboard. Einen Eintrag entfernen, um ein Modul auszublenden, oder verschieben, um seine Position zu ändern.

Verfügbare Modul-IDs:

- `mppt` — Tracker-Gauges mit aktueller Leistung, Tagesertrag und eingestellter Maximalleistung
- `pvTotal` — gesamte PV-Leistung, PV-Prozentwert und nach Trackern geteilter Produktionsbalken
- `battery` — SoC, verbleibende Batterieenergie, aktuelle Batterieleistung und Status
- `live` — kompakte Live-Übersicht für PV, Haus, Netz und Batterie inklusive Tagesenergiewerten
- `payment` — heutiger Einspeiseerlös bzw. Vergütung
- `runtime` — geschätzte verbleibende Batterie-Restlaufzeit

Power Flux ist absichtlich nicht Teil dieser Liste. Die Karte bleibt als separate erste Lovelace-Karte bestehen.

## MPPT-/Tracker-Konfiguration

In der User Config sind vier Tracker-Slots vorbereitet. Nicht verwendete Tracker können deaktiviert bleiben:

```js
{
  enabled: false,
  name: 'MPPT 3',
  power: '',
  energyToday: '',
  maxKw: 0,
  colorStart: '#2196f3',
  colorEnd: '#00e5ff'
}
```

Zum Aktivieren `enabled: true` setzen und Entities sowie `maxKw` eintragen. Deaktivierte Tracker beeinflussen weder Gauges noch PV-Maximum noch den geteilten PV-Total-Balken.

Die Beispielkonfiguration im Repository verwendet:

- MPPT 1: 9,10 kW
- MPPT 2: 6,37 kW
- automatisch berechnete PV-Gesamtleistung: 15,47 kW
- Batterie: 12,50 kWh

## Modulare Quellcode-Architektur

`dashboard.yaml` ist eine generierte Datei. Neue Entwicklung wird aufgeteilt in:

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
