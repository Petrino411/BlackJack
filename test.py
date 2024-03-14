# Imports
import sys
import pygame

from Button import Button


class Win:
    def __init__(self):

        # Configuration
        pygame.init()
        self.fps = 60
        self.fpsClock = pygame.time.Clock()
        self.width, height = 640, 480
        self.sc = pygame.display.set_mode((self.width, height))

        self.font = pygame.font.SysFont('Arial', 40)

        self.objects = []
        self.b1 = Button(self, 30, 30, 400, 100, 'Button One (onePress)', self.myFunction)
        self.b2 = Button(self, 30, 140, 400, 100, 'Button Two (multiPress)', self.myFunction, True)



    def play(self):

        while True:
            self.sc.fill((20, 20, 20))
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            for object in self.objects:
                object.process()
            pygame.display.flip()
            self.fpsClock.tick(self.fps)

    def myFunction(self):
        print('Button Pressed')


win = Win()
win.play()
