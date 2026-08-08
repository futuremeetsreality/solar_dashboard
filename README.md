# Solar Dashboard for Home Assistant

[English](README.md) | [Deutsch](README_DE.md)

A responsive solar and battery dashboard for Home Assistant with Power Flux visualization, dynamic MPPT gauges, daily energy values, grid flow, battery status, feed-in revenue, adaptive light/dark styling, bilingual UI support, and dedicated wall-display profiles.

Current version: **v0.8.3-alpha**

> Alpha means the dashboard is already usable, but configuration, compatibility and UI behavior are still being tested across different Home Assistant installations.

## Highlights

- Automatic Home Assistant light/dark mode support
- Adaptive glows and gradients in both modes
- Dynamic support for 1, 2, 3 or more MPPT/PV trackers
- Four prepared MPPT configuration slots
- Automatic PV maximum based on all enabled tracker `maxKw` values
- Dynamic split PV Total bar for all enabled trackers
- User-configurable module visibility and ordering
- Battery, house and grid live values plus daily values
- `auto`, `de` and `en` dashboard languages
- Locale-aware number formatting
- Manufacturer-independent sensor mapping
- Dedicated `wall` layout for permanently mounted tablets
- Automatic low-performance compatibility mode for older Safari/iPadOS devices
- Modular source architecture with generated `dashboard.yaml`

## Requirements

Install via HACS → Frontend:

- `Button Card` (`custom:button-card`)
- `Power Flux Card` (`custom:power-flux-card`)
- `card-mod`

Reload Home Assistant or your browser afterwards.

## Quick test

[`dashboard.yaml`](dashboard.yaml) is one complete Lovelace card configuration.

In Home Assistant:

1. Edit the target dashboard.
2. Add a card.
3. Select **Manual**.
4. Paste the complete contents of `dashboard.yaml`.
5. Save.

Do not paste it directly into the raw configuration editor for the entire dashboard.

## Language

```js
language: 'auto',
```

Supported values: `auto`, `de`, `en`. Number formatting follows the selected language.

## Display and performance profiles

```js
displayMode: 'auto',
performanceMode: 'auto',
```

`displayMode`: `auto`, `desktop`, `tablet`, `wall`

`performanceMode`: `auto`, `high`, `balanced`, `low`

Older Safari/iPadOS versions that do not support `color-mix()` automatically fall back to `low` mode. For an older permanently mounted iPad, start with:

```js
displayMode: 'wall',
performanceMode: 'auto',
```

## Module visibility and order

v0.8.3-alpha adds `CONFIG.modules`:

```js
modules: [
  'mppt',
  'pvTotal',
  'battery',
  'live',
  'payment',
  'runtime'
],
```

Only listed modules are shown, and the array order is the dashboard order. Remove an ID to hide a module or move it to change its position.

Available module IDs:

- `mppt` — tracker gauges with current power, daily production and configured maximum
- `pvTotal` — total PV power, PV percentage and tracker-split production bar
- `battery` — SoC, remaining battery energy, current battery power and status
- `live` — compact PV/house/grid/battery live overview with daily energy values
- `payment` — today's feed-in revenue/compensation
- `runtime` — estimated remaining battery runtime

Power Flux is intentionally not part of this list. It remains the separate first Lovelace card.

## MPPT / tracker configuration

Four tracker slots are prepared in the user configuration. Unused trackers can stay disabled:

```js
{
  enabled: false,
  name: 'MPPT 3',
  power: '',
  energyToday: '',
  maxKw: 0,
  colorStart: '#2196f3',
  colorEnd: '#00e5ff'
}
```

Set `enabled: true` and configure the entities plus `maxKw` to activate a tracker. Disabled trackers do not affect gauges, PV maximum calculation or the PV Total split bar.

The example configuration included in the repository uses:

- MPPT 1: 9.10 kW
- MPPT 2: 6.37 kW
- calculated PV maximum: 15.47 kW
- battery capacity: 12.50 kWh

## Modular source architecture

`dashboard.yaml` is generated from smaller source modules:

```text
src/
├── config.js
├── i18n.js
├── layout.js
├── logic.js
├── styles.css
└── README.md

tools/
└── build_dashboard.py
```

Local build:

```bash
python tools/build_dashboard.py
```

GitHub Actions automatically runs the same builder whenever source files or build tooling change. Normal Home Assistant users still only need `dashboard.yaml`.

The proven legacy V7 base remains temporarily in the v0.8.x build pipeline while sections are migrated into `src/` step by step. This avoids a risky rewrite of a working dashboard.

## Sensor mapping

The included SolaX entity IDs are only examples. Other inverter, battery or meter systems can be used as long as the mapped sensors provide the expected measurement.

See:

- [Entity reference](docs/ENTITY_REFERENCE.md)
- [Home Assistant testing guide](docs/TESTING.md)
- [Source architecture](src/README.md)
- [Changelog](CHANGELOG.md)

## Versioning

The project follows semantic pre-release versioning:

- `v0.8.x-alpha` — active feature development and compatibility testing
- `v0.9.x-beta` — feature-complete testing phase
- `v1.0.0` — first stable release
