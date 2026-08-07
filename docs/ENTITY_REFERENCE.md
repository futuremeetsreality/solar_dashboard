# Entity Reference — v0.8.0-alpha

[English](ENTITY_REFERENCE.md) | [Deutsch](ENTITY_REFERENCE_DE.md)

This document explains which measurements the dashboard expects. Your Home Assistant entity names do not matter; only the measurement meaning and unit matter.

## MPPT / PV trackers

Trackers are configured as objects in `CONFIG.trackers`.

| Key | Required | Expected measurement | Unit |
|---|---|---|---|
| `name` | Yes | Display name such as `MPPT 1` | Text |
| `power` | Yes | Current power of this PV/MPPT input | W or kW |
| `energyToday` | Yes | Energy produced by this tracker since midnight | Wh or kWh |
| `maxKw` | Yes | Maximum/assigned generator power for this tracker | kW |
| `colorStart` | No | Start color for gauge and PV segment | HEX |
| `colorEnd` | No | End color for gauge and PV segment | HEX |

Example:

```js
{
  name: 'MPPT 1',
  power: 'sensor.my_mppt_power',
  energyToday: 'sensor.my_mppt_energy_today',
  maxKw: 8.00,
  colorStart: '#ff9800',
  colorEnd: '#ffd740'
}
```

Use one tracker object for one MPPT, two objects for two MPPTs, and so on. The dashboard creates the tracker cards, responsive grid and split PV bar automatically. Total PV maximum is calculated from all `maxKw` values.

## Other dashboard entities

| CONFIG key | Required | Expected measurement | Unit |
|---|---|---|---|
| `pvPowerTotal` | Yes | Current total PV power across all trackers | W or kW |
| `pvEnergyToday` | Yes | Total PV energy produced since midnight | Wh or kWh |
| `housePower` | Yes | Current total house load | W or kW |
| `houseEnergyToday` | No | House energy consumption since midnight | Wh or kWh |
| `gridImportPower` | Yes | Current power imported from the grid | W or kW |
| `gridExportPower` | Yes | Current power exported to the grid | W or kW |
| `gridImportEnergyToday` | Yes | Grid import energy since midnight | Wh or kWh |
| `gridExportEnergyToday` | Yes | Grid export energy since midnight | Wh or kWh |
| `batterySoc` | Yes | Battery state of charge | % |
| `batteryPower` | Yes | Current battery charge/discharge power | W or kW |
| `batteryEnergyRemaining` | Yes | Energy currently remaining in the battery | Wh or kWh |
| `batteryChargeEnergyToday` | Yes | Energy charged into the battery today | Wh or kWh |
| `batteryDischargeEnergyToday` | Yes | Energy discharged from the battery today | Wh or kWh |
| `compensationToday` | No | Feed-in revenue for today | EUR |
| `batteryRuntime` | No | Estimated battery runtime | Number/Text |

## Battery power sign

The current dashboard logic expects:

- positive value = battery charging
- negative value = battery discharging

If your integration reports the opposite sign, invert it with a Home Assistant template sensor or adjust the battery logic.

## House energy today

`houseEnergyToday` is optional. If it is not configured, the dashboard calculates it from the energy balance:

```text
PV production
+ grid import
+ battery discharge
- grid export
- battery charge
= house consumption
```

## Power Flux Card

The Power Flux Card has its own `entities:` block near the top of `dashboard.yaml`. It is independent from the JavaScript `CONFIG` object and therefore currently requires the relevant entity IDs to be mapped separately.
