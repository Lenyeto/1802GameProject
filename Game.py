import pygame
import EntitiyClasses
import MapSystem
import mymath

pygame.init()

resolution = (1200, 800)

window = pygame.display.set_mode(resolution)
clock = pygame.time.Clock()

list_of_keys = []

list_of_entities = []
list_of_entities.append(EntitiyClasses.Dummy(mymath.Vector2(200, 200)))
Player = EntitiyClasses.Player(mymath.Vector2(100, 100), 100, True)

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


    Player.update(dtime, list_of_keys, list_of_entities)


    window.fill((0, 0, 0))
    Player.render(window)
    for i in list_of_entities:
        i.render(window)
    pygame.display.flip()
pygame.quit()