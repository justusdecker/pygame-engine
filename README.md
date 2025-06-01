# Pygame-engine project:


## Current State of the project:

### The previos Roadmap is cancelled because:

some features i tried to implement will not work properly in the engine currently...

**Here are a few of them:**

- The performance of the depth buffer to Surface in WSP3D is so depressingly poor.
- The FloorCasting method itself is not slow, but overwriting pixels on a Surface is.
- Simply overwriting a surface consumes too much frame time.

### Restructurization & optimizatization

- [x] A better Method to create, edit & render pixels!
- [ ] All of the WSP3D code will be restructurized in the new **data/modules/wsp3d.py**
- [ ] The restructurized code will be using the new **data/modules/kernel/opt_surfarray.SurfArray** class to fast create, edit & render pixels to a surface.
- [ ] **Pygame Surface** will be only called once every frame for performance reasons
- [ ] ctypes.CDLL, C code & jit will be used to go vroom vroom!🐢 >> 🐇
- [ ] the depth buffer will take into account the Sprites & other transparent stuff
- [ ] A better system to track frame times
- [ ] The pathfinding algorithm will be rewritten in C to go vroom vroom!


## The current Project [Version 0.3]:
- engine logo blend in
## This stuff will coming soon:
- ui overhaul
& much more!
Use:
- Essential stuff in the UI Elements will be fixed or expanded
The new datamanagement system will be:
- Encrypted
- use bitarray to save memory(RAM & RWM)
- can be interacting with the registry(If needed)
    

## Already implemented:
- simple box collisions between two entitys
- vectors
- logging
- Animationsystem
- JSON Datamanagement
- UI Elements:
    - Colorpicker
    - Buttons
    - Textinputs
    - labels
    - dropdown menus
    - progress bars
    - Switches
- Some UI Elements may not work currently.
## Subprojects:
### The Cookie Clicker Clone Project:
<p align="center" width="100%">
    <img width="50%" src="https://justusdeckerde.wordpress.com/wp-content/uploads/2025/04/cookie_clicker_clone_project-1.png">
</p>


### Coming soon: 

- A DOOM Clone to get into pseudo 3D(variant)
- A Mario Kart Clone to to get into pseudo 3D(variant)
- A 2D mini RPG to get all of the stuff together & check for missing features,(text_boxes, type_writer_effect and so on!)
- for more detail: view repo project!
