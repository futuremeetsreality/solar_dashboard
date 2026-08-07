# Entity-Referenz — v0.8.0-alpha

[English](ENTITY_REFERENCE.md) | [Deutsch](ENTITY_REFERENCE_DE.md)

Diese Datei beschreibt, welche Messwerte das Dashboard erwartet. Die Namen deiner Home-Assistant-Entities sind egal; entscheidend sind Messwert und Einheit.

## MPPT-/PV-Tracker

Tracker werden als Objekte in `CONFIG.trackers` eingetragen.

| Schlüssel | Pflicht | Erwarteter Messwert | Einheit |
|---|---|---|---|
| `name` | Ja | Anzeigename, z. B. `MPPT 1` | Text |
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

Für einen Tracker wird ein Objekt verwendet, für zwei Tracker zwei Objekte usw. Das Dashboard erzeugt Tracker-Karten, responsives Raster und geteilten PV-Balken automatisch. Die maximale PV-Gesamtleistung wird aus allen `maxKw`-Werten berechnet.

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
| `batteryPower` | Ja | Aktuelle Lade-/Entladeleistung | W oder kW |
| `batteryEnergyRemaining` | Ja | Aktuell verbleibende Batterieenergie | Wh oder kWh |
| `batteryChargeEnergyToday` | Ja | Heute in die Batterie geladene Energie | Wh oder kWh |
| `batteryDischargeEnergyToday` | Ja | Heute aus der Batterie entladene Energie | Wh oder kWh |
| `compensationToday` | Nein | Einspeiseerlös heute | EUR |
| `batteryRuntime` | Nein | Geschätzte Restlaufzeit | Zahl/Text |

## Vorzeichen der Batterieleistung

Die aktuelle Dashboard-Logik erwartet:

- positiver Wert = Batterie lädt
- negativer Wert = Batterie entlädt

Wenn deine Integration das Vorzeichen umgekehrt liefert, kannst du einen Home-Assistant-Template-Sensor verwenden oder die Batterielogik anpassen.

## Hausverbrauch heute

`houseEnergyToday` ist optional. Ohne eigenen Sensor wird der Wert aus der Energiebilanz berechnet:

```text
PV-Produktion
+ Netzimport
+ Batterieentladung
- Netzeinspeisung
- Batterieladung
= Hausverbrauch
```

## Power Flux Card

Die Power Flux Card besitzt am Anfang von `dashboard.yaml` einen eigenen `entities:`-Block. Dieser ist unabhängig vom JavaScript-`CONFIG`-Objekt und muss derzeit separat mit den passenden Entity-IDs befüllt werden.
