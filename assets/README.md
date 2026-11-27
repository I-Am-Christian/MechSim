# Frontier engine extensions

The base game continues to use Three.js r160 and the original campaign and combat rules. frontier-extensions.js loads optional components separately; failures leave the existing engine active.

- GLTFLoader imports the bundled original frontier-armor.gltf, attached to existing damageable arm modules. Named nodes are modular, and the original articulated mech joints remain authoritative. MeshoptDecoder and KTX2Loader are configured for future compressed assets; the included small armor model is uncompressed.
- Rapier 0.17.3: gravity, bounce, friction and collision for detached insect parts and shell fragments, with a 72-body limit. Existing gameplay collision and swept projectiles are unchanged.
- Yuka 0.7.8: local separation steering, combined with the game's existing avoidance and pilot AI.
- Recast 0.43.1: walkable navigation mesh from active obstacles, queried only when the direct local route is blocked. Rebuilds are throttled and existing steering remains available.
- Three.js r160 postprocessing: bloom and SSAO on High; bloom only on Balanced; direct rendering on Low. Auto lowers settings when frame times stay high. Cockpit/HUD stay separate.
- Poly Haven and ambientCG: local assets preferred; optional upstream URLs are attempted and procedural fallback is retained if unavailable. To avoid runtime CDN/CORS issues, run python tools/fetch_cc0_assets.py and commit the resulting assets/cc0 files if successful.

## Asset sources
- https://polyhaven.com/a/rocky_terrain — Rocky Terrain, CC0.
- https://polyhaven.com/a/rocky_ridge — Rocky Ridge HDRI, CC0.
- https://ambientcg.com/view?id=Metal032 — Metal 032, CC0.
- frontier-armor.gltf — original geometry generated for MechSim; no third-party model.

No API keys, paid model generators or npm build step are required by the game. Optional CDN modules and remote textures require a network connection. Graphics selection is saved locally, and clicking the EXTENSIONS indicator shows the runtime status. Use Low if the new effects are too expensive for your GPU.

## Verification
The source is syntax-checked and the included glTF structure is validated. CDN availability, real asset loading, WebAssembly initialization, browser visuals and actual frame rate need live browser testing. No full game-ready external mech skeleton or compressed GLB/KTX2 texture is bundled yet.
