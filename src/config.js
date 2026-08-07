/*
 * Solar Dashboard source configuration
 * Solar-Dashboard Quellkonfiguration
 *
 * This file documents the user-facing configuration model used by the builder.
 * Diese Datei dokumentiert das benutzerseitige Konfigurationsmodell des Builders.
 */

const SOURCE_CONFIG = {
  language: 'auto',        // auto | de | en
  displayMode: 'auto',     // auto | desktop | tablet | wall
  performanceMode: 'auto', // auto | high | balanced | low

  /*
   * MPPT / PV trackers
   * MPPT / PV-Tracker
   *
   * Add one object per tracker. / Pro Tracker einen Block ergänzen.
   * power: current power in W or kW / aktuelle Leistung in W oder kW
   * energyToday: daily energy in Wh or kWh / Tagesenergie in Wh oder kWh
   * maxKw: installed DC power assigned to this tracker / zugeordnete Generatorleistung
   */
  trackers: [
    {
      name: 'MPPT 1',
      power: 'sensor.solax_inverter_pv_power_1',
      energyToday: 'sensor.technikraum_solax_inverter_mppt_1_tageszahler',
      maxKw: 9.10,
      colorStart: '#ff9800',
      colorEnd: '#ffd740'
    },
    {
      name: 'MPPT 2',
      power: 'sensor.solax_inverter_pv_power_2',
      energyToday: 'sensor.technikraum_solax_inverter_mppt_2_tageszahler',
      maxKw: 6.37,
      colorStart: '#43a047',
      colorEnd: '#76ff7a'
    }
  ]
};
