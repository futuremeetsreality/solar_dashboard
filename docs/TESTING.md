# Dashboard in Home Assistant testen

## Voraussetzungen

Über HACS → Frontend installieren:

- Button Card
- Power Flux Card
- card-mod

Anschließend Home Assistant bzw. den Browser neu laden.

## Schnellster Test

`dashboard.yaml` ist eine vollständige Lovelace-Kartenkonfiguration.

1. Home Assistant öffnen.
2. Das gewünschte Dashboard öffnen.
3. Dashboard bearbeiten.
4. Karte hinzufügen.
5. Karte **Manuell** auswählen.
6. Den kompletten Inhalt von `dashboard.yaml` einfügen.
7. Speichern.

Die Datei beginnt mit:

```yaml
type: vertical-stack
cards:
```

Sie gehört deshalb in **eine manuelle Karte** und nicht direkt in den Rohkonfigurationseditor des gesamten Dashboards.

## Eigene Anlage konfigurieren

Im zweiten Kartenblock (`custom:button-card`) befindet sich der Abschnitt:

```text
BENUTZERKONFIGURATION – NUR DIESEN BLOCK ANPASSEN
```

Dort werden die Entity-IDs und Anlagenlimits angepasst.

Die Power Flux Card besitzt zusätzlich ihren eigenen `entities:`-Block am Anfang von `dashboard.yaml`. Dort müssen die entsprechenden Live-/Tages-Sensoren ebenfalls angepasst werden.

Für die aktuell hinterlegte SolaX-Testanlage sind die Werte bereits vorkonfiguriert.
