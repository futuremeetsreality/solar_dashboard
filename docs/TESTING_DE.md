# Dashboard in Home Assistant testen

[English](TESTING.md) | [Deutsch](TESTING_DE.md)

## Voraussetzungen

Über HACS → Frontend installieren:

- Button Card
- Power Flux Card
- card-mod

Danach Home Assistant bzw. den Browser neu laden.

## Schnellster Test

`dashboard.yaml` ist eine vollständige Lovelace-Kartenkonfiguration.

1. Home Assistant öffnen.
2. Das gewünschte Dashboard öffnen.
3. Dashboard bearbeiten.
4. Karte hinzufügen.
5. **Manuell** auswählen.
6. Den kompletten Inhalt von `dashboard.yaml` einfügen.
7. Speichern.

Die Datei beginnt mit:

```yaml
type: vertical-stack
cards:
```

Sie gehört deshalb in **eine manuelle Karte** und nicht direkt in den Rohkonfigurationseditor des gesamten Dashboards.

## Sprachumschaltung testen

Im JavaScript-`CONFIG`-Block steht:

```js
language: 'auto',
```

Teste danach:

- `auto`
- `de`
- `en`

Bei `auto` die Home-Assistant-Profilsprache ändern und das Dashboard neu laden. Deutsch soll deutsche Texte und Dezimalkomma verwenden, Englisch englische Texte und Dezimalpunkt.

## Hell- und Dunkelmodus testen

Unter Home Assistant die Darstellung zwischen Hell und Dunkel wechseln. Texte, Kartenflächen, Verläufe und Glows sollen in beiden Modi sauber lesbar bleiben.

## Eigene Anlage konfigurieren

Im `custom:button-card`-Teil befindet sich die zentrale Benutzerkonfiguration. Dort Tracker und Entity-IDs zuordnen.

Die Power Flux Card besitzt am Anfang von `dashboard.yaml` zusätzlich einen eigenen `entities:`-Block, der separat angepasst werden muss.
