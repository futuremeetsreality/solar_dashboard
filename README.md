# Solar Dashboard for Home Assistant

Ein responsives PV-/Batterie-Dashboard für Home Assistant mit Power-Flux-Ansicht, dynamischen MPPT-Gauges, Tageswerten, Netzfluss, Batterie und Einspeisevergütung.

Aktueller Stand: **V7.2**

## Was ist neu in V7.2?

V7.2 erweitert die automatische Hell-/Dunkelmodus-Unterstützung um ein adaptives Glow- und Verlaufsdesign.

Die Karten verwenden die aktiven Home-Assistant-Themefarben als Basis und mischen die Solar-Akzentfarben automatisch dazu. Dadurch bleibt das Dashboard sowohl im hellen als auch im dunklen Modus kontrastreich, ohne auf die farbigen Verläufe zu verzichten.

Angepasst wurden insbesondere:

- MPPT-Karten mit Tracker-spezifischem Glow,
- PV Total mit Orange-/Grün-Verlauf und verbessertem Textkontrast,
- Batterie mit Grün-/Warmton-Glow,
- Live-Leiste mit dezenten Farbzonen für PV, Haus, Netz und Batterie,
- Vergütung mit blauem Glow,
- Restlaufzeit mit violettem Glow,
- adaptive Farben für kleine Tracker-/Prozenttexte,
- adaptive Rahmen, Tracks, Inset-Flächen und neutrale Texte.

Die Power Flux Card behält ihr eigenes automatisches Theme-Verhalten.

## Was ist neu seit V7?

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
6. Unter Profil / Erscheinungsbild zwischen Hell und Dunkel wechseln und beide Varianten prüfen.

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

Nur einen Eintrag in `trackers` stehen lassen. Die MPPT-Karte nutzt automatisch die verfügbare Breite.

### Drei oder mehr MPPTs

Weitere Tracker-Objekte ergänzen. Das Raster und der PV-Total-Balken werden automatisch erweitert.

## Beispielanlage im Repository

Die Standardkonfiguration verwendet:

- MPPT 1: 9,10 kW
- MPPT 2: 6,37 kW
- automatisch berechnete PV-Gesamtleistung: 15,47 kW
- Batterie: 12,50 kWh

Weitere Details zu den benötigten Sensoren stehen in [`docs/ENTITY_REFERENCE.md`](docs/ENTITY_REFERENCE.md).
