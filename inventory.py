import pygame
pygame.init()
from pygame.locals import *
from engine import *
from constants import *
import json


class RareItemSimple():

    cansell = True
    icorare = pygame.image.load('sprites/icons/inventory patterns/simple_item_pattern.png').convert_alpha()

    def render(self, item, cords:tuple):
        window.blit(self.icorare, (cords[0], cords[1]))
        window.blit(item, (cords[0], cords[1]))

class RareItemMedium():

    cansell = True
    icorare = pygame.image.load('sprites/icons/inventory patterns/medium_item_pattern.png').convert_alpha()
    def render(self, item, cords: tuple):
        window.blit(self.icorare, (cords[0], cords[1]))
        window.blit(item, (cords[0], cords[1]))

class RareItemQuests():

    cansell = False
    icorare = pygame.image.load('sprites/icons/inventory patterns/quest_item_pattern.png').convert_alpha()

    def render(self, item, cords: tuple):
        window.blit(self.icorare, (cords[0], cords[1]))
        window.blit(item, (cords[0], cords[1]))

class RareItemLegendary():

    cansell = True
    icorare = pygame.image.load('sprites/icons/inventory patterns/legendary_item_pattern.png').convert_alpha()

    def render(self, item, cords: tuple):
        window.blit(self.icorare, (cords[0], cords[1]))
        window.blit(item, (cords[0], cords[1]))

class Inventory():

    hovered_texture = pygame.image.load('sprites/other gui/hovered_item.png').convert_alpha()

    def __init__(self, save):
        with open(f'data/{save}/inventory.json', encoding='utf-8') as file:
            self.inventory_file = json.load(file)

        with open(f'data/{save}/clothes.json', encoding='utf-8') as file:
            self.clothes_save = json.load(file)

        self.clothes = [ObjInventory(i) for i in self.inventory_file["clothes"]]

        self.inventory = [
            ItemInventory(ITEMS[i], counts) for i, counts in self.inventory_file["inventory"].items()
        ]

        self.clothes = self._set_rects(self.clothes)
        self.inventory = self._set_rects(self.inventory)

        self.chosen_item_id = 0
        self.rect_hovered = None
        self.item_got = None

        self.taked_item = False

        self.update_character_clothes = False
        self.delay_drop = -1
        self.return_delay = 50

    def _set_rects(self, cells:list):
        x = -76
        y = 0
        for item in cells:
            item.id = cells.index(item) + 1
            x += 76
            item.collider_item.x += x
            item.collider_item.y += y
            if x > 992:
                x = 0
                y += 64

        return cells


    def render_clothes(self): # одежда
        self.mouse = pygame.mouse.get_pos()
        self.click = pygame.mouse.get_pressed()

        for item in self.clothes:
            item.render()

            if self.click[0]:
                if item.collider_item.collidepoint(*self.mouse):
                    self.chosen_item_id = item.id
                    self.rect_hovered = item.collider_item
                    self.item_got = item

            if self.click[2]:
                if self.chosen_item_id == item.id:
                    if not (item.path in self.list_clothes_weared):
                        item.rect_taked.x, item.rect_taked.y = self.mouse[0] - 26, self.mouse[1] - 26
                        window.blit(item.image_obj_taked, (item.rect_taked.x, item.rect_taked.y))
                        self.taked_item = True
                    else:
                        self.taked_item = False


            if self.chosen_item_id:
                window.blit(self.hovered_texture, (self.rect_hovered.x - 6, self.rect_hovered.y - 6))


    def render_inventory_items(self): # инвентарь предметов
        self.mouse = pygame.mouse.get_pos()
        self.click = pygame.mouse.get_pressed()
        self.key = pygame.key.get_pressed()

        for item in self.inventory:
            item.render()
            if self.click[0]:
                if item.collider_item.collidepoint(*self.mouse):
                    self.chosen_item_id = item.id
                    self.rect_hovered = item.collider_item
                    self.item_got = item

            if self.click[2]:
                if self.chosen_item_id == item.id:
                    item.rect_taked.x, item.rect_taked.y = self.mouse[0] - 26, self.mouse[1] - 26
                    window.blit(item.taked_obj_image, (item.rect_taked.x, item.rect_taked.y))
                    self.taked_item = True

            if self.chosen_item_id:
                window.blit(self.hovered_texture, (self.rect_hovered.x - 6, self.rect_hovered.y - 6))
                self.item_got.render_info_obj()

                if self.key[pygame.K_q] and self.item_got.typerare != 'квестовый':
                    if self.delay_drop > 0:
                        self.delay_drop -= 1
                    else:
                        self.delay_drop = self.return_delay
                        self.return_delay = int(self.return_delay * 0.8)
                        self.item_got.count -= 1
                        if self.item_got.count == 0:
                            self.inventory.remove(self.item_got)
                            self.chosen_item_id = 0

                else:
                    self.delay_drop = -1
                    self.return_delay = 50



    def render_character_clothes(self):
        x = 0
        y = 0
        self.list_clothes_weared = [None, None, None, None, None]
        counter = 0

        for types, clothes in self.clothes_save.items():
            counter += 1
            if types == '1':
                continue
            x += 86
            if x > 440:
                x = 0
                y += 90

            window.blit(
                pygame.image.load(f'sprites/items/{CLOTHES[f"{types}/{clothes}"]}/idle.png').convert_alpha(),
                (270 + x, 352 + y)
            )
            self.list_clothes_weared[counter] = f'{CLOTHES[f"{types}/{clothes}"]}'

        self.wear_clothes()

    def wear_clothes(self):
        self.button = pygame.key.get_pressed()

        if self.chosen_item_id != 0:
            if self.button[pygame.K_e]:
                for keys, values in CLOTHES.items():
                    if values == self.item_got.path:
                        ''' замениться значение в сохраненном файле игры на новое из CLOTHES '''
                        self.clothes_save[f"{keys[0]}"] = keys[2::]
                        self.update_character_clothes = True




