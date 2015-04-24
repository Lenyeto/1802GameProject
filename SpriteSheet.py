from EntitiyClasses import *
from mymath import *
import math
import pygame


class Imgload(object):
    def __init__(self, imglocation, width=64, height=64, name="None"):

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

    def getimg(self):
        """

        :return: returns a single image based on the current frame and direction
        """
        tmplist = []

        if self.Entity.direction == RIGHT:
            for i in range(0, 2):
                tmplist.append(self.SpriteSheet[i])

        if self.Entity.direction == UP:
            for i in range(3, 5):
                tmplist.append(self.SpriteSheet[i])

        if self.Entity.direction == LEFT:
            for i in range(6, 8):
                tmplist.append(self.SpriteSheet[i])

        if self.Entity.direction == DOWN:
            for i in range(9, 11):
                tmplist.append(self.SpriteSheet[i])

        if self.Entity.direction != IDLE:
            return tmplist[math.floor(self.frame)]
        else:
            return tmplist[1]

    def update(self, dtime):
        k = 1  # magnitude
        forward = True

        if self.frame <= 0:
            forward = True

        elif self.frame >= 3:
            forward = False

        if forward:
            self.frame += (self.Entity.speed * dtime) * k
        else:
            self.frame -= (self.Entity.speed * dtime) * k


if __name__ == "__main__":  # Testing
    pygame.init()
    win = pygame.display.set_mode((800, 600))
    clock = pygame.time.Clock()
    keys = []
    player = Player()

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