# Solar Dashboard for Home Assistant

[English](README.md) | [Deutsch](README_DE.md)

A responsive solar and battery dashboard for Home Assistant with Power Flux visualization, dynamic MPPT gauges, daily energy values, grid flow, battery status, feed-in revenue, adaptive light/dark styling, bilingual UI support, dedicated wall-display profiles, and configurable dashboard modules.

Current version: **v0.8.4-alpha**

> Alpha means the dashboard is already usable, but configuration, compatibility and UI behavior are still being tested across different Home Assistant installations.

## Highlights

- Automatic Home Assistant light/dark mode support
- Adaptive glows and gradients in both modes
- Dynamic support for 1, 2, 3 or more MPPT/PV trackers
- Four prepared MPPT configuration slots
- Automatic PV maximum based on all enabled tracker `maxKw` values
- Dynamic split PV Total bar for all enabled trackers
- User-configurable module visibility, order and size
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

In Home Assistant: edit the target dashboard, add a **Manual** card, paste the complete contents of `dashboard.yaml`, and save.

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

## Module visibility, order and size

Each module is configured with an `id` and a preferred `size`:

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

The array order is the display order. Remove an object to hide that module.

Sizes use a four-column layout:

- `small` — 1 of 4 columns
- `large` — 2 of 4 columns
- `max` — full row

On narrow screens the dashboard automatically increases the minimum span where needed for readability. The default configuration keeps `payment` and `runtime` side-by-side on phones by assigning both `large`.

Available module IDs:

- `mppt` — tracker gauges with current power, daily production and configured maximum
- `pvTotal` — total PV power, PV percentage and tracker-split production bar
- `battery` — SoC, remaining battery energy, current battery power and status
- `live` — compact PV/house/grid/battery live overview with daily energy values
- `payment` — today's feed-in revenue/compensation
- `runtime` — estimated remaining battery runtime

Power Flux intentionally remains the separate first Lovelace card.

## MPPT / tracker configuration

Four tracker slots are prepared in the user configuration. Set `enabled: false` for unused trackers. Disabled trackers do not affect gauges, PV maximum calculation or the PV Total split bar.

The example configuration uses MPPT 1 = 9.10 kW and MPPT 2 = 6.37 kW, resulting in 15.47 kW calculated PV maximum. Battery capacity is 12.50 kWh.

## Modular source architecture

`dashboard.yaml` is generated from smaller source modules under `src/` via `tools/build_dashboard.py`. GitHub Actions rebuilds the user-facing file automatically whenever source files or build tooling change.

Normal Home Assistant users only need `dashboard.yaml`.

## Sensor mapping

The included SolaX entity IDs are examples. Other inverter, battery or meter systems can be used as long as the mapped sensors provide the expected measurement.

See:

- [Entity reference](docs/ENTITY_REFERENCE.md)
- [Home Assistant testing guide](docs/TESTING.md)
- [Source architecture](src/README.md)
- [Changelog](CHANGELOG.md)

## Versioning

- `v0.8.x-alpha` — active feature development and compatibility testing
- `v0.9.x-beta` — feature-complete testing phase
- `v1.0.0` — first stable release
