import pygame


class imgload(object):

    """ this class will grab the spritesheet image and return a list of the image objects
    """
    def __init__(self, imglocation, width=64, height=64, name="None"):
        self.name = name
        self.spritelist = []
        img = pygame.image.load(imglocation).convert_alpha()
        self.spriteheight = height
        self.spritewidth = width

        for y in range(0, img.get_height(), self.spriteheight):
            for x in range(0, img.get_width(), self.spritewidth):
                tmpimg = img.subsurface((x, y, self.spritewidth, self.spriteheight))
                self.spritelist.append(tmpimg)

        return self.spritelist