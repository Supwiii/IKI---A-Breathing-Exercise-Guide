import pygame
import sys

from config import *
from home import create_buttons, BackButton, draw_home
from modes import BreathingController
from bg import draw_bg_gradient, draw_mode_decor, draw_radial_spotlight
from music import (
    MUSIC_END_EVENT,
    music_play,
    music_restart,
    music_stop,
)

def main():
    pygame.init()
    pygame.mixer.init(frequency=44100, size=-16, channels=2, buffer=512)

    music_volume = 1.0

    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("IKI")
    clock = pygame.time.Clock()

    buttons = create_buttons()
    back_button = BackButton()
    current_mode = None
    controller = None

    running = True
    while running:
        dt = clock.tick(FPS) / 1000.0
        mouse = pygame.mouse.get_pos()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            elif event.type == MUSIC_END_EVENT:
                if current_mode is not None:
                    music_restart()

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    if current_mode is not None:
                        current_mode = None
                        controller = None
                        music_stop()
                    else:
                        running = False

                elif event.key in [pygame.K_1, pygame.K_2, pygame.K_3, pygame.K_4]:
                    mode = event.key - pygame.K_0
                    current_mode = mode
                    controller = BreathingController(mode)
                    music_play(current_mode, music_volume)

            elif current_mode is None:
                for btn in buttons:
                    if btn.clicked(event):
                        current_mode = btn.mode_index
                        controller = BreathingController(current_mode)
                        music_play(current_mode, music_volume)

            else:
                if back_button.clicked(event):
                    current_mode = None
                    controller = None
                    music_stop()

       
        if current_mode is None:
            draw_home(screen, mouse, dt, buttons)
        else:
            draw_bg_gradient(screen, controller.colors["bg"])
            draw_mode_decor(screen, controller.colors, pygame.time.get_ticks() / 1000.0)

            title_font = pygame.font.SysFont("arial", 32, bold=True)
            title = title_font.render(PATTERN_NAMES[current_mode], True, controller.colors["text"])
            screen.blit(title, (WIDTH // 2 - title.get_width() // 2, 40))

            controller.update(dt)

            draw_radial_spotlight(
                screen,
                (WIDTH // 2, HEIGHT // 2),
                controller.colors["aura"],
                int(controller.radius) + 20,
            )

            controller.draw(screen)

            back_button.update(mouse, dt)
            back_button.draw(screen, controller.colors["text"])

        pygame.display.flip()

    music_stop()
    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()