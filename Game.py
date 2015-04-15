import pygame
import MapSystem
import EntitiyClasses
import mymath
import xmlweapons

pygame.init()

resolution = (640, 800)


window = pygame.display.set_mode(resolution)
clock = pygame.time.Clock()

list_of_keys = []

#list_of_entities= [EntitiyClasses.Dummy(mymath.Vector2(200, 200)), EntitiyClasses.Dummy(mymath.Vector2(500, 500)), EntitiyClasses.WeaponStand(xmlweapons.Weapon().getWeapon("Short Bow"), mymath.Vector2(50, 50))]
Players = []
Players.append(EntitiyClasses.Player(mymath.Vector2(100, 100), 100, True))

room_size = (640, 640)
roomSurface = pygame.Surface((640, 640))

hudSurface = pygame.Surface((640, 160))

TestRoom = MapSystem.Room("TYPE")
TestRoom.generate_room(roomSurface)


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

    for i in TestRoom.entities:
        if isinstance(i, EntitiyClasses.WeaponStand):
            i.update(dtime, Players)
        else:
            if i.update(dtime):
                TestRoom.entities.remove(i)
    for i in TestRoom.entities:
        if isinstance(i, EntitiyClasses.Dummy):
            i.AI(Players, dtime)



    for i in Players:
        i.update(dtime, list_of_keys, TestRoom.entities)


    roomSurface.fill((0, 0, 0))
    TestRoom.render(roomSurface)
    for i in Players:
        i.render(roomSurface)
    window.blit(roomSurface, (0, 0))
    window.blit(hudSurface, (0, 640))
    pygame.display.flip()
pygame.quit()