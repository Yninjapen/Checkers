import pygame

black = (0, 0, 0)
white = (255, 255, 255)
green = (0, 255, 0)
red = (255, 0, 0)
blue = (0, 0, 255)
grey = (127, 127, 127)
dark_grey = (80, 80, 80)

def darken_color(color):
    r, g, b = color
    r = int(r*.5)
    g = int(g*.5)
    b = int(b*.5)
    return r, g, b

class Slider:
    def __init__(self, length, menu_pos, font: pygame.font.Font, extremes: tuple = (0, 10), descriptor: str = '', display_precision: int = 0) -> None:
        self.length = length
        self.height = length//20
        self.slider_height = self.height*1.5
        self.slider_width = self.slider_height / 4

        self.extremes = self.min, self.max = min(extremes), max(extremes)
        self.range = self.max - self.min
        self.middle = (self.min + self.max)/2
        self.set_value(self.middle)

        self.menu_pos = self.menu_x, self.menu_y = menu_pos

        self.bar_color = grey
        self.slider_color = dark_grey

        self.dimensions = self.x_dims, self.y_dims = (0, self.length), (-self.height*.25, self.height*1.25)

        self.min_y, self.max_y = self.menu_y, self.menu_y + self.y_dims[1]
        self.min_x, self.max_x = self.menu_x, self.menu_x + self.length

        self.descriptor = descriptor
        self.display_precision = display_precision
        self.font = font
        self.init_text()

    def init_text(self):
        self.text = self.font.render(self.descriptor, True, white)
        self.text_rect = self.text.get_rect()
        self.text_rect.center = self.menu_x + self.length/2, self.menu_y

        self.text1 = self.font.render(str(round(self.value, self.display_precision)), True, white)
        self.text1_rect = self.text1.get_rect()
        self.text1_rect.center = self.menu_x + self.length/2, self.menu_y + self.height

    def draw(self, screen, menu):
        # draws bar
        x = menu.pos[0] + self.menu_x
        y = menu.pos[1] + self.menu_y + menu.scroll_pos
        pygame.draw.rect(screen, self.bar_color, pygame.Rect(x, y, self.length, self.height))

        # draws slider
        x = menu.pos[0] + self.menu_x + self.length*self.slider_pos
        y = y - self.height*.25
        pygame.draw.rect(screen, self.slider_color, pygame.Rect(x, y, self.slider_width, self.slider_height))

        # draws necessary text
        
        x = menu.pos[0] + self.menu_x
        y = menu.pos[1] + self.menu_y + menu.scroll_pos

        self.text_rect.center = x + self.length/2, y - self.height/2

        self.text1 = self.font.render(str(round(self.value, self.display_precision)), True, white)
        self.text1_rect = self.text1.get_rect()
        self.text1_rect.center = x + self.length/2, y + self.height*1.5

        screen.blit(self.text, self.text_rect)
        screen.blit(self.text1, self.text1_rect)

    # click should already be in terms of menu positioning
    def handle_click(self, click):
        x = click[0] - self.menu_x
        y = click[1] - self.menu_y
        if (x >= self.x_dims[0]) and (x <= self.x_dims[1]) and (y >= self.y_dims[0]) and (y <= self.y_dims[1]):
            self.slider_pos = (click[0] - self.menu_x)/self.length
            self.value = self.min + self.range*self.slider_pos

    def set_value(self, value):
        self.value = value
        self.slider_pos = value/self.range

class Button:

    def __init__(self, menu_pos, label: str, dimensions, font: pygame.font.Font, text_color = white, button_color = grey) -> None:
        self.label = label

        self.menu_pos = self.menu_x, self.menu_y = menu_pos
        self.dimensions = self.width, self.height = dimensions
        self.bounds = self.min_x, self.max_x, self.min_y, self.max_y = self.menu_x, self.menu_x + self.width, self.menu_y, self.menu_y + self.height

        self.font = font
        self.text_color = text_color
        self.button_color = button_color
        self.select_color = darken_color(self.button_color)

        self.selected = False

        self.init_text()

    def init_text(self):
        self.text = self.font.render(self.label, True, self.text_color)
        self.text_rect = self.text.get_rect()
        self.text_rect.center = self.menu_x + self.width/2, self.menu_y + self.height/2

    def draw(self, screen, menu):
        x = menu.pos[0] + self.menu_x
        y = menu.pos[1] + self.menu_y + menu.scroll_pos

        self.text_rect.center = x + self.width/2, y + self.height/2

        if self.selected:
            color = self.select_color
        else:
            color = self.button_color

        rect = pygame.Rect(x, y, self.width, self.height)
        pygame.draw.rect(screen, color, rect)

        screen.blit(self.text, self.text_rect)

    def pos_in_button(self, menu_pos):
        x, y = menu_pos
        return (x >= self.min_x) and (x <= self.max_x) and (y >= self.min_y) and (y <= self.max_y)

    def handle_click(self, click):
        if self.pos_in_button(click):
            self.selected = not self.selected

