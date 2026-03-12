import os
os.environ["PYGAME_HIDE_SUPPORT_PROMPT"] = "1"
import pygame
from sys import exit

from ..GUI.constantes import *
from ..GUI.init import *
from ..GUI.dessin import *
from ..GUI.affichage import *
from ..GUI.events import *
from ..GUI.logi import *


class GraphicalInterface:
    def __init__(self):
        self.screen, self.clock = init_pygame()

        self.layout = create_layout()
        self.fonts = create_fonts(self.layout["h"])
        self.surfaces = create_surfaces(self.layout)
        self.rect_pions = create_rect_pions(self.layout)
        self.rect_cases = create_rect_cases(self.layout)

        (
            self.background,
            self.rect_lance,
            self.rect_star1,
            self.rect_star2,
        ) = build_background(self.layout, self.surfaces, self.fonts)

        self.reset_game()

    def reset_game(self):
        self.dice = []
        self.ori_dest = []
        self.plateau = init_plateau()
        self.winner = []
        self.current_player, self.msg = determiner_premier_joueur()

    def handle_quit(self):
        pygame.quit()
        exit()

    def handle_mouse_click(self, pos_mouse):
        if self.dice == [] and click_lance(pos_mouse, self.layout):
            self.dice = lance_de()

        clicked_case = get_indice_case(
            pos_mouse,
            self.rect_cases,
            self.rect_star1,
            self.rect_star2
        )

        if clicked_case is not None:
            self.ori_dest.append(clicked_case)

        if len(self.ori_dest) == 2:
            origine, destination = self.ori_dest
            self.ori_dest = []

            continuer, move_executed, self.dice, self.msg = gestion_deplacement(
                origine,
                destination,
                self.plateau,
                self.current_player,
                self.dice
            )

            if check_victoire(self.plateau, self.current_player):
                self.winner.append(self.current_player)

            if not continuer:
                return

            if move_executed:
                self.current_player, self.dice, new_winner, self.msg = update_turn_after_move(
                    self.plateau,
                    self.current_player,
                    self.dice
                )
                if new_winner:
                    self.winner = new_winner

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.handle_quit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                pos_mouse = pygame.mouse.get_pos()
                self.handle_mouse_click(pos_mouse)

    def render(self):
        if self.winner:
            self.msg = f"Le joueur {self.winner[0]} a gagné !"

        render_game(
            self.screen,
            self.background,
            self.plateau,
            self.dice,
            self.msg,
            self.rect_pions,
            self.fonts,
            self.layout
        )

        pygame.display.update()

    def run(self):
        while True:
            self.handle_events()
            self.render()
            self.clock.tick(60)