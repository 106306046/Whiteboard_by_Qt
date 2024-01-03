#TODO:COLOR

import numpy as np
from datetime import datetime

import sys
import pygame
from pygame import Surface, time
from pygame.locals import *
from pathlib import Path

# --- path ---

path = Path('./P2_20231117')

# --- constants ---

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
YELLOW = (255, 255, 0)


# --- classes ---

class Button():

    def __init__(self, name, color, rect, time, target_f, img=None, text=None):
        self.name = name
        self.color = color
        self.rect = rect
        self.target_f = target_f
        self.delay = 1000 / target_f
        self.time = time + self.delay
        self.show = False
        self.show_portion = 0.5
        self.time_buffer = []
        self.maxBuffer = 16
        self.font_size = 40
        self.font_color = WHITE
        if img:
            self.img = pygame.transform.scale(img, (80, 80))
        else:
            self.img = None
        if text:
            font = pygame.font.SysFont("simhei", self.font_size)
            t = font.render(text, True, self.font_color)
            self.text = t
        else:
            self.text = None

    def draw(self, screen):
        if self.show:
            pygame.draw.rect(screen, self.color, self.rect)
            pygame.draw.rect(screen, BLACK, self.rect, 5)
            if self.img:
                screen.blit(
                    self.img, (self.rect[0] + self.rect[2] / 2 - 40, self.rect[1] + self.rect[3] / 2 - 40))
            elif self.text:
                text_width = self.text.get_width()
                text_height = self.text.get_height()
                screen.blit(self.text, (
                self.rect[0] + self.rect[2] / 2 - text_width / 2, self.rect[1] + self.rect[3] / 2 - text_height / 2))

    def update(self, current_time):
        if current_time >= self.time:
            if self.show:
                # show
                self.time = current_time + self.delay * self.show_portion
            else:
                # no-show
                self.time = current_time + self.delay * (1 - self.show_portion)
            self.show = not self.show
            if self.show:
                self.time_buffer.append(current_time)
                if (len(self.time_buffer) > self.maxBuffer):
                    dif = np.diff(self.time_buffer)
                    actual_f = 1000 / np.mean(dif)
                    if actual_f - self.target_f > 0.05:
                        self.delay += 0.5
                    elif actual_f - self.target_f < 0.05:
                        self.delay -= 0.5
                    self.time_buffer.clear()

    # print the average time interval per blink of the button
    def observe(self):
        if (len(self.time_buffer) > 1):
            dif = np.diff(self.time_buffer)
            actual_f = 1000 / np.mean(dif)
            print(
                f" {self.name} | Sample: {len(self.time_buffer):2d} | Actual Frequency: {actual_f:.5f} Hz | Delay: {self.delay:.5f} ms    \r",
                end="\b")

    def get_rect(self) -> pygame.Rect:
        return pygame.Rect(self.rect)

class Canvas():

    def __init__(self, color, rect):
        self.color = color
        self.rect = rect
        self.canvas = Surface((rect[2], rect[3])).convert()
        self.canvas.fill(color)

    def draw(self, screen):
        screen.blit(self.canvas, (self.rect[0], self.rect[1]))
        pygame.draw.rect(screen, BLACK, self.rect, 5)

    def add_brush(self, color, position, size):
        pygame.draw.circle(self.canvas, color, (position[0] - self.rect[0], position[1] - self.rect[1]), size, 0)

    def add_rect(self, color, rect, size):
        pygame.draw.rect(self.canvas, color, (rect[0] - self.rect[0], rect[1] - self.rect[1],rect[2],rect[3]), size)

    def add_circle(self, color, rect, size):
        pygame.draw.ellipse(self.canvas, color, (rect[0] - self.rect[0], rect[1] - self.rect[1],rect[2],rect[3]), size)

    def reset(self):
        self.canvas.fill(self.color)

    def save(self):
        current_time = datetime.now()
        time_string = current_time.strftime(f"%Y%m%d_%H%M%S")
        str_path = str(path)
        name = str_path + "/saveimg/paint_" + time_string + ".png"
        pygame.image.save(self.canvas, name)
        return name

    def load(self,image_path):
        self.canvas = pygame.image.load(image_path).convert()

    def get_rect(self) -> pygame.Rect:
        return pygame.Rect(self.rect)

