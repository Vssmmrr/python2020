import game
import pygame
from player import InteractivePlayer, AIPlayer


def main():
    field = game.DraughtsField()
    field.place_default()
    players = list()
    players.append(InteractivePlayer(field, field.WHITE))
    players.append(AIPlayer(field, field.BLACK, AIPlayer.MEDIUM))
    # players.append(AIPlayer(field, field.WHITE, AIPlayer.HARD))
    pygame.init()

    win = pygame.display.set_mode((8 * field.CELL_SIZE, 8 * field.CELL_SIZE))
    pygame.display.set_caption("Russian Draughts")

    run = True

    while run:
        pygame.time.delay(16)

        event_list = pygame.event.get()
        for event in event_list:
            if event.type == pygame.QUIT:
                run = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_s:
                    field.save()
                elif event.key == pygame.K_l:
                    field.load()

        if not field.game_over():
            for player in players:
                if player.obtain_events(event_list):
                    break
            if field.game_over():
                print("Game over")

        field.draw(win)
        pygame.display.update()

    pygame.quit()


if __name__ == "__main__":
    main()