class ObjInventory():

    rares = {
        'обычный': RareItemSimple,
        'редкий': RareItemMedium,
        'квестовый': RareItemQuests,
        'легендарный': RareItemLegendary
    }

    def __init__(self, path):

        self.path = path # логическое наименование предмета

        self.image_obj = pygame.image.load(f'sprites/items/{self.path}/idle.png').convert_alpha()
        self.collider_item = Rect(764, 180, self.image_obj.get_width(), self.image_obj.get_height())
        self.hovered = False
        self.id = 0
        self.image_obj_taked = pygame.image.load(f'sprites/items/{self.path}/idle.png').convert_alpha()
        self.image_obj_taked.set_alpha(175)
        self.rect_taked = Rect(0, 0, self.image_obj_taked.get_width(), self.image_obj.get_height())
        self.rare = self.rares[CLOTHES_RARES[self.path]]()

    def render(self):
        self.rare.render(self.image_obj, (self.collider_item.x, self.collider_item.y))




class ItemInventory():

    rares = {
        'обычный' : RareItemSimple,
        'редкий' : RareItemMedium,
        'квестовый' : RareItemQuests,
        'легендарный' : RareItemLegendary
    }

    font_14px = pygame.font.Font('fonts/Hardpixel-nn51.otf', 14)
    font_14px_2 = pygame.font.Font('fonts/PixeloidSans.ttf', 14)
    font_16px = pygame.font.Font('fonts/Hardpixel-nn51.otf', 16)
    buy_ico = pygame.image.load('sprites/icons/buy_ico.png').convert_alpha()
    sell_ico = pygame.image.load('sprites/icons/sell_ico.png').convert_alpha()
    font_10px_2 = pygame.font.Font('fonts/PixeloidSans.ttf', 10)
    font_12px_2 = pygame.font.Font('fonts/PixeloidSans.ttf', 12)

    def __init__(self, info:dict, count):

        self.id = 0
        self.hovered = False

        self.use = info['use'] # можно ли использовать

        self.name = info['name']
        self.location = info['location']
        self.buy = info['buy'] # цена за покупку
        self.sell = info['sell'] # цена за продажу
        self.count = count # количество этого предмета

        if self.use:
            self.properties = ITEM_PROPERTIES[self.name]


        self.typerare = info['rare'] # редкость предмета
        self.rare = self.rares[self.typerare]()


        self.cansell = self.rares[info['rare']].cansell

        self.path = ITEMS[self.name]['path'] # путь до изображения

        self.obj_image = pygame.image.load(f'sprites/items/{self.path}/idle.png').convert_alpha()
        self.taked_obj_image = pygame.image.load(f'sprites/items/{self.path}/idle.png').convert_alpha()
        self.taked_obj_image.set_alpha(175)

        self.rect_taked = Rect(0, 0, self.taked_obj_image.get_width(), self.taked_obj_image.get_height())

        self.collider_item = Rect(758, 186, self.obj_image.get_width(), self.obj_image.get_height())
        self.describe = ITEMS[self.name]['describe']

        self.big_img = pygame.transform.scale(self.obj_image, (88, 88))
        # self.big_rare_texture = pygame.transform.scale(
        #     self.rare.icorare, (88, 88)
        # )

    def render(self):
        self.rare.render(self.obj_image, (self.collider_item.x, self.collider_item.y))
        window.blit(self.font_14px.render(f'x{self.count}', True, (27, 34, 54)),
                    (self.collider_item.x + 2, self.collider_item.y + 35))

    def render_info_obj(self):
        # window.blit(self.big_rare_texture, (336, 168))
        window.blit(self.big_img, (336, 168))
        window.blit(self.font_14px_2.render(f'{self.name}'.title(), True, (27, 34, 54)), (336, 144))
        if self.use:
            y = 0
            for key, value in self.properties.items():
                window.blit(self.font_14px_2.render(f'{key.title()}', True, (27, 34, 54)), (320, 306 + y))
                window.blit(self.font_14px_2.render(f'+{value}', True, (27, 34, 54)), (422, 306 + y))
                y += 26
        else:
            window.blit(self.font_14px_2.render('--', True, (27, 34, 54)), (375, 306))
            window.blit(self.font_14px_2.render('--', True, (27, 34, 54)), (375, 332))

        window.blit(self.font_14px_2.render(f'Тип: {self.typerare.title()}', True, (27, 34, 54)), (320, 358))
        window.blit(self.font_14px_2.render(f'{self.location.title()}', True, (27, 34, 54)), (320, 388))

        window.blit(self.buy_ico, (310, 422))
        window.blit(self.font_14px_2.render(f'{self.buy}', True, (27, 34, 54)), (326, 424))

        window.blit(self.sell_ico, (396, 422))
        window.blit(self.font_14px_2.render(f'{self.sell}', True, (27, 34, 54)), (412, 424))

        window.blit(self.font_10px_2.render('Инфо', True, (27, 34, 54)), (370, 480))

        window.blit(self.font_14px_2.render(f'{self.name.title()}', True, (27, 34, 54)), (266, 512))

        blit_multilines((560, 28), f"{self.describe.capitalize()}", (262, 534), self.font_14px_2, (51, 39, 42))

        window.blit(self.font_14px_2.render('Описание', True, (27, 34, 54)), (348, 270))
