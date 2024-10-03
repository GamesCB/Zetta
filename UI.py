import datetime

import pygame
import sys
import pyautogui
import os
import shutil
from random import randint
pygame.init()

from pygame.locals import *
from engine import *
from textures import *
from Tasks import *
from constants import *
import json
from GUIelements import *
from inventory import *



class Menu():
    ''' класс для главного меню '''
    def __init__(self, saved):
        self.saved = saved
        self.font_16_rus = pygame.font.Font('fonts/rus-pixel.otf', 16)
        self.font_16_en = pygame.font.Font('fonts/UND.ttf', 16)
        self.font_32_rus = pygame.font.Font('fonts/rus-pixel.otf', 32)
        self.font_64_rus = pygame.font.Font('fonts/rus-pixel.otf', 64)
        self.font_32_en = pygame.font.Font('fonts/UND.ttf', 32)

        self.delay = 0

        with open('data/maindata.json', 'r', encoding='utf-8') as json_file:
            self.maindata = json.load(json_file)

        self.volume_sound = self.maindata['volume_sound']
        self.volume_music = self.maindata['volume_music']

        # кнопки
        self.rect_new_game = Rect(555, 315, 128, 44)
        self.count_new_game = 32
        self.font_new_game = pygame.font.Font('fonts/rus-pixel.otf', self.count_new_game)
        self.color_new_game = (200, 200, 200)

        self.rect_load_game = Rect(495, 375, 750-490, 44)
        self.count_load_game = 32
        self.font_load_game = pygame.font.Font('fonts/rus-pixel.otf', self.count_load_game)
        self.color_load_game = (200, 200, 200)

        self.rect_settings = Rect(560, 435, 680 - 560, 44)
        self.count_settings = 32
        self.font_settings = pygame.font.Font('fonts/rus-pixel.otf', self.count_settings)
        self.color_settings = (200, 200, 200)

        self.rect_stats = Rect(552, 495, 690 - 552, 44)
        self.count_stats = 32
        self.font_stats = pygame.font.Font('fonts/rus-pixel.otf', self.count_stats)
        self.color_stats = (200, 200, 200)

        self.rect_exit = Rect(587, 555, 660 - 585, 44)
        self.count_exit = 32
        self.font_exit = pygame.font.Font('fonts/rus-pixel.otf', self.count_exit)
        self.color_exit = (200, 200, 200)

        # ////////////

        self.exit_from_main = False
        self.exit_from_menu = False
        self.chosen_save = False

        self.rect_slide_music = pygame.Rect(1280 - 428 + 142, 140, 16, 16)
        self.rect_slide_sound = pygame.Rect(1280 - 428 + 142, 140 + 64, 16, 16)

        self.create_character_bg = pygame.image.load('sprites/background/create character.png').convert_alpha()
        self.mainbg = pygame.image.load('sprites/background/mainbg.png').convert_alpha()

        self.zetta_song = create_sound('songs/zetta.wav', 'm')
        self.zetta_song.play(-1)

        self.render_menu()


    def checksaved(self):

        if self.saved:
            self.delay = randint(100, 150)
            self.saved = False
        if self.delay > 0:
            self.delay -= 1
            save_animation.show_anim_static(1280 - 32 - 64, 720 - 32 - 64)


    def render_menu(self):
        ''' отрисовка главного меню '''

        while True:

            self.mouse = pygame.mouse.get_pos()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:

                    pygame.quit()
                    sys.exit()

            # window.blit(screen, (0,0))
            # screen.fill((0,0,0))

            window.blit(self.mainbg, (0,0))

            self.render_texts_menu()

            self.checksaved()

            window.blit(mouse_cursor, self.mouse)

            clock.tick(FPS)
            pygame.display.update()
            if self.exit_from_main:
                break



    def render_texts_menu(self):

        ''' отрисовка и отслеживание событий на кнопках '''

        window.blit(namegame, (256, 64))

        self.font_new_game, self.rect_new_game, self.count_new_game, self.color_new_game = self.controlbutton(
            self.rect_new_game, self.font_new_game, self.count_new_game, self.new_game
        )

        self.font_load_game, self.rect_load_game, self.count_load_game, self.color_load_game = self.controlbutton(
            self.rect_load_game, self.font_load_game, self.count_load_game, self.load_game
        )

        self.font_settings, self.rect_settings, self.count_settings, self.color_settings = self.controlbutton(
            self.rect_settings, self.font_settings, self.count_settings, self.settings
        )

        self.font_stats, self.rect_stats, self.count_stats, self.color_stats = self.controlbutton(
            self.rect_stats, self.font_stats, self.count_stats, self.stats
        )

        self.font_exit, self.rect_exit, self.count_exit, self.color_exit = self.controlbutton(
            self.rect_exit, self.font_exit, self.count_exit, self.exit_game
        )

        window.blit(self.font_new_game.render('новая игра', True, self.color_new_game), (self.rect_new_game.x, self.rect_new_game.y))
        window.blit(self.font_load_game.render('загрузить сохранение', True, self.color_load_game), (self.rect_load_game.x, self.rect_load_game.y))
        window.blit(self.font_settings.render('настройки', True, self.color_settings), (self.rect_settings.x, self.rect_settings.y))
        window.blit(self.font_stats.render('статистика', True, self.color_stats), (self.rect_stats.x, self.rect_stats.y))
        window.blit(self.font_exit.render('выход', True, self.color_exit), (self.rect_exit.x, self.rect_exit.y))


    def controlbutton(self, button:Rect, font:pygame.font.Font, count:int, func=None, hover = True):

        ''' controlling buttons like a func use or hover '''

        self.click = pygame.mouse.get_pressed()
        color = (200, 200, 200)
        if button.collidepoint(self.mouse[0], self.mouse[1]):
            color = (45, 78, 86)
            if count < 48:
                # count += 1
                font = pygame.font.Font('fonts/rus-pixel.otf', count)
                if self.click[0] and func != None:
                    func()
            if hover:
                window.blit(endbuttonleft, (button.x - endbuttonleft.get_width(), button.y))
                window.blit(endbuttonright, (button.x + button.width, button.y))
        else:
            if count > 32:
                font = pygame.font.Font('fonts/rus-pixel.otf', count)
                # count -= 1

            color = (200, 200, 200)


        return font, button, count, color

    def new_game(self):

        self.create_save()

        if self.back_main_menu:
            return False

        self.search_saves()
        os.mkdir(f'data/save{self.saves_count + 1}')

        json_file = {'pos_x' : 100,
                     'pos_y' : 320,
                     'timesec' : 0,
                     'status' : 'безработный',
                     'tutorial' : False,
                     'money' : 100,
                     'season' : 'summer',
                     'timegame' : '17:30',
                     'location' : 'train',
                     'name_chr' : f'{self.name_character.string}',
                     'lvl' : 1,
                     'xp' : 0,
                     'newlvlxp' : 100,
                     'loving' : 0,
                     'day' : 'понедельник',
                     'year' : 1982,
                     'gender' : self.gender_name,
                     'age' : self.number_type_box.string,
                     'hungry' : randint(90, 100),
                     'thirst' : randint(90, 100),
                     'health' : 100,
                     'energy' : 100,
                     'color_filter' : [252, 151, 92],
                     'alpha_filter' : 70



                     }

        if self.counter_hears < 0:
            self.counter_hears = abs(self.counter_hears) + 1
        if self.counter_clothes < 0:
            self.counter_clothes = abs(self.counter_clothes) + 1
        if self.counter_pants < 0:
            self.counter_pants = abs(self.counter_pants) + 1


        json_clothes = {
            '1' : f'{self.gender_name}/{str(self.counter_hears + 1)}',
            '2' : str(self.counter_clothes + 1),
            '3' : str(self.counter_pants + 1),
        }

        json_tasks = {
            'Обучение' : {
                'by' : f'{self.name_character.string}',
                'status' : False,
                'task' : {
                    'Покинуть станцию' : {
                        'status' : False,
                        'desc' : 'Идите прямо и покиньте станцию'
                    },
                    'Снять комнату' : {
                        'status' : False,
                        'desc' : 'Близится ночь, проверьте отель поблизости и снимите комнату'
                    }
                },
                'number_of_task' : 1,
                'reward' : {
                    'money' : 0,
                    'xp' : 100
                }
            }
        }

        json_inventory = {
            "inventory" : {

            },
            "clothes" : [
                CLOTHES[f"2/{self.counter_clothes + 1}"], CLOTHES[f'3/{self.counter_pants + 1}']
            ]
        }

        with open(f'data/save{self.saves_count + 1}/data.json', 'w', encoding='utf-8') as file:
            json.dump(json_file, file, indent=4, ensure_ascii=True)

        with open(f'data/save{self.saves_count + 1}/clothes.json', 'w', encoding='utf-8') as file:
            json.dump(json_clothes, file, indent=4, ensure_ascii=True)

        with open(f'data/save{self.saves_count + 1}/tasks.json', 'w', encoding='utf-8') as file:
            json.dump(json_tasks, file, indent=4, ensure_ascii=True)

        with open(f'data/save{self.saves_count + 1}/inventory.json', 'w', encoding='utf-8') as file:
            json.dump(json_inventory, file, indent=4, ensure_ascii=True)

        img = pyautogui.screenshot()
        img.save(f'data/save{self.saves_count + 1}/sh.png')

        self.scroll_saves = self.saves_count + 1
        self.total_saves.append(f'save{self.scroll_saves}')

        self.zetta_song.stop()

        self.exit_from_main = True

    def load_game(self):
        self.exit_from_main = True
        self.exit_loads = False
        self.search_saves()
        self.scroll_saves = 0

        ''' кнопка загрузки '''
        self.rect_loadsave = Rect(575, 555, 117, 44)
        self.count_loadsave = 32
        self.font_loadsave = pygame.font.Font('fonts/rus-pixel.otf', self.count_loadsave)
        self.color_loadsave = (200, 200, 200)

        ''' кпнока удаления '''
        self.rect_delete = Rect(587, 600, 90, 44)
        self.count_delete = 32
        self.font_delete = pygame.font.Font('fonts/rus-pixel.otf', self.count_delete)
        self.color_delete = (200, 200, 200)

        ''' кнопка выхода обратно в меню '''
        self.rect_back = Rect(595, 645, 75, 44)
        self.count_back = 32
        self.font_back = pygame.font.Font('fonts/rus-pixel.otf', self.count_back)
        self.color_back = (200, 200, 200)



        self.left_side_rect = pygame.Rect(16, 244, 32, 128)
        self.right_side_rect = pygame.Rect(1280 - 16 - rightside.get_width(), 244, 32, 128)


        self.surf_black = pygame.Surface((32, 128)).convert_alpha()
        self.surf_black.set_alpha(150)
        self.last_save_count = 0

        while True:
            self.mouse = pygame.mouse.get_pos()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.exit_loads = True

                    if event.key == pygame.K_RETURN:
                        if self.saves_count:
                            self.loadsave()

                    if event.key == pygame.K_RIGHT:
                        if self.scroll_saves + 1 != self.saves_count:
                            self.scroll_saves += 1

                    if event.key == pygame.K_LEFT:
                        if self.scroll_saves > 0:
                            self.scroll_saves -= 1

                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        if self.left_side_rect.collidepoint(self.mouse[0], self.mouse[1]):
                            if self.scroll_saves > 0:
                                self.scroll_saves -= 1
                        if self.right_side_rect.collidepoint(self.mouse[0], self.mouse[1]):
                            if self.scroll_saves + 1 != self.saves_count:
                                self.scroll_saves += 1

                        if self.rect_delete.collidepoint(self.mouse[0], self.mouse[1]):
                            self.delete_button()

                        if self.rect_loadsave.collidepoint(self.mouse[0], self.mouse[1]):
                            self.loadsave()


            window.blit(screen, (0,0))
            screen.fill((0,0,0))

            if self.saves_count != 0:

                if self.last_save_count != int(self.total_saves[self.scroll_saves][4::]):
                    with open(f'data/{self.total_saves[self.scroll_saves]}/data.json', 'r',
                              encoding='utf-8') as jsonfile:
                        self.data_save = json.load(jsonfile)

                    self.screenshot = pygame.transform.scale(
                        pygame.image.load(f'data/{self.total_saves[self.scroll_saves]}/sh.png'),
                        (640, 360)).convert_alpha()

                window.blit(leftside, (16, 244))
                window.blit(rightside, (1280 - 16 - rightside.get_width(), 244))


                self.hours = str(self.data_save['timesec'] // 3600)
                self.mins = str(self.data_save['timesec'] % 3600 // 60)
                self.secs = str(self.data_save['timesec'] % 60)

                if int(self.hours) < 10:
                    self.hours = '0' + self.hours
                if int(self.mins) < 10:
                    self.mins = '0' + self.mins
                if int(self.secs) < 10:
                    self.secs = '0' + self.secs

                if not(self.scroll_saves):
                    window.blit(self.surf_black, (16, 244))
                if self.scroll_saves + 1 == self.saves_count:
                    window.blit(self.surf_black, (1280 - 16 - rightside.get_width(), 244))
                self.surf_black.fill((0,0,0))


                window.blit(self.font_32_en.render(f'{self.data_save["name_chr"]}', True, (200, 200, 200)),
                            (SIZE[0] // 2 - 18 * len(f'{self.data_save["name_chr"]}') // 2, 64))
                window.blit(self.screenshot, (320, 96))
                window.blit(self.font_32_rus.render(f'{self.hours}:{self.mins}:{self.secs}', True, (200, 200, 200)), (1030, 96))
                window.blit(clock_icon, (980, 96 + 4))
                window.blit(self.font_32_rus.render(f'{self.data_save["status"]}', True, (200, 200, 200)), (1030, 128+32))
                window.blit(status_icon, (980, 128+32 + 4))





                ''' описание кнопок на экране'''
                self.font_loadsave, self.rect_loadsave, self.count_loadsave, self.color_loadsave = self.controlbutton(
                    self.rect_loadsave, self.font_loadsave, self.count_loadsave
                )

                self.font_delete, self.rect_delete, self.count_delete, self.color_delete = self.controlbutton(
                    self.rect_delete, self.font_delete, self.count_delete
                )

                self.font_back, self.rect_back, self.count_back, self.color_back = self.controlbutton(
                    self.rect_back, self.font_back, self.count_back, self.returnbackload
                )

                window.blit(self.font_loadsave.render('загрузить', True, self.color_loadsave), (self.rect_loadsave.x, self.rect_loadsave.y))
                window.blit(self.font_delete.render('стереть', True, self.color_delete), (self.rect_delete.x, self.rect_delete.y))
                window.blit(self.font_back.render('в меню', True, self.color_back), (self.rect_back.x, self.rect_back.y))

                self.checksaved()
                self.last_save_count = int(self.total_saves[self.scroll_saves][4::])

            else:
                window.blit(self.font_64_rus.render('пока не было создано сохранений', True, (200, 200, 200)), (256, 340))

            window.blit(mouse_cursor, self.mouse)

            clock.tick(FPS)
            pygame.display.update()
            if self.exit_loads:
                if not self.exit_from_menu:
                    self.exit_from_main = False
                break

    def settings(self):
        ''' настройки '''

        with open('data/maindata.json', 'r', encoding='utf-8') as json_file:
            self.maindata = json.load(json_file)

        self.volume_sound = self.maindata['volume_sound']
        self.volume_music = self.maindata['volume_music']
        self.font_controls = pygame.font.Font('fonts/rus-pixel.otf', 32)
        self.color_controls = (200, 200, 200)
        self.rect_controls = Rect(120, 255, 265 - 120, 30)
        self.count_controls = 20

        self.rect_slide_sound.x = 1280 - 428 + 6 + self.volume_sound * 300
        self.rect_slide_music.x = 1280 - 428 + 6 + self.volume_music * 300

        self.exit_from_settings = False

        self.rect_music = pygame.Rect(1280 - 428, 146, 300, 4)

        self.rect_sound = pygame.Rect(1280 - 428, 146 + 64, 300, 4)

        while True:
            self.mouse = pygame.mouse.get_pos()
            self.click = pygame.mouse.get_pressed()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.exit_from_settings = True

            window.blit(screen, (0,0))
            screen.fill((0,0,0))

            window.blit(self.font_64_rus.render('настройки', True, (200, 200, 200)), (512, 32))

            self.font_controls, self.rect_controls, self.count_controls, self.color_controls = self.controlbutton(
                self.rect_controls, self.font_controls, self.count_controls, self.controls
            )

            window.blit(self.font_32_rus.render('музыка', True, (200, 200, 200)), (128, 128))
            pygame.draw.rect(window, (150, 150, 150), self.rect_music)
            pygame.draw.rect(window, (180, 180, 180), self.rect_slide_music)

            window.blit(self.font_32_rus.render('звуки', True, (200, 200, 200)), (128, 128 + 64))
            pygame.draw.rect(window, (150, 150, 150), self.rect_sound)
            pygame.draw.rect(window, (180, 180, 180), self.rect_slide_sound)

            window.blit(self.font_32_rus.render('управление', True, self.color_controls), (128, 128 + 128))

            if self.click[0]:
                if self.mouse[0] in range(1280 - 436 + 8, 1280 - 436 + 308):

                    if self.mouse[1] in range(115, 170):
                        self.rect_slide_music.x = self.mouse[0] - 8

                    if self.mouse[1] in range(180, 240):
                        self.rect_slide_sound.x = self.mouse[0] - 8


            self.checksaved()

            window.blit(mouse_cursor, self.mouse)
            pygame.display.update()
            clock.tick(FPS)

            if self.exit_from_settings:
                ''' сохранение громкости музыки в меню '''
                break


            self.volume_music = round((abs(1280 - 436 + 8 - self.rect_slide_music.x) / 300) - 0.02, 2)
            self.volume_sound = round((abs(1280 - 436 + 8 - self.rect_slide_sound.x) / 300) - 0.02, 2)

    def controls(self):

        self.exit_controls = False


        while True:
            self.mouse = pygame.mouse.get_pos()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.exit_controls = True

            window.blit(screen, (0,0))
            screen.fill((0,0,0))

            window.blit(self.font_64_rus.render('управление', True, (200, 200, 200)), (512, 32))

            window.blit(self.font_32_rus.render('вперед', True, (200, 200, 200)), (128, 128))
            # window.blit(self.line_controls, (128, 128 + 48))
            window.blit(self.font_32_rus.render('назад', True, (200, 200, 200)), (128, 128 + 64))
            # window.blit(self.line_controls, (128, 128 + 64 + 48))
            window.blit(self.font_32_rus.render('вправо', True, (200, 200, 200)), (128, 256))
            # window.blit(self.line_controls, (128, 256 + 48))
            window.blit(self.font_32_rus.render('влево', True, (200, 200, 200)), (128, 256 + 64))
            # window.blit(self.line_controls, (128, 256 + 64 + 48))
            window.blit(self.font_32_rus.render('меню', True, (200, 200, 200)), (128, 128 + 256))
            # window.blit(self.line_controls, (128, 128 + 256 + 48))
            window.blit(self.font_32_rus.render('прошлая вкладка', True, (200, 200, 200)), (128, 128 + 256 + 64))
            # window.blit(self.line_controls, (128, 128 + 256 + 64 + 48))
            window.blit(self.font_32_rus.render('дневник', True, (200, 200, 200)), (128, 512))
            # window.blit(self.line_controls, (128, 512 + 48))
            window.blit(self.font_32_rus.render('использовать', True, (200, 200, 200)), (128, 512 + 64))
            # window.blit(self.line_controls, (128, 512 + 64 + 48))

            window.blit(self.font_32_en.render('w', True, (200, 200, 200)), (1280 - 128, 128))
            window.blit(self.font_32_en.render('s', True, (200, 200, 200)), (1280 - 128, 128 + 64))
            window.blit(self.font_32_en.render('d', True, (200, 200, 200)), (1280 - 128, 256))
            window.blit(self.font_32_en.render('a', True, (200, 200, 200)), (1280 - 128, 256 + 64))
            window.blit(self.font_32_en.render('esc', True, (200, 200, 200)), (1280 - 128, 128 + 256))
            window.blit(self.font_32_en.render('esc', True, (200, 200, 200)), (1280 - 128, 128 + 256 + 64))
            window.blit(self.font_32_en.render('tab', True, (200, 200, 200)), (1280 - 128, 512))
            window.blit(self.font_32_en.render('e', True, (200, 200, 200)), (1280 - 128, 512 + 64))

            self.checksaved()

            window.blit(mouse_cursor, self.mouse)
            pygame.display.update()
            clock.tick(FPS)

            if self.exit_controls:
                break



    def returnbackload(self):
        self.exit_from_main = False
        self.exit_loads = True

    def stats(self):
        ''' общая статистика по игре '''
        print('stats')

    def exit_game(self):
        if self.chosen_save == False:
            self.maindata['volume_music'] = self.volume_music
            self.maindata['volume_sound'] = self.volume_sound
            with open('data/maindata.json', 'w', encoding='utf-8') as json_file:
                json.dump(self.maindata, json_file, ensure_ascii=False, indent=4)
            pygame.quit()
            sys.exit()

    def search_saves(self):
        ''' search saves in data '''
        self.total_saves = [i for i in os.listdir('data')]
        self.total_saves.pop(0)
        self.saves_count = len(self.total_saves)

    def loadsave(self):
        ''' load save and exit from menu '''
        self.chosen_save = self.total_saves[self.scroll_saves]
        self.exit_loads = True
        self.exit_from_menu = True
        self.exit_from_main = True
        self.zetta_song.stop()
        with open('data/maindata.json', 'w', encoding='utf-8') as jsonfile:
            json.dump(self.maindata, jsonfile, ensure_ascii=False, indent=4)

    def delete_button(self):
        shutil.rmtree(f'data/{self.total_saves[self.scroll_saves]}')
        self.saves_count -= 1
        self.total_saves.remove(self.total_saves[self.scroll_saves])
        self.scroll_saves -= 1 if self.scroll_saves != 0 and self.saves_count > 0 else 0

    def create_save(self):
        self.surf_black = pygame.Surface(SIZE)
        self.surf_black.set_alpha(100)
        self.rect_surf_black = Rect(SIZE[0], 0, 1, 1)
        self.create_character_bg_clouds = pygame.image.load('sprites/background/cr_ch_clouds.png').convert_alpha()
        self.rect_clouds1 = Rect(-1280, 0, 400, 1280)
        self.rect_clouds2 = Rect(-2560, 0, 400, 1280)

        self.name_character = Input_Box(pygame.font.Font('fonts/Hardpixel-nn51.otf', 32), 10, 240)

        self.window_gui = pygame.transform.scale(pygame.image.load('sprites/icons/alerts/chose_alert.png'),
                                                 (960, 576)).convert_alpha()

        self.input_name = pygame.transform.scale(pygame.image.load('sprites/other gui/input_any.png'),
                                                 (270, 60)).convert_alpha()

        self.player_ico = pygame.image.load('sprites/other gui/player_ico.png').convert_alpha()

        self.female_ico = pygame.image.load('sprites/icons/female_ico.png').convert_alpha()
        self.male_ico = pygame.image.load('sprites/icons/male_ico.png').convert_alpha()

        self.checkbox_na = pygame.image.load('sprites/other gui/checkbox_na.png').convert_alpha()
        self.checkbox_a = pygame.image.load('sprites/other gui/checkbox_a.png').convert_alpha()

        self.rect_checkbox_male = pygame.Rect(260 + 20, 300 + 8, 64, 64)
        self.rect_checkbox_female = pygame.Rect(340 + 20, 300 + 8, 64, 64)

        self.gender = self.male_ico
        self.gender_name = 'male'

        self.font_chose_ch = pygame.font.Font('fonts/Hardpixel-nn51.otf', 32)

        self.alpha_win_gui = 0
        self.window_gui.set_alpha(self.alpha_win_gui)

        self.number_type = pygame.image.load('sprites/other gui/number_typing.png').convert_alpha()
        self.number_type_box = Input_Box(self.font_chose_ch, 2, 32)

        self.button_sprite = pygame.image.load('sprites/other gui/button-long.png').convert_alpha()
        self.button_back_rect = Rect(322, 545, self.button_sprite.get_width(), self.button_sprite.get_height())
        self.button_create_rect = Rect(728, 545, self.button_sprite.get_width(), self.button_sprite.get_height())
        self.exit_create = False
        self.back_main_menu = False
        self.continuecreate = False

        self.color_button_back_mainmenu = (226, 178, 126)
        self.color_button_create = (226, 178, 126)

        self.alert_continue_create = Alert('не все поля заполнены')

        self.player_flat = pygame.transform.scale(
            pygame.image.load('sprites/characters/flat/stay/front/1.png'), (512, 512)
        ).convert_alpha()

        self.left_arrow2 = pygame.transform.scale(
            pygame.image.load('sprites/icons/left_arrow2.png').convert_alpha(), (64, 64)
            ).convert_alpha()

        self.right_arrow2 = pygame.transform.scale(
            pygame.image.load('sprites/icons/right_arrow2.png').convert_alpha(), (64, 64)
        ).convert_alpha()

        self.clothes_selector = pygame.transform.scale(
            pygame.image.load('sprites/other gui/clothes_selector.png').convert_alpha(), (96, 96)
        )

        self.counter_hears = 0
        self.counter_clothes = 0
        self.counter_pants = 0

        self.rect_leftarrow_hears = Rect(560, 236, 20, 24)
        self.rect_rightarrow_hears = Rect(696, 236, 20, 24)
        self.rect_leftarrow_clothes = Rect(560, 336, 20, 24)
        self.rect_rightarrow_clothes = Rect(696, 336, 20, 24)
        self.rect_leftarrow_pants = Rect(560, 436, 20, 24)
        self.rect_rightarrow_pants = Rect(696, 436, 20, 24)

        self.len_male = len([i for i in os.listdir('sprites/clothes/1/male')])
        self.len_female = len([i for i in os.listdir('sprites/clothes/1/female')])

        self.len_clothes = len([i for i in os.listdir('sprites/clothes/2')])
        self.len_pants = len([i for i in os.listdir('sprites/clothes/3')])

        self.total_hears = []
        self.total_hears_male = [pygame.transform.scale(pygame.image.load(f'sprites/clothes/1/male/{i}/idle.png'), (96, 96)).convert_alpha() for i in range(1, self.len_male + 1)]
        self.total_hears_female = [pygame.transform.scale(pygame.image.load(f'sprites/clothes/1/female/{i}/idle.png'), (96, 96)).convert_alpha() for i in range(1, self.len_female + 1)]
        self.total_hears_big = []

        self.total_clothes = [pygame.transform.scale(pygame.image.load(f'sprites/clothes/2/{i}/idle.png'), (96, 96)).convert_alpha() for i in range(1, self.len_clothes + 1)]
        self.total_pants = [pygame.transform.scale(pygame.image.load(f'sprites/clothes/3/{i}/idle.png'), (96, 96)).convert_alpha() for i in range(1, self.len_pants + 1)]

        self.dummy_img = pygame.transform.scale(pygame.image.load('sprites/characters/flat/stay/front/1.png').convert_alpha(), (96,96))

        self.total_clothes_big = [pygame.transform.scale(i, (512, 512)) for i in self.total_clothes]
        self.total_pants_big = [pygame.transform.scale(i, (512, 512)) for i in self.total_pants]

        while True:
            self.mouse = pygame.mouse.get_pos()
            # print(self.mouse)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:

                        if self.rect_leftarrow_hears.collidepoint(*self.mouse):
                            self.counter_hears -= 1
                            if self.counter_hears <= -len(self.total_hears):
                                self.counter_hears = 0
                        if self.rect_rightarrow_hears.collidepoint(*self.mouse):
                            if self.counter_hears < len(self.total_hears):
                                self.counter_hears += 1
                            if self.counter_hears >= len(self.total_hears):
                                self.counter_hears = 0

                        if self.rect_leftarrow_clothes.collidepoint(*self.mouse):
                            self.counter_clothes -= 1
                            if self.counter_clothes <= -len(self.total_clothes):
                                self.counter_clothes = 0
                        if self.rect_rightarrow_clothes.collidepoint(*self.mouse):
                            if self.counter_clothes < len(self.total_clothes):
                                self.counter_clothes += 1
                            if self.counter_clothes >= len(self.total_clothes):
                                self.counter_clothes = 0

                        if self.rect_leftarrow_pants.collidepoint(*self.mouse):
                            self.counter_pants -= 1
                            if self.counter_pants <= -len(self.total_pants):
                                self.counter_pants = 0
                        if self.rect_rightarrow_pants.collidepoint(*self.mouse):
                            if self.counter_pants < len(self.total_pants):
                                self.counter_pants += 1
                            if self.counter_pants >= len(self.total_pants):
                                self.counter_pants = 0

            window.blit(screen, (0,0))
            screen.fill((0,0,0))

            window.blit(self.create_character_bg, (self.rect_surf_black.x,self.rect_surf_black.y))
            if self.rect_surf_black.x > 0:
                window.blit(self.surf_black, (self.rect_surf_black.x, self.rect_surf_black.y))


            if self.rect_surf_black.x > 0:
                self.rect_surf_black.x -= 64
            else:
                self.rect_surf_black.x = 0
                window.blit(self.create_character_bg_clouds, (self.rect_clouds1.x, self.rect_clouds1.y))
                window.blit(self.create_character_bg_clouds, (self.rect_clouds2.x, self.rect_clouds2.y))
                window.blit(self.surf_black, (self.rect_surf_black.x, self.rect_surf_black.y))
                self.rect_clouds1.x += 1
                self.rect_clouds2.x += 1
                if self.rect_clouds1.x > 1280:
                    self.rect_clouds1.x = -1280
                if self.rect_clouds2.x > 1280:
                    self.rect_clouds2.x = -1280

                window.blit(self.window_gui, (160, 100))

                if self.alpha_win_gui < 255:
                    self.alpha_win_gui += 15
                else:
                    self.alpha_win_gui = 255
                self.window_gui.set_alpha(self.alpha_win_gui)

                if self.alpha_win_gui == 255:
                    window.blit(self.input_name, (260, 200))

                    self.name_character.render_input((10, 10, 10), 265, 205, 'имя персонажа')

                    window.blit(self.player_ico, (260 - 70, 198))

                    window.blit(self.gender, (210, 312))

                    window.blit(self.checkbox_na, (self.rect_checkbox_male.x, self.rect_checkbox_male.y))
                    window.blit(self.checkbox_na, (self.rect_checkbox_female.x, self.rect_checkbox_female.y))

                    window.blit(self.font_chose_ch.render('М', True, (20,20,20)), (260 + 20 + 20, 300 + 8 + 12))
                    window.blit(self.font_chose_ch.render('Ж', True, (20,20,20)), (340 + 20 + 18, 300 + 8 + 12))

                    if self.gender_name == 'male':
                        window.blit(self.checkbox_a, (self.rect_checkbox_male.x, self.rect_checkbox_male.y))

                    elif self.gender_name == 'female':
                        window.blit(self.checkbox_a, (self.rect_checkbox_female.x, self.rect_checkbox_male.y))

                    self.chose_gender()


                    window.blit(self.font_chose_ch.render('возраст:', True, (20, 20, 20)), (260 - 70, 420))
                    window.blit(self.number_type, (340, 415))
                    self.number_type_box.render_input((0,0,0), 353, 425, '0')

                    window.blit(self.button_sprite, (322, 545))
                    window.blit(self.button_sprite, (728, 545))



                    window.blit(self.font_chose_ch.render('назад', True, self.color_button_back_mainmenu), (390, 550))
                    window.blit(self.font_chose_ch.render('создать', True, self.color_button_create), (780, 550))

                    self.button_create_rect, self.color_button_create = self.chose_btn2(
                        self.button_create_rect, self.create_btn_event
                    )

                    self.button_back_rect, self.color_button_back_mainmenu = self.chose_btn2(
                        self.button_back_rect, self.back_btn_event
                    )


                    self.render_clothes()



            if self.continuecreate:
                if self.alert_continue_create.midalert(2, 565, 575, 'не все поля', 'заполнены'):
                    self.continuecreate = False



            window.blit(mouse_cursor, self.mouse)
            pygame.display.update()
            clock.tick(FPS)

            if self.exit_create:
                break

            if self.gender_name == 'male':
                self.total_hears = self.total_hears_male
                self.total_hears_big = [pygame.transform.scale(i, (512, 512)) for i in self.total_hears]
            else:
                self.total_hears = self.total_hears_female
                self.total_hears_big = [pygame.transform.scale(i, (512, 512)) for i in self.total_hears]

    def chose_gender(self):
        self.click = pygame.mouse.get_pressed()
        self.mouse = pygame.mouse.get_pos()

        if self.rect_checkbox_male.collidepoint(self.mouse[0], self.mouse[1]) and self.click[0]:
            self.gender_name = 'male'
            self.gender = self.male_ico
        elif self.rect_checkbox_female.collidepoint(self.mouse[0], self.mouse[1]) and self.click[0]:
            self.gender_name = 'female'
            self.gender = self.female_ico

    def back_btn_event(self):
        self.back_main_menu = True
        self.exit_create = True


    def create_btn_event(self):
        if self.name_character.string.isdigit() or len(self.name_character.string) < 2 or\
                self.name_character.string == '' or self.name_character == ' ' or not self.number_type_box.string.isdigit() or\
                int(self.number_type_box.string) < 14:
            self.continuecreate = True
            return False
        self.exit_create = True

    def chose_btn2(self, button:Rect, func=None):

        ''' controlling buttons like a func use or hover '''

        self.click = pygame.mouse.get_pressed()
        self.mouse = pygame.mouse.get_pos()
        color = (226, 178, 126)
        if button.collidepoint(self.mouse[0], self.mouse[1]):
            color = (107, 65, 43)

            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1 and func != None:

                        func()
            if self.click[0]:
                func()

        return button, color

    def render_clothes(self):
        window.blit(self.player_flat, (572, -7))

        window.blit(self.clothes_selector, (590, 204))
        window.blit(self.clothes_selector, (590, 304))
        window.blit(self.clothes_selector, (590, 404))

        window.blit(self.left_arrow2, (540, 220))
        window.blit(self.right_arrow2, (672, 220))
        window.blit(self.left_arrow2, (540, 320))
        window.blit(self.right_arrow2, (672, 320))
        window.blit(self.left_arrow2, (540, 420))
        window.blit(self.right_arrow2, (672, 420))

        window.blit(self.dummy_img, (590, 204 - 15))

        window.blit(self.total_hears[self.counter_hears], (590, 204 - 15))
        window.blit(self.total_hears_big[self.counter_hears], (572, -7))

        window.blit(self.dummy_img, (590, 270 + 20))

        window.blit(self.total_clothes[self.counter_clothes], (590, 270 + 20))
        window.blit(self.total_clothes_big[self.counter_clothes], (572, -7))

        window.blit(self.dummy_img, (590, 370 + 20))

        window.blit(self.total_pants[self.counter_pants], (590, 370 + 20))
        window.blit(self.total_pants_big[self.counter_pants], (572, -7))

''' лого Cartoon Box '''
def render_start_window():
    texture = pygame.image.load('sprites/icons/icon_CB.png').convert_alpha()

    alpha_channel = 150
    font_x32_us = pygame.font.Font('fonts/UND.ttf', 32)
    font_x24_ru = pygame.font.Font('fonts/rus-pixel.otf', 24)
    screen.set_alpha(alpha_channel)
    reverse = False
    exited = False
    wait = 100
    while alpha_channel < 255 and (not exited):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        window.blit(texture, (475, 150))
        window.blit(font_x32_us.render('Cartoon Box', True, (255,255,255)), (520, 473))
        window.blit(font_x24_ru.render('представляет', True, (255,255,255)), (570, 520))

        window.blit(screen, (0, 0))
        screen.fill((0, 0, 0))
        screen.set_alpha(alpha_channel)
        if alpha_channel <= 255:
            alpha_channel -= 2
            if alpha_channel == 0:
                reverse = True
            if reverse:
                alpha_channel += 3
        else:
            wait -= 2
            if wait == 0:
                exited = True

        pygame.display.update()
        clock.tick(FPS)

''' меню для пользовательского отображения на ESC '''
class Menu_Uses():

    def __init__(self, save):

        # x = 134; y = -192
        with open(f'data/{save}/data.json', encoding='utf-8') as datafile:
            self.datafile = json.load(datafile)

        self.tutorial_completed = self.datafile['tutorial']
        if not self.tutorial_completed:
            self.helper_items = Helper([{
                "name" : "Использовать предмет",
                "text" : 'для использования нажмите на предмет левой кнопкой мыши, а после нажмите на Е, '
                         'чтобы использовать его\n\n\n' + 'Вы можете прочитать про свойства предмета слева на панели'.capitalize(),
                "buttons" : [],
                "imgs" : [pygame.image.load('sprites/helpers img/inventory help/1.png')]
            }, {
                "name": "Выбросить предмет",
                "text": 'Для того чтобы выбросить все предметы одного типа, выберите предмет, зажмите правую кнопку '
                        'мыши и перенесите его к урне\n\nчтобы поштучно выбрасывать предметы нажмите на Q',
                "buttons": [],
                "imgs": [pygame.image.load('sprites/helpers img/inventory help/2.png')]
            }, {
                "name": "Покупка и продажа товаров",
                "text": 'Продать или купить предметы вы можете на рынке Зетты\n\nстоимость продажи в инвентаре помечена'
                        ' зеленой стрелкой вверх, а стоимость покупки предмета красной стрелкой вниз',
                "buttons": [],
                "imgs": [pygame.image.load('sprites/helpers img/inventory help/3.png')]
            }])

        with open(f'data/{save}/clothes.json', encoding='utf-8') as clothesfile:
            self.clothes = json.load(clothesfile)

        self.open_anim = Animation([pygame.image.load(f'sprites/icons/book/open/{i}.png').convert_alpha() for i in range(15)], 4)
        self.close_anim = Animation([pygame.image.load(f'sprites/icons/book/close/{i}.png').convert_alpha() for i in range(15)], 4)
        self.tabs = [
            pygame.transform.scale(pygame.image.load(f'sprites/icons/book/tabs/{i}.png'),
                                   (1092, 640)).convert_alpha() for i in range(1, 7)
        ]


        self.rect_book = Rect(-64 + 134, -850 + 192,
                              self.open_anim.list_sprites[0].get_width(), self.open_anim.list_sprites[1].get_height())
        self.opened = True
        self.closed = True


        self.closing = False
        self.opening = False

        self.counter = 0
        # добавить коллайдеры
        self.rect_main = Rect(90, 122, 35, 28)
        self.rect_inventory = Rect(90, 175, 35, 28)
        self.rect_view = Rect(90, 230, 35, 28)
        self.rect_tasks = Rect(90, 282, 35, 28)
        self.rect_save = Rect(90, 337, 35, 28)
        self.rect_settings = Rect(90, 391, 35, 28)
        self.rect = 1

        self.executes = {
            1 : self.render_main,
            2 : self.render_inventory,
            3 : self.render_view,
            4 : self.render_tasks,
            5 : self.render_save,
            6 : self.render_settings
        }

        self.save_alert = pygame.image.load('sprites/icons/alerts/long-alert.png').convert_alpha()
        self.font_1_32 = pygame.font.Font('fonts/Hardpixel-nn51.otf', 32)
        self.font_1_48 = pygame.font.Font('fonts/Hardpixel-nn51.otf', 48)
        self.font_1_24 = pygame.font.Font('fonts/Hardpixel-nn51.otf', 24)
        self.font_1_16 = pygame.font.Font('fonts/Hardpixel-nn51.otf', 16)
        self.font_1_14 = pygame.font.Font('fonts/Hardpixel-nn51.otf', 13)
        self.font_2_10 = pygame.font.Font('fonts/rus-pixel.otf', 10)

        self.font_3_12 = pygame.font.Font('fonts/PixeloidSans.ttf', 12)
        self.font_3_14 = pygame.font.Font('fonts/PixeloidSans.ttf', 12)
        self.font_3_32 = pygame.font.Font('fonts/PixeloidSans.ttf', 32)


        self.font_2_32 = pygame.font.Font('fonts/rus-pixel.otf', 32)
        self.font_2_48 = pygame.font.Font('fonts/rus-pixel.otf', 48)
        self.font_2_16 = pygame.font.Font('fonts/rus-pixel.otf', 16)

        self.btn_save = Rect(180, 180, 440 - 180, 224 - 180)
        self.color_save = (133, 75, 65)

        self.btn_save_exit = Rect(180, 240, 510 - 180, 224 - 180)
        self.color_save_exit = (133, 75, 65)

        self.btn_exit = Rect(180, 300, 430 - 180, 224 - 180)
        self.color_exit = (133, 75, 65)

        self.black_surface = pygame.Surface(SIZE, pygame.DOUBLEBUF)
        self.black_surface.convert_alpha()
        self.black_surface.set_alpha(100)

        self.chose_alert = pygame.image.load('sprites/icons/alerts/chose_alert.png').convert_alpha()
        self.show_save_alert = False

        self.yes_btn_texture = pygame.image.load('sprites/icons/yes_btn.png').convert_alpha()
        self.no_btn_texture = pygame.image.load('sprites/icons/no_btn.png').convert_alpha()

        self.yes_btn = pygame.Rect(530+16, 360, self.yes_btn_texture.get_width(), self.yes_btn_texture.get_height())
        self.no_btn = pygame.Rect(700-16, 360, self.no_btn_texture.get_width(), self.no_btn_texture.get_height())
        # 480 264

        self.health_bar = pygame.transform.scale(
            pygame.image.load('sprites/character UI/health_bar2.png'), (126 * self.datafile['health'] / 100, 10)
        ).convert_alpha()

        self.thirst_bar = pygame.transform.scale(
            pygame.image.load('sprites/character UI/thirst_bar.png'), (126 * self.datafile['thirst'] / 100, 10)
        ).convert_alpha()

        self.hungry_bar = pygame.transform.scale(
            pygame.image.load('sprites/character UI/hungry_bar.png'), (126 * self.datafile['hungry'] / 100, 10)
        ).convert_alpha()

        self.color_worker = {
            'безработный' : (128, 123, 122)
        }


        self.player_head = pygame.transform.scale(
            pygame.image.load('sprites/character UI/head_ico.png'), (96, 96)
        ).convert_alpha()

        self.hear = pygame.transform.scale(
            pygame.image.load(f'sprites/clothes/1/{self.clothes["1"]}/idle.png'), (96,96)
        ).convert_alpha()

        self.bar_long = pygame.transform.scale(
            pygame.image.load('sprites/other gui/health_outline.png'), (325, 35)
        ).convert_alpha()

        self.time_at_day = 'день'
        self.times = [pygame.image.load(f'sprites/time/icons/{i}.png') for i in range(1, 5)]
        self.times_cycles = {
            'ночь' : self.times[-1],
            'рассвет' : self.times[1],
            'день' : self.times[0],
            'закат' : self.times[2],
        }

        self.locations = {
            'train' : 'станция',
            'zetta' : 'зетта',
        }



        with open(f'data/{save}/tasks.json', encoding='utf-8') as tasksfile:
            self.tasks_json = json.load(tasksfile)


        self.tasks = Tasks(self.tasks_json)

        self.pos_reward_x = 334

        self.slider_text = pygame.image.load('sprites/icons/slider.png').convert_alpha()
        self.rect_slider = Rect(1104, 186, self.slider_text.get_width(), self.slider_text.get_height())

        self.attention_ico = pygame.image.load('sprites/icons/attention_ico.png').convert_alpha()

        self.big_attention = pygame.transform.scale(self.attention_ico, (64, 64))

        self.att_rect = Rect(-32, -32, self.attention_ico.get_width(), self.attention_ico.get_height())
        self.att_types = {
            1 : self.rect_main,
            2 : self.rect_inventory,
            3 : self.rect_view,
            4 : self.rect_tasks,
            5 : self.rect_save,
            6 : self.rect_settings
        }
        self.att_type = 0

        self.rect_settings_controls = Rect(320, 200, 123, 38)
        self.rect_settings_audio = Rect(342, 264, 72, 38)
        self.rect_settings_other = Rect(326, 324, 110, 38)

        self.window_render_settings = 1

        self.controls_image = pygame.image.load('sprites/other gui/controls.png').convert_alpha()

        self.w_btn_img = pygame.transform.scale(
            pygame.image.load('sprites/icons/btns/w/1.png').convert_alpha(), (18, 21)
        )
        self.a_btn_img = pygame.transform.scale(
            pygame.image.load('sprites/icons/btns/a/1.png').convert_alpha(), (18, 21)
        )
        self.s_btn_img = pygame.transform.scale(
            pygame.image.load('sprites/icons/btns/s/1.png').convert_alpha(), (18, 21)
        )
        self.d_btn_img = pygame.transform.scale(
            pygame.image.load('sprites/icons/btns/d/1.png').convert_alpha(), (18, 21)
        )

        self.e_btn_img = pygame.transform.scale(
            pygame.image.load('sprites/icons/btns/e/1.png').convert_alpha(), (18, 21)
        )

        self.q_btn_img = pygame.transform.scale(
            pygame.image.load('sprites/icons/btns/q/1.png').convert_alpha(), (18, 21)
        )

        self.esc_btn_img = pygame.transform.scale(
            pygame.image.load('sprites/icons/btns/esc/1.png').convert_alpha(), (33, 21)
        )

        self.rect_music_slider = Rect(0, 204, 12, 12)
        self.rect_sound_slider = Rect(0, 261, 12, 12)

        with open('data/maindata.json', 'r', encoding='utf-8') as file:
            self.main_data_file = json.load(file)

        self.vol_music = self.main_data_file['volume_music']
        self.vol_sound = self.main_data_file['volume_sound']

        self.fps_rect = Rect(1052, 186, self.yes_btn_texture.get_width(), self.yes_btn_texture.get_height())
        self.cam_rect = Rect(1052, 236, self.yes_btn_texture.get_width(), self.yes_btn_texture.get_height())
        self.fullscreen = Rect(1052, 286, self.yes_btn_texture.get_width(), self.yes_btn_texture.get_height())

        self.tired_bar = pygame.transform.scale(
            pygame.image.load('sprites/character UI/tired_bar.png'), (126 * self.datafile['hungry'] / 100, 10)
        ).convert_alpha()

        self.mini_xp_bar = Rect(356, 248, self.datafile['xp']/self.datafile['newlvlxp'] * 100, 10)

        self.obj_inventory = Inventory(save)

        self.trash_rect = Rect(863, 600, 76, 71)
        self.pressed_rmb = False




    def open(self):
        if self.rect_book.y < -136 + 192 and self.counter:
            self.rect_book.y += 16

        else:
            self.rect_book.y = -136 + 192

        if self.open_anim.show_anim_static(self.rect_book.x, self.rect_book.y):
            self.rect_book.y = -136 + 192
            self.opening = True

    def render_win(self):
        self.mouse = pygame.mouse.get_pos()
        print(self.mouse)
        if self.rect in self.executes:

            self.executes[self.rect]()

    def render_main(self):
        window.blit(self.tabs[0], (self.rect_book.x, self.rect_book.y))

        window.blit(self.font_1_48.render('Профиль', True, (102, 57, 49)), (232, 88))

        # window.blit(self.selector, (222, 180))
        window.blit(self.font_1_16.render(f'{self.datafile["name_chr"]}', True, (27, 34, 54)), (355, 162))
        window.blit(self.player_head, (228, 151))
        window.blit(self.hear, (228, 151))

        window.blit(self.font_1_16.render(f'УР {self.datafile["lvl"]}', True, (27, 34, 54)), (256, 245))
        window.blit(self.health_bar, (356, 188))
        window.blit(self.font_2_10.render(f'{self.datafile["health"]}/100', True, (27, 34, 54)), (443, 176))

        window.blit(self.hungry_bar, (356, 216))
        window.blit(self.font_2_10.render(f'{self.datafile["hungry"]}/100', True, (27, 34, 54)), (443, 204))

        window.blit(self.thirst_bar, (356, 244))
        window.blit(self.font_2_10.render(f'{self.datafile["thirst"]}/100', True, (27, 34, 54)), (443, 232))

        window.blit(self.font_2_16.render(f'{self.datafile["money"]}', True, (27, 34, 54)), (400, 264))

        window.blit(self.font_1_24.render('Уровень доверия', True, (27, 34, 54)), (203, 309))
        pygame.draw.rect(window, (143, 93, 56), Rect(230, 345 + 10, 315 * self.datafile["loving"] / 100, 25))
        window.blit(self.bar_long, (225, 340 + 10))
        window.blit(self.font_1_16.render(f'{self.datafile["loving"]}%',
                                          True, (27, 34, 54)), (233, 360))

        window.blit(self.font_1_24.render('Опыт исследования', True, (27, 34, 54)), (203, 400 - 10))
        pygame.draw.rect(window, (223, 139, 95), Rect(230, 440 - 10, 315 * self.datafile["loving"] / 100, 25))
        window.blit(self.bar_long, (225, 435 - 10))
        window.blit(self.font_1_16.render(f'{self.datafile["xp"]}/{self.datafile["newlvlxp"]}',
                                          True, (27, 34, 54)), (233, 434))

        window.blit(self.font_2_16.render('время', True, (27, 34, 54)), (364, 482))
        window.blit(self.font_2_16.render(f'{self.datafile["day"]}', True, (27, 34, 54)), (456, 523))
        window.blit(self.font_2_16.render(f'{timegame}', True, (27, 34, 54)), (472, 546))
        window.blit(self.font_2_16.render(f'{self.datafile["year"]}', True, (27, 34, 54)), (474, 568))
        window.blit(self.font_2_16.render(f'{self.time_at_day}', True, (27, 34, 54)), (262, 545))

        window.blit(self.times_cycles[self.time_at_day], (336 - 20, 514 - 20))
        window.blit(self.font_1_16.render(f'{self.locations[self.datafile["location"]].title()}', True, (27, 34, 54)), (780, 175))

        # window.blit(self.font_1_48.render('Карта', True, (27, 34, 54)), (830, 90))

    def render_inventory(self):
        window.blit(self.tabs[1], (self.rect_book.x, self.rect_book.y))

        window.blit(self.font_1_48.render('Инвентарь', True, (102, 57, 49)), (232, 88))
        window.blit(self.font_1_48.render('Предметы', True, (102, 57, 49)), (762, 88))

        self.obj_inventory.render_inventory_items()

        window.blit(self.font_3_12.render('Вещи', True, (27, 34, 54)), (885, 153))
        window.blit(self.font_3_12.render('Мусор', True, (27, 34, 54)), (883, 580))

        if self.obj_inventory.chosen_item_id:
            window.blit(self.font_1_14.render('Переместите предмет'.upper(), True, (27, 34, 54)), (704, 605))
            window.blit(self.font_1_14.render('для уничтожения!'.upper(), True, (27, 34, 54)), (712, 625))
        else:
            pygame.draw.rect(window, (209, 195, 150), Rect(181, 155, 581 - 181, 591 - 155))
            if len(self.obj_inventory.inventory) != 0:
                window.blit(self.font_3_32.render('Выберите предмет', True, (27, 34, 54)), (225, 301))
                window.blit(self.font_3_32.render('для просмотра', True, (27, 34, 54)), (254, 340))
            else:
                window.blit(self.font_3_32.render('Инвентарь пуст', True, (27, 34, 54)), (235, 301))

        if self.click[2]:
            if self.trash_rect.collidepoint(*self.mouse):
                if self.obj_inventory.taked_item:
                    ''' меняется текстура мусорки '''
                    self.pressed_rmb = True
                    self.item_trash = self.obj_inventory.item_got
        else:
            if self.pressed_rmb:
                if self.trash_rect.collidepoint(*self.mouse) and self.item_trash.typerare != 'квестовый':
                    self.obj_inventory.inventory.remove(self.item_trash)
                    self.pressed_rmb = False
                    self.obj_inventory.chosen_item_id = 0

                else:
                    self.pressed_rmb = False

        if not self.tutorial_completed:
            self.helper_items.render()
            if not self.helper_items.on:
                self.tutorial_completed = True
                del self.helper_items

    def render_view(self):
        window.blit(self.tabs[2], (self.rect_book.x, self.rect_book.y))

        window.blit(self.font_1_48.render('Персонаж', True, (102, 57, 49)), (232, 88))
        window.blit(self.font_1_16.render(f'{self.datafile["name_chr"]}', True, (27, 34, 54)), (355, 168))

        window.blit(self.font_3_14.render('Снаряжение', True, (27, 34, 54)), (343, 308))
        window.blit(self.font_2_16.render(f'{self.datafile["money"]}', True, (27, 34, 54)), (398, 264))
        window.blit(self.font_1_48.render('Снаряжение', True, (102, 57, 49)), (756, 88))

        window.blit(self.font_1_16.render(f'УР {self.datafile["lvl"]}', True, (27, 34, 54)), (256, 248))

        window.blit(self.player_head, (228, 155))
        window.blit(self.hear, (228, 155))

        window.blit(self.health_bar, (356, 192))
        window.blit(self.font_2_10.render(f'{self.datafile["health"]}/100', True, (27, 34, 54)), (443, 180))

        window.blit(self.tired_bar, (356, 220))
        window.blit(self.font_2_10.render(f'{self.datafile["hungry"]}/100', True, (27, 34, 54)), (443, 208))

        window.blit(self.font_3_14.render('прическа', True, (27, 34, 54)), (265, 332))
        window.blit(self.font_3_14.render('тело', True, (27, 34, 54)), (366, 332))
        window.blit(self.font_3_14.render('низ', True, (27, 34, 54)), (455, 332))
        window.blit(self.font_3_14.render('руки', True, (27, 34, 54)), (280, 420))
        window.blit(self.font_3_14.render('браслеты', True, (27, 34, 54)), (348, 420))
        window.blit(self.font_3_14.render('обувь', True, (27, 34, 54)), (450, 420))

        window.blit(pygame.transform.scale(self.hear, (60, 60)), (266, 352))

        pygame.draw.rect(window, (97, 165, 63), self.mini_xp_bar)
        window.blit(self.font_2_10.render(f'{self.datafile["xp"]}/{self.datafile["newlvlxp"]}', True, (27, 34, 54)), (443, 236))

        window.blit(self.font_3_14.render('Вещи', True, (27, 34, 54)), (891, 152))

        window.blit(self.font_3_14.render('Мусор', True, (27, 34, 54)), (883, 580))

        if self.obj_inventory.chosen_item_id != 0:
            window.blit(self.font_1_14.render('Переместите предмет'.upper(), True, (27, 34, 54)), (704, 605))
            window.blit(self.font_1_14.render('для уничтожения!'.upper(), True, (27, 34, 54)), (712, 625))

        self.obj_inventory.render_clothes()
        self.obj_inventory.render_character_clothes()

        if self.click[2]:
            if self.trash_rect.collidepoint(*self.mouse):
                if self.obj_inventory.taked_item:
                    ''' меняется текстура мусорки '''
                    self.pressed_rmb = True
                    self.item_trash = self.obj_inventory.item_got
        else:
            if self.pressed_rmb:
                if self.trash_rect.collidepoint(*self.mouse):
                    self.obj_inventory.clothes.remove(self.item_trash)
                    self.pressed_rmb = False
                    self.obj_inventory.chosen_item_id = 0
                else:
                    self.pressed_rmb = False




    def render_tasks(self):
        self.click = pygame.mouse.get_pressed()
        self.mouse = pygame.mouse.get_pos()

        window.blit(self.tabs[3], (self.rect_book.x, self.rect_book.y))

        window.blit(self.font_1_48.render('Подробности', True, (102, 57, 49)), (232, 88))
        window.blit(self.font_1_48.render('Задания', True, (102, 57, 49)), (810, 88))


        for event in pygame.event.get():
            if self.mouse[0] in range(686, 1111) and self.mouse[1] in range(185, 613):
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 4:
                    if self.tasks.y < 0 and self.rect_slider.y < self.tasks.height_task:

                        self.tasks.y += 15
                        self.tasks.update_pos_tasks()
                        self.rect_slider.y -= self.tasks.added

                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 5:
                    if self.rect_slider.y < self.tasks.height_task:

                        self.tasks.y -= 15
                        self.tasks.update_pos_tasks()
                        self.rect_slider.y += self.tasks.added

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.counter = abs(self.counter - 1)

        if self.rect_slider.y > self.tasks.height_task:
            self.tasks.y += 15
            self.rect_slider.y -= self.tasks.added

        self.tasks.render_tasks()

        window.blit(self.slider_text, (self.rect_slider.x, self.rect_slider.y))

        self.task_chose = self.tasks.task_chose

        window.blit(self.font_1_14.render(f'{self.task_chose.by}', True, (27, 34, 54)), (334, 164))
        window.blit(self.font_1_14.render(f'Задание{self.task_chose.number_of_task}: {self.task_chose.name_task}', True, (27, 34, 54)), (334, 188))
        window.blit(self.font_1_14.render('< Награда >', True, (27, 34, 54)), (334, 212))

        window.blit(self.font_1_16.render('ИНФО', True, (27, 34, 54)), (360, 285))

        for reward_type, reward_count in self.task_chose.reward.items():
            window.blit(REWARDS[reward_type], (self.pos_reward_x, 238))
            window.blit(self.font_1_16.render(f'x{reward_count}', True, (27, 34, 54)), (self.pos_reward_x + 36, 244))
            self.pos_reward_x += 90

        window.blit(self.font_1_16.render(f'{self.task_chose.steps_name_list[-1]}', True, (115, 66, 150)), (295, 320))

        self.pos_reward_x = 334

        blit_multilines((500, 181), f'{self.task_chose.steps_desc_list[-1]}', (286, 349), self.font_1_16, (87, 57, 34))
        window.blit(self.big_attention, (242, 172))

    def render_save(self):
        window.blit(self.tabs[4], (self.rect_book.x, self.rect_book.y))

        window.blit(self.font_1_48.render('Сохранение', True, (102, 57, 49)), (232, 88))
        window.blit(self.font_1_32.render('сохранить игру', True, self.color_save),
                    (self.btn_save.x, self.btn_save.y))

        window.blit(self.font_1_32.render('сохранить и выйти', True, self.color_save_exit),
                    (self.btn_save_exit.x, self.btn_save_exit.y))

        window.blit(self.font_1_32.render('выйти в меню', True, self.color_exit),
                    (self.btn_exit.x, self.btn_exit.y))

        self.btn_save, self.color_save = self.chose_btn(self.btn_save, self.save_check)
        self.btn_save_exit, self.color_save_exit = self.chose_btn(self.btn_save_exit, lambda: self.save_check(exit_menu=True))
        self.btn_exit, self.color_exit = self.chose_btn(self.btn_exit, self.exit_to_menu)

        if self.show_save_alert:
            self.save_progress()

    def render_settings(self):
        window.blit(self.tabs[5], (self.rect_book.x, self.rect_book.y))

        window.blit(self.font_1_48.render('Настройки', True, (102, 57, 49)), (232, 88))
        window.blit(self.font_1_16.render('опции'.title(), True, (27, 34, 54)), (357, 158))
        window.blit(self.font_1_16.render('управление', True, (27, 34, 54)), (330, 208))
        window.blit(self.font_1_16.render('звуки', True, (27, 34, 54)), (360, 270))
        window.blit(self.font_1_16.render('прочее', True, (27, 34, 54)), (350, 333))



        window.blit(self.font_1_14.render('ВАЖНО', True, (27, 34, 54)), (362, 420))

        window.blit(self.font_1_14.render('После изменений, настройки', True, (27, 34, 54)), (260, 468))
        window.blit(self.font_1_14.render('автоматически сохраняются', True, (27, 34, 54)), (260, 488))

        if self.click[0]:
            if self.rect_settings_controls.collidepoint(*self.mouse):
                self.window_render_settings = 1

            elif self.rect_settings_audio.collidepoint(*self.mouse):
                self.window_render_settings = 2

            elif self.rect_settings_other.collidepoint(*self.mouse):
                self.window_render_settings = 3


        if self.window_render_settings == 1:
            self.settings_controls()

        elif self.window_render_settings == 2:
            self.settings_audio()

        elif self.window_render_settings == 3:
            self.settings_other()

    def settings_controls(self):
        window.blit(self.font_1_48.render('Управление', True, (102, 57, 49)), (762, 88))

        window.blit(self.controls_image, (700, 120))

        window.blit(self.font_1_16.render('Вперед', True, (27, 34, 54)), (750, 185))
        window.blit(self.font_1_16.render('Назад', True, (27, 34, 54)), (750, 225))
        window.blit(self.font_1_16.render('Вправо', True, (27, 34, 54)), (750, 265))
        window.blit(self.font_1_16.render('Влево', True, (27, 34, 54)), (750, 302))
        window.blit(self.font_1_16.render('Меню', True, (27, 34, 54)), (750, 340))
        window.blit(self.font_1_16.render('Использовать', True, (27, 34, 54)), (750, 380))
        window.blit(self.font_1_16.render('Выбросить', True, (27, 34, 54)), (750, 420))

        window.blit(self.w_btn_img, (990, 185))
        window.blit(self.s_btn_img, (990, 225))
        window.blit(self.d_btn_img, (990, 265))
        window.blit(self.a_btn_img, (990, 302))
        window.blit(self.esc_btn_img, (984, 340))
        window.blit(self.e_btn_img, (990, 378))
        window.blit(self.q_btn_img, (990, 378 + 38))

    def settings_audio(self):
        window.blit(self.font_1_48.render('Звуки', True, (102, 57, 49)), (830, 88))




        self.rect_music_slider.x = 880 + self.vol_music * 200
        self.rect_sound_slider.x = 880 + self.vol_sound * 200

        self.rect_music_slider.y = 204
        self.rect_sound_slider.y = 261

        window.blit(self.font_1_32.render('музыка', True, (27, 34, 54)), (700, 190))
        window.blit(self.font_1_32.render('звуки', True, (27, 34, 54)), (700, 250))

        pygame.draw.rect(window, (133, 95, 57), Rect(880, 208, 200, 4))
        pygame.draw.rect(window, (133, 95, 57), Rect(880, 265, 200, 4))

        ''' slider '''
        pygame.draw.rect(window, (178, 139, 120), self.rect_music_slider)
        pygame.draw.rect(window, (178, 139, 120), self.rect_sound_slider)

        if self.click[0]:
            if self.mouse[0] in range(880, 1080):
                if self.mouse[1] in range(197, 221):
                    self.rect_music_slider.x = self.mouse[0] - 6
                    self.vol_music = 1 - ((1080 - self.rect_music_slider.x - 4) / 200) - 0.01

                if self.mouse[1] in range(257, 279):

                    self.rect_sound_slider.x = self.mouse[0] - 6
                    self.vol_sound = 1 - ((1080 - self.rect_sound_slider.x - 4) / 200) - 0.01



        self.main_data_file['volume_music'] = self.vol_music
        self.main_data_file['volume_sound'] = self.vol_sound

        with open('data/maindata.json', 'w', encoding='utf-8') as file:
            json.dump(self.main_data_file, file, indent=4)

    def settings_other(self):
        global window
        window.blit(self.font_1_48.render('Прочее', True, (102, 57, 49)), (820, 88))

        window.blit(self.font_1_32.render('FPS', True, (27, 34, 54)), (700, 190))



        if self.main_data_file['FPS']:
            window.blit(self.yes_btn_texture, (self.fps_rect.x, self.fps_rect.y))
        else:
            window.blit(self.no_btn_texture, (self.fps_rect.x, self.fps_rect.y))

        window.blit(self.font_1_32.render('Режим камеры', True, (27, 34, 54)), (700, 240))

        if self.main_data_file['CAMmode']:
            window.blit(self.yes_btn_texture, (self.cam_rect.x, self.cam_rect.y))
        else:
            window.blit(self.no_btn_texture, (self.cam_rect.x, self.cam_rect.y))

        window.blit(self.font_1_32.render('Полный экран', True, (27, 34, 54)), (700, 290))

        if self.main_data_file["FullScreen"]:
            window.blit(self.yes_btn_texture, (self.fullscreen.x, self.fullscreen.y))
        else:
            window.blit(self.no_btn_texture, (self.fullscreen.x, self.fullscreen.y))



        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    if self.fps_rect.collidepoint(*self.mouse):
                        self.main_data_file['FPS'] = abs(self.main_data_file['FPS'] - 1)

                    if self.cam_rect.collidepoint(*self.mouse):
                        self.main_data_file['CAMmode'] = abs(self.main_data_file['CAMmode'] - 1)

                    if self.fullscreen.collidepoint(*self.mouse):
                        self.main_data_file['FullScreen'] = abs(self.main_data_file['FullScreen'] - 1)
                        if self.main_data_file['FullScreen']:
                            window = pygame.display.set_mode((1920, 1080), pygame.FULLSCREEN)
                        else:
                            window = pygame.display.set_mode((1920, 1080))

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.counter = abs(self.counter - 1)




        with open('data/maindata.json', 'w', encoding='utf-8') as file:
            json.dump(self.main_data_file, file, indent=4)

    def exit_to_menu(self):
        pass

    def render_menu(self):
        self.mouse = pygame.mouse.get_pos()
        self.click = pygame.mouse.get_pressed()

        if self.att_type in self.att_types:
            self.att_rect.x = self.att_types[self.att_type].x - 48
            self.att_rect.y = self.att_types[self.att_type].y - 2

        if self.counter == 1 and not self.opening:
            self.open()

        if self.opening and self.counter:
            if self.rect_book.y >= -136 + 192:
                if self.click[0]:
                    if self.rect_main.collidepoint(self.mouse[0], self.mouse[1]):
                        self.rect = 1
                    elif self.rect_settings.collidepoint(self.mouse[0], self.mouse[1]):
                        self.rect = 6
                    elif self.rect_inventory.collidepoint(self.mouse[0], self.mouse[1]):
                        self.rect = 2
                        self.obj_inventory.chosen_item_id = 0
                    elif self.rect_save.collidepoint(self.mouse[0], self.mouse[1]):
                        self.rect = 5
                    elif self.rect_view.collidepoint(self.mouse[0], self.mouse[1]):
                        self.rect = 3
                        self.obj_inventory.chosen_item_id = 0
                    elif self.rect_tasks.collidepoint(self.mouse[0], self.mouse[1]):
                        self.rect = 4
                        self.tasks.y = 0

                if self.att_type == self.rect:
                    self.att_type = 0
                    self.att_rect.x = -32
                    self.att_rect.y = -32

                if self.tasks.ended_quests:
                    window.blit(self.attention_ico, (self.att_rect.x, self.att_rect.y))


                self.render_win()
            else:
                self.counter = 0
                self.rect_book.y -= 16


        if self.counter == 0:
            self.close()

    def close(self):
        if self.rect_book.y > -850 + 192 and not self.counter:
            self.rect_book.y -= 16

        else:
            self.rect_book.y = -850 + 192


        if self.close_anim.show_anim_static(self.rect_book.x, self.rect_book.y):

            self.closing = False
            self.opening = False

    def save_progress(self):
        window.blit(self.black_surface, (0,0))
        self.black_surface.fill((0,0,0))
        window.blit(self.chose_alert, (480, 264))
        window.blit(self.yes_btn_texture, (self.yes_btn.x, self.yes_btn.y))
        window.blit(self.no_btn_texture, (self.no_btn.x, self.no_btn.y))
        window.blit(self.font_1_24.render('сохранить прогресс?', True, (115, 65, 56)), (510, 294))

        if self.click[0]:
            if self.yes_btn.collidepoint(self.mouse[0], self.mouse[1]):
                self.save_info(self.exit_menu)
                self.show_save_alert = False
            elif self.no_btn.collidepoint(self.mouse[0], self.mouse[1]):
                self.show_save_alert = False

    def execute_func_from_entry(self, func=None):
        if func != None:
            func()

    def save_info(self, exit_menu):
        pass

    def save_check(self, exit_menu=False):
        self.exit_menu = exit_menu
        self.show_save_alert = True

    def chose_btn(self, button:Rect, func=None):

        ''' controlling buttons like a func use or hover '''

        self.click = pygame.mouse.get_pressed()
        self.mouse = pygame.mouse.get_pos()
        color = (115, 65, 56)
        if button.collidepoint(self.mouse[0], self.mouse[1]):
            color = (46, 120, 89)

            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1 and func != None:

                        func()
            if self.click[0]:
                func()

        return button, color

''' отображение информации о персонаже на главном экране'''
class CharacterUI():

    parameters_ui = pygame.transform.scale(
        pygame.image.load('sprites/character UI/parameters_top.png'), (385, 160)
    ).convert_alpha()

    font_money = pygame.font.Font('fonts/PixeloidSans.ttf', 24)

    head_character = pygame.image.load('sprites/character UI/head_ico.png').convert_alpha()
    font_location = pygame.font.Font('fonts/Hardpixel-nn51.otf', 48)
    font_16 = pygame.font.Font('fonts/PixeloidSans.ttf', 16)

    string_time = ''

    def __init__(self, save):

        with open(f'data/{save}/clothes.json') as clothesfile:
            self.clothes = json.load(clothesfile)

        with open(f'data/{save}/data.json') as datafile:
            self.data = json.load(datafile)

        self.hear_character = pygame.transform.scale(
            pygame.image.load(f'sprites/clothes/1/{self.clothes["1"]}/idle.png'), (128, 128)
        ).convert_alpha()

        self.health_bar = pygame.transform.scale(
            pygame.image.load('sprites/character UI/health_bar.png'), (245 * (self.data['health'] / 100), 15)
        ).convert_alpha()


        self.locations = {
            'train' : 'Станция',
            'zetta' : 'Зетта'
        }
        self.rect_location = Rect(1280 - 220, 720 - 64, 100, 1)
        self.delay_font_location = 300
        self.speed_font_loc = 0

        self.start_time = datetime.datetime.now()

        self.time_file = self.data['timegame']

        self.seconds = int(self.time_file[0:2]) * 60 + int(self.time_file[3::])
        self.timesecs = 500


    def render(self):
        self.add_time = (datetime.datetime.now() - self.start_time).seconds
        print(self.add_time, 'addtime')
        self.update_time()


        with open('data/maindata.json', 'r') as file:
            jsonfile = json.load(file)
        self.mouse = pygame.mouse.get_pos()
        print(self.mouse)

        if not jsonfile['CAMmode']:
            window.blit(self.parameters_ui, (32, 32))
            window.blit(self.head_character, (32, 48))
            window.blit(self.hear_character, (32, 48))

            window.blit(self.font_money.render(f'{self.data["money"]}', True, (200, 200, 200)), (200, 98))
            window.blit(self.health_bar, (162, 62))

            window.blit(self.font_16.render(f'{timegame}', True, (200, 200, 200)), (172, 140))

        if jsonfile['FPS']:
            window.blit(self.font_location.render(f'{int(clock.get_fps())}', True, (200, 200, 200)), (20, 720 - 64))

    def show_location(self):

        if self.rect_location.x > 1280:
            self.delay_font_location = 300
            self.speed_font_loc = 0

        if self.delay_font_location < 0:
            self.rect_location.x += self.speed_font_loc
            self.speed_font_loc += 1.5
        self.delay_font_location -= 1

        window.blit(self.font_location.render(self.locations[self.data['location']], True, (240, 240, 240)),
                    (self.rect_location.x, self.rect_location.y))

    def update_time(self):
        global timegame
        self.timesecs = (self.seconds + int(self.add_time))
        if self.timesecs >= 1440:
            self.timesecs = 0
            self.seconds = 0
            self.start_time = datetime.datetime.now()

        if self.timesecs // 60 < 10:
            timegame = f"0{self.timesecs // 60}"
        else:
            timegame = f"{self.timesecs // 60}"

        if self.timesecs % 60 < 10:
            timegame += f":0{self.timesecs % 60}"
        else:
            timegame += f":{self.timesecs % 60}"
