import pygame


def run(*players, background=(0, 0, 0), display=None):
    clock = pygame.time.Clock()
    while True:
        display.fill(background)
        keys = pygame.key.get_pressed()

        for player in players:
            if keys[player.controls["left"]]:
                player.left()
            if keys[player.controls["right"]]:
                player.right()
            if keys[player.controls["up"]]:
                player.up()
            if keys[player.controls["down"]]:
                player.down()
            player.draw(display)

        for event in pygame.event.get():
            # Actions before application is closed.
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        pygame.display.update()
        clock.tick(100)
