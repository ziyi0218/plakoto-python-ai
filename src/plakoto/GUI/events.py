# ------------------------------ #
# INPUT / CLIC
# ------------------------------ #

def is_in_rect(pos, rect):
    x, y = pos
    rect_x, rect_y, width, height = rect
    return rect_x <= x <= (rect_x + width) and rect_y <= y <= (rect_y + height)


def click_lance(pos, layout):
    x, y = pos
    infos_x, infos_y = layout["infos_x"], layout["infos_y"]
    r, h = layout["r"], layout["h"]
    return (infos_x + 2 * r) <= x <= (infos_x + 6 * r) and (infos_y + h) <= y <= (infos_y + 3 * h)


def get_indice_case(pos, rect_cases, rect_star1, rect_star2):
    if is_in_rect(pos, rect_star1):
        return -1
    if is_in_rect(pos, rect_star2):
        return 24

    for i in range(24):
        if is_in_rect(pos, rect_cases[i]):
            return i
    return None
