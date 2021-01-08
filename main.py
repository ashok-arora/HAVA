import pygame
import pygame_menu
from asteroid_deflector import start_asteroid_deflector
from game_2048 import start_2048
from dx_ball_lite import start_dx_ball_lite
from air_hockey import start_air_hockey

pygame.init()
surface = pygame.display.set_mode((600, 400))
pygame.display.set_caption('Game World')
game_selected_to_play = 0

font = pygame_menu.font.FONT_MUNRO

mytheme = pygame_menu.themes.Theme(background_color=(
    0, 0, 0, 0), title_shadow=True, title_background_color=(187, 0, 0), widget_font=font, title_font=font)


def set_game(_, value):
    global game_selected_to_play
    game_selected_to_play = value


def start_the_game():
    if game_selected_to_play == 0:
        start_asteroid_deflector()
    elif game_selected_to_play == 1:
        start_2048()
    elif game_selected_to_play == 2:
        start_dx_ball_lite()
    elif game_selected_to_play == 3:
        start_air_hockey()


menu = pygame_menu.Menu(
    width=600,
    height=400,
    title='Game World',
    theme=mytheme
)

menu.add_selector('', [('Asteroid Deflector', 0), ('2048', 1),
                       ('DX Ball Lite', 2), ('Air Hockey', 3)], onchange=set_game)
menu.add_button('LET\'S PLAY!', start_the_game)
menu.add_button('Quit', pygame_menu.events.EXIT)


if __name__ == '__main__':
    menu.mainloop(surface)
