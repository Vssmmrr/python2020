import game
import pygame
from player import InteractivePlayer, AIPlayer


def main():
    field = game.DraughtsField()
    field_draw = game.FieldDrawer(field)
    field.place_default()
    players = list()
    players.append(InteractivePlayer(field, is_order_white=True, cell_size=field_draw.CELL_SIZE))
    players.append(AIPlayer(field, is_order_white=False, num_predicted_moves=AIPlayer.MEDIUM))
    # players.append(AIPlayer(field, is_order_white=True, num_predicted_moves=AIPlayer.HARD))
    pygame.init()

    win = pygame.display.set_mode((8 * field_draw.CELL_SIZE, 8 * field_draw.CELL_SIZE))
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

        field_draw.draw(win)
        pygame.display.update()

    pygame.quit()


if __name__ == "__main__":
    main()
