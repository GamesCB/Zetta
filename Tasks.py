import pygame
pygame.init()
from pygame.locals import *

from engine import *
from textures import *

class Tasks():
    def __init__(self, tasks):
        self.all_tasks = []

        self.convert_task(tasks)

        self.all_tasks[0].allowed = True
        self.task_chose = self.all_tasks[0]

        self.y = 0

        self.max_y = 0
        self.set_pos_tasks()

        self.height_task = self.max_y
        self.added = self.height_task / len(self.all_tasks)

        self.ended_quests = True



    def set_pos_tasks(self):
        for task in self.all_tasks:
            task.rect.y += self.y
            self.y += 50
            if not task.status:
                self.ended_quests = False

        self.max_y = max(self.max_y, self.y)
        self.max_y += 30

        self.y = 0

    def update_pos_tasks(self):
        pass

    def render_tasks(self):
        self.mouse = pygame.mouse.get_pos()
        self.click = pygame.mouse.get_pressed()
        for task in self.all_tasks:
            task.render(self.y)
            if task.allowed:
                self.task_chose.allowed = False
                self.task_chose = task
                self.task_chose.allowed = True



    def convert_task(self, tasks:dict):
        for name, task in tasks.items():

            self.all_tasks.append(Task(name, task))

class Task():

    task_temp = pygame.image.load('sprites/other gui/task_temp.png').convert_alpha()
    task_temp_allowed = pygame.image.load('sprites/other gui/allowed task.png').convert_alpha()

    font = pygame.font.Font('fonts/Hardpixel-nn51.otf', 24)

    def __init__(self, name, task:dict):

        self.name_task = name
        self.infotask = task

        self.by = self.infotask['by']
        self.status = self.infotask['status']
        self.steps_task = self.infotask['task']
        self.number_of_task = self.infotask['number_of_task']
        self.reward = self.infotask['reward']
        self.steps_name_list = []
        self.steps_desc_list = []
        self.allowed = False

        self.rect = Rect(730, 183, 358, 37)


        self.get_stepstask()

    def get_stepstask(self):
        for key, steps in self.steps_task.items():
            print(steps)

            if not steps['status']:
                self.steps_name_list.append(key)
                self.steps_desc_list.append(steps['desc'])
                break

    def __str__(self):
        return self.name_task

    def __repr__(self):
        return self.name_task

    def render(self, y):
        self.rect.y += y
        self.mouse = pygame.mouse.get_pos()
        self.click = pygame.mouse.get_pressed()
        if self.rect.y in range(182, 581):

            if self.rect.collidepoint(*self.mouse) and self.click[0]:
                self.allowed = True
                self.task_chose = self

            window.blit(self.task_temp, (self.rect.x, self.rect.y))
            if self.status:
                window.blit(task_complete, (self.rect.x - 28, self.rect.y + 8))
            else:
                window.blit(task_not_complete, (self.rect.x - 28, self.rect.y + 8))

            if self.allowed:
                window.blit(self.task_temp_allowed, (self.rect.x - 4, self.rect.y - 4))

            window.blit(self.font.render(f'{self.name_task}', True, (27, 34, 54)), (self.rect.x + 8, self.rect.y))
            window.blit(self.font.render(f'Зад{self.number_of_task}', True, (27, 34, 54)), (self.rect.x + 285, self.rect.y))

        self.rect.y -= y


