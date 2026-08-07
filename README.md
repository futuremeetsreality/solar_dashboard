# Solar Dashboard for Home Assistant

Ein responsives PV-/Batterie-Dashboard für Home Assistant mit Power-Flux-Ansicht, MPPT-Gauges, Tageswerten, Netzfluss, Batterie und Einspeisevergütung.

Aktueller Stand: **V6**

## Voraussetzungen

Installiere über HACS unter **Frontend**:

- `Button Card` (`custom:button-card`)
- `Power Flux Card` (`custom:power-flux-card`)
- `card-mod`

Danach Home Assistant bzw. den Browser neu laden.

## Schnelltest

Die Datei [`dashboard.yaml`](dashboard.yaml) ist als **eine komplette Lovelace-Karte** aufgebaut.

Zum Testen:

1. Home Assistant öffnen.
2. Gewünschtes Dashboard öffnen.
3. **Dashboard bearbeiten**.
4. **Karte hinzufügen**.
5. **Manuell** auswählen.
6. Den kompletten Inhalt von `dashboard.yaml` einfügen.
7. Speichern.

> Wichtig: `dashboard.yaml` nicht direkt in den Rohkonfigurationseditor des gesamten Dashboards einfügen. Die Datei beginnt mit `type: vertical-stack` und ist daher eine Kartenkonfiguration.

## Konfiguration

Im `custom:button-card`-Teil von `dashboard.yaml` gibt es direkt am Anfang des JavaScript-Templates den Abschnitt:

```text
BENUTZERKONFIGURATION – NUR DIESEN BLOCK ANPASSEN
```

Dort sind alle benötigten Sensoren mit Beschreibung, erwarteter Messgröße und Einheit dokumentiert.

Zusätzlich müssen die Sensoren im Abschnitt `Power Flux Card` angepasst werden. Diese Custom Card kann die JavaScript-Konfiguration der Button Card technisch nicht mitbenutzen, daher gibt es dort einen zweiten kleinen Entity-Block.

## Anlagenwerte

Die Maximalwerte werden zentral unter `CONFIG.limits` festgelegt:

- `pvMaxKw`: installierte PV-Gesamtleistung
- `mppt1MaxKw`: maximale/zugeordnete Leistung an MPPT 1
- `mppt2MaxKw`: maximale/zugeordnete Leistung an MPPT 2
- `batteryCapacityKwh`: Batteriekapazität

Beispielkonfiguration dieser Anlage:

```javascript
limits: {
  pvMaxKw: 15.47,
  mppt1MaxKw: 9.10,
  mppt2MaxKw: 6.37,
  batteryCapacityKwh: 12.50
}
```

## Sensoren

Eine ausführliche Übersicht findest du in [`docs/ENTITY_REFERENCE.md`](docs/ENTITY_REFERENCE.md).

Das Dashboard akzeptiert bei Leistung automatisch **W oder kW** und bei Energie **Wh oder kWh**.

## Hersteller

Das Dashboard ist nicht auf SolaX festgelegt. Die Sensoren dürfen unter anderem aus folgenden Integrationen stammen:

- SolaX
- Fronius
- SMA
- Huawei
- Victron
- GoodWe
- Kostal
- SolarEdge
- Shelly
- ESPHome
- beliebigen Template-Sensoren

Entscheidend ist nur, dass die jeweilige Entity den dokumentierten Messwert liefert.

## Optionale Sensoren

`houseEnergyToday`, `compensationToday` und `batteryRuntime` sind konzeptionell optional.

Wenn `houseEnergyToday` leer gelassen wird, berechnet das Dashboard den Tages-Hausverbrauch aus:

```text
PV-Produktion
+ Netzimport
+ Batterieentladung
- Netzeinspeisung
- Batterieladung
```

## Aufbau

Auf dem Smartphone:

1. Power Flux
2. MPPT 1 / MPPT 2
3. PV Total / Batterie
4. PV / Haus / Netz / Batterie Livewerte
5. Vergütung / Batterierestlaufzeit

Das Layout passt sich an größere Displays und Querformat an.

## Hinweis zur Batterieleistung

Die aktuelle Logik erwartet:

- positiver Wert = Batterie lädt
- negativer Wert = Batterie entlädt

Falls deine Integration das Vorzeichen umgekehrt liefert, muss diese Logik angepasst werden.

## Version

V6 basiert auf dem zuvor getesteten V5.2-Layout und zentralisiert die Entity-Zuordnung im Haupt-Dashboard.
