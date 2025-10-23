import sys

# module-level rendering state (set via set_state or by assigning attributes)
coords_list = []
map_width = 0
map_height = 0
playerpos = 0

def set_state(_coords_list, _map_width, _map_height, _playerpos):
    global coords_list, map_width, map_height, playerpos
    coords_list = _coords_list
    map_width = _map_width
    map_height = _map_height
    playerpos = _playerpos

def render_rows():
    out_lines = []
    for y in range(map_height):
        row = []
        for x in range(map_width):
            if (x, y) == (playerpos, map_height - 1):
                row.append("A")
            elif coords_list and [x, y] in coords_list:
                row.append("O")
            else:
                row.append(" ")
        out_lines.append("".join(row))
    return "\n".join(out_lines)

def render_and_draw(header):
    rows_text = render_rows()
    out = "\033[H\033[J" + header + "\n" + rows_text + "\n"
    sys.stdout.write(out)
    sys.stdout.flush()
