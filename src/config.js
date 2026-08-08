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
   * MODULES: VISIBILITY AND ORDER
   * MODULE: SICHTBARKEIT UND REIHENFOLGE
   *
   * Only modules listed below are shown. The order in this list is also the
   * display order. Remove an entry to hide that module or move an entry to
   * change its position.
   *
   * Nur die unten eingetragenen Module werden angezeigt. Die Reihenfolge in
   * dieser Liste ist zugleich die Anzeigereihenfolge. Einen Eintrag entfernen,
   * um das Modul auszublenden, oder verschieben, um die Position zu ändern.
   *
   * Available modules / Verfügbare Module:
   *
   * 'mppt'
   *   One gauge card per enabled PV tracker including current power,
   *   daily production and configured maximum.
   *   Eine Gauge-Karte pro aktiviertem PV-Tracker mit aktueller Leistung,
   *   Tagesertrag und eingestellter Maximalleistung.
   *
   * 'pvTotal'
   *   Total current PV power, percentage of installed PV maximum and a
   *   color-split bar showing the contribution of every enabled tracker.
   *   Gesamte aktuelle PV-Leistung, Prozent der installierten Maximalleistung
   *   und farblich geteilter Balken für alle aktivierten Tracker.
   *
   * 'battery'
   *   Battery state of charge, remaining energy, current charge/discharge
   *   power and battery status.
   *   Batterie-SoC, verbleibende Energie, aktuelle Lade-/Entladeleistung
   *   und Batteriestatus.
   *
   * 'live'
   *   Compact live overview of PV, house load, grid and battery including
   *   daily energy values.
   *   Kompakte Live-Übersicht für PV, Haus, Netz und Batterie inklusive
   *   Tagesenergiewerten.
   *
   * 'payment'
   *   Today's feed-in revenue/compensation. Intended for an optional
   *   calculated Home Assistant sensor.
   *   Heutiger Einspeiseerlös bzw. Vergütung. Für einen optionalen
   *   berechneten Home-Assistant-Sensor gedacht.
   *
   * 'runtime'
   *   Estimated remaining battery runtime. The sensor unit is displayed
   *   automatically; if no unit exists, hours (h) are assumed.
   *   Geschätzte Batterie-Restlaufzeit. Die Sensoreinheit wird automatisch
   *   angezeigt; ohne Einheit werden Stunden (h) angenommen.
   *
   * Power Flux is intentionally NOT part of this list. It remains the separate
   * first Lovelace card and is not mixed into the module order.
   * Power Flux ist absichtlich NICHT Teil dieser Liste. Die Karte bleibt als
   * separate erste Lovelace-Karte außerhalb der Modul-Reihenfolge.
   */
  modules: [
    'mppt',
    'pvTotal',
    'battery',
    'live',
    'payment',
    'runtime'
  ],

  /*
   * MPPT / PV TRACKERS
   * MPPT / PV-TRACKER
   *
   * Up to four ready-to-use slots are included below. More can still be added.
   * Set enabled: false for unused trackers. Disabled trackers are ignored by
   * gauges, PV maximum calculation and the PV Total split bar.
   *
   * Unten sind vier vorbereitete Slots enthalten. Weitere können weiterhin
   * ergänzt werden. Nicht verwendete Tracker auf enabled: false setzen.
   * Deaktivierte Tracker werden bei Gauges, PV-Maximum und PV-Total-Balken
   * vollständig ignoriert.
   *
   * power: current power in W or kW / aktuelle Leistung in W oder kW
   * energyToday: daily energy in Wh or kWh / Tagesenergie in Wh oder kWh
   * maxKw: installed DC power assigned to this tracker / zugeordnete Generatorleistung
   */
  trackers: [
    {
      enabled: true,
      name: 'MPPT 1',
      power: 'sensor.solax_inverter_pv_power_1',
      energyToday: 'sensor.technikraum_solax_inverter_mppt_1_tageszahler',
      maxKw: 9.10,
      colorStart: '#ff9800',
      colorEnd: '#ffd740'
    },
    {
      enabled: true,
      name: 'MPPT 2',
      power: 'sensor.solax_inverter_pv_power_2',
      energyToday: 'sensor.technikraum_solax_inverter_mppt_2_tageszahler',
      maxKw: 6.37,
      colorStart: '#43a047',
      colorEnd: '#76ff7a'
    },
    {
      enabled: false,
      name: 'MPPT 3',
      power: '',
      energyToday: '',
      maxKw: 0,
      colorStart: '#2196f3',
      colorEnd: '#00e5ff'
    },
    {
      enabled: false,
      name: 'MPPT 4',
      power: '',
      energyToday: '',
      maxKw: 0,
      colorStart: '#ab47bc',
      colorEnd: '#e040fb'
    }
  ]
};
