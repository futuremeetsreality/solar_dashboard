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
   * MODULES: VISIBILITY, ORDER AND SIZE
   * MODULE: SICHTBARKEIT, REIHENFOLGE UND GRÖSSE
   *
   * Only modules listed below are shown. The order in this list is also the
   * display order. Remove an object to hide that module or move an object to
   * change its position.
   *
   * Nur die unten eingetragenen Module werden angezeigt. Die Reihenfolge in
   * dieser Liste ist zugleich die Anzeigereihenfolge. Einen Block entfernen,
   * um das Modul auszublenden, oder verschieben, um die Position zu ändern.
   *
   * size controls the preferred width / size steuert die bevorzugte Breite:
   * small = 1 of 4 columns / 1 von 4 Spalten
   * large = 2 of 4 columns / 2 von 4 Spalten
   * max   = full row / ganze Zeile
   *
   * On narrow screens the dashboard automatically increases the minimum width
   * where necessary so modules stay readable.
   * Auf schmalen Displays wird die Mindestbreite automatisch vergrößert, damit
   * die Module lesbar bleiben.
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
   *   Today's feed-in revenue/compensation.
   *   Heutiger Einspeiseerlös bzw. Vergütung.
   *
   * 'runtime'
   *   Estimated remaining battery runtime.
   *   Geschätzte Batterie-Restlaufzeit.
   *
   * Power Flux is intentionally NOT part of this list.
   * Power Flux ist absichtlich NICHT Teil dieser Liste.
   */
  modules: [
    { id: 'mppt',    size: 'max' },
    { id: 'pvTotal', size: 'large' },
    { id: 'battery', size: 'large' },
    { id: 'live',    size: 'max' },
    { id: 'payment', size: 'large' },
    { id: 'runtime', size: 'large' }
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
