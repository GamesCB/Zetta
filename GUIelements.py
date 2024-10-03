import pygame
pygame.init()
from pygame.locals import *

from engine import *

class Input_Box():
    buttons_en = {
        20: 'q',
        26: 'w',
        8: 'e',
        21: 'r',
        23: 't',
        28: 'y',
        24: 'u',
        12: 'i',
        18: 'o',
        19: 'p',
        4: 'a',
        22: 's',
        7: 'd',
        9: 'f',
        10: 'g',
        11: 'h',
        13: 'j',
        14: 'k',
        15: 'l',
        29: 'z',
        27: 'x',
        6: 'c',
        25: 'v',
        5: 'b',
        17: 'n',
        16: 'm',
        44: ' ',
        30: '1',
        31: '2',
        32: '3',
        33: '4',
        34: '5',
        35: '6',
        36: '7',
        37: '8',
        38: '9',
        39: '0',
    }

    ru_buttons = {
        20: 'й',
        26: 'ц',
        8: 'у',
        21: 'к',
        23: 'е',
        28: 'н',
        24: 'г',
        12: 'ш',
        18: 'щ',
        19: 'х',
        47: 'х',
        48: 'ъ',
        4: 'ф',
        22: 'ы',
        7: 'в',
        9: 'а',
        10: 'п',
        11: 'р',
        13: 'о',
        14: 'л',
        15: 'д',
        51: 'ж',
        52: 'э',
        29: 'я',
        27: 'ч',
        6: 'с',
        25: 'м',
        5: 'и',
        17: 'т',
        16: 'ь',
        54: 'б',
        55: 'ю',
        44: ' ',
        30: '1',
        31: '2',
        32: '3',
        33: '4',
        34: '5',
        35: '6',
        36: '7',
        37: '8',
        38: '9',
        39: '0',
    }

    def __init__(self, font:pygame.font.Font, max_length:int=10, width_rect:int=100):
        self.string = ''

        self.font = font

        self.max_length = max_length
        self.width_rect = width_rect



        self.buttons = self.buttons_en



        self.placeholder = True
        self.apply = False
        self.delayer = 0
        self.lang = 1
        self.button = -1

    def render_input(self, color:tuple, x:int, y:int, placeholder=''):
        self.rect_box = Rect(x, y, self.width_rect, self.font.get_height())
        self.mouse = pygame.mouse.get_pos()
        if self.lang % 2 == 0:
            self.buttons = self.ru_buttons
        else:
            self.buttons = self.buttons_en


        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()



        self.typing = pygame.key.get_pressed()
        self.click_mouse = pygame.mouse.get_pressed()

        if self.click_mouse[0]:
            if self.rect_box.collidepoint(self.mouse[0], self.mouse[1]):
                self.apply = True
                self.placeholder = False
            else:
                self.apply = False
                if len(self.string) == 0:
                    self.placeholder = True


        if self.delayer % 9 == 0:
            if any(self.typing):

                print(self.typing.index(any(self.typing)))
                self.button = self.typing.index(any(self.typing))
                print(self.button)


                if len(self.string) < self.max_length and self.apply:
                    if self.button in self.buttons:
                        self.string += self.buttons[self.button]
                        self.placeholder = False
                        self.delayer += 1

            if self.typing[pygame.K_BACKSPACE] and self.apply:
                if len(self.string) > 0:
                    self.placeholder = False
                    self.string = self.string[0:-1]
                    self.delayer += 1
                else:
                    self.placeholder = True

            if self.button == 225 or self.button == 226:
                ''' меняем язык '''
                self.lang += 1

        else:
            self.delayer += 1

        if self.placeholder:
            window.blit(self.font.render(placeholder, True, (color[0] + 100, color[1] + 100, color[2] + 100)), (x, y))

        window.blit(self.font.render(self.string, True, color), (x, y))

