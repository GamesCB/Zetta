import pygame
pygame.init()

# иконки и прочее

namegame = pygame.transform.scale(pygame.image.load('sprites/icons/namegame.png').convert_alpha(), (768, 210))
rightside = pygame.image.load('sprites/icons/right.png').convert_alpha()
leftside = pygame.transform.rotate(rightside, 180).convert_alpha()
endbuttonleft = pygame.image.load('sprites/icons/endbutton.png').convert_alpha()
endbuttonright = pygame.transform.rotate(endbuttonleft, 180).convert_alpha()
clock_icon = pygame.image.load('sprites/icons/clock icon.png').convert_alpha()
status_icon = pygame.image.load('sprites/icons/status icon.png').convert_alpha()
task_not_complete = pygame.image.load('sprites/other gui/task_not_complete.png').convert_alpha()
task_complete = pygame.image.load('sprites/other gui/task_complete.png').convert_alpha()

# интерьер дома

mouse_cursor = pygame.image.load('sprites/icons/mouse_cursor.png').convert_alpha()


# жд
powers_railway_down = pygame.transform.scale(pygame.image.load('sprites/street/powers_railway_down.png').convert_alpha(),
                                             (pygame.image.load('sprites/street/powers_railway_down.png').get_width() * 2,
                                              pygame.image.load('sprites/street/powers_railway_down.png').get_height() * 2))
powers_railway_top = pygame.transform.scale(pygame.image.load('sprites/street/powers_railway_top.png').convert_alpha(),
                                             (pygame.image.load('sprites/street/powers_railway_top.png').get_width() * 2,
                                              pygame.image.load('sprites/street/powers_railway_top.png').get_height() * 2))

watercastle = pygame.image.load('sprites/street/watercastle.png').convert_alpha()

double_flashlights = pygame.image.load('sprites/street/urbs/double flashstands.png').convert_alpha()
bench_right_rotated = pygame.transform.scale(
    pygame.image.load('sprites/street/urbs/bench_rotated.png'), (32, 96)
)