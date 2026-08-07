from pathlib import Path

path = Path('dashboard.yaml')
text = path.read_text(encoding='utf-8')

# Version header
text = text.replace('# solar_dashboard V7.2 - dashboard.yaml', '# solar_dashboard v0.8.0-alpha - dashboard.yaml', 1)
text = text.replace('# solar_dashboard V7.1 - dashboard.yaml', '# solar_dashboard v0.8.0-alpha - dashboard.yaml', 1)
text = text.replace('# solar_dashboard V7 - dashboard.yaml', '# solar_dashboard v0.8.0-alpha - dashboard.yaml', 1)

# Add language option to user configuration.
needle = "          const CONFIG = {\n"
if "            language: 'auto'," not in text:
    if needle not in text:
        raise SystemExit('CONFIG block not found')
    text = text.replace(
        needle,
        needle + "\n            // UI language: 'auto', 'de' or 'en'.\n            // auto follows the Home Assistant language and falls back to English.\n            language: 'auto',\n",
        1,
    )

# Insert translation table and locale resolver after CONFIG.
marker = "          };\n\n          /*\n           * ========================================================\n           * HILFSFUNKTIONEN"
if "const I18N = {" not in text:
    if marker not in text:
        raise SystemExit('helper marker not found')
    i18n = r'''          };

          /*
           * ========================================================
           * INTERNATIONALIZATION / I18N
           * ========================================================
           */

          const I18N = {
            de: {
              today: 'Heute',
              todayUpper: 'HEUTE',
              max: 'Max.',
              maxUpper: 'MAX',
              pv: 'PV',
              pvTotal: 'PV TOTAL',
              house: 'HAUS',
              grid: 'NETZ',
              import: 'Import',
              export: 'Export',
              battery: 'BATTERIE',
              charge: 'Laden',
              discharge: 'Entladen',
              compensationToday: 'Vergütung heute',
              feedInRevenue: 'Einspeiseerlös',
              runtime: 'Restlaufzeit',
              unknown: 'Unbekannt',
              standby: 'STANDBY',
              charging: 'LÄDT',
              discharging: 'ENTLÄDT'
            },
            en: {
              today: 'Today',
              todayUpper: 'TODAY',
              max: 'Max.',
              maxUpper: 'MAX',
              pv: 'PV',
              pvTotal: 'PV TOTAL',
              house: 'HOUSE',
              grid: 'GRID',
              import: 'Import',
              export: 'Export',
              battery: 'BATTERY',
              charge: 'Charge',
              discharge: 'Discharge',
              compensationToday: 'Revenue today',
              feedInRevenue: 'Feed-in revenue',
              runtime: 'Runtime',
              unknown: 'Unknown',
              standby: 'STANDBY',
              charging: 'CHARGING',
              discharging: 'DISCHARGING'
            }
          };

          const configuredLanguage =
            String(CONFIG.language || 'auto').toLowerCase();

          const detectedLanguage =
            String(
              hass?.language ||
              window?.navigator?.language ||
              'en'
            ).toLowerCase();

          const language =
            configuredLanguage === 'de' ||
            configuredLanguage === 'en'
              ? configuredLanguage
              : detectedLanguage.startsWith('de')
                ? 'de'
                : 'en';

          const t = I18N[language] || I18N.en;
          const locale = language === 'de' ? 'de-AT' : 'en-US';

          /*
           * ========================================================
           * HILFSFUNKTIONEN'''
    text = text.replace(marker, i18n, 1)

# Locale-aware number formatting.
text = text.replace("return value.toLocaleString('de-AT', {", "return value.toLocaleString(locale, {", 1)

# Dynamic status strings.
text = text.replace("let batteryStatus = 'STANDBY';", "let batteryStatus = t.standby;", 1)
text = text.replace("batteryStatus = 'LÄDT';", "batteryStatus = t.charging;", 1)
text = text.replace("batteryStatus = 'ENTLÄDT';", "batteryStatus = t.discharging;", 1)
text = text.replace("runtimeSensor?.state || 'Unbekannt';", "runtimeSensor?.state || t.unknown;", 1)
text = text.replace("? 'Unbekannt'\n              : runtimeRaw;", "? t.unknown\n              : runtimeRaw;", 1)

# UI labels inside HTML template strings.
replacements = {
    'HEUTE · MAX ${formatNumber(': '${t.todayUpper} · ${t.maxUpper} ${formatNumber(',
    '>\n                      PV\n                    </div>': '>\n                      ${t.pv}\n                    </div>',
    '>\n                      HAUS\n                    </div>': '>\n                      ${t.house}\n                    </div>',
    '>\n                      NETZ\n                    </div>': '>\n                      ${t.grid}\n                    </div>',
    '>\n                      BATTERIE\n                    </div>': '>\n                      ${t.battery}\n                    </div>',
    'Heute ${formatEnergy(solarToday)} kWh': '${t.today} ${formatEnergy(solarToday)} kWh',
    'Max. ${formatNumber(pvMaximum, 2, 2)} kW': '${t.max} ${formatNumber(pvMaximum, 2, 2)} kW',
    'Heute ${formatEnergy(houseToday)} kWh': '${t.today} ${formatEnergy(houseToday)} kWh',
    'Import\n                        ${formatEnergy(importToday)}': '${t.import}\n                        ${formatEnergy(importToday)}',
    'Export\n                        ${formatEnergy(exportToday)}': '${t.export}\n                        ${formatEnergy(exportToday)}',
    'Laden\n                        ${formatEnergy(batteryInputToday)}': '${t.charge}\n                        ${formatEnergy(batteryInputToday)}',
    'Entladen\n                        ${formatEnergy(batteryOutputToday)}': '${t.discharge}\n                        ${formatEnergy(batteryOutputToday)}',
    '>\n                    PV TOTAL\n                  </div>': '>\n                    ${t.pvTotal}\n                  </div>',
    '} kWh heute': '} kWh ${t.today.toLowerCase()}',
    '>\n                    Vergütung heute\n                  </div>': '>\n                    ${t.compensationToday}\n                  </div>',
    '>\n                    Einspeiseerlös\n                  </div>': '>\n                    ${t.feedInRevenue}\n                  </div>',
    '>\n                    Restlaufzeit\n                  </div>': '>\n                    ${t.runtime}\n                  </div>',
    '>\n                    Batterie\n                  </div>': '>\n                    ${t.battery}\n                  </div>',
}
for old, new in replacements.items():
    text = text.replace(old, new)

path.write_text(text, encoding='utf-8')
print('Applied v0.8.0-alpha auto/de/en i18n')
