import pygame
from mymath import *

"""
helm = 0
chest = 1
legs = 2
foot = 3
weapon = 4
offhand = 5
consumable =6
trinkets =7


hp
atk
speed
knockback

"""


class HUD_Element(object):
    def __init__(self, pos=Vector2(0, 0)):
        self.pos = pos

class Image(HUD_Element):
    def __init__(self, pos=Vector2(0, 0)):
        HUD_Element.__init__(self, pos)


class Bar(HUD_Element):
    def __init__(self, height, cur, width, maximum, pos=Vector2(0, 0), color=(255, 0, 0)):
        HUD_Element.__init__(self, pos)
        self.color = color
        self.height = height
        self.cur = cur
        self.width = width
        self.maximum = maximum

    def update(self, cur):
        self.cur = cur

    def render(self, surface):
        pygame.draw.rect(surface, (125, 125, 125), (self.pos.x, self.pos.y, self.width, self.height))
        if not self.cur <= 0:
            pygame.draw.rect(surface, self.color, (self.pos.x, self.pos.y, int((self.cur / self.maximum) * self.width), self.height))

class Text(HUD_Element):
    def __init__(self, pos=Vector2(0, 0)):
        HUD_Element.__init__(self, pos)

class HUD(object):
    def __init__(self, players=[]):
        self.players = players
        self.stats = []
        for i in players:
            self.stats.append(i.stats)
        self.text = pygame.font.Font("Assets/Fonts/FONT.TTF", 10)
        print(self.stats)
        self.Elements = []

        if len(players) == 1:
            self.Elements.append(Bar(20, self.stats[0], 200, 100, Vector2(20, 120)))

    def update(self):
        for i in self.Elements:
            if isinstance(i, Bar):
                i.update(self.players[0].health)
            else:
                i.update()

    def render(self, surface):
        for i in self.Elements:
            i.render(surface)

if __name__ == "__main__":
    import EntityClasses
    pygame.init()
    surface = pygame.display.set_mode((640, 160))
    clock = pygame.time.Clock()

    players = [EntityClasses.Player()]
    hud = HUD(players)

    done = False
    while not done:



        #input
        dtime = clock.tick()

        evtList = pygame.event.get()
        for evt in evtList:
            if evt.type == pygame.QUIT:
                done = True

        players[0].health -= 0.001

        hud.update()

        surface.fill((0, 0, 0))

        hud.render(surface)

        pygame.display.flip()





    pygame.quit()