import pygame


def move(players, keys, display):
    """This function checks, if someone need to move and draws them in right position."""
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

def events(events):
    for event in events:
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()
