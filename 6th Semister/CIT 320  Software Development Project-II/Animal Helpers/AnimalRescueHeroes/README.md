# Animal Rescue Heroes

Educational mini-game collection for tablets (iOS/Android). This repo includes starter scripts and structure to implement shape matching, counting, food sorting, and bandage application.

## Folder Structure
AnimalRescueHeroes/
- Assets/
  - Scenes/
  - Scripts/
    - Managers/
    - Animals/
    - MiniGames/
    - UI/
  - Sprites/
  - Animations/
  - Audio/
  - Prefabs/
- ProjectSettings/
- Docs/

## Unity Setup
1. Open Unity Hub and create a new 2D project named "Animal Rescue Heroes".
2. Copy the contents of `Assets/` from this folder into your Unity project's `Assets/`.
3. In Unity, create scenes in `Assets/Scenes`: `MainMenu`, `AnimalSelect`, and one per mini-game.
4. Add `GameManager` and `AudioManager` to a bootstrap scene and mark them `DontDestroyOnLoad` (already in code).
5. Wire UI buttons to load scenes and start mini-games.

## Initial Mini-Games
- Counting: tap to reach a target number.
- Shape Matching: drag shapes to slots.
- Food Sorting: drag food to the correct bowl.
- Bandage: drag a bandage to an injury.

## Next Steps
- Add sprites, audio clips, and prefabs.
- Hook up `AnimalData` assets and selection flow.
- Build touch-friendly UI with large buttons and icons.

## Quick Wiring Guide
1. Bootstrap:
  - Create an empty scene and add `GameManager` and `AudioManager` as GameObjects.
  - Add `SceneLoader` to a persistent UI canvas or a controller object.
2. Main Menu (scene name: MainMenu):
  - Canvas with a big `Play` button.
  - Add `MainMenuController` and assign the `Play` button and a `SceneLoader` reference.
  - Optional: add `UIAudioButton` to buttons for SFX.
3. Animal Select (scene name: AnimalSelect):
  - Grid/Vertical layout container.
  - Provide a `Button` prefab with `Image` + `Text` children.
  - Add `AnimalSelectController`, set `gridContainer`, `animalButtonPrefab`, `SceneLoader` and fill `animals` list with `AnimalData` assets.
4. Counting (scene name: Counting):
  - Add `CountingGame` to a controller object.
  - Hook a UI button to call `CountingGame.DropMedicine()`.
5. Shape Matching (scene name: ShapeMatching):
  - Create target slots with `DropTarget` + `ShapeSlotTarget`.
  - Set `DropTarget.requiredTag` as needed; make draggable shapes with `DraggableItem` and matching tag.
6. Food Sorting (scene name: FoodSorting):
  - Bowls: `DropTarget` + `FoodBowlTarget` and `requiredTag` per food type.
  - Food items: `DraggableItem` with appropriate tag.
7. Bandage (scene name: Bandage):
  - Injury area: `DropTarget` + `BandageTarget`.
  - Bandage UI element: `DraggableItem`.

## Build Targets
- Tablet resolution baseline: 1024x768.
- Test on multiple aspect ratios.
