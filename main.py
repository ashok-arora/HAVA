import pygame
import pygame_menu

pygame.init()
surface = pygame.display.set_mode((600, 400))
game_selected_to_play = 0

font = pygame_menu.font.FONT_MUNRO

mytheme = pygame_menu.themes.Theme(background_color=(
    0, 0, 0, 0), title_shadow=True, title_background_color=(187, 0, 0), widget_font=font, title_font=font)


def set_game(_, value):
    global game_selected_to_play
    game_selected_to_play = value


def start_the_game():
    pass


menu = pygame_menu.Menu(
    width=600,
    height=400,
    title='Game World',
    theme=mytheme
)

menu.add_selector('', [('Game 1', 0), ('Game 2', 1),
                       ('Game 3', 2), ('Game 4', 3)], onchange=set_game)
menu.add_button('LET\'S PLAY!', start_the_game)
menu.add_button('Quit', pygame_menu.events.EXIT)


if __name__ == '__main__':
    menu.mainloop(surface)
