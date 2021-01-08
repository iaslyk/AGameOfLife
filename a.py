from sys import exit
import pygame
from pygame.constants import MOUSEBUTTONUP
import pygame.freetype
from pygame.sprite import Sprite
from pygame.rect import Rect
from enum import Enum


# Screen definitions and starting postions for some shapes
x_size = 150
y_size = 120
cell_size = 7
x_start = 3
y_start = 3

# Color definitions
color_about_to_die = (179, 179, 255)
color_alive = (255, 255, 255)
color_background = (0, 0, 0)
color_grid = (30, 30, 60)

def create_surface_with_text(text, font_size, text_rgb, bg_rgb):
    """ Returns surface with text written on """
    font = pygame.freetype.SysFont("Courier", font_size, bold=True)
    surface, _ = font.render(text=text, fgcolor=text_rgb, bgcolor=bg_rgb)
    return surface.convert_alpha()

class UIElement(Sprite):
    

    def __init__(self, center_position, text, font_size, bg_rgb, text_rgb, action=None):

        self.mouse_over = False  # indicates if the mouse is over the element

        # create the default image
        default_image = create_surface_with_text(
            text=text, font_size=font_size, text_rgb=text_rgb, bg_rgb=bg_rgb
        )

        # create the image that shows when mouse is over the element
        highlighted_image = create_surface_with_text(
            text=text, font_size=font_size * 1.2, text_rgb=text_rgb, bg_rgb=bg_rgb
        )

        # add both images and their rects to lists
        self.images = [default_image, highlighted_image]
        self.rects = [
            default_image.get_rect(center=center_position),
            highlighted_image.get_rect(center=center_position),
        ]

        # calls the init method of the parent sprite class
        super().__init__() 
        self.action = action
    
    @property
    def image(self):
        return self.images[1] if self.mouse_over else self.images[0]

    @property
    def rect(self):
        return self.rects[1] if self.mouse_over else self.rects[0]
    def update_mouse(self, mouse_pos, mouse_up):
        if self.rect.collidepoint(mouse_pos):
            self.mouse_over = True
            if mouse_up:
                return self.action
        else:
            self.mouse_over = False

    def draw(self, surface):
    # Draws element onto a surface
        surface.blit(self.image, self.rect)

class GameState(Enum):
    QUIT = -1
    TITLE = 0
    NEWGAME = 1

def title_screen(screen):
    start_btn = UIElement(
        center_position = (550, 700),
        font_size = 20,
        bg_rgb = color_grid,
        text_rgb = color_alive,
        text = "Start",
        action = GameState.NEWGAME,
    )
    quit_btn = UIElement(
        center_position = (550, 700),
        font_size = 20,
        bg_rgb = color_grid,
        text_rgb = color_alive,
        text = "Quit",
        action = GameState.QUIT,
    )
    buttons = [start_btn, quit_btn]

    while True:
        mouse_up = False
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                mouse_up = True
        screen.fill(color_grid)

        for button in buttons:
            ui_action = button.update(pygame.mouse.get_pos(), mouse_up)
            if ui_action is not None:
                return ui_action
            button.draw(surface)

        pygame.display.update()

def play_level(screen):
    return_btn = UIElement(
        center_position=(140, 570),
        font_size=20,
        bg_rgb=color_grid,
        text_rgb=color_alive,
        text="Return to main menu",
        action=GameState.TITLE,
    )

    while True:
        mouse_up = False
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                mouse_up = True
        screen.fill(color_grid)

        ui_action = return_btn.update(pygame.mouse.get_pos(), mouse_up)
        if ui_action is not None:
            return ui_action
        return_btn.draw(surface)

        pygame.display.flip()

        
def main(dimx, dimy, cellsize):
    pygame.init()
    surface = pygame.display.set_mode((dimx * cellsize, dimy * cellsize))
    pygame.display.set_caption("A Game of Life")

    game_state = GameState.TITLE
    
    while True:
        if game_state == GameState.TITLE:
            game_state = title_screen(surface)
        if game_state == GameState.NEWGAME:
            game_state = play_level(surface)
        if game_state == GameState.QUIT:
            pygame.quit() 
            exit()

if __name__ == "__main__":
    main(x_size, y_size, cell_size)