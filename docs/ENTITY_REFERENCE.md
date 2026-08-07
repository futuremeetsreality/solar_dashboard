# Entity Reference – V7

Diese Datei beschreibt, welche Messwerte für das Dashboard benötigt werden. Die Namen deiner Home-Assistant-Entities sind egal. Entscheidend ist nur, dass der jeweilige Sensor den beschriebenen Wert liefert.

## MPPT-/PV-Tracker

V7 verwendet keine fest eingebauten `mppt1`-/`mppt2`-Variablen mehr. Jeder Tracker wird als Objekt in `CONFIG.trackers` eingetragen.

Pro Tracker werden folgende Werte benötigt:

| Schlüssel | Pflicht | Erwarteter Messwert | Einheit |
|---|---|---|---|
| `name` | Ja | Frei wählbarer Anzeigename, z. B. `MPPT 1` | Text |
| `power` | Ja | Aktuelle Leistung dieses PV-/MPPT-Eingangs | W oder kW |
| `energyToday` | Ja | Seit Mitternacht erzeugte Energie dieses Trackers | Wh oder kWh |
| `maxKw` | Ja | Maximale/zugeordnete Generatorleistung dieses Trackers | kW |
| `colorStart` | Nein | Startfarbe für Gauge und PV-Segment | HEX |
| `colorEnd` | Nein | Endfarbe für Gauge und PV-Segment | HEX |

Beispiel:

```js
{
  name: 'MPPT 1',
  power: 'sensor.mein_mppt_power',
  energyToday: 'sensor.mein_mppt_energy_today',
  maxKw: 8.00,
  colorStart: '#ff9800',
  colorEnd: '#ffd740'
}
```

### Anzahl der Tracker

- 1 Tracker: genau ein Objekt in `CONFIG.trackers`.
- 2 Tracker: zwei Objekte.
- 3 Tracker: drei Objekte.
- Weitere Tracker können nach demselben Schema ergänzt werden.

Das Dashboard erzeugt die MPPT-Karten und den geteilten PV-Balken automatisch.

Die maximale PV-Gesamtleistung wird automatisch aus allen `maxKw`-Werten berechnet.

## Weitere Dashboard-Entities

| CONFIG-Schlüssel | Pflicht | Erwarteter Messwert | Einheit |
|---|---|---|---|
| `pvPowerTotal` | Ja | Aktuelle gesamte PV-Leistung über alle Tracker | W oder kW |
| `pvEnergyToday` | Ja | Gesamte PV-Produktion seit Mitternacht | Wh oder kWh |
| `housePower` | Ja | Aktueller Gesamtverbrauch des Hauses | W oder kW |
| `houseEnergyToday` | Nein | Hausverbrauch seit Mitternacht | Wh oder kWh |
| `gridImportPower` | Ja | Aktuelle Leistung aus dem Stromnetz | W oder kW |
| `gridExportPower` | Ja | Aktuelle Leistung ins Stromnetz | W oder kW |
| `gridImportEnergyToday` | Ja | Netzbezug seit Mitternacht | Wh oder kWh |
| `gridExportEnergyToday` | Ja | Netzeinspeisung seit Mitternacht | Wh oder kWh |
| `batterySoc` | Ja | Ladezustand der Batterie | % |
| `batteryPower` | Ja | Aktuelle Lade-/Entladeleistung der Batterie | W oder kW |
| `batteryEnergyRemaining` | Ja | Aktuell noch gespeicherte/verfügbare Batterieenergie | Wh oder kWh |
| `batteryChargeEnergyToday` | Ja | Heute in die Batterie geladene Energie | Wh oder kWh |
| `batteryDischargeEnergyToday` | Ja | Heute aus der Batterie entladene Energie | Wh oder kWh |
| `compensationToday` | Nein | Heutiger Einspeiseerlös | EUR |
| `batteryRuntime` | Nein | Geschätzte Restlaufzeit der Batterie | Zahl/Text |

## Vorzeichen der Batterieleistung

Die aktuelle Dashboard-Logik erwartet:

- positiver Wert = Batterie lädt,
- negativer Wert = Batterie entlädt.

Wenn deine Integration das umgekehrt liefert, muss die Batterielogik angepasst oder vorher ein Template-Sensor erstellt werden.

## Hausverbrauch heute

`houseEnergyToday` ist optional. Wenn kein entsprechender Sensor vorhanden ist, berechnet das Dashboard den Tagesverbrauch aus der Energiebilanz:

```text
PV-Produktion
+ Netzimport
+ Batterieentladung
- Netzeinspeisung
- Batterieladung
= Hausverbrauch
```

## Power Flux Card

Die Power Flux Card ist unabhängig vom `CONFIG`-Block und hat in `dashboard.yaml` einen eigenen `entities:`-Abschnitt. Dort werden benötigt:

- aktuelle PV-Gesamtleistung,
- Netzimport,
- Netzexport,
- Batterieleistung,
- Batterie-SoC,
- Hausverbrauch.

Die dortigen Zusatzsensoren für Tageswerte sind abhängig von der verwendeten Power-Flux-Card-Konfiguration.
