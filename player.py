import json

import pygame
from engine import *
from textures import *
pygame.init()

from pygame.locals import *

''' класс для камеры '''
class Camera():
    def __init__(self):
        self.scroll = [0, 0]
        self.texture = pygame.image.load('sprites/characters/main/idle.png').convert_alpha()
        self.player_rect = pygame.rect.Rect(100, 320, self.texture.get_width(), 1)

    def move_camera(self):
        true_scroll[0] += (self.player_rect.x - true_scroll[0] + 75 - (SIZE[0] / 2)) // CAMERA_SPEED_DIVISION
        true_scroll[1] += (self.player_rect.y - true_scroll[1] - (SIZE[1] / 2)) // CAMERA_SPEED_DIVISION
        self.scroll = true_scroll.copy()
        self.scroll[0] = int(self.scroll[0])
        self.scroll[1] = int(self.scroll[1])

''' класс для столкновений '''
class Collider(Camera):
    def __init__(self):
        super(Collider, self).__init__()

        self.hitboxes = [
            # train station
            Rect(3640, 1410, 24, 2850),
            Rect(3652, 1410 + 2850, 24, 100),
            Rect(4340, 1410, 10, 2850),
            Rect(4328, 1410 + 2850, 24, 100),
            Rect(3476, 4335, 1000, 200),
            Rect(3664, 3900, 240, 115 + 22),
            Rect(4100, 3900, 240, 115 + 22),
            Rect(4270, 4155, 48, 101),


            # flashlights
            Rect(3664, 4174 - 45, 48, 20),
            # Rect(4306, 3845, 48, 30),
            Rect(3664, 3514, 48, 20),
            # Rect(4306, 3175, 48, 30),
            Rect(3664, 2854, 48, 20),



        ]