# pygame initialize
pygame.init()


# UI Settings
WIDTH, HEIGHT = 1000, 600
W1 = 200
H1 = 120
BACKGROUND_COLOR = 255, 255, 225
CANVAS_COLOR = 255, 255, 255
CAPTION = "BCI Drawing"
MARGIN1 = 10
MARGIN2 = 10
BRUSH_COLOR = BLACK

start_point = 600, 300
mouse = start_point[:]

pygame.display.set_caption(CAPTION)
screen = pygame.display.set_mode((WIDTH, HEIGHT))

# build objects
canvas = Canvas(
    color=CANVAS_COLOR,
    rect=(
        MARGIN1 * 2 + W1,  # x coordinate
        MARGIN1,  # y coordinate
        WIDTH - MARGIN1 * 3 - W1,  # width
        HEIGHT - MARGIN1 * 2  # height
    )
)

current_time = pygame.time.get_ticks()


button_A = Button(
    name="Undo/Redo",
    color=BLACK,
    rect=(
        MARGIN1,  # x coordinate
        MARGIN1,  # y coordinate
        W1 - MARGIN2,  # width
        H1  # height
    ),
    time=current_time,
    target_f=4.3,  # target frequency
    img=pygame.image.load(path / 'icons' / 'undo.png'),
)

button_B = Button(
    name="Eraser",
    color=BLACK,
    rect=(
        MARGIN1,  # x coordinate
        MARGIN1 + H1 + 20*MARGIN1,  # y coordinate
        W1 - MARGIN2,  # width
        H1  # height
    ),
    time=current_time,
    target_f=7.6,  # target frequency
    img=pygame.image.load(path / 'icons' / 'eraser.png'),
)

button_C = Button(
    name="Color",
    color=BLACK,
    rect=(
        MARGIN1,  # x coordinate
        MARGIN1 + 2*H1 + 8*MARGIN1,  # y coordinate
        W1 - MARGIN2,  # width
        H1  # height
    ),
    time=current_time,
    target_f=10,  # target frequency
    img=pygame.image.load(path / 'icons' / 'color.png'),
)

button_D = Button(
    name="Pencil",
    color=BLACK,
    rect=(
        600-W1/2,  # x coordinate
        300-H1/2,  # y coordinate
        W1 - MARGIN2,  # width
        H1  # height
    ),
    time=current_time,
    target_f=10,  # target frequency
    img=pygame.image.load(path / 'icons' / 'pencil.png'),
)

button_E = Button(
    name="Done",
    color=BLACK,
    rect=(
        MARGIN1,  # x coordinate
        HEIGHT - MARGIN1 - H1,  # y coordinate
        W1,  # width
        H1  # height
    ),
    time=current_time,
    target_f=6,  # target frequency
    img=pygame.image.load(path / 'icons' / 'check.png'),
)
button_list = [button_A, button_B, button_D, button_E]

# --- Clock, fps ---
"""
fps = 60
"""
clock = pygame.time.Clock()

# --- events ---
running = True
in_menu = True
in_check = 0
last_order = ['','','']
move_step = 10
mode = 'menu'
pencil_color = BLACK
last2save = ["",""]
newsave = canvas.save()
last2save = [last2save[1], newsave]


#standby mode:
screen.fill(BACKGROUND_COLOR)
canvas.draw(screen)
for button in button_list:
    button.show = True
    button.draw(screen)
pygame.display.update()

standby = True
while standby:
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            standby = False
    # start if space is pressed

