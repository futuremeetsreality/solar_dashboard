# apply_theme_v7_1.py
# Zeitstempel: 2026-08-07 21:25

from pathlib import Path
import re
import yaml

path = Path("dashboard.yaml")
text = path.read_text(encoding="utf-8")

text = text.replace(
    "# solar_dashboard V7 - dashboard.yaml",
    "# solar_dashboard V7.1 - dashboard.yaml",
    1,
)
text = re.sub(
    r"# Aktualisiert: .*",
    "# Aktualisiert: 2026-08-07 21:25",
    text,
    count=1,
)

# Power Flux: Home-Assistant-Theme verwenden statt dunklen Hintergrund zu erzwingen.
old_powerflux = '''        ha-card {
          background:
            linear-gradient(
              145deg,
              rgba(16, 29, 39, 0.98),
              rgba(5, 12, 18, 0.98)
            ) !important;

          border: 1px solid rgba(255, 255, 255, 0.08) !important;
          border-radius: 24px !important;

          box-shadow:
            0 8px 24px rgba(0, 0, 0, 0.28) !important;

          color: white !important;
          overflow: hidden !important;

          --primary-text-color: #ffffff;
          --secondary-text-color: rgba(255, 255, 255, 0.62);
          --card-background-color: transparent;
          --ha-card-background: transparent;
        }'''

new_powerflux = '''        ha-card {
          background: var(--ha-card-background, var(--card-background-color)) !important;
          border: 1px solid var(--divider-color, rgba(127,127,127,0.22)) !important;
          border-radius: 24px !important;
          box-shadow: 0 8px 24px rgba(0, 0, 0, 0.16) !important;
          color: var(--primary-text-color) !important;
          overflow: hidden !important;
        }'''

if old_powerflux not in text:
    raise RuntimeError("Power-Flux style block not found")
text = text.replace(old_powerflux, new_powerflux, 1)

# Inaktiver MPPT-Gauge folgt dem aktuellen HA-Theme.
text = text.replace(
    'stroke="rgba(255,255,255,0.11)"',
    'stroke="var(--solar-gauge-track)"',
)

# Zentrale Theme-Variablen.
old_dashboard = '''      .solar-dashboard {
        box-sizing: border-box;
        display: grid;
        width: 100%;
        gap: 10px;
        color: white;'''

new_dashboard = '''      .solar-dashboard {
        --solar-surface: var(--ha-card-background, var(--card-background-color));
        --solar-surface-soft: color-mix(in srgb, var(--solar-surface) 94%, var(--primary-text-color) 6%);
        --solar-surface-strong: color-mix(in srgb, var(--solar-surface) 88%, var(--primary-text-color) 12%);
        --solar-text: var(--primary-text-color);
        --solar-text-secondary: var(--secondary-text-color);
        --solar-border: var(--divider-color, color-mix(in srgb, var(--primary-text-color) 14%, transparent));
        --solar-divider: var(--divider-color, color-mix(in srgb, var(--primary-text-color) 16%, transparent));
        --solar-gauge-track: color-mix(in srgb, var(--primary-text-color) 13%, transparent);
        --solar-inset: color-mix(in srgb, var(--primary-text-color) 5%, transparent);
        --solar-track: color-mix(in srgb, var(--primary-text-color) 8%, transparent);
        --solar-shadow: 0 8px 24px rgba(0,0,0,0.16);

        box-sizing: border-box;
        display: grid;
        width: 100%;
        gap: 10px;
        color: var(--solar-text);'''

if old_dashboard not in text:
    raise RuntimeError("Solar dashboard style block not found")
text = text.replace(old_dashboard, new_dashboard, 1)

# Neutrale Flächen, Linien und Texte über Theme-Variablen.
replacements = [
    ("border: 1px solid rgba(255,255,255,0.08);", "border: 1px solid var(--solar-border);"),
    ("border: 1px solid rgba(255,255,255,0.09);", "border: 1px solid var(--solar-border);"),
    ("1px solid rgba(255,255,255,0.10);", "1px solid var(--solar-divider);"),
    ("background: rgba(255,255,255,0.035);", "background: var(--solar-inset);"),
    ("background: rgba(255,255,255,0.05);", "background: var(--solar-inset);"),
    ("background: rgba(255,255,255,0.07);", "background: var(--solar-track);"),
    ("color: rgba(255,255,255,0.62);", "color: var(--solar-text-secondary);"),
    ("color: rgba(255,255,255,0.48);", "color: var(--solar-text-secondary);"),
    ("color: rgba(255,255,255,0.56);", "color: var(--solar-text-secondary);"),
    ("color: rgba(255,255,255,0.58);", "color: var(--solar-text-secondary);"),
    ("color: white;", "color: var(--solar-text);"),
    ("background: rgba(255,255,255,0.68);", "background: color-mix(in srgb, var(--solar-text) 68%, transparent);"),
    ("border: 3px solid rgba(255,255,255,0.68);", "border: 3px solid color-mix(in srgb, var(--solar-text) 68%, transparent);"),
    ("inset 0 1px 3px rgba(0,0,0,0.45);", "inset 0 1px 3px rgba(0,0,0,0.22);"),
    ("box-shadow:\n          0 8px 24px rgba(0,0,0,0.28);", "box-shadow: var(--solar-shadow);"),
]
for old, new in replacements:
    text = text.replace(old, new)

# Dunkle Basis-Gradienten durch themefähige Flächen ersetzen.
text = text.replace(
    '''background:
          linear-gradient(
            145deg,
            rgba(16,29,39,0.98),
            rgba(5,12,18,0.98)
          );''',
    '''background:
          linear-gradient(
            145deg,
            var(--solar-surface-soft),
            var(--solar-surface)
          );''',
)
text = text.replace(
    '''          linear-gradient(
            145deg,
            rgba(16,29,39,0.98),
            rgba(5,12,18,0.98)
          );''',
    '''          linear-gradient(
            145deg,
            var(--solar-surface-soft),
            var(--solar-surface)
          );''',
)
text = text.replace(
    '''            rgba(16,29,39,0.98),
            rgba(5,12,18,0.98)''',
    '''            var(--solar-surface-soft),
            var(--solar-surface)''',
)

# Info-Karten erhalten im Hell- und Dunkelmodus nur einen dezenten Farbstich.
text = text.replace(
    '''      .payment-panel {
        background:
          linear-gradient(
            145deg,
            rgba(12,31,46,0.98),
            rgba(4,12,18,0.98)
          );
      }''',
    '''      .payment-panel {
        background:
          linear-gradient(
            145deg,
            color-mix(in srgb, var(--solar-surface) 86%, #42a5f5 14%),
            var(--solar-surface)
          );
      }''',
)
text = text.replace(
    '''      .runtime-panel {
        background:
          linear-gradient(
            145deg,
            rgba(28,17,49,0.98),
            rgba(7,9,19,0.98)
          );
      }''',
    '''      .runtime-panel {
        background:
          linear-gradient(
            145deg,
            color-mix(in srgb, var(--solar-surface) 86%, #8e5cff 14%),
            var(--solar-surface)
          );
      }''',
)

# Syntaxprüfung.
data = yaml.safe_load(text)
assert data["type"] == "vertical-stack"
assert data["cards"][0]["type"] == "custom:power-flux-card"
assert data["cards"][1]["type"] == "custom:button-card"

path.write_text(text, encoding="utf-8")
