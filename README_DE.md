# Solar Dashboard für Home Assistant

[English](README.md) | [Deutsch](README_DE.md)

Ein responsives PV- und Batterie-Dashboard für Home Assistant mit Power-Flux-Ansicht, dynamischen MPPT-Gauges, Tageswerten, Netzfluss, Batterie, Einspeisevergütung, adaptivem Hell-/Dunkelmodus, zweisprachiger Oberfläche und eigenem Wall-Display-Profil.

Aktuelle Version: **v0.8.4-alpha**

## Highlights

- automatischer Hell-/Dunkelmodus
- dynamische Unterstützung für mehrere MPPT-/PV-Tracker
- vier vorbereitete MPPT-Konfigurationsslots
- automatische PV-Maximalleistung aus allen aktivierten `maxKw`-Werten
- frei konfigurierbare Modul-Sichtbarkeit, Reihenfolge und Größe
- `auto`, `de` und `en`
- Wall- und Performance-Modus
- generierte `dashboard.yaml`

## Schnelltest

[`dashboard.yaml`](dashboard.yaml) vollständig kopieren und in Home Assistant als **manuelle Karte** einfügen.

## Modul-Sichtbarkeit, Reihenfolge und Größe

Jedes Modul wird mit `id` und `size` konfiguriert:

```js
modules: [
  { id: 'mppt',    size: 'max' },
  { id: 'pvTotal', size: 'large' },
  { id: 'battery', size: 'large' },
  { id: 'live',    size: 'max' },
  { id: 'payment', size: 'large' },
  { id: 'runtime', size: 'large' }
],
```

Die Reihenfolge der Blöcke ist gleichzeitig die Reihenfolge im Dashboard. Einen Block entfernen, um das Modul auszublenden.

Größen:

- `small` = 1 von 4 Spalten
- `large` = 2 von 4 Spalten
- `max` = ganze Zeile

Auf schmalen Displays wird die Mindestbreite automatisch vergrößert, damit Module lesbar bleiben. In der Standardkonfiguration stehen `payment` und `runtime` am iPhone wieder nebeneinander.

Verfügbare Modul-IDs:

- `mppt` — Tracker-Gauges
- `pvTotal` — gesamte PV-Leistung und Tracker-Balken
- `battery` — SoC, Restenergie, Leistung und Status
- `live` — PV/Haus/Netz/Batterie Live-Übersicht
- `payment` — heutiger Einspeiseerlös
- `runtime` — Batterie-Restlaufzeit

Power Flux bleibt separat als erste Lovelace-Karte.

## MPPT-/Tracker-Konfiguration

Vier Tracker-Slots sind vorbereitet. Nicht verwendete Tracker bleiben mit `enabled: false` deaktiviert. Deaktivierte Tracker beeinflussen weder Gauges noch PV-Maximum noch den PV-Total-Balken.

## Weitere Dokumentation

- [Entity-Referenz](docs/ENTITY_REFERENCE_DE.md)
- [Home-Assistant-Testanleitung](docs/TESTING_DE.md)
- [Quellcode-Architektur](src/README.md)
- [Changelog](CHANGELOG.md)

## Versionierung

- `v0.8.x-alpha` — aktive Entwicklung
- `v0.9.x-beta` — breite Testphase
- `v1.0.0` — erste stabile Version
