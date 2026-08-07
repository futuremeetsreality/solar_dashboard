# Solar Dashboard für Home Assistant

[English](README.md) | [Deutsch](README_DE.md)

Ein responsives PV- und Batterie-Dashboard für Home Assistant mit Power-Flux-Ansicht, dynamischen MPPT-Gauges, Tageswerten, Netzfluss, Batterie, Einspeisevergütung, adaptivem Hell-/Dunkelmodus und zweisprachiger Oberfläche.

Aktuelle Version: **v0.8.0-alpha**

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

Im Konfigurationsbereich der `custom:button-card` steht:

```js
language: 'auto',
```

Unterstützte Werte:

- `auto` — übernimmt die Home-Assistant-Sprache; Deutsch wird als `de` erkannt, alle anderen Sprachen fallen derzeit auf Englisch zurück
- `de` — Deutsch erzwingen
- `en` — Englisch erzwingen

Auch die Zahlenformatierung passt sich an die gewählte Sprache an.

## MPPT-/Tracker-Konfiguration

Die Tracker werden in `CONFIG.trackers` definiert:

```js
trackers: [
  {
    name: 'MPPT 1',
    power: 'sensor.mein_mppt_1_power',
    energyToday: 'sensor.mein_mppt_1_energy_today',
    maxKw: 9.10,
    colorStart: '#ff9800',
    colorEnd: '#ffd740'
  },
  {
    name: 'MPPT 2',
    power: 'sensor.mein_mppt_2_power',
    energyToday: 'sensor.mein_mppt_2_energy_today',
    maxKw: 6.37,
    colorStart: '#43a047',
    colorEnd: '#76ff7a'
  }
]
```

Für einen Tracker bleibt nur ein Objekt stehen. Für weitere Tracker werden zusätzliche Objekte ergänzt. Raster, Gauges und PV-Total-Balken passen sich automatisch an.

## Beispielkonfiguration im Repository

- MPPT 1: 9,10 kW
- MPPT 2: 6,37 kW
- automatisch berechnete PV-Gesamtleistung: 15,47 kW
- Batterie: 12,50 kWh

## Sensor-Zuordnung

Die enthaltenen SolaX-Entity-IDs sind nur Beispiele. Andere Wechselrichter-, Batterie- oder Messsysteme funktionieren ebenfalls, sofern die verknüpften Sensoren den erwarteten Messwert liefern.

Siehe:

- [Entity-Referenz](docs/ENTITY_REFERENCE_DE.md)
- [Home-Assistant-Testanleitung](docs/TESTING_DE.md)
- [Changelog](CHANGELOG.md)

## Versionierung

Das Projekt verwendet ab jetzt semantische Pre-Release-Versionierung:

- `v0.8.x-alpha` — aktive Funktionsentwicklung und Kompatibilitätstests
- `v0.9.x-beta` — weitgehend vollständiger Funktionsumfang, breite Tests
- `v1.0.0` — erste stabile Version