class Alert():


    button_collects = {
        'w': Animation([pygame.image.load(f'sprites/icons/btns/w/{i}.png') for i in range(1, 3)], 40),
        's': Animation([pygame.image.load(f'sprites/icons/btns/s/{i}.png') for i in range(1, 3)], 40),
        'd': Animation([pygame.image.load(f'sprites/icons/btns/d/{i}.png') for i in range(1, 3)], 40),
        'a': Animation([pygame.image.load(f'sprites/icons/btns/a/{i}.png') for i in range(1, 3)], 40),
        'e': Animation([pygame.image.load(f'sprites/icons/btns/e/{i}.png') for i in range(1, 3)], 40),
        'esc': Animation([pygame.image.load(f'sprites/icons/btns/esc/{i}.png') for i in range(1, 3)], 40)
    }

    chose_alert = pygame.image.load('sprites/icons/alerts/chose_alert.png').convert_alpha()
    ok_texture = pygame.image.load('sprites/icons/no_btn.png').convert_alpha()
    font_24 = pygame.font.Font('fonts/Hardpixel-nn51.otf', 24)

    def __init__(self, text='any', button='Q'):
        self.long_alert_text = pygame.image.load('sprites/icons/alerts/long-alert.png').convert_alpha()
        self.font = pygame.font.Font('fonts/Hardpixel-nn51.otf', 32)
        self.text = text

        self.button = button

        self.delay_short_alert = 300

        self.black_surface = pygame.Surface(SIZE)
        self.black_surface.set_alpha(100)

        self.ok_btn = pygame.Rect(615, 365, self.ok_texture.get_width(), self.ok_texture.get_height())


    def short_render_long_alert(self):
        if self.delay_short_alert == 300:
            self.long_alert_text = pygame.transform.scale(self.long_alert_text, (len(self.text) * 21, 64))
        if self.delay_short_alert > 0:
            self.delay_short_alert -= 1

            window.blit(self.long_alert_text, (SIZE[0] - self.long_alert_text.get_width() - 10, 10))
            window.blit(self.font.render(f'{self.text}', True, (20, 20, 20)),
                        (SIZE[0] - self.long_alert_text.get_width() + 25, 25))
        else:
            return True
        return False

    def render_button_allert(self, done:bool):
        if not done:
            self.button_collects[self.button].show_anim_static(
                SIZE[0] - 20 - self.button_collects[self.button].list_sprites[0].get_width(), 20
            )

    def midalert(self, dunders:int=1, x1:int=510, x2:int=510, dun1:str='', dun2:str=''):
        self.mouse = pygame.mouse.get_pos()
        self.click = pygame.mouse.get_pressed()

        window.blit(self.black_surface, (0, 0))
        self.black_surface.fill((0, 0, 0))
        window.blit(self.chose_alert, (480, 264))
        window.blit(self.ok_texture, (self.ok_btn.x, self.ok_btn.y))
        window.blit(self.font_24.render(f'{dun1}', True, (115, 65, 56)), (x1, 294))
        if dunders > 1:
            window.blit(self.font_24.render(f'{dun2}', True, (115, 65, 56)), (x2, 320))

        if self.click[0]:
            if self.ok_btn.collidepoint(self.mouse[0], self.mouse[1]):
                return True

        return False

class Helper():
    display_help = pygame.transform.scale(pygame.image.load('sprites/helpers img/helper win.png'),
                                                 (960, 576)).convert_alpha()
    font_text = pygame.font.Font('fonts/PixeloidSans.ttf', 16)
    font_header = pygame.font.Font('fonts/PixeloidSans.ttf', 32)

    black_filter = pygame.Surface(SIZE).convert_alpha()
    black_filter.set_alpha(100)
    not_used_color = (51, 39, 42)

    def __init__(self, slides:list):
        self.slides = slides
        self.step_slide = 0
        self.on = True
        self.close_btn = Rect(1090, 72, 30, 30)
        for i in self.slides:
            for img in i['imgs']:
                img.convert_alpha()

    def render(self):
        if self.on:
            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        self.step_slide += 1
            self.mouse = pygame.mouse.get_pos()
            self.click = pygame.mouse.get_pressed()

            if self.step_slide == len(self.slides):
                self.on = False
                return

            window.blit(self.black_filter, (0,0))
            window.blit(self.display_help, (160, 72))
            header = self.font_header.render(f'{self.slides[self.step_slide]["name"]}',
                                                True, (234, 224, 221))
            window.blit(header, (SIZE[0]/2 - header.get_width()/2 , 120))

            count_imgs = len(self.slides[self.step_slide]['imgs'])

            blit_multilines((1086, 384), self.slides[self.step_slide]['text'].capitalize(), (720, 196), self.font_text, (200, 200, 200))
            # 721 196

            if count_imgs == 1:

                window.blit(self.slides[self.step_slide]['imgs'][0],
                            ((220, SIZE[1] // 2 - self.slides[self.step_slide]['imgs'][0].get_height() / 2)))

            elif count_imgs == 2:
                ''' позиционирование для двух картинок '''
            else:
                ''' позиционирование для трех картинок '''

            if self.close_btn.collidepoint(self.mouse[0], self.mouse[1]) and self.click[0]:
                self.on = False

            self.draw_circles_slides()


    def draw_circles_slides(self):
        x = 0
        for circ in range(len(self.slides)):
            x += 10
            rect = pygame.draw.circle(window, self.not_used_color, (circ * 15 + 220 + 10 + x, 576), 6)
            if circ == self.step_slide:
                self.x = x

            if rect.collidepoint(self.mouse[0], self.mouse[1]) and self.click[0]:
                self.step_slide = circ



        pygame.draw.circle(window, (241, 235, 219), (self.step_slide * 15 + 220 + 10 + self.x, 576), 6)


def loading():
    pass