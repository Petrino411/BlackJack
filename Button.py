import pygame

class Button:

    def __init__(self,win, x, y, width, height, text=None, onclickFunction=None, image=None, one_press=False):
        self.win = win
        self.x = x
        self.y = y
        self.onclickFunction = onclickFunction
        self.width = width
        self.height = height
        self.one_press = one_press
        self.alreadyPressed = False
        self.image = pygame.image.load(image).convert_alpha() if image is not None else None
        self.text = text
        self.number_c = [8, 11]
        self.fillColors = {
            # ffffff
            'normal': '#910000',
            'hover': '#ffbaba',
            'pressed': '#c7adad',
        }
        self.Color = self.fillColors['normal'] if self.image is None else None

        self.buttonSurface = pygame.Surface((self.width, self.height))

        self.buttonRect = pygame.Rect(self.x, self.y, self.width, self.height)

        self.font = pygame.font.SysFont('Arial', 40)
        self.buttonSurf = self.font.render(self.text, True, (255, 255, 255)) if self.image is None else self.font.render("", True, (255, 255, 255))
        self.win.objects.append(self)



    def process(self):
        """функция меняет внешний вид кнопки и проверяет нажание и наведение мыши на нее"""
        mouse_pos = pygame.mouse.get_pos()
        self.buttonSurface.fill(self.fillColors['normal']) if self.image is None else self.buttonSurface.set_colorkey((0, 0, 0))
        if self.buttonRect.collidepoint(mouse_pos):
            self.buttonSurface.fill(self.fillColors['hover']) if self.image is None else self.buttonSurface.set_colorkey((0, 0, 0))
            if pygame.mouse.get_pressed(num_buttons=3)[0]:
                self.buttonSurface.fill(self.fillColors['pressed']) if self.image is None else self.buttonSurface.set_colorkey((0, 0, 0))
                if self.one_press:
                    self.onclickFunction()
                    self.alreadyPressed = True
                elif not self.alreadyPressed:
                    self.onclickFunction()
                    self.alreadyPressed = True
                self.alreadyPressed = True
            else:
                self.alreadyPressed = False
        if self.image is not None:
            self.buttonSurface.set_colorkey((0, 0, 0))
            img = pygame.transform.scale(self.image, (self.width, self.height))
            self.buttonSurface.blit(img, (0,0))

        self.buttonSurface.blit(self.buttonSurf, [self.buttonRect.width / 2 - self.buttonSurf.get_rect().width / 2,
                                                  self.buttonRect.height / 2 - self.buttonSurf.get_rect().height / 2])
        self.win.sc.blit(self.buttonSurface, self.buttonRect)

        return self.alreadyPressed









