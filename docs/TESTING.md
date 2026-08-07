# Testing the dashboard in Home Assistant

[English](TESTING.md) | [Deutsch](TESTING_DE.md)

## Requirements

Install via HACS → Frontend:

- Button Card
- Power Flux Card
- card-mod

Reload Home Assistant or the browser afterwards.

## Fastest test

`dashboard.yaml` is a complete Lovelace card configuration.

1. Open Home Assistant.
2. Open the target dashboard.
3. Edit dashboard.
4. Add card.
5. Select **Manual**.
6. Paste the full contents of `dashboard.yaml`.
7. Save.

The file begins with:

```yaml
type: vertical-stack
cards:
```

Therefore it belongs inside **one Manual card**, not directly in the raw configuration editor for the entire dashboard.

## Test language switching

Inside the JavaScript `CONFIG` block set:

```js
language: 'auto',
```

Then test:

- `auto`
- `de`
- `en`

With `auto`, change the Home Assistant profile language and reload the dashboard. German should use German labels and decimal commas; English should use English labels and decimal points.

## Test light and dark mode

Switch Home Assistant appearance between Light and Dark. The dashboard should keep readable text, adaptive card surfaces, gradients and glows in both modes.

## Configure your own installation

The `custom:button-card` contains the main user configuration. Map the tracker and entity IDs there.

The Power Flux Card has a separate `entities:` block at the beginning of `dashboard.yaml`; map its entities separately.