class Button_Group:

    def __init__(self, width, menu_pos, labels: list[str], font: pygame.font.Font, buttons_per_row: int = 3) -> None:
        self.width = width
        self.buttons_per_row = buttons_per_row
        self.button_width = (self.width*.8)//self.buttons_per_row
        self.rows = (len(labels)%self.buttons_per_row)
        self.button_height = (self.button_width/2)
        self.height = self.button_height*self.rows

        self.menu_pos = self.menu_x, self.menu_y = menu_pos

        self.labels = labels
        self.font = font
        self.buttons = []
        self.selected_button = None
        self.init_buttons()

        self.min_y, self.max_y = self.buttons[0].min_y, self.buttons[-1].max_y
        self.min_x, self.max_x = self.buttons[0].min_x, self.menu_x + self.width

    def init_buttons(self):
        start = self.menu_x + self.width*.1, self.menu_y
        row = -1
        for i, label in enumerate(self.labels):
            if i%self.buttons_per_row == 0:
                row += 1
            menu_pos = start[0] + self.button_width*(i%self.buttons_per_row), start[1] + self.button_height*(row)
            self.buttons.append(Button(menu_pos, label, (self.button_width, self.button_height), self.font))

        self.buttons[-1].selected = True
        self.selected_button = self.buttons[-1]

    def draw_buttons(self, screen, menu):
        for button in self.buttons:
            button.draw(screen, menu)

    def draw(self, screen, menu):
        self.draw_buttons(screen, menu)

    def deselect_all(self):
        for button in self.buttons:
            button.selected = False
        self.selected_button = None

    def select_button(self, button):
        button.selected = True
        self.selected_button = button

    def handle_click(self, click):
        for button in self.buttons:
            if button.pos_in_button(click):
                self.deselect_all()
                self.select_button(button)
                return button

class Menu:
    # takes in the physical menu position and dimensions (in pixels) and 
    # a list containing the numerical upper and lower ends of each slider
    # as well as the spacing between each slider
    def __init__(self, tl_pos, dimensions: tuple, spacing: int = 30) -> None:
        self.pos = int(tl_pos[0]), int(tl_pos[1])
        self.size = self.width, self.height = int(dimensions[0]), int(dimensions[1])
        self.spacing = max(spacing, 1)
        self.elements = []
        self.scroll_pos = 0
        self.bounds = self.min_x, self.max_x, self.min_y, self.max_y = tl_pos[0] - 1, tl_pos[0] + self.width + 1, tl_pos[1] - 1, tl_pos[1] + self.height + 1
        
        self.max_scroll = 0

    def draw_elements(self, screen):
        for element in self.elements:
            real_y = (self.pos[1] + element.menu_y + element.height + self.scroll_pos)
            element.draw(screen, self)###
            # if (real_y <= self.max_y) and (real_y >= self.min_y):
            #     element.draw(screen, self)

    def to_menu_pos(self, click_pos):
        x, y = click_pos
        x -= self.pos[0]
        y -= self.pos[1]
        y -= self.scroll_pos
        return x, y

    def pos_in_menu(self, pos):
        x, y = pos
        return (x >= self.min_x) and (x <= self.max_x) and (y >= self.min_y) and (y <= self.max_y)

    def find_nearest(self, menu_pos):
        x, y = menu_pos
        min_dif = 100000
        nearest = self.elements[0]
        for element in self.elements:
            dif = (y - element.menu_y)
            if (dif <= min_dif) and (y > element.min_y):
                min_dif = dif
                nearest = element

        return nearest

    def update(self, screen):
        if not self.elements:
            return

        keys = pygame.key.get_pressed()

        if pygame.mouse.get_pressed()[0]:
            click = pygame.mouse.get_pos()
            pos = self.to_menu_pos(click)
            nearest = self.find_nearest(pos)
            real_y = (self.pos[1] + nearest.menu_y + self.scroll_pos)
            if (self.pos_in_menu(click)) and (real_y <= self.max_y) and (real_y >= self.min_y):
                nearest.handle_click(pos)

        if keys[pygame.K_UP]:
            x, y = pygame.mouse.get_pos()
            if self.pos_in_menu((x, y)):
                self.scroll_pos += 1
                self.scroll_pos = max(min(0, self.scroll_pos), self.max_scroll)
        
        if keys[pygame.K_DOWN]:
            x, y = pygame.mouse.get_pos()
            if self.pos_in_menu((x, y)):
                self.scroll_pos -= 1
                self.scroll_pos = max(min(0, self.scroll_pos), self.max_scroll)

        for event in pygame.event.get(pygame.MOUSEWHEEL):
            x, y = pygame.mouse.get_pos()
            if self.pos_in_menu((x, y)):
                self.scroll_pos += event.y * 40
                self.scroll_pos = max(min(0, self.scroll_pos), self.max_scroll)

        self.draw_elements(screen)

    def add_slider(self, upper, lower, display_precision: int = 0, descriptor: str = ''):
        if not self.elements:
            pos = (int(self.width*.1), 0)
        else:
            pos = (int(self.width*.1), int(self.elements[-1].max_y+self.spacing))

        font = pygame.font.Font(None, round((self.width*.8)//20))
        slider = Slider(int(self.width*.8), pos, font, (upper, lower), descriptor, display_precision)
        self.elements.append(slider)
        self.max_scroll = min(-(slider.max_y + slider.height) + self.height, 0)
        return slider

    def add_button_group(self, labels: list[str], buttons_per_row: int = 3, font: str = None):
        if len(labels) < buttons_per_row:
            x = int(self.width*.1)
        else:
            x = 0

        if not self.elements:
            pos = (x, 0)
        else:
            pos = (x, int(self.elements[-1].max_y+self.spacing))

        font_size = int(((self.width*.8)//buttons_per_row)/5)
        font = pygame.font.Font(font, font_size)

        group = Button_Group(self.width, pos, labels, font, buttons_per_row)
        self.elements.append(group)
        self.max_scroll = min(-(group.max_y + group.height) + self.height, 0)
        return group

    def add_button(self, label: str, font: str = None):
        if not self.elements:
            pos = (0, 0)
        else:
            pos = (int(self.width*.1), int(self.elements[-1].max_y+self.spacing))

        font_size = int((self.width*.8)/5)
        font = pygame.font.Font(font, font_size)

        button = Button(pos, label, (self.width * .8, self.height * .4), font)

        self.elements.append(button)
        self.max_scroll = min(-(button.max_y + button.height) + self.height, 0)

        return button