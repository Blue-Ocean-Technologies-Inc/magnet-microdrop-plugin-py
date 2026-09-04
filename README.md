# magnet-microdrop-plugin

[![Copier](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/copier-org/copier/master/img/badge/badge-grayscale-inverted-border-orange.json)](https://github.com/copier-org/copier)
[![Template](https://img.shields.io/badge/template-microdrop--plugin--template%40v0.1.1-blue)](https://github.com/Blue-Ocean-Technologies-Inc/microdrop-plugin-template)

MicroDrop magnet/Z-Stage peripheral plugin, packaged as an installable conda
package:

- `peripheral_controller/` — backend board driver (connection monitor,
  Z-Stage state setter, dramatiq serial proxy).
- `peripherals_ui/` — Z-Stage status/controls dock pane, status-bar icon,
  Peripheral Settings preferences pane.
- `peripheral_protocol_controls/` — magnet/Z-Stage protocol column.

`microdrop_plugin.toml` declares the two toggleable plugin groups
(`zstage_ui`, `zstage_backend`); MicroDrop discovers it through the
`microdrop.plugins` entry point. See `docs/PLUGIN_DEVELOPMENT.md` in the
MicroDrop source tree for the plugin model.

## Build

```bash
pixi build
```

(uses `pixi-build-python`; the wheel force-includes the manifest as package
data of `peripheral_controller`).
