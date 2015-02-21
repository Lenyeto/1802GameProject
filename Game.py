import pygame

pygame.init()

resolution = (600, 800)

window = pygame.display.set_mode(resolution)
clock = pygame.time.Clock()






done = False
while not done:
    dtime = clock.tick()

    evtList = pygame.event.get()
    for evt in evtList:
        if evt.type == pygame.QUIT:
            done = True

    window.fill((0, 0, 0))

    pygame.display.flip()
pygame.quit()