#start drawing
while running:
    # clock.tick(fps)

    #read the predict order
    with open(path / 'log.txt', 'r') as f:
        last_line = f.readlines()[-1].split()
        if (last_order != last_line):
            print("get new order:\n" + str(last_line))
            last_order = last_line
            MI_input = last_order[2]
            SSVEP_input = last_order[3]

            if mode == 'menu':
                in_menu = True
                mouse = start_point[:]
                if SSVEP_input == 'A':
                    if last2save[0] != "":
                        canvas.load(last2save[0])
                        mode = 'redo_menu'
                        button_A.img = pygame.transform.scale(pygame.image.load(path / 'icons' / 'redo.png'), (80, 80))
                    print('switch to Undo mode')
                elif SSVEP_input == 'B':
                    mode = 'cursor_mode'
                    next_mode = 'eraser_mode'
                    print('switch to Eraser mode')
                elif SSVEP_input == 'C':
                    mode = 'color_mode'
                    print('switch to Color mode')
                elif SSVEP_input == 'D':
                    mode = 'cursor_mode'
                    next_mode = 'pencil_mode'
                    print('switch to Pencil mode')

            elif mode == 'redo_menu':
                in_menu = True
                mouse = start_point[:]
                if SSVEP_input == 'A':
                    canvas.load(last2save[1])
                    mode = 'menu'
                    button_A.img = pygame.transform.scale(pygame.image.load(path / 'icons' / 'undo.png'), (80, 80))
                    print('switch to Redo mode')
                elif SSVEP_input == 'B':
                    mode = 'cursor_mode'
                    next_mode = 'eraser_mode'
                    print('switch to Eraser mode')
                elif SSVEP_input == 'C':
                    mode = 'color_mode'
                    print('switch to Color mode')
                elif SSVEP_input == 'D':
                    mode = 'cursor_mode'
                    next_mode = 'pencil_mode'
                    print('switch to Pencil mode')

            # EEG-mouse control system
            elif mode == 'cursor_mode':
                in_menu = False

                # EEG-mouse control system
                if SSVEP_input == 'E': #END
                    first_pt = mouse
                    mode = next_mode
                    in_check = 0
                    button_E.show = False

                elif MI_input == 'idle':
                    in_check = min(3,in_check+1)

                elif MI_input == 'Right':
                    mouse = mouse[0] + move_step, mouse[1]
                    in_check = max(0,in_check - 1)
                elif MI_input == 'Left':
                    mouse = mouse[0] - move_step, mouse[1]
                    in_check = max(0,in_check - 1)
                elif MI_input == 'Down':
                    mouse = mouse[0], mouse[1] + move_step
                    in_check = max(0,in_check - 1)
                elif MI_input == 'Up':
                    mouse = mouse[0], mouse[1] - move_step
                    in_check = max(0,in_check - 1)

            elif mode == 'pencil_mode':
                print('test')

                canvas.add_brush(
                    color=pencil_color,
                    position=mouse,
                    size=10
                )

                if SSVEP_input == 'E': #END
                    mode = 'menu'
                    in_check = 0
                    newsave = canvas.save()
                    last2save = [last2save[1], newsave]

                elif MI_input == 'idle':
                    in_check = min(3,in_check+1)
                elif MI_input == 'Right':
                    for step in range(move_step):
                        canvas.add_brush(
                            color=pencil_color,
                            position=[mouse[0] + step, mouse[1]],
                            size=10
                        )
                    mouse = mouse[0] + move_step, mouse[1]
                    in_check = max(0,in_check - 1)
                elif MI_input == 'Left':
                    for step in range(move_step):
                        canvas.add_brush(
                            color=pencil_color,
                            position=(mouse[0] - step, mouse[1]),
                            size=10
                        )
                    mouse = mouse[0] - move_step, mouse[1]
                    in_check = max(0,in_check - 1)
                elif MI_input == 'Down':
                    for step in range(move_step):
                        canvas.add_brush(
                            color=pencil_color,
                            position=(mouse[0] , mouse[1]+step),
                            size=10
                        )
                    mouse = mouse[0], mouse[1] + move_step
                    in_check = max(0,in_check - 1)
                elif MI_input == 'Up':
                    for step in range(move_step):
                        canvas.add_brush(
                            color=pencil_color,
                            position=(mouse[0], mouse[1]-step),
                            size=10
                        )
                    mouse = mouse[0], mouse[1] - move_step
                    in_check = max(0,in_check - 1)

            elif mode == 'eraser_mode':

                canvas.add_brush(
                    color=WHITE,
                    position=mouse,
                    size=10
                )

                if SSVEP_input == 'E': #END
                    mode = 'menu'
                    in_check = 0
                    newsave = canvas.save()
                    last2save = [last2save[1],newsave]

                elif MI_input == 'idle':
                    in_check = min(3,in_check+1)
                elif MI_input == 'Right':
                    mouse = mouse[0] + move_step, mouse[1]
                    in_check = max(0,in_check - 1)
                elif MI_input == 'Left':
                    mouse = mouse[0] - move_step, mouse[1]
                    in_check = max(0,in_check - 1)
                elif MI_input == 'Down':
                    mouse = mouse[0], mouse[1] + move_step
                    in_check = max(0,in_check - 1)
                elif MI_input == 'Up':
                    mouse = mouse[0], mouse[1] - move_step
                    in_check = max(0,in_check - 1)

            elif mode == 'color_mode':
                continue
                #TODO

            elif mode == 'rectangle':
                # EEG-mouse control system
                if SSVEP_input == 'E':  # END
                    temp_rect = [min(rect_first_pt[0], mouse[0]), min(rect_first_pt[1], mouse[1]),
                                 max(abs(rect_first_pt[0] - mouse[0]), 1), max(abs(rect_first_pt[1] - mouse[1]), 1)]
                    canvas.add_rect(BLACK,temp_rect,4)
                    mode = 'menu'
                elif MI_input == 'Right':
                    mouse = mouse[0] + move_step, mouse[1]
                elif MI_input == 'Left':
                    mouse = mouse[0] - move_step, mouse[1]
                elif MI_input == 'Down':
                    mouse = mouse[0], mouse[1] + move_step
                elif MI_input == 'Up':
                    mouse = mouse[0], mouse[1] - move_step

            elif mode == 'circle':
                # EEG-mouse control system
                if SSVEP_input == 'E':  # END
                    temp_rect = [min(rect_first_pt[0], mouse[0]), min(rect_first_pt[1], mouse[1]),
                                 max(abs(rect_first_pt[0] - mouse[0]), 1), max(abs(rect_first_pt[1] - mouse[1]), 1)]
                    canvas.add_circle(BLACK,temp_rect,4)
                    mode = 'menu'
                elif MI_input == 'Right':
                    mouse = mouse[0] + move_step, mouse[1]
                elif MI_input == 'Left':
                    mouse = mouse[0] - move_step, mouse[1]
                elif MI_input == 'Down':
                    mouse = mouse[0], mouse[1] + move_step
                elif MI_input == 'Up':
                    mouse = mouse[0], mouse[1] - move_step


    # Aux func: not control by EEG

    ## --- events ---
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.VIDEORESIZE:
            print("The Pygame window is now " + str(event.w) + " pixels wide and " + str(event.h) + " pixels high")
            WIDTH, HEIGHT = event.size
            if WIDTH < min_width:
                WIDTH = min_width
            if HEIGHT < min_height:
                HEIGHT = min_height
            screen = pygame.display.set_mode((WIDTH, HEIGHT), HWSURFACE | DOUBLEBUF | RESIZABLE)
            CANVAS_SIZE = (WIDTH - MARGIN1 * 2) / 2, HEIGHT - MARGIN1 * 2
            screen.fill(BACKGROUND_COLOR)
            canvas = pygame.transform.scale(canvas, CANVAS_SIZE)
        elif event.type == pygame.KEYDOWN:
            # Save canvas when "S" is pressed
            if event.key == pygame.K_s:
                canvas.save()
            # Reset canvas when "R" is pressed
            if event.key == pygame.K_r:
                canvas.reset()
            # Open/Close button blinking when "F" is pressed
            if event.key == pygame.K_f:
                is_flashing = not is_flashing

        if event.type == MOUSEBUTTONDOWN:
            mouse_pos = pygame.mouse.get_pos()
            for button in button_list:
                if button.get_rect().collidepoint(mouse_pos):
                    print(button.name + " got pressed")
                    if button.name == 'Undo/Redo':
                        if last2save[0] != "":
                            canvas.load(last2save[0])
                            mode = 'redo_menu'
                            button_A.img = pygame.image.load(path / 'icons' / 'redo.png')
                        print('switch to Undo mode')
                    elif button.name == 'Eraser':
                        mode = 'cursor_mode'
                        next_mode = 'eraser_mode'
                        print('switch to Eraser mode')
                    elif button.name == 'Color':
                        mode = 'color_mode'
                        print('switch to Color mode')
                    elif button.name == 'Pencil':
                        mode = 'cursor_mode'
                        next_mode = 'pencil_mode'
                        print('switch to Pencil mode')


    ## mouse in control bar
    if pygame.mouse.get_pressed()[0]:
        mouse_pos = pygame.mouse.get_pos()
        if canvas.get_rect().collidepoint(mouse_pos):
            canvas.add_brush(
                color=BRUSH_COLOR,
                position=mouse_pos,
                size=10
            )
    ## mouse in canvas
    if pygame.mouse.get_pressed()[0]:
        mouse_pos = pygame.mouse.get_pos()
        if canvas.get_rect().collidepoint(mouse_pos):
            canvas.add_brush(
                color=BRUSH_COLOR,
                position=mouse_pos,
                size=10
            )



    # --- SSVEP control system ---
    if in_menu == True:
        current_time = pygame.time.get_ticks()
        for button in button_list[:-1]:
            button.update(current_time)
        button_E.show = False
    else:
        for button in button_list[:-1]:
            button.show = False
        if in_check >= 3:
            current_time = pygame.time.get_ticks()
            button_E.update(current_time)



    # --- draws ---
    screen.fill(BACKGROUND_COLOR)
    canvas.draw(screen)
    for button in button_list:
        button.draw(screen)

    #button_back.observe()     # Uncomment to observe actual frequency of button

    #preview mouse, rect, etc.
    if mode == 'cursor_mode' or mode == 'pencil_mode':
        #pygame.draw.circle(screen, RED,mouse, 4)
        img = pygame.image.load(path / 'icons' / 'cursor.png')
        cursor_size = 30
        img = pygame.transform.scale(img, (cursor_size, cursor_size))
        screen.blit(img, (mouse[0]-cursor_size/2,mouse[1]-cursor_size/2))
    elif mode == 'eraser_mode':
        pygame.draw.circle(screen, RED,mouse, 10)
    """
    elif mode == 'rectangle':
        temp_rect = [min(first_pt[0],mouse[0]), min(first_pt[1],mouse[1]),
                    max(abs(first_pt[0]-mouse[0]),1), max(abs(first_pt[1]-mouse[1]),1)]
        pygame.draw.rect(screen, RED, temp_rect, 4)
    elif mode == 'rectangle':
        temp_rect = [min(first_pt[0],mouse[0]), min(first_pt[1],mouse[1]),
                    max(abs(first_pt[0]-mouse[0]),1), max(abs(first_pt[1]-mouse[1]),1)]
        pygame.draw.rect(screen, RED, temp_rect, 4)
    elif mode == 'circle':
        temp_rect = [min(first_pt[0],mouse[0]), min(first_pt[1],mouse[1]),
                    max(abs(first_pt[0]-mouse[0]),1), max(abs(first_pt[1]-mouse[1]),1)]
        pygame.draw.ellipse(screen, RED, temp_rect, 4)
        """


    pygame.display.update()



print("Ended" + " " * 100)
pygame.quit()