''' класс игрока '''
class Player(Collider):
    def __init__(self, save):
        super(Player, self).__init__()
        self.speed = 8  # normal speed

        with open(f'data/{save}/clothes.json') as clothesfile:
            self.clothesfile = json.load(clothesfile)

        ''' подгрузка одежды и анимаций персонажа '''

        self.update_loading_clothes(self.clothesfile)

        ''' конец загрузки одежды и анимаций '''

        self.front_bool = True
        self.back_bool = False
        self.right_bool = False
        self.left_bool = False

        self.you_can_move = True
        self.visible = True


        # self.key = pygame.key.get_pressed()
        #
        # self.ivents = {
        #     self.key[pygame.K_w]: self.front_walk_func,
        #     self.key[pygame.K_a]: self.left_walk_func,
        #     self.key[pygame.K_d]: self.right_walk_func,
        #     self.key[pygame.K_s]: self.back_walk_func
        # }

        self.shadow = pygame.image.load('sprites/characters/flat/shadow.png').convert_alpha()



    def render(self):
        self.key = pygame.key.get_pressed()
        self.move_camera()
        self.player_movement = [0, 0]
        self.mouse = pygame.mouse.get_pos()




        if self.you_can_move:

            # self.ivents.update()
            #
            # if any(self.ivents):
            #     self.ivents[True]()

            # window.blit(self.shadow, (self.player_rect.x + 34 - scroll[0], self.player_rect.y + 64 + 12 - scroll[1]))

            if self.key[pygame.K_w]:

                self.front_walk_func()

            elif self.key[pygame.K_s]:

                self.back_walk_func()

            elif self.key[pygame.K_a]:

                self.left_walk_func()

            elif self.key[pygame.K_d]:

                self.right_walk_func()


            else:
                if self.visible:
                    if self.back_bool:
                        self.stand_back.show_anim(self.player_rect.x, self.player_rect.y)

                        self.hear_stay_front.show_anim(self.player_rect.x, self.player_rect.y)
                        self.clothes_stay_front.show_anim(self.player_rect.x, self.player_rect.y)
                        self.pants_stay_front.show_anim(self.player_rect.x, self.player_rect.y)

                    elif self.front_bool:
                        self.stand_front.show_anim(self.player_rect.x, self.player_rect.y)

                        self.hear_stay_back.show_anim(self.player_rect.x, self.player_rect.y)
                        self.clothes_stay_back.show_anim(self.player_rect.x, self.player_rect.y)
                        self.pants_stay_back.show_anim(self.player_rect.x, self.player_rect.y)

                    elif self.right_bool:
                        self.stand_right.show_anim(self.player_rect.x, self.player_rect.y)

                        self.hear_stay_right.show_anim(self.player_rect.x, self.player_rect.y)
                        self.clothes_stay_right.show_anim(self.player_rect.x, self.player_rect.y)
                        self.pants_stay_right.show_anim(self.player_rect.x, self.player_rect.y)

                    elif self.left_bool:
                        self.stand_left.show_anim(self.player_rect.x, self.player_rect.y)

                        self.hear_stay_left.show_anim(self.player_rect.x, self.player_rect.y)
                        self.clothes_stay_left.show_anim(self.player_rect.x, self.player_rect.y)
                        self.pants_stay_left.show_anim(self.player_rect.x, self.player_rect.y)

        else:
            if self.visible:

                # window.blit(self.shadow, (self.player_rect.x + 34 - scroll[0], self.player_rect.y + 64 + 12 - scroll[1]))

                if self.back_bool:
                    self.stand_back.show_anim(self.player_rect.x, self.player_rect.y)

                    self.hear_stay_front.show_anim(self.player_rect.x, self.player_rect.y)
                    self.clothes_stay_front.show_anim(self.player_rect.x, self.player_rect.y)
                    self.pants_stay_front.show_anim(self.player_rect.x, self.player_rect.y)

                elif self.front_bool:
                    self.stand_front.show_anim(self.player_rect.x, self.player_rect.y)

                    self.hear_stay_back.show_anim(self.player_rect.x, self.player_rect.y)
                    self.clothes_stay_back.show_anim(self.player_rect.x, self.player_rect.y)
                    self.pants_stay_back.show_anim(self.player_rect.x, self.player_rect.y)

                elif self.right_bool:
                    self.stand_right.show_anim(self.player_rect.x, self.player_rect.y)

                    self.hear_stay_right.show_anim(self.player_rect.x, self.player_rect.y)
                    self.clothes_stay_right.show_anim(self.player_rect.x, self.player_rect.y)
                    self.pants_stay_right.show_anim(self.player_rect.x, self.player_rect.y)

                elif self.left_bool:
                    self.stand_left.show_anim(self.player_rect.x, self.player_rect.y)

                    self.hear_stay_left.show_anim(self.player_rect.x, self.player_rect.y)
                    self.clothes_stay_left.show_anim(self.player_rect.x, self.player_rect.y)
                    self.pants_stay_left.show_anim(self.player_rect.x, self.player_rect.y)


        self.player_rect, self.collision = self.move(self.player_rect, self.player_movement, self.hitboxes)

    def get_collider_location(self, location):
        if location == 'train':
            self.hitboxes = [
            # train station
            Rect(3640, 1410, 24, 2850),
            Rect(3652, 1410 + 2850, 24, 100),
            Rect(4340, 1410, 10, 2850),
            Rect(4328, 1410 + 2850, 24, 100),
            Rect(3476, 4335, 1000, 200),
            Rect(3664, 3900, 240, 115 + 22),
            Rect(4100, 3900, 240, 115 + 22),
            Rect(4270, 4155, 48, 101),


            # flashlights
            Rect(3664, 4174 - 45, 48, 20),
            # Rect(4306, 3845, 48, 30),
            Rect(3664, 3514, 48, 20),
            # Rect(4306, 3175, 48, 30),
            Rect(3664, 2854, 48, 20),

        ]
        elif location == 'zetta':
            self.hitboxes = [
                Rect(274, 3800, 380, 1000),
                Rect(626, 4758, 1000, 10),
                # отель
                Rect(1414 - 52, 3597, 635, 220),
                # бар эксклюз
                Rect(2245, 3585 - 64, 650, 300 - 20),
                Rect(2245, 3801, 155, 20),
                # кафе ху
                Rect(1398 - 28, 2293, 470, 1400),
                Rect(1330, 2741, 50, 160),
                Rect(1295, 2718, 100, 30),
                # заборы за баром
                Rect(2270, 2461, 20, 1100),
                Rect(2270, 2461, 274, 40),
                Rect(2270 + 315, 2461, 128, 40),
                Rect(1920, 2204, 40, 1500),
                Rect(1930, 2000, 555, 210),
                Rect(1390 - 32, 1950, 420 + 32, 74),
                Rect(1794, 2000, 150, 24),
                Rect(1286, 2047 - 50, 45, 15)

            ]
    def __collision_test(self, rect, tiles) -> list:
        hitbox = []
        for tile in tiles:
            if rect.colliderect(tile):
                hitbox.append(tile)
        return hitbox

    def move(self, rect, collision_cords,
             tiles):  # rect --> pygame.Rect(), collision_cords --> list, tiles --> list(hitboxes)
        collision_types = {
            'top': False,
            'bottom': False,
            'right': False,
            'left': False
        }
        rect.x += collision_cords[0]
        hitbox = self.__collision_test(rect, tiles)
        for hits in hitbox:
            if collision_cords[0] > 0:
                rect.right = hits.left
                collision_types['left'] = True
            if collision_cords[0] < 0:
                rect.left = hits.right
                collision_types['right'] = True
        rect.y += collision_cords[1]
        hitbox = self.__collision_test(rect, tiles)
        for hits in hitbox:
            if collision_cords[1] > 0:
                rect.bottom = hits.top
                collision_types['top'] = True
            if collision_cords[1] < 0:
                rect.top = hits.bottom
                collision_types['bottom'] = True
        return rect, collision_types

    def update_loading_clothes(self, file_clothes):

        self.stand_front = Animation(
            [pygame.transform.scale(pygame.image.load(f'sprites/characters/flat/stay/back/{i}.png').convert_alpha(),
                                    (96, 96)) for i in range(1, 3)], 15
        )
        self.stand_back = Animation(
            [pygame.transform.scale(pygame.image.load(f'sprites/characters/flat/stay/front/{i}.png').convert_alpha(),
                                    (96, 96)) for i in range(1, 3)], 15
        )
        self.stand_right = Animation(
            [pygame.transform.scale(pygame.image.load(f'sprites/characters/flat/stay/right/{i}.png').convert_alpha(),
                                    (96, 96)) for i in range(1, 3)], 15
        )
        self.stand_left = Animation(
            [pygame.transform.scale(pygame.image.load(f'sprites/characters/flat/stay/left/{i}.png').convert_alpha(),
                                    (96, 96)) for i in range(1, 3)], 15
        )

        # ходьба
        self.walk_front = Animation(
            [pygame.transform.scale(pygame.image.load(f'sprites/characters/flat/walk/back/{i}.png').convert_alpha(),
                                    (96, 96)) for i in range(1, 9)], 4
        )

        self.walk_back = Animation(
            [pygame.transform.scale(pygame.image.load(f'sprites/characters/flat/walk/front/{i}.png').convert_alpha(),
                                    (96, 96)) for i in range(1, 9)], 4
        )

        self.walk_right = Animation(
            [pygame.transform.scale(pygame.image.load(f'sprites/characters/flat/walk/right/{i}.png').convert_alpha(),
                                    (96, 96)) for i in range(1, 9)], 4
        )

        self.walk_left = Animation(
            [pygame.transform.scale(pygame.image.load(f'sprites/characters/flat/walk/left/{i}.png').convert_alpha(),
                                    (96, 96)) for i in range(1, 9)], 4
        )

        self.hear_stay_back = Animation(
            [pygame.transform.scale(pygame.image.load(f'sprites/clothes/1/{file_clothes["1"]}/stay/back/{i}.png'),
                                    (96, 96)).convert_alpha() for i in range(1, 3)], 15
        )
        self.hear_stay_left = Animation(
            [pygame.transform.scale(pygame.image.load(f'sprites/clothes/1/{file_clothes["1"]}/stay/left/{i}.png'),
                                    (96, 96)).convert_alpha() for i in range(1, 3)], 15
        )
        self.hear_stay_right = Animation(
            [pygame.transform.scale(pygame.image.load(f'sprites/clothes/1/{file_clothes["1"]}/stay/right/{i}.png'),
                                    (96, 96)).convert_alpha() for i in range(1, 3)], 15
        )
        self.hear_stay_front = Animation(
            [pygame.transform.scale(pygame.image.load(f'sprites/clothes/1/{file_clothes["1"]}/stay/front/{i}.png'),
                                    (96, 96)).convert_alpha() for i in range(1, 3)], 15
        )

        self.hear_walk_left = Animation(
            [pygame.transform.scale(pygame.image.load(f'sprites/clothes/1/{file_clothes["1"]}/walk/left/{i}.png'),
                                    (96, 96)).convert_alpha() for i in range(1, 9)], 4
        )
        self.hear_walk_front = Animation(
            [pygame.transform.scale(pygame.image.load(f'sprites/clothes/1/{file_clothes["1"]}/walk/front/{i}.png'),
                                    (96, 96)).convert_alpha() for i in range(1, 9)], 4
        )
        self.hear_walk_back = Animation(
            [pygame.transform.scale(pygame.image.load(f'sprites/clothes/1/{file_clothes["1"]}/walk/back/{i}.png'),
                                    (96, 96)).convert_alpha() for i in range(1, 9)], 4
        )
        self.hear_walk_right = Animation(
            [pygame.transform.scale(pygame.image.load(f'sprites/clothes/1/{file_clothes["1"]}/walk/right/{i}.png'),
                                    (96, 96)).convert_alpha() for i in range(1, 9)], 4
        )

        self.clothes_stay_back = Animation(
            [pygame.transform.scale(pygame.image.load(f'sprites/clothes/2/{file_clothes["2"]}/stay/back/{i}.png'),
                                    (96, 96)).convert_alpha() for i in range(1, 3)], 15
        )
        self.clothes_stay_front = Animation(
            [pygame.transform.scale(pygame.image.load(f'sprites/clothes/2/{file_clothes["2"]}/stay/front/{i}.png'),
                                    (96, 96)).convert_alpha() for i in range(1, 3)], 15
        )
        self.clothes_stay_left = Animation(
            [pygame.transform.scale(pygame.image.load(f'sprites/clothes/2/{file_clothes["2"]}/stay/left/{i}.png'),
                                    (96, 96)).convert_alpha() for i in range(1, 3)], 15
        )
        self.clothes_stay_right = Animation(
            [pygame.transform.scale(pygame.image.load(f'sprites/clothes/2/{file_clothes["2"]}/stay/right/{i}.png'),
                                    (96, 96)).convert_alpha() for i in range(1, 3)], 15
        )

        self.clothes_walk_back = Animation(
            [pygame.transform.scale(pygame.image.load(f'sprites/clothes/2/{file_clothes["2"]}/walk/back/{i}.png'),
                                    (96, 96)).convert_alpha() for i in range(1, 9)], 4
        )
        self.clothes_walk_left = Animation(
            [pygame.transform.scale(pygame.image.load(f'sprites/clothes/2/{file_clothes["2"]}/walk/left/{i}.png'),
                                    (96, 96)).convert_alpha() for i in range(1, 9)], 4
        )
        self.clothes_walk_right = Animation(
            [pygame.transform.scale(pygame.image.load(f'sprites/clothes/2/{file_clothes["2"]}/walk/right/{i}.png'),
                                    (96, 96)).convert_alpha() for i in range(1, 9)], 4
        )
        self.clothes_walk_front = Animation(
            [pygame.transform.scale(pygame.image.load(f'sprites/clothes/2/{file_clothes["2"]}/walk/front/{i}.png'),
                                    (96, 96)).convert_alpha() for i in range(1, 9)], 4
        )

        self.pants_stay_back = Animation(
            [pygame.transform.scale(pygame.image.load(f'sprites/clothes/3/{file_clothes["3"]}/stay/back/{i}.png'),
                                    (96, 96)).convert_alpha() for i in range(1, 3)], 15
        )
        self.pants_stay_left = Animation(
            [pygame.transform.scale(pygame.image.load(f'sprites/clothes/3/{file_clothes["3"]}/stay/left/{i}.png'),
                                    (96, 96)).convert_alpha() for i in range(1, 3)], 15
        )
        self.pants_stay_right = Animation(
            [pygame.transform.scale(pygame.image.load(f'sprites/clothes/3/{file_clothes["3"]}/stay/right/{i}.png'),
                                    (96, 96)).convert_alpha() for i in range(1, 3)], 15
        )
        self.pants_stay_front = Animation(
            [pygame.transform.scale(pygame.image.load(f'sprites/clothes/3/{file_clothes["3"]}/stay/front/{i}.png'),
                                    (96, 96)).convert_alpha() for i in range(1, 3)], 15
        )

        self.pants_walk_back = Animation(
            [pygame.transform.scale(pygame.image.load(f'sprites/clothes/3/{file_clothes["3"]}/walk/back/{i}.png'),
                                    (96, 96)).convert_alpha() for i in range(1, 9)], 4
        )
        self.pants_walk_left = Animation(
            [pygame.transform.scale(pygame.image.load(f'sprites/clothes/3/{file_clothes["3"]}/walk/left/{i}.png'),
                                    (96, 96)).convert_alpha() for i in range(1, 9)], 4
        )
        self.pants_walk_right = Animation(
            [pygame.transform.scale(pygame.image.load(f'sprites/clothes/3/{file_clothes["3"]}/walk/right/{i}.png'),
                                    (96, 96)).convert_alpha() for i in range(1, 9)], 4
        )
        self.pants_walk_front = Animation(
            [pygame.transform.scale(pygame.image.load(f'sprites/clothes/3/{file_clothes["3"]}/walk/front/{i}.png'),
                                    (96, 96)).convert_alpha() for i in range(1, 9)], 4
        )



    def rotated_left(self):
        self.walk_left.show_anim(self.player_rect.x, self.player_rect.y)

        self.hear_walk_left.show_anim(self.player_rect.x, self.player_rect.y)
        self.clothes_walk_left.show_anim(self.player_rect.x, self.player_rect.y)
        self.pants_walk_left.show_anim(self.player_rect.x, self.player_rect.y)

    def rotated_forward(self):
        self.walk_front.show_anim(self.player_rect.x, self.player_rect.y)

        self.hear_walk_back.show_anim(self.player_rect.x, self.player_rect.y)
        self.clothes_walk_back.show_anim(self.player_rect.x, self.player_rect.y)
        self.pants_walk_back.show_anim(self.player_rect.x, self.player_rect.y)

    def rotated_right(self):
        self.walk_right.show_anim(self.player_rect.x, self.player_rect.y)

        self.hear_walk_right.show_anim(self.player_rect.x, self.player_rect.y)
        self.clothes_walk_right.show_anim(self.player_rect.x, self.player_rect.y)
        self.pants_walk_right.show_anim(self.player_rect.x, self.player_rect.y)

    def rotated_back(self):
        self.walk_back.show_anim(self.player_rect.x, self.player_rect.y)

        self.hear_walk_front.show_anim(self.player_rect.x, self.player_rect.y)
        self.clothes_walk_front.show_anim(self.player_rect.x, self.player_rect.y)
        self.pants_walk_front.show_anim(self.player_rect.x, self.player_rect.y)

    def front_walk_func(self):
        self.player_movement[1] -= self.speed
        if self.key[pygame.K_a]:
            self.player_movement[0] -= self.speed

            self.rotated_left()

        elif self.key[pygame.K_d]:
            self.player_movement[0] += self.speed

            self.rotated_right()

        else:

            self.rotated_forward()

            self.front_bool = True
            self.back_bool = False
            self.right_bool = False
            self.left_bool = False

    def back_walk_func(self):
        self.player_movement[1] += self.speed

        if self.key[pygame.K_a]:
            self.player_movement[0] -= self.speed

            self.rotated_left()

        elif self.key[pygame.K_d]:
            self.player_movement[0] += self.speed

            self.rotated_right()

        else:

            self.rotated_back()

            self.back_bool = True
            self.front_bool = False
            self.right_bool = False
            self.left_bool = False

    def right_walk_func(self):
        self.player_movement[0] += self.speed

        self.rotated_right()

        self.right_bool = True
        self.left_bool = False
        self.front_bool = False
        self.back_bool = False

    def left_walk_func(self):
        self.player_movement[0] -= self.speed

        self.rotated_left()

        self.left_bool = True
        self.front_bool = False
        self.back_bool = False
        self.right_bool = False
