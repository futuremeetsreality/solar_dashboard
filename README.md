# Solar Dashboard for Home Assistant

Ein responsives PV-/Batterie-Dashboard für Home Assistant mit Power-Flux-Ansicht, dynamischen MPPT-Gauges, Tageswerten, Netzfluss, Batterie und Einspeisevergütung.

Aktueller Stand: **V7**

## Was ist neu in V7?

V7 unterstützt eine **beliebige Anzahl an MPPT-/PV-Trackern**. Die Tracker werden nur noch in einer Liste konfiguriert. Daraus erzeugt das Dashboard automatisch:

- eine MPPT-Karte pro Tracker,
- das responsive MPPT-Raster,
- den individuellen Maximalwert jedes Gauges,
- die Farben jedes Trackers,
- den geteilten PV-Total-Balken,
- die maximale PV-Gesamtleistung als Summe aller `maxKw`-Werte.

Damit funktioniert das Dashboard z. B. mit 1, 2, 3 oder mehr Trackern, ohne den eigentlichen Dashboard-Code umzubauen.

## Voraussetzungen

Installiere über HACS unter **Frontend**:

- `Button Card` (`custom:button-card`)
- `Power Flux Card` (`custom:power-flux-card`)
- `card-mod`

Danach Home Assistant bzw. den Browser neu laden.

## Schnelltest

Die Datei [`dashboard.yaml`](dashboard.yaml) ist als **eine komplette Lovelace-Karte** aufgebaut.

In Home Assistant:

1. Dashboard bearbeiten.
2. **Karte hinzufügen**.
3. **Manuell** auswählen.
4. Den vollständigen Inhalt von `dashboard.yaml` einfügen.
5. Speichern.

Es müssen nicht mehrere Dateien oder Karten eingebunden werden.

## Benutzerkonfiguration

Im `custom:button-card`-Teil befindet sich der Block:

```js
const CONFIG = {
  trackers: [ ... ],
  entities: { ... },
  limits: { ... }
};
```

### MPPT-/Tracker konfigurieren

Jeder Tracker ist ein Objekt in `CONFIG.trackers`:

```js
{
  name: 'MPPT 1',
  power: 'sensor.mein_mppt_1_power',
  energyToday: 'sensor.mein_mppt_1_energy_today',
  maxKw: 9.10,
  colorStart: '#ff9800',
  colorEnd: '#ffd740'
}
```

Bedeutung:

- `name`: Anzeigename des Trackers.
- `power`: aktuelle Leistung des Trackers in W oder kW.
- `energyToday`: seit Mitternacht erzeugte Energie in Wh oder kWh.
- `maxKw`: maximale/zugeordnete Generatorleistung dieses Trackers in kW.
- `colorStart` / `colorEnd`: Farbe für Gauge und PV-Segment.

### Nur ein MPPT

Lass nur einen Tracker in der Liste stehen.

### Drei MPPTs

Füge einfach einen dritten Tracker hinzu:

```js
{
  name: 'MPPT 3',
  power: 'sensor.mein_mppt_3_power',
  energyToday: 'sensor.mein_mppt_3_energy_today',
  maxKw: 5.00,
  colorStart: '#2196f3',
  colorEnd: '#00e5ff'
}
```

Das Layout und der PV-Balken passen sich automatisch an.

## PV-Gesamtmaximum

In V7 muss `pvMaxKw` nicht mehr separat gepflegt werden. Das Dashboard berechnet automatisch:

```text
PV max = Summe aller Tracker maxKw
```

Beispiel der mitgelieferten SolaX-Konfiguration:

```text
MPPT 1 = 9,10 kW
MPPT 2 = 6,37 kW
PV max  = 15,47 kW
```

## Batterie

Die Batteriekapazität bleibt zentral konfigurierbar:

```js
limits: {
  batteryCapacityKwh: 12.50
}
```

## Sensoren

Eine ausführliche Beschreibung jedes benötigten Messwerts findest du unter:

[`docs/ENTITY_REFERENCE.md`](docs/ENTITY_REFERENCE.md)

Dort ist beschrieben, **was** ein Sensor liefern muss. Die konkrete Integration bzw. der Hersteller ist egal.

## Power Flux Card

Die Power Flux Card ist eine eigenständige Custom Card und besitzt deshalb ihren eigenen `entities:`-Block am Anfang von `dashboard.yaml`.

Diese Entity-IDs müssen bei einer Übernahme auf ein anderes System zusätzlich angepasst werden. Die Tracker-Liste betrifft den selbst entwickelten Dashboard-Bereich.

## Testen

Siehe [`docs/TESTING.md`](docs/TESTING.md).

## Versionen

- V6: zentrale Entity-Konfiguration und dokumentierte Sensoren.
- V7: dynamische Anzahl von MPPT-/PV-Trackern.

## Lizenz / Nutzung

Das Projekt ist als Home-Assistant-Dashboard-Vorlage gedacht und darf an die eigene Anlage angepasst werden.
