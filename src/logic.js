/*
 * Shared logic snippets / Gemeinsame Logikbausteine
 *
 * The build script injects these helpers into dashboard.yaml.
 * Das Build-Skript fügt diese Helfer in dashboard.yaml ein.
 */

function formatRuntimeSensor(runtimeSensor, unknownLabel) {
  const raw = runtimeSensor?.state;

  if (!raw || raw === 'unknown' || raw === 'unavailable') {
    return unknownLabel;
  }

  const unit = String(
    runtimeSensor?.attributes?.unit_of_measurement || ''
  ).trim();

  const numeric = Number.parseFloat(raw);

  if (Number.isFinite(numeric)) {
    // If Home Assistant exposes a unit, keep it. Otherwise runtime defaults to hours.
    // Wenn Home Assistant eine Einheit liefert, wird sie verwendet. Sonst gilt Stunde als Standard.
    const runtimeUnit = unit || 'h';
    return `${numeric.toLocaleString(locale, {
      minimumFractionDigits: 1,
      maximumFractionDigits: 1
    })} ${runtimeUnit}`;
  }

  return unit ? `${raw} ${unit}` : raw;
}
