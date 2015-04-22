import pygame

class imgload(object):
    def __init__(self, imglocation, width=64, height=64, name="None"):

        """
        :param imglocation: refers to the location of an image file on the machine
        :param width: refers to the width of the spritesheet
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
