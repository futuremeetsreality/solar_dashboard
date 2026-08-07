# Entity Reference

Diese Datei beschreibt, welche Messwerte für das Dashboard benötigt werden. Die Namen deiner Home-Assistant-Entities sind egal.

| CONFIG-Schlüssel | Pflicht | Erwarteter Messwert | Einheit |
|---|---|---|---|
| `mppt1Power` | Ja | Aktuelle Leistung des ersten PV-/MPPT-Eingangs | W oder kW |
| `mppt2Power` | Ja | Aktuelle Leistung des zweiten PV-/MPPT-Eingangs | W oder kW |
| `mppt1EnergyToday` | Ja | Seit Mitternacht erzeugte Energie von MPPT 1 | Wh oder kWh |
| `mppt2EnergyToday` | Ja | Seit Mitternacht erzeugte Energie von MPPT 2 | Wh oder kWh |
| `pvPowerTotal` | Ja | Aktuelle gesamte PV-Leistung | W oder kW |
| `pvEnergyToday` | Ja | Gesamte PV-Produktion seit Mitternacht | Wh oder kWh |
| `housePower` | Ja | Aktueller Gesamtverbrauch des Hauses | W oder kW |
| `houseEnergyToday` | Nein | Hausverbrauch seit Mitternacht | Wh oder kWh |
| `gridImportPower` | Ja | Aktuelle Leistung aus dem Stromnetz | W oder kW |
| `gridExportPower` | Ja | Aktuelle Leistung ins Stromnetz | W oder kW |
| `gridImportEnergyToday` | Ja | Netzbezug seit Mitternacht | Wh oder kWh |
| `gridExportEnergyToday` | Ja | Netzeinspeisung seit Mitternacht | Wh oder kWh |
| `batterySoc` | Ja | Ladezustand der Batterie | % |
| `batteryPower` | Ja | Aktuelle Lade-/Entladeleistung | W oder kW |
| `batteryEnergyRemaining` | Ja | Aktuell verbleibende gespeicherte Energie | Wh oder kWh |
| `batteryChargeEnergyToday` | Ja | Heute in die Batterie geladene Energie | Wh oder kWh |
| `batteryDischargeEnergyToday` | Ja | Heute aus der Batterie entladene Energie | Wh oder kWh |
| `compensationToday` | Nein | Heutiger Einspeiseertrag / Vergütung | EUR |
| `batteryRuntime` | Nein | Geschätzte Restlaufzeit der Batterie | Zahl oder Text |

## Power Flux Card

Die Power Flux Card benötigt dieselben Live-Sensoren noch einmal in ihrem eigenen `entities:`-Block. Das ist keine unnötige Doppelung im JavaScript, sondern eine technische Grenze zwischen zwei unabhängigen Lovelace Custom Cards.

Wichtigste Zuordnung:

| Power Flux Feld | Messwert |
|---|---|
| `solar` | aktuelle PV-Gesamtleistung |
| `grid` | aktueller Netzimport |
| `grid_export` | aktuelle Netzeinspeisung |
| `battery` | aktuelle Batterieleistung |
| `battery_soc` | Batterie-SoC |
| `house` | aktueller Hausverbrauch |
| `secondary_grid` | Netzeinspeisung heute |
| `secondary_solar` | PV-Produktion heute |
| `secondary_house` | Hausverbrauch heute |
| `tertiary_house` | Netzimport heute |
| `secondary_battery` | Batterie-Ladeenergie heute |
| `grid_to_battery` | optionale aktuelle Leistung Netz → Batterie |

## Vorzeichen der Batterie

Die Dashboard-Logik geht derzeit davon aus:

```text
positiv  = Laden
negativ  = Entladen
```

Bei umgekehrter Vorzeichenkonvention muss die Statuslogik in `dashboard.yaml` angepasst werden.
