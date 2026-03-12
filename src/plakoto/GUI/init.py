import os
os.environ["PYGAME_HIDE_SUPPORT_PROMPT"] = "1"
import pygame
from .constantes import *

# ------------------------------ #
# INITIALISATION
# ------------------------------ #

def init_pygame():
    pygame.init()
    screen = pygame.display.set_mode((1200, 600))
    pygame.display.set_caption('Plakoto')
    clock = pygame.time.Clock()
    return screen, clock


def create_layout():
    layout = {}

    layout["plateau_x"], layout["plateau_y"] = 40, 40
    layout["H"] = 400
    layout["W"] = 600
    layout["r"] = layout["W"] / 30
    layout["h"] = layout["H"] / 16

    layout["sous_pla1_x"] = layout["plateau_x"] + 2 * layout["r"]
    layout["sous_pla1_y"] = layout["plateau_y"] + layout["h"]
    layout["sous_pla2_x"] = layout["plateau_x"] + 16 * layout["r"]
    layout["sous_pla2_y"] = layout["plateau_y"] + layout["h"]

    layout["infos_x"], layout["infos_y"] = 680, 40
    layout["infos_H"] = 12 * layout["h"]
    layout["infos_W"] = 24 * layout["r"]
    layout["sous_infos_x"] = layout["infos_x"]
    layout["sous_infos_y"] = layout["infos_y"] + layout["infos_H"] / 3

    return layout


def create_fonts(h):
    fonts = {
        "font_24": pygame.font.Font(None, int(1.2 * h)),
        "font_infos": pygame.font.Font(None, int(1.8 * h)),
        "font_lance": pygame.font.Font(None, int(1.5 * h)),
    }
    return fonts


def create_surfaces(layout):
    background = pygame.Surface((1200, 600))
    background.fill('grey17')

    plateau = pygame.Surface((layout["W"], layout["H"]))
    plateau.fill(COLOR_01)

    sous_pla1 = pygame.Surface((12 * layout["r"], 14 * layout["h"]))
    sous_pla2 = pygame.Surface((12 * layout["r"], 14 * layout["h"]))
    sous_pla1.fill(COLOR_02)
    sous_pla2.fill(COLOR_02)

    infos = pygame.Surface((layout["infos_W"], layout["infos_H"]))
    infos.fill(COLOR_05)

    sous_infos = pygame.Surface((layout["infos_W"], layout["infos_H"] / 3))
    sous_infos.fill(COLOR_06)

    return {
        "background": background,
        "plateau_surface": plateau,
        "sous_pla1": sous_pla1,
        "sous_pla2": sous_pla2,
        "infos": infos,
        "sous_infos": sous_infos,
    }


def create_rect_pions(layout):
    rect_pions = {}
    r = layout["r"]
    h = layout["h"]
    x1, y1 = layout["sous_pla1_x"], layout["sous_pla1_y"]
    x2, y2 = layout["sous_pla2_x"], layout["sous_pla2_y"]

    for i in range(24):
        if 0 <= i <= 5:
            rect_pions[i] = {j: (x2 + 12 * r - (i + 1) * 2 * r, y2 + j * h, 2 * r, h) for j in range(6)}
        elif 6 <= i <= 11:
            rect_pions[i] = {j: (x1 + 12 * r - (i - 6 + 1) * 2 * r, y1 + j * h, 2 * r, h) for j in range(6)}
        elif 12 <= i <= 17:
            rect_pions[i] = {j: (x1 + (i - 12) * 2 * r, y1 + 14 * h - (j + 1) * h, 2 * r, h) for j in range(6)}
        else:
            rect_pions[i] = {j: (x2 + (i - 18) * 2 * r, y2 + 14 * h - (j + 1) * h, 2 * r, h) for j in range(6)}

    return rect_pions


def create_rect_cases(layout):
    rect_cases = {}
    r = layout["r"]
    h = layout["h"]
    x1, y1 = layout["sous_pla1_x"], layout["sous_pla1_y"]
    x2, y2 = layout["sous_pla2_x"], layout["sous_pla2_y"]

    for i in range(24):
        if 0 <= i <= 5:
            rect_cases[i] = (x2 + 12 * r - (i + 1) * 2 * r, y2, 2 * r, 6 * h)
        elif 6 <= i <= 11:
            rect_cases[i] = (x1 + 12 * r - (i - 6 + 1) * 2 * r, y1, 2 * r, 6 * h)
        elif 12 <= i <= 17:
            rect_cases[i] = (x1 + (i - 12) * 2 * r, y1 + 8 * h, 2 * r, 6 * h)
        else:
            rect_cases[i] = (x2 + (i - 18) * 2 * r, y2 + 8 * h, 2 * r, 6 * h)

    return rect_cases
