from EntityClasses import *
from mymath import *
import math
import pygame

DOWN = mymath.Vector2(0, 1)
UP = mymath.Vector2(0, -1)
RIGHT = mymath.Vector2(1, 0)
LEFT = mymath.Vector2(-1, 0)
IDLE = mymath.Vector2(0, 0)

class Imgload(object):
    def __init__(self, imglocation="Assets/Graphics/Players/PlaceHolder.png", width=64, height=64, name="None"):

        """
        :param imglocation: refers to the location of an image file on the machine
        :param width: refers to the width of each frame in the spritesheet
        :param height: refers to the height of the spritesheet
        :param name: just a reference
        :return: returns a list of image objects that can be blit to a surface
        """

        self.name = name
        self.spritelist = []
        img = pygame.image.load(imglocation).convert_alpha()
        self.spriteheight = height
        self.spritewidth = width

        for y in range(0, img.get_height(), self.spriteheight):
            for x in range(0, img.get_width(), self.spritewidth):
                tmpimg = img.subsurface((x, y, self.spritewidth, self.spriteheight))
                self.spritelist.append(tmpimg)

    def getlist(self):
        return self.spritelist


class Animate(object):

    def __init__(self, entity, sprites):
        """

        :param entity: This will be the creature or player entity
        :param sprites: A list of the sprite frames

        """
        self.Entity = entity
        self.SpriteSheet = sprites
        self.frame = 0
        self.forward = True

    def getimg(self, size=32):
        """

        :return: returns a single image based on the current frame and direction
        """
        tmplist = self.SpriteSheet

        if self.Entity.direction == RIGHT:
            tmplist = []
            for i in range(0, 3):
                tmplist.append(self.SpriteSheet[i])

        elif self.Entity.direction == UP:
            tmplist = []
            for i in range(3, 6):
                tmplist.append(self.SpriteSheet[i])

        elif self.Entity.direction == LEFT:
            tmplist = []
            for i in range(6, 9):
                tmplist.append(self.SpriteSheet[i])

        elif self.Entity.direction == DOWN:
            tmplist = []
            for i in range(9, 12):
                tmplist.append(self.SpriteSheet[i])



        tmptmplist = []
        for i in tmplist:
            tmptmplist.append(pygame.transform.scale(i, (size, size)))


        if self.Entity.direction != IDLE:
            return tmptmplist[math.floor(self.frame)]
        else:
            return tmptmplist[11]

    def update(self, dtime):
        k = 15  # magnitude

        if self.forward:
            if self.Entity.direction != IDLE:
                self.frame += (self.Entity.speed * dtime / 1000) * k
            else:
                self.frame = 2
        else:
            if self.Entity.direction != IDLE:
                self.frame -= (self.Entity.speed * dtime / 1000) * k
            else:
                self.frame = 2

        if self.frame <= 0:
            self.frame = 0
            self.forward = True
        elif self.frame >= 3:
            self.frame = 2
            self.forward = False




if __name__ == "__main__":  # Testing
    pygame.init()
    win = pygame.display.set_mode((800, 600))
    clock = pygame.time.Clock()
    keys = []
    player = Player(Vector2(100, 100))

    done = False
    while not done:

        dtime = clock.tick()

        # input
        evtList = pygame.event.get()
        for evt in evtList:
            if evt.type == pygame.QUIT:
                done = True
            elif evt.type == pygame.KEYDOWN:
                keys.append(evt.key)
            elif evt.type == pygame.KEYUP:
                keys.remove(evt.key)

        # update

        player.update(dtime, keys, [])

        # render
        
        win.fill((0, 0, 0))
        player.render(win)

        pygame.display.flip()
