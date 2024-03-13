import pygame



class Button:
    """
               класс для управления кнопками

               методы
               __init__()
               функции:
               process()
               create_buttons()
               image_yes
               btn_press
    """

    def __init__(self,win, number, x, y, width, height, text=None, text2=None, image=None, one_press=False):
        """инциализация атрибутов класса"""
        self.number = number
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.one_press = one_press
        self.alreadyPressed = False
        self.image = image
        self.text = text
        self.text2 = text2
        self.number_c = [8, 11]
        self.fillColors = {
            # ffffff
            'normal': '#c0c0c0',
            'hover': '#666666',
            'pressed': '#333333',
        }
        self.Color = self.fillColors['normal']

        self.buttonSurface = pygame.Surface((self.width, self.height))

        self.buttonRect = pygame.Rect(self.x, self.y, self.width, self.height)
        pygame.draw.rect(self.buttonSurface, (0, 255, 0), (0, 0, self.width - 1, self.height - 1), 1)
        font = pygame.font.SysFont('Arial', 40)
        self.buttonSurf = font.render(self.text, True, (0, 0, 0))

        win.objects.append(self)

    def process(self,win):
        """функция меняет внешний вид кнопки и проверяет нажание и наведение мыши на нее"""
        mouse_pos = pygame.mouse.get_pos()
        self.buttonSurface.fill(self.fillColors['normal'])
        if self.buttonRect.collidepoint(mouse_pos):
            self.buttonSurface.fill(self.fillColors['hover'])
            if pygame.mouse.get_pressed(num_buttons=3)[0]:
                self.buttonSurface.fill(self.fillColors['pressed'])
                self.btn_press(win)
                if self.one_press:
                    self.alreadyPressed = True
                elif not self.alreadyPressed:
                    self.alreadyPressed = True
                self.alreadyPressed = True
            else:
                self.alreadyPressed = False

        pygame.draw.rect(self.buttonSurface, self.Color, (0, 0, self.width - 1, self.height - 1), 2)
        self.buttonSurface.blit(self.buttonSurf, [self.buttonRect.width / 2 - self.buttonSurf.get_rect().width / 2,
                                                  self.buttonRect.height / 2 - self.buttonSurf.get_rect().height / 2])
        win.sc.blit(self.buttonSurface, self.buttonRect)
        return self.alreadyPressed

    def image_yes(self):
        """функция для оформления элементов меню с картинкой"""
        if self.image is not None:
            surf = pygame.image.load(self.image).convert_alpha()
            self.buttonSurface.blit(surf, (10, 10))
            font_style = pygame.font.SysFont('arial', 40)
            text = font_style.render(self.text2, True, (0, 255, 0))  # оформление
            text_rect = text.get_rect(center=(self.width / 2, 200))
            self.buttonSurface.blit(text, text_rect)

    def btn_press(self,win):
        """функция для выделения выбранного элемента меню"""
        for btn in win.objects:
            if self.height == 240 and btn.height == 240:
                btn.Color = self.fillColors['normal']
                self.Color = self.fillColors['hover']
            if self.height == 65 and btn.height == 65:
                btn.Color = self.fillColors['normal']
                self.Color = self.fillColors['hover']


