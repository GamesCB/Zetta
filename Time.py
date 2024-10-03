import pygame
pygame.init()
from pygame.locals import *

from engine import *
import datetime
import json

class Summer_Time():
    def __init__(self, color, alpha):
        self.filter = pygame.Surface(SIZE)
        self.filter.convert_alpha()
        self.alpha_channel = alpha
        self.filter.set_alpha(self.alpha_channel)
        self.color_switcher = color



    def switchtime(self, time):
        if time in range(0, 360):
            self.color_switcher = [34, 32, 60]
        elif time in range(360, 600):
            if self.color_switcher[0] < 232:
                self.color_switcher[0] += 0.02
            else:
                self.color_switcher[0] = 232

            if self.color_switcher[1] < 232:
                self.color_switcher[1] += 0.02
            else:
                self.color_switcher[1] = 232

            if self.color_switcher[2] < 92:
                self.color_switcher[2] += 0.003
            else:
                self.color_switcher[2] = 92

            if self.alpha_channel > 30:
                self.alpha_channel -= 0.01
            else:
                self.alpha_channel = 30

        elif time in range(600, 1020):
            if self.alpha_channel > 0:
                self.alpha_channel -= 0.005
            else:
                self.alpha_channel = 0

        elif time in range(1020, 1110):
            if self.color_switcher[1] > 151:
                self.color_switcher[1] -= 0.01

            if self.alpha_channel < 70:
                self.alpha_channel += 0.02
            else:
                self.alpha_channel = 70

        else:
            if self.color_switcher[0] > 34:
                self.color_switcher[0] -= 0.08
            else:
                self.color_switcher[0] = 34

            if self.color_switcher[1] > 32:
                self.color_switcher[1] -= 0.06
            else:
                self.color_switcher[1] = 32

            if self.color_switcher[2] > 60:
                self.color_switcher[2] -= 0.012
            else:
                self.color_switcher[2] = 60

            if self.alpha_channel < 150:
                self.alpha_channel += 0.06
            else:
                self.alpha_channel = 150



        self.filter.set_alpha(self.alpha_channel)
        window.blit(self.filter, (0,0))
        self.filter.fill(self.color_switcher)

class TimeGame():
    def __init__(self, save):
        with open(f'data/{save}/data.json') as datafile:
            self.datafile = json.load(datafile)

        self.timegame = self.datafile['timegame']

        self.maintimeseconds = int(self.timegame[0:2]) * 60 + int(self.timegame[3::])
        self.secs_started = self.maintimeseconds

        if self.datafile['season'] == 'summer':
            self.filter_rendering = Summer_Time(self.datafile['color_filter'], self.datafile['alpha_filter'])

            # if self.maintimeseconds in range(360, 600):
            #     self.filter_rendering.color_switcher = [232, 232, 92]
            #     self.filter_rendering.alpha_channel = 30
            #     self.filter_rendering.filter.set_alpha(self.filter_rendering.alpha_channel)
            # elif self.maintimeseconds in range(600, 1020):
            #     self.filter_rendering.alpha_channel = 0
            #     self.filter_rendering.filter.set_alpha(self.filter_rendering.alpha_channel)
            # elif self.maintimeseconds in range(1020, 1110):
            #     self.filter_rendering.color_switcher = [232, 151, 92]
            #     self.filter_rendering.alpha_channel = 70
            #     self.filter_rendering.filter.set_alpha(self.filter_rendering.alpha_channel)
            # else:
            #     self.filter_rendering.color_switcher = [34, 32, 60]
            #     self.filter_rendering.alpha_channel = 150
            #     self.filter_rendering.filter.set_alpha(self.filter_rendering.alpha_channel)

            print(self.filter_rendering.color_switcher, self.filter_rendering.alpha_channel, 'colors')


        self.start_time = datetime.datetime.now()

    def ticktime(self):
        self.maintimeseconds = self.secs_started + (datetime.datetime.now() - self.start_time).seconds
        print(self.maintimeseconds, 'maintimeseconds')
        if self.maintimeseconds >= 1440:
            self.maintimeseconds = 0

        if self.maintimeseconds == 1440:
            self.maintimeseconds = 0


    def render(self):
        self.ticktime()

        self.filter_rendering.switchtime(self.maintimeseconds)


    def taketime_string(self):
        if self.maintimeseconds // 60 < 10:
            timegame = f"0{self.maintimeseconds // 60}"
        else:
            timegame = f"{self.maintimeseconds // 60}"

        if self.maintimeseconds % 60 < 10:
            timegame += f":0{self.maintimeseconds % 60}"
        else:
            timegame += f":{self.maintimeseconds % 60}"


        return timegame