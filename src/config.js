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
   * 'benefit'
   *   Today's financial PV benefit split into feed-in revenue and savings from
   *   self-consumption. The amount of detail automatically follows module size:
   *   small = compact totals, large = split values + daily energy,
   *   max = full economic overview including rates and benefit split bar.
   *   Heutiger finanzieller PV-Nutzen, aufgeteilt in Einspeiseerlös und
   *   Eigenverbrauchsersparnis. Der Detailgrad folgt automatisch der Größe:
   *   small = kompakte Summen, large = Splitwerte + Tagesenergie,
   *   max = vollständige Wirtschaftsansicht inkl. Tarifen und Anteilbalken.
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
    { id: 'benefit', size: 'large' },
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
  ],

  /*
   * FINANCIAL / PV BENEFIT ENTITIES
   * FINANZ / PV-NUTZEN ENTITÄTEN
   *
   * These defaults target Solar Yield Calculator entity names. Replace them
   * with equivalent sensors from any other integration if required.
   * Diese Vorgaben verwenden die Entity-Namen des Solar Yield Calculators.
   * Bei anderen Integrationen einfach durch gleichwertige Sensoren ersetzen.
   */
  benefitEntities: {
    // Today's feed-in revenue in EUR.
    // Heutiger Einspeiseerlös in EUR.
    exportRevenueToday: 'sensor.solar_yield_calculator_day_export_revenue',

    // Today's avoided electricity cost from self-consumption in EUR.
    // Heutige Ersparnis durch Eigenverbrauch in EUR.
    selfConsumptionSavingToday: 'sensor.solar_yield_calculator_day_self_consumption_saving',

    // Optional total benefit in EUR. If unavailable, the dashboard adds the two values above.
    // Optionaler Gesamtnutzen in EUR. Wenn nicht verfügbar, werden die beiden Werte oben addiert.
    totalBenefitToday: 'sensor.solar_yield_calculator_day_total_benefit',

    // Current effective feed-in revenue rate, preferably ct/kWh.
    // Aktueller effektiver Einspeiseerlös, vorzugsweise ct/kWh.
    exportRevenueRate: 'sensor.solar_yield_calculator_export_revenue_rate',

    // Current self-consumption saving rate, preferably ct/kWh.
    // Aktuelle Eigenverbrauchsersparnis, vorzugsweise ct/kWh.
    selfConsumptionSavingRate: 'sensor.solar_yield_calculator_self_consumption_saving_rate'
  }
};
