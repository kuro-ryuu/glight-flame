import sys
# module-level rendering state (set via set_state or by assigning attributes)
projectiles = []  # List of Projectile objects for rich rendering
map_width = 0
map_height = 0
playerpos = 0

def set_state(_projectiles, _map_width, _map_height, _playerpos):
    """Set render state with projectiles for symbol-aware rendering.
    
    Args:
        _projectiles: List of Projectile objects with x, y, symbol attributes
        _map_width: Map width
        _map_height: Map height
        _playerpos: Player X position
    """
    global projectiles, map_width, map_height, playerpos
    projectiles = _projectiles
    map_width = _map_width
    map_height = _map_height
    playerpos = _playerpos

def render_rows():
    """Render game grid with projectile symbols."""
    # Build symbol map for quick lookup
    symbol_map = {}
    for p in projectiles:
        if p.active and 0 <= p.x < map_width and 0 <= p.y < map_height:
            symbol_map[(p.x, p.y)] = p.symbol
    
    out_lines = []
    for y in range(map_height):
        row = []
        for x in range(map_width):
            # Check collision at player position
            if (x, y) == (playerpos, map_height - 1) and (x, y) in symbol_map:
                return "GAME OVER"
            # Render player
            elif (x, y) == (playerpos, map_height - 1):
                row.append("A")
            # Render projectiles with their symbols
            elif (x, y) in symbol_map:
                row.append(symbol_map[(x, y)])
            else:
                row.append(" ")
        out_lines.append("".join(row))
    return "\n".join(out_lines)

def render_and_draw(header):
    rows_text = render_rows()
    out = "\033[H\033[J" + header + "\n" + rows_text + "\n"
    sys.stdout.write(out)
    sys.stdout.flush()
