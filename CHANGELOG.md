# Changelog

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
- README und Entity Reference auf V7 aktualisiert.

## V6 - 2026-08-07

- Benutzerkonfiguration für alle Haupt-Entities zentralisiert.
- Jeder Sensor direkt im Code dokumentiert.
- MPPT-Maximalwerte getrennt konfigurierbar.
- MPPT 1: 9,10 kW Beispielwert.
- MPPT 2: 6,37 kW Beispielwert.
- PV-Gesamtmaximum: 15,47 kW Beispielwert.
- Batterie: 12,50 kWh Beispielwert.
- `triggers_update: all`, damit Entity-IDs nicht zusätzlich in einer Triggerliste gepflegt werden müssen.
- Optionaler Haus-Tagesverbrauch mit Fallback auf Energiebilanz.
- V5.2-Layout beibehalten.
