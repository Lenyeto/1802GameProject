import pygame
import MapSystem
from EntityClasses import *
import mymath
import equipment

pygame.init()

resolution = (640, 800)


window = pygame.display.set_mode(resolution)
clock = pygame.time.Clock()

list_of_keys = []

Players = []
Players.append(Player(mymath.Vector2(100, 100), 100, True))

room_size = (640, 640)
roomSurface = pygame.Surface((640, 640))

hudSurface = pygame.Surface((640, 160))



Floor = MapSystem.Floor(roomSurface)


done = False
while not done:
    dtime = clock.tick()

    evtList = pygame.event.get()
    for evt in evtList:
        if evt.type == pygame.QUIT:
            done = True
        elif evt.type == pygame.KEYDOWN:
            list_of_keys.append(evt.key)
        elif evt.type == pygame.KEYUP:
            list_of_keys.remove(evt.key)

    Floor.update(Players, roomSurface)

    for i in Floor.cur_room.entities:
        if isinstance(i, WeaponStand):
            i.update(dtime, Players)
        else:
            if i.update(dtime):
                Floor.cur_room.entities.remove(i)
    for i in Floor.cur_room.entities:
        if isinstance(i, Dummy):
            i.AI(Players, dtime)



    for i in Players:
        i.update(dtime, list_of_keys, Floor.cur_room.entities)


    roomSurface.fill((0, 0, 0))
    Floor.cur_room.render(roomSurface)
    for i in Players:
        i.render(roomSurface)
    window.blit(roomSurface, (0, 0))
    window.blit(hudSurface, (0, 640))
    pygame.display.flip()
pygame.quit()
