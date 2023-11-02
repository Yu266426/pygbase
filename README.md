# `pygbase-engine`

`pygbase-engine` is a simple engine for pygame that handles states, ui, resources, and more.
__________________
## Current Features
- Game States
  - Easily switch between states:
    - `set_next_state`, `set_next_state_type`
    - `enter` and `exit` methods for detecting changes
  - Has `update`, `fixed_update` (interval adjustable through settings), `draw`
__________________
- Resource Management
  - Loads folders containing assets using `Loader` game state, loads specifiable number of assets per frame (default `1`)
  - Custom config for each folder (`config.json`)
  - Built in types:
    - Images:
      - Config: scale and rotatable
      - Supports cached rotation, but uses large amount RAM for larger surfaces 
    - Sprite Sheets:
    - Config: `rows`, `columns`, `tile_width`, `tile_height`, `scale` (default -1, change to initialise), `rotatable`
  - Can specify custom resources:
    - Provide custom config and loader
    - Can specify initialised asset based on configs
_________________
- Event System / Input Manager
_________________
- Particle System
_________________
- UI system
_________________
## Whats Next
- Todo
