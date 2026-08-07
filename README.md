# Solar Dashboard for Home Assistant

[English](README.md) | [Deutsch](README_DE.md)

A responsive solar and battery dashboard for Home Assistant with Power Flux visualization, dynamic MPPT gauges, daily energy values, grid flow, battery status, feed-in revenue, adaptive light/dark styling, bilingual UI support, and dedicated wall-display profiles.

Current version: **v0.8.1-alpha**

> Alpha means the dashboard is already usable, but configuration, compatibility and UI behavior are still being tested across different Home Assistant installations.

## Highlights

- Automatic Home Assistant light/dark mode support
- Adaptive glows and gradients in both modes
- Dynamic support for 1, 2, 3 or more MPPT/PV trackers
- Automatic PV maximum based on all tracker `maxKw` values
- Dynamic split PV Total bar for all configured trackers
- Battery, house and grid live values plus daily values
- `auto`, `de` and `en` dashboard languages
- Locale-aware number formatting
- Manufacturer-independent sensor mapping
- Dedicated `wall` layout for permanently mounted tablets
- Automatic low-performance compatibility mode for older Safari/iPadOS devices

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

Inside the `custom:button-card` configuration, set:

```js
language: 'auto',
```

Supported values:

- `auto` — follows the Home Assistant language; German is detected as `de`, everything else currently falls back to English
- `de` — force German
- `en` — force English

Number formatting follows the selected language as well.

## Display and performance profiles

v0.8.1-alpha adds two independent options:

```js
displayMode: 'auto',
performanceMode: 'auto',
```

`displayMode` supports:

- `auto` — normal responsive behavior; tablet-like touch devices are detected as tablets
- `desktop` — desktop profile
- `tablet` — tablet profile
- `wall` — larger values, thicker bars and optimized spacing for permanently mounted displays

`performanceMode` supports:

- `auto` — checks browser capabilities automatically
- `high` — full visual effects
- `balanced` — reduced GPU-heavy effects
- `low` — compatibility profile with simpler rendering, no expensive SVG filters and no animations

Older Safari/iPadOS versions that do not support `color-mix()` automatically fall back to `low` mode. This is intended for older wall tablets such as an iPad Air 2 on iPadOS 15.

For a permanently mounted older iPad, start with:

```js
displayMode: 'wall',
performanceMode: 'auto',
```

## MPPT / tracker configuration

Trackers are configured in `CONFIG.trackers`:

```js
trackers: [
  {
    name: 'MPPT 1',
    power: 'sensor.my_mppt_1_power',
    energyToday: 'sensor.my_mppt_1_energy_today',
    maxKw: 9.10,
    colorStart: '#ff9800',
    colorEnd: '#ffd740'
  },
  {
    name: 'MPPT 2',
    power: 'sensor.my_mppt_2_power',
    energyToday: 'sensor.my_mppt_2_energy_today',
    maxKw: 6.37,
    colorStart: '#43a047',
    colorEnd: '#76ff7a'
  }
]
```

Use one object for one tracker, add more objects for additional trackers. The grid, gauges and PV Total bar adapt automatically.

## Example configuration included in the repository

- MPPT 1: 9.10 kW
- MPPT 2: 6.37 kW
- calculated PV maximum: 15.47 kW
- battery capacity: 12.50 kWh

## Sensor mapping

The included SolaX entity IDs are only examples. Other inverter, battery or meter systems can be used as long as the mapped sensors provide the expected measurement.

See:

- [Entity reference](docs/ENTITY_REFERENCE.md)
- [Home Assistant testing guide](docs/TESTING.md)
- [Changelog](CHANGELOG.md)

## Versioning

The project follows semantic pre-release versioning:

- `v0.8.x-alpha` — active feature development and compatibility testing
- `v0.9.x-beta` — feature-complete testing phase
- `v1.0.0` — first stable release
