import os
os.environ["PYGAME_HIDE_SUPPORT_PROMPT"] = "1"
import pygame
from .constantes import *

# ------------------------------ #
# AFFICHAGE DYNAMIQUE
# ------------------------------ #

def afficher_pions(screen, plateau, rect_pions, fonts, layout):
    for i in range(24):
        count = len(plateau[i]) if isinstance(plateau[i], list) else 0
        max_display = min(count, 6)

        for j in range(max_display):
            color = COLOR_PION_B if plateau[i][j] == 'B' else COLOR_PION_N
            pygame.draw.ellipse(screen, color, rect_pions[i][j])

    font_infos = fonts["font_infos"]
    infos_x, infos_y = layout["infos_x"], layout["infos_y"]
    r, h = layout["r"], layout["h"]

    nb_B = font_infos.render(str(plateau["off_B"]), False, COLOR_07)
    nb_N = font_infos.render(str(plateau["off_N"]), False, COLOR_07)

    rect_nb_B = nb_B.get_rect(midbottom=(infos_x + 10 * r, infos_y + 6 * h))
    rect_nb_N = nb_N.get_rect(midbottom=(infos_x + 10 * r, infos_y + 8 * h))

    screen.blit(nb_B, rect_nb_B)
    screen.blit(nb_N, rect_nb_N)


def afficher_de(screen, dice, fonts, layout):
    font_infos = fonts["font_infos"]
    infos_x, infos_y = layout["infos_x"], layout["infos_y"]
    r, h = layout["r"], layout["h"]

    if dice:
        s = "  ".join(str(d) for d in dice)
        txt = font_infos.render(s, False, COLOR_07)
    else:
        txt = font_infos.render("Click 'lance' !", False, COLOR_07)

    txt_rect = txt.get_rect(midbottom=(infos_x + 16 * r, infos_y + 4 * h))
    screen.blit(txt, txt_rect)


def afficher_message(screen, message, fonts, layout):
    font_lance = fonts["font_lance"]
    infos_x, infos_y = layout["infos_x"], layout["infos_y"]
    r, h = layout["r"], layout["h"]

    msg = font_lance.render(message, False, 'darkblue')
    msg_rect = msg.get_rect(midbottom=(infos_x + 12 * r, infos_y + 10.5 * h))
    screen.blit(msg, msg_rect)


def render_game(screen, background, plateau, dice, msg, rect_pions, fonts, layout):
    screen.blit(background, (0, 0))
    afficher_de(screen, dice, fonts, layout)
    afficher_message(screen, msg, fonts, layout)
    afficher_pions(screen, plateau, rect_pions, fonts, layout)

