import pygame
import pyautogui
import sys
from engine import *
from player import *
from textures import *
from UI import *
import json
import datetime
pygame.init()
from pygame.locals import *
from random import randint
from StreetMap import *
from Entities import *

time_session = datetime.datetime.now()

class Tutorial():

    def __init__(self, save):
        self.save = save


        with open(f'data/{self.save}/data.json', 'r', encoding='utf-8') as json_file:
            self.save_file = json.load(json_file)

        self.player = Player(self.save)
        self.player.player_rect.x = self.save_file['pos_x']
        self.player.player_rect.y = self.save_file['pos_y']

        self.status = self.save_file['status']
        self.season = self.save_file['season']
        self.money = self.save_file['money']
        self.time_session = self.save_file['timesec']

        self.start_time = datetime.datetime.now()
        self.tutorial = False

        self.delay = 100
        self.saved = False

        self.window_alert = pygame.transform.scale(pygame.image.load('sprites/icons/alerts/chose_alert.png'),
                                                 (960, 576)).convert_alpha()

        with open('data/maindata.json', 'r', encoding='utf-8') as jsons:
            self.maindata = json.load(jsons)

        with open(f'data/{self.save}/tasks.json', 'r', encoding='utf-8') as tasksfile:
            self.tasks = json.load(tasksfile)


        self.exit_menu = False
        self.black_filter = pygame.Surface((1280, 720)).convert_alpha()

        self.main_map = StreetMap(self.save)

        self.train = Train()
        self.rect_top = Rect(0, 0, SIZE[0], SIZE[1] // 8)
        self.rect_bottom = Rect(0, SIZE[1] - SIZE[1] // 8, SIZE[0], SIZE[1] // 8)

        self.alert_move_forward = Alert(button='w')
        self.alert_move_left = Alert(button='a')
        self.alert_move_right = Alert(button='d')
        self.alert_move_back = Alert(button='s')
        self.alert_press_esc = Alert(button='esc')
        self.moved_w = False
        self.moved_d = False
        self.moved_s = False
        self.moved_a = False
        self.pressed_esc = False

        self.menu_uses = Menu_Uses(self.save)

        self.menu_uses.save_info = self.save_exit
        self.menu_uses.exit_to_menu = self.exit_to_menu

        self.interact = False
        self.rect_button_interact = Rect(SIZE[0] - SIZE[0] // 2 - 32, 560, 64, 64)
        self.yes_ico = pygame.transform.scale(
            pygame.image.load('sprites/icons/yes_btn.png').convert_alpha(), (64, 64)
        )

        self.loading_loc_anim = Animation(
            [pygame.image.load(f'sprites/other gui/loading location/{i}.png').convert_alpha() for i in range(1, 10)], 3
        )

        self.uploading_loc_anim = Animation(
            [pygame.image.load(f'sprites/other gui/loading location/{i}.png').convert_alpha() for i in range(1, 10)][::-1], 3
        )


        # self.timegame = TimeGame(self.save)
        self.character_UI = CharacterUI(self.save)

        self.go_next_location = False
        self.location = self.save_file['location']

        self.player.get_collider_location(self.location)
        self.locations = {
            'zetta' : self.zetta_location,
            'train' : self.render_tutorial,
        }

        self.locations[self.location]()
        # self.render_tutorial()
        # self.zetta_location()

    def save_exit(self, exit=True):
        global saved
        self.save_file['pos_x'] = self.player.player_rect.x
        self.save_file['pos_y'] = self.player.player_rect.y
        self.save_file['status'] = self.status
        self.save_file['season'] = self.season
        self.save_file['money'] = self.money
        self.save_file['tutorial'] = self.tutorial
        self.save_file['timesec'] += self.time_session
        self.save_file['location'] = self.location
        self.save_file['timegame'] = self.main_map.filters.taketime_string()
        self.save_file['color_filter'] = self.main_map.filters.filter_rendering.color_switcher
        self.save_file['alpha_filter'] = self.main_map.filters.filter_rendering.alpha_channel



        self.img.save(f'data/{self.save}/sh.png')

        with open(f'data/{self.save}/data.json', 'w', encoding='utf-8') as json_file:
            json.dump(self.save_file, json_file, indent=4, ensure_ascii=False)

        with open(f'data/{self.save}/tasks.json', 'w', encoding='utf-8') as task_file:
            json.dump(self.tasks, task_file, indent=4, ensure_ascii=False)

        with open(f'data/{self.save}/clothes.json', 'w', encoding='utf-8') as clothesfile:
            json.dump(self.menu_uses.obj_inventory.clothes_save, clothesfile, indent=4, ensure_ascii=False)

        with open(f'data/{self.save}/inventory.json', 'w', encoding='utf-8') as inventory_file:
            inv = {}
            for items in self.menu_uses.obj_inventory.inventory:
                inv[items.name] = items.count

            inventory_upload = {
                "inventory" : inv,
                "clothes" : [i.path for i in self.menu_uses.obj_inventory.clothes],
            }
            json.dump(inventory_upload, inventory_file, indent=4, ensure_ascii=False)


        # добавить сохранение инвентаря и одежды


        if exit:
            self.saved = True
            self.exit_menu = True

    def exit_to_menu(self):
        self.exit_menu = True

    def render_tutorial(self):
        global scroll, saved
        self.player.you_can_move = False
        self.loading_show = True
        while True:

            self.get_time()
            self.main_map.set_time_game(self.character_UI.timesecs)

            print(self.player.player_rect.x, self.player.player_rect.y)
            self.mouse = pygame.mouse.get_pos()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_w:
                        self.moved_w = True
                    if event.key == pygame.K_s:
                        self.moved_s = True
                    if event.key == pygame.K_d:
                        self.moved_d = True
                    if event.key == pygame.K_a:
                        self.moved_a = True

                    if event.key == pygame.K_ESCAPE:
                        self.pressed_esc = True
                        if self.menu_uses.att_type != 4:
                            self.menu_uses.att_type = 4
                        self.menu_uses.counter = abs(self.menu_uses.counter - 1)
                        self.img = pyautogui.screenshot()




            self.main_map.render_tiles_station()

            self.main_map.render_trees_station()

            self.main_map.render_station_under(self.player.player_rect.y)

            self.player.render()

            self.main_map.render_station_above(self.player.player_rect.y)

            self.main_map.render_powers_station_under()


            self.list_moved = [self.moved_d, self.moved_a, self.moved_w, self.moved_s]


            if any(self.list_moved):
                self.train.move_next()
            if not self.train.move():

                self.player.player_rect.x = self.train.rect_train.x + 1030
                self.player.player_rect.y = self.train.rect_train.y + 100
                self.cinema_effect = True
                self.player.you_can_move = False

            else:
                self.player.you_can_move = True
                self.cinema_effect = False
                self.alert_move_forward.render_button_allert(self.moved_w)
                if self.moved_w:
                    self.alert_move_right.render_button_allert(self.moved_d)
                if self.moved_d:
                    self.alert_move_left.render_button_allert(self.moved_a)
                if self.moved_a:
                    self.alert_move_back.render_button_allert(self.moved_s)
                if all(list((self.moved_w, self.moved_d, self.moved_a, self.moved_s))):
                    self.alert_press_esc.render_button_allert(self.pressed_esc)



            self.main_map.render_powers_station_above()

            ''' отрисовка интерфейса'''

            if not self.cinema_effect:
                self.character_UI.show_location()
                if not self.menu_uses.opening and not self.menu_uses.counter:
                    self.character_UI.render()

            self.menu_uses.render_menu()



            # if self.loading_show:
            #     if self.uploading_loc_anim.show_anim_static(0, 0):
            #         self.loading_show = False

            if self.go_next_location:
                if self.loading_loc_anim.show_anim_static(0, 0):
                    self.locations[self.location]()


            self.main_map.render_filter()

            self.draw_cinema()

            window.blit(mouse_cursor, self.mouse)

            clock.tick(FPS)
            pygame.display.update()

            if self.exit_menu:
                break

            if self.menu_uses.obj_inventory.update_character_clothes:
                self.player.update_loading_clothes(self.menu_uses.obj_inventory.clothes_save)
                self.menu_uses.obj_inventory.update_character_clothes = False

            if self.player.player_rect.y <= 2578:
                ''' go city '''
                self.player.you_can_move = False
                self.location = 'zetta'
                self.go_next_location = True





    def draw_cinema(self):
        pygame.draw.rect(window, (0, 0, 0), self.rect_top)
        pygame.draw.rect(window, (0, 0, 0), self.rect_bottom)
        if not self.cinema_effect:
            self.rect_top.y -= 5
            self.rect_bottom.y += 5

    def get_time(self):
        self.time_session = (datetime.datetime.now() - self.start_time).seconds



    def zetta_location(self):
        self.player.you_can_move = True
        loading()

        self.loading_show = True
        self.main_map.tiles_map = load_tiles('static/zetta_tiles')

        self.player.get_collider_location('zetta')
        self.player.player_rect.x = 1174
        self.player.player_rect.y = 4733

        while True:
            self.get_time()

            print(self.player.player_rect.x, self.player.player_rect.y)
            self.mouse = pygame.mouse.get_pos()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_w:
                        self.moved_w = True
                    if event.key == pygame.K_s:
                        self.moved_s = True
                    if event.key == pygame.K_d:
                        self.moved_d = True
                    if event.key == pygame.K_a:
                        self.moved_a = True

                    if event.key == pygame.K_ESCAPE:
                        self.pressed_esc = True
                        if self.menu_uses.att_type != 4:
                            self.menu_uses.att_type = 4
                        self.menu_uses.counter = abs(self.menu_uses.counter - 1)
                        self.img = pyautogui.screenshot()

            window.blit(screen, (0,0))
            screen.fill((0,0,0))

            self.main_map.render_zetta_location(self.player)

            self.character_UI.show_location()
            if not self.menu_uses.opening and not self.menu_uses.counter:
                self.character_UI.render()

            self.menu_uses.render_menu()

            if self.menu_uses.obj_inventory.update_character_clothes:
                self.player.update_loading_clothes(self.menu_uses.obj_inventory.clothes_save)
                self.menu_uses.obj_inventory.update_character_clothes = False


            if self.loading_show:
                if self.uploading_loc_anim.show_anim_static(0,0):
                    self.loading_show = False


            window.blit(mouse_cursor, self.mouse)

            pygame.display.update()
            clock.tick(FPS)

            if self.exit_menu:
                break

            ''' начать проектировать город '''

            ''' начать обдумывать отрисовку шейдеров '''





class Gameplay():
    def __init__(self, save):
        self.save = save

        with open(f'data/{self.save}/data.json', 'r', encoding='utf-8') as json_file:
            self.save_file = json.load(json_file)

        self.player = Player(self.save)
        self.player.player_rect.x = self.save_file['pos_x']
        self.player.player_rect.y = self.save_file['pos_y']

        self.status = self.save_file['status']

        self.rect_timeslider = pygame.Surface(SIZE).convert_alpha()
        self.alpha_channel_time = 255
        self.rect_timeslider.set_alpha(self.alpha_channel_time)

        self.font_x48_en = pygame.font.Font('fonts/UND.ttf', 48)
        self.delay = 100
        self.saved = False

        with open('data/maindata.json', 'r', encoding='utf-8') as jsons:
            self.maindata = json.load(jsons)





        self.exit_menu = False
        self.black_filter = pygame.Surface((1280, 720)).convert_alpha()

        self.main_map = StreetMap(self.save)


        self.menu = Menu_Uses(self.save)



    def render_world(self):
        while True:
            self.mouse = pygame.mouse.get_pos()


            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            window.blit(screen, (0,0))
            screen.fill((0,0,0))

            self.main_map.render_tiles_station()

            self.player.render()

            window.blit(mouse_cursor, self.mouse)


            clock.tick(FPS)
            pygame.display.update()

    def render_tavern(self):
        ''' прорисовка таверны в случае, если игрок в таверне '''
