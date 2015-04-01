import pygame
from essen_vars import NONE, GAME, OPTIONS, SINGLEPLAYER
import CustomClasses
import mymath

pygame.init()

resolution = (600, 800)

window = pygame.display.set_mode(resolution)
clock = pygame.time.Clock()

mode = NONE

floors = []
curFloor = None
curRoom = None
player = None

if __name__ == "__main__":
    mode = GAME

    #CustomClasses.Floor
    floors.append(CustomClasses.Floor())
    curFloor = floors[0]
    curRoom = curFloor.rooms[0]

    player = CustomClasses.Player(100, mymath.Vector2(300, 400))




done = False
while not done:
    dtime = clock.tick()

    evtList = pygame.event.get()
    for evt in evtList:
        if evt.type == pygame.QUIT:
            done = True

    if mode == GAME:
        pass

    player.update(dtime, evtList)

    curRoom.render()
    player.render()

    window.fill((0, 0, 0))

    pygame.display.flip()
pygame.quit()