# Projectile System Implementation

## Overview
Implemented an encapsulated projectile hierarchy with two specialized projectile types: **Meteorites** and **Supply Boxes**. The system uses configuration objects for easy tweaking.

## Architecture

### ProjectileConfig (Encapsulation)
Centralized configuration class that makes projectile properties tweakable:
```python
ProjectileConfig(
    symbol,               # Display character
    speed,                # Pixels per move
    delay,                # Seconds between moves
    size,                 # 'small', 'medium', 'large'
    collision_damage,     # Damage on collision
    refuel_amount         # Fuel restored (if any)
)
```

### Base Projectile Class
- Accepts a `ProjectileConfig` object
- Handles movement with frame-rate independent timing
- Provides collision detection framework via `on_collision()` method
- Properties proxy to config for clean attribute access

### Meteorite (Subclass)
**Characteristics:**
- **Symbol:** ● (Large circle)
- **Speed:** 2 pixels/move (2x faster than default)
- **Delay:** 0.08s (faster movement interval)
- **Size:** Large
- **Damage:** 50 HP (instant kill)
- **Collision Effect:** Sets player fuel to 0 → Game Over

### SupplyBox (Subclass)
**Characteristics:**
- **Symbol:** □ (Small square)
- **Speed:** 0.5 pixels/move (0.5x slower)
- **Delay:** 0.15s (slower movement interval)
- **Size:** Small
- **Damage:** 0 (non-damaging)
- **Collision Effect:** Restores 200 fuel (capped at max_fuel)

## Game Logic Integration

### Projectile Spawning
- Modified `obstacle_gen()` to randomly spawn projectile types
- **70% chance:** Meteorite
- **30% chance:** SupplyBox
- Adds strategic element (dodging vs. collecting)

### Projectile Management
- `_update_projectiles()`: 
  - Moves all active projectiles
  - Removes inactive projectiles
  - Detects collisions with player
  - Triggers `on_collision()` callbacks

- `_update_render_state()`:
  - Converts projectile positions to render format
  - Only includes active projectiles

### Collision System
- Collision occurs when projectile reaches player's Y position AND X matches player position
- Player-specific collision handling via polymorphic `on_collision()` method
- Projectile is removed after collision

## Extensibility

To add new projectile types (e.g., Asteroid, LaserShell):

```python
class NewProjectile(Projectile):
    _config = ProjectileConfig(
        symbol='X',
        speed=1.5,
        delay=0.1,
        size='medium',
        collision_damage=25,
        refuel_amount=0
    )
    
    def __init__(self, x, y=0):
        super().__init__(x, y, self._config)
    
    def on_collision(self, player):
        # Custom collision logic
        pass
```

Then update the spawn weights in `obstacle_gen()`:
```python
random.choices(
    [Meteorite, SupplyBox, NewProjectile],
    weights=[60, 25, 15],
    k=1
)
```

## Configuration Tweaking Points

All easily adjustable parameters:

| Aspect | Location | Parameters |
|--------|----------|-----------|
| **Spawn Frequency** | `obs_interval` in Player | 0.6s (change for faster/slower spawning) |
| **Type Distribution** | `obstacle_gen()` | weights=[70, 30] (meteorite/supply ratio) |
| **Meteorite Stats** | `Meteorite._config` | speed, delay, collision_damage |
| **SupplyBox Stats** | `SupplyBox._config` | speed, delay, refuel_amount |
| **Max Fuel** | `Player.max_fuel` | 1000 (player fuel capacity) |

## Testing Checklist

- [x] Code compiles without errors
- [ ] Meteorites spawn and move correctly
- [ ] Supply boxes spawn and move correctly
- [ ] Collision detection works for both types
- [ ] Fuel restoration works for supply boxes
- [ ] Game over triggers on meteorite hit
- [ ] Projectiles render with correct symbols (● and □)
