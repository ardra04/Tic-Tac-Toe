import pygame
import time
import code_tic_tac_toe as tic
import sys
pygame.init()
size = width, height = 610, 410
white = (255, 255, 255)
violet = (127, 0, 255)
black = (0, 0, 0)
screen = pygame.display.set_mode(size)
mf = pygame.font.SysFont('arial', 20)
lf = pygame.font.SysFont('arial', 40)
mof = pygame.font.SysFont('arial', 60)
user = None
board = tic.initial_state()
ai_turn = False
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
    screen.fill(violet)
    if user is None:
        title = lf.render("Let's Play Tic-Tac-Toe", True, white)
        titleRect = title.get_rect()
        titleRect.center = ((width / 2), 60)
        screen.blit(title, titleRect)
        
        title1 = mf.render("please select your character to start the game", True, black)
        title1Rect = title1.get_rect()
        title1Rect.center = ((width / 2), 95)
        screen.blit(title1, title1Rect)

        title2 = mf.render("AI - Case Study", True, black)
        title2Rect = title1.get_rect()
        title2Rect.center = ((width / 2), 370)
        screen.blit(title2, title2Rect)
    
        plyXbtn = pygame.Rect((width / 8), (height / 2), width / 4, 90)
        playX = mf.render("X", True, black)
        playXRect = playX.get_rect()
        playXRect.center = plyXbtn.center
        pygame.draw.rect(screen, white, plyXbtn)
        screen.blit(playX, playXRect)

        plyObtn = pygame.Rect(5 * (width / 8), (height / 2), width / 4, 90)
        playO = mf.render("O", True, black)
        playORect = playO.get_rect()
        playORect.center = plyObtn.center
        pygame.draw.rect(screen, white, plyObtn)
        screen.blit(playO, playORect)
        click, _, _ = pygame.mouse.get_pressed()
        if click == 1:
            mouse = pygame.mouse.get_pos()
            if plyXbtn.collidepoint(mouse):
                time.sleep(0.2)
                user = tic.X
            elif plyObtn.collidepoint(mouse):
                time.sleep(0.2)
                user = tic.O
    else:
        tile_size = 80
        tile_origin = (width / 2 - (1.5 * tile_size),
                       height / 2 - (1.5 * tile_size))
        tiles = []
        for i in range(3):
            row = []
            for j in range(3):
                rect = pygame.Rect(
                    tile_origin[0] + j * tile_size,
                    tile_origin[1] + i * tile_size,
                    tile_size, tile_size
                )
                pygame.draw.rect(screen, white, rect, 3)

                if board[i][j] != tic.EMPTY:
                    move = mof.render(board[i][j], True, white)
                    moveRect = move.get_rect()
                    moveRect.center = rect.center
                    screen.blit(move, moveRect)
                row.append(rect)
            tiles.append(row)

        game_over = tic.terminal(board)
        player = tic.player(board)
        if game_over:
            winner = tic.winner(board)
            if winner is None:
                title = f"DRAW!."
            else:
                title = f"Game Over: {winner} WINS!."
        elif user == player:
            title = f"Play as {user}"
        else:
            title = f""
        title = lf.render(title, True, white)
        titleRect = title.get_rect()
        titleRect.center = ((width / 2), 30)
        screen.blit(title, titleRect)
        if user != player and not game_over:
            if ai_turn:
                time.sleep(0.5)
                move = tic.mini_max(board)
                board = tic.result(board, move)
                ai_turn = False
            else:
                ai_turn = True
        click, _, _ = pygame.mouse.get_pressed()
        if click == 1 and user == player and not game_over:
            mouse = pygame.mouse.get_pos()
            for i in range(3):
                for j in range(3):
                    if (board[i][j] == tic.EMPTY and tiles[i][j].collidepoint(mouse)):
                        board = tic.result(board, (i, j))
        if game_over:
            againButton = pygame.Rect(width / 3, height - 65, width / 3, 50)
            again = mf.render("Restart Game", True, black)
            againRect = again.get_rect()
            againRect.center = againButton.center
            pygame.draw.rect(screen, white, againButton)
            screen.blit(again, againRect)
            click, _, _ = pygame.mouse.get_pressed()
            if click == 1:
                mouse = pygame.mouse.get_pos()
                if againButton.collidepoint(mouse):
                    time.sleep(0.2)
                    user = None
                    board = tic.initial_state()
                    ai_turn = False

    pygame.display.flip()
