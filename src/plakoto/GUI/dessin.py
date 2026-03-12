import os
os.environ["PYGAME_HIDE_SUPPORT_PROMPT"] = "1"
import pygame
from .constantes import *
import math

# ------------------------------ #
# DESSIN UTILITAIRE
# ------------------------------ #

def draw_star(surface, center, outer_radius, inner_radius, color):
    x0, y0 = center
    points = []
    for i in range(10):
        angle_deg = i * 36
        angle_rad = math.radians(angle_deg)
        radius = outer_radius if i % 2 == 0 else inner_radius
        x = x0 + math.cos(angle_rad - math.pi / 2) * radius
        y = y0 + math.sin(angle_rad - math.pi / 2) * radius
        points.append((x, y))

    pygame.draw.polygon(surface, color, points)

    min_x = min(p[0] for p in points)
    max_x = max(p[0] for p in points)
    min_y = min(p[1] for p in points)
    max_y = max(p[1] for p in points)

    return pygame.Rect(min_x, min_y, max_x - min_x, max_y - min_y)


def draw_triangles(background, layout):
    r = layout["r"]
    h = layout["h"]
    x1, y1 = layout["sous_pla1_x"], layout["sous_pla1_y"]
    x2, y2 = layout["sous_pla2_x"], layout["sous_pla2_y"]

    for i in range(6):
        color = COLOR_04 if i % 2 == 0 else COLOR_03
        triangle = [(x2 + i * 2 * r, y2), (x2 + (i + 1) * 2 * r, y2), (x2 + r + i * 2 * r, y2 + 6 * h)]
        pygame.draw.polygon(background, color, triangle)

    for i in range(6):
        color = COLOR_04 if i % 2 == 0 else COLOR_03
        triangle = [(x1 + i * 2 * r, y1), (x1 + (i + 1) * 2 * r, y1), (x1 + r + i * 2 * r, y1 + 6 * h)]
        pygame.draw.polygon(background, color, triangle)

    for i in range(6):
        color = COLOR_03 if i % 2 == 0 else COLOR_04
        triangle = [(x1 + i * 2 * r, y1 + 14 * h), (x1 + (i + 1) * 2 * r, y1 + 14 * h), (x1 + r + i * 2 * r, y1 + 8 * h)]
        pygame.draw.polygon(background, color, triangle)

    for i in range(6):
        color = COLOR_03 if i % 2 == 0 else COLOR_04
        triangle = [(x2 + i * 2 * r, y2 + 14 * h), (x2 + (i + 1) * 2 * r, y2 + 14 * h), (x2 + r + i * 2 * r, y2 + 8 * h)]
        pygame.draw.polygon(background, color, triangle)


def draw_case_numbers(background, layout, fonts):
    font_24 = fonts["font_24"]
    color_24 = 'khaki1'
    r = layout["r"]
    h = layout["h"]
    x1, y1 = layout["sous_pla1_x"], layout["sous_pla1_y"]
    x2, y2 = layout["sous_pla2_x"], layout["sous_pla2_y"]

    for i in range(6):
        j = i + 1
        txt = font_24.render(str(j), True, color_24)
        txt_rect = txt.get_rect(midbottom=(x2 + 11 * r - i * 2 * r, y2))
        background.blit(txt, txt_rect)

    for i in range(6):
        j = i + 7
        txt = font_24.render(str(j), True, color_24)
        txt_rect = txt.get_rect(midbottom=(x1 + 11 * r - i * 2 * r, y1))
        background.blit(txt, txt_rect)

    for i in range(6):
        j = i + 13
        txt = font_24.render(str(j), True, color_24)
        txt_rect = txt.get_rect(midbottom=(x1 + r + i * 2 * r, y1 + 15 * h))
        background.blit(txt, txt_rect)

    for i in range(6):
        j = i + 19
        txt = font_24.render(str(j), True, color_24)
        txt_rect = txt.get_rect(midbottom=(x2 + r + i * 2 * r, y2 + 15 * h))
        background.blit(txt, txt_rect)


def draw_info_panel(background, layout, fonts):
    font_infos = fonts["font_infos"]
    font_lance = fonts["font_lance"]
    r = layout["r"]
    h = layout["h"]
    infos_x, infos_y = layout["infos_x"], layout["infos_y"]

    text01 = font_infos.render("Résultat des dés", False, 'black')
    text01_rect = text01.get_rect(midbottom=(infos_x + 16 * r, infos_y + 2 * h))
    background.blit(text01, text01_rect)

    text02 = font_infos.render("off_B :", False, 'black')
    text02_rect = text02.get_rect(midbottom=(infos_x + 4 * r, infos_y + 6 * h))
    background.blit(text02, text02_rect)

    text03 = font_infos.render("off_N :", False, 'black')
    text03_rect = text03.get_rect(midbottom=(infos_x + 4 * r, infos_y + 8 * h))
    background.blit(text03, text03_rect)

    rect_lance = (infos_x + 2 * r, infos_y + h, 4 * r, 2 * h)
    pygame.draw.rect(background, COLOR_07, rect_lance)

    text_lance = font_lance.render("lance", False, 'khaki1')
    text_lance_rect = text_lance.get_rect(midbottom=(infos_x + 4 * r, infos_y + 2.5 * h))
    background.blit(text_lance, text_lance_rect)

    return rect_lance


def build_background(layout, surfaces, fonts):
    background = surfaces["background"]

    background.blit(surfaces["plateau_surface"], (layout["plateau_x"], layout["plateau_y"]))
    background.blit(surfaces["sous_pla1"], (layout["sous_pla1_x"], layout["sous_pla1_y"]))
    background.blit(surfaces["sous_pla2"], (layout["sous_pla2_x"], layout["sous_pla2_y"]))
    background.blit(surfaces["infos"], (layout["infos_x"], layout["infos_y"]))
    background.blit(surfaces["sous_infos"], (layout["sous_infos_x"], layout["sous_infos_y"]))

    draw_triangles(background, layout)
    draw_case_numbers(background, layout, fonts)
    rect_lance = draw_info_panel(background, layout, fonts)

    rect_star1 = draw_star(
        background,
        (layout["plateau_x"] + layout["W"], layout["plateau_y"]),
        2 * layout["r"],
        layout["r"],
        COLOR_STAR
    )
    rect_star2 = draw_star(
        background,
        (layout["plateau_x"] + layout["W"], layout["plateau_y"] + layout["H"]),
        2 * layout["r"],
        layout["r"],
        COLOR_STAR
    )

    return background, rect_lance, rect_star1, rect_star2
