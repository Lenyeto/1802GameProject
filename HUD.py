import pygame

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

pygame.init()
surface = pygame.display.set_mode((640, 160))



class HUD(object):
    def __init__(self, player):
        self.player = player
        self.stats = player.stats()
        self.text = pygame.font.Font("Assets/Fonts/FONT.TTF", 10)

    def render(self, surface):





clock = pygame.time.Clock()



done = False
while not done:

    #input
    dtime = clock.tick()

    evtList = pygame.event.get()
    for evt in evtList:
        if evt.type == pygame.QUIT:
            done = True

    surface.fill((125, 125, 125))
    pygame.display.flip()





pygame.quit()