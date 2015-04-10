import pygame
import MapSystem
import EntitiyClasses
import mymath
import xmlweapons

pygame.init()

resolution = (1200, 800)


window = pygame.display.set_mode(resolution)
clock = pygame.time.Clock()

list_of_keys = []

list_of_entities= [EntitiyClasses.Dummy(mymath.Vector2(200, 200)), EntitiyClasses.Dummy(mymath.Vector2(500, 500)), EntitiyClasses.WeaponStand(xmlweapons.Weapon().getWeapon("Short Bow"), mymath.Vector2(50, 50))]
Players = []
Players.append(EntitiyClasses.Player(mymath.Vector2(100, 100), 100, True))

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

    for i in list_of_entities:
        if isinstance(i, EntitiyClasses.WeaponStand):
            i.update(dtime, Players)
        else:
            if i.update(dtime):
                list_of_entities.remove(i)
    for i in list_of_entities:
        if isinstance(i, EntitiyClasses.Dummy):
            i.AI(Players, dtime)

    for i in Players:
        i.update(dtime, list_of_keys, list_of_entities)


    window.fill((0, 0, 0))
    for i in Players:
        i.render(window)
    for i in list_of_entities:
        i.render(window)
    pygame.display.flip()
pygame.quit()