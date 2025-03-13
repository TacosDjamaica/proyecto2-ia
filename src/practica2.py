import pygame 
import numpy as np
import random
import sys

#definimos los niveles de dificultad
facil = 1
medio = 2
dificil = 3

#configuracion del tablero
row_count = 6
column_count = 7
square_len = 100
radio = int(square_len / 2 - 5)
width = column_count * square_len
height = (row_count + 1) * square_len

#definimos colores
blue = (0, 0, 255)
black = (0, 0, 0)
red = (255, 0, 0)
yellow = (255, 255, 0)

pygame.init()
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Practica 2")

def cpu_player(board, piece, dificultad):
    depth = 2 if dificultad == facil else (4 if dificultad == medio else 8)     #asignamos la profundidad dependiendo de la dificultad
    fac = dificultad == facil     #si la dificultad es facil asignamos True para hacer minimax facil
    best_score= -float('inf') #inicializar menos infinito
    best_col= random.choice([col for col in range (column_count) if is_valid_location(board,col)]) #escoge una columna aleatoria si no hay ninguna disponible
    
    for col in range(column_count):
         if is_valid_location(board, col):
               row = get_next_open_row(board,col)
               temp_board = board.copy()
               drop_piece(temp_board, row,col, piece)

               if fac: score = minimax_facil(temp_board, depth, False)
               else: score=minimax(temp_board,depth,-float('inf'), float('inf'), False)
               if score> best_score:
                    best_score=score
                    best_col =col
    return best_col

def is_valid_location(board, col):
    #verifica si la parte superior de una columna especcfica está vacca
    return board[row_count - 1][col] == 0

def get_next_open_row(board, col):
    #encuentra la primera fila vacia en la columna especificada
    for r in range(row_count):
        if board[r][col] == 0:
            return r

def draw_board(board):
    #dibuja el tablero y las fichas en la pantalla
    for x in range(column_count):
        for y in range(row_count):
            pygame.draw.rect(screen, blue, (x * square_len, (y + 1) * square_len, square_len, square_len))
            pygame.draw.circle(screen, black, (int(x * square_len + square_len / 2), int((y + 1) * square_len + square_len / 2)), radio)
    for x in range(column_count):
        for y in range(row_count):
            if board[y][x] == 1:
                pygame.draw.circle(screen, red, (int(x * square_len + square_len / 2), height - int(y * square_len + square_len / 2)), radio)
            elif board[y][x] == 2:
                pygame.draw.circle(screen, yellow, (int(x * square_len + square_len / 2), height - int(y * square_len + square_len / 2)), radio)
                pygame.display.update()

def drop_piece(board, row, col, piece):
    #coloca una ficha en la posicion especificada
    board[row][col] = piece

def winning_move(board, piece):
    #verifica si hay una combinación ganadora en el tablero
    for x in range(row_count):
        for y in range(column_count - 3):
            if all(board[x][y + i] == piece for i in range(4)):
                return True
    for x in range(column_count):
        for y in range(row_count - 3):
            if all(board[y + i][x] == piece for i in range(4)):
                return True
    for x in range(row_count - 3):
        for y in range(column_count - 3):
            if all(board[x + i][y + i] == piece for i in range(4)):
                return True
    for y in range(column_count - 3):
        for x in range(3, row_count):
            if all(board[x - i][y + i] == piece for i in range(4)):
                return True
    return False

def minimax(board, depth, alpha, beta, maximizing_player):
    
    #algoritmo minimax con poda alfa-beta.
    #board: estado actual del tablero.
    #depth: profundidad maxima de exploración.
    #alpha: valor maximo que el cpu puede asegurar.
    #beta: valor minimo que el cpu puede asegurar
    #maximizing_player: determina si es el turno del cpu o del jugador
    
    #verificamos si se llego a la profundidad maxima o si hay un ganador
    if depth == 0 or winning_move(board, 1) or winning_move(board, 2):
        if winning_move(board, 2):  #si el cpu gana, devuelve un valor alto
            return 1000000000
        elif winning_move(board, 1):  #si el jugador gana, devuelve un valor bajo
            return -1000000000
        else:  #si no hay ganador, es un empate
            return 0
    
    if maximizing_player:
        #turno del cpu (maximizacion)
        max_eval = -float('inf')
        for col in range(column_count):
            if is_valid_location(board, col):
                row = get_next_open_row(board, col)
                temp_board = board.copy()
                drop_piece(temp_board, row, col, 2)
                eval1 = minimax(temp_board, depth - 1, alpha, beta, False)
                max_eval = max(max_eval, eval1)  #escoge el valor maximo encontrado
                alpha = max(alpha, eval1)  #actualiza el valor de alpha
                if alpha >= beta:
                    break  #se realiza la poda beta
        return max_eval
    else:
        #turno del jugador (minimizacion)
        min_eval = float('inf')
        for col in range(column_count):
            if is_valid_location(board, col):
                row = get_next_open_row(board, col)
                temp_board = board.copy()
                drop_piece(temp_board, row, col, 1)
                eval1 = minimax(temp_board, depth - 1, alpha, beta, True)
                min_eval = min(min_eval, eval1)  #escoge el valor minimo encontrado
                beta = min(beta, eval1)  #actualiza el valor de beta
                if alpha >= beta:
                    break  #se realiza la poda alfa
        return min_eval
  
def minimax_facil(board, depth,  maximizing_player):
     if depth==0 or winning_move(board, 1) or winning_move(board, 2): #si se exploro todo el arbol o encontramos un movimiento ganador
          if winning_move(board,2): return 1000000000 #garantiza que el cpu gane
          elif winning_move(board, 1): return -1000000000 #no debemos tener este movimiento
          else: return 0 #empate
          
     if maximizing_player: #turno de la cpu
          max_eval=-float('inf')
          for col in range(column_count):
                    if is_valid_location(board, col):
                         row=get_next_open_row(board, col)
                         temp_board=board.copy()
                         drop_piece(temp_board, row, col,2)
                         eval1 = minimax_facil(temp_board, depth -1, False)
                         max_eval = max(max_eval,eval1)         
          return max_eval

     else: #turno del jugador
          min_eval = float("inf")
          for col in range(column_count):
                    if is_valid_location(board,col):
                         row=get_next_open_row(board, col)
                         temp_board=board.copy()
                         drop_piece(temp_board, row, col,1)
                         eval1 =minimax_facil(temp_board, depth -1, True)
                         min_eval=min(min_eval,eval1)
          return min_eval

def main():
    #funcion principal del juego
    dificultad = sys.argv[1].lower()
    board = np.zeros((row_count, column_count))
    game_over = False
    turn = 0
    pygame.display.update()
    while not game_over:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
            if event.type == pygame.MOUSEMOTION:
                pygame.draw.rect(screen, black, (0, 0, width, square_len))
                posx = event.pos[0]
                if turn == 0:
                    pygame.draw.circle(screen, red, (posx, int(square_len / 2)), radio)
                pygame.display.update()
            if event.type == pygame.MOUSEBUTTONDOWN and turn == 0:
                posx = event.pos[0]
                col = int(posx // square_len)
                if is_valid_location(board, col):
                    row = get_next_open_row(board, col)
                    drop_piece(board, row, col, 1)
                    if winning_move(board, 1):
                        print("el jugador ha ganado!!!!")
                        game_over = True
                    turn = 1
                    draw_board(board)
        if turn == 1 and not game_over:
            col = cpu_player(board, 2, dificultad)
            if is_valid_location(board, col):
                row = get_next_open_row(board, col)
                drop_piece(board, row, col, 2)
                if winning_move(board, 2):
                    print("el cpu ha ganado!!!")
                    game_over = True
                turn = 0
                draw_board(board)
        if game_over:
            pygame.time.wait(3000)

if __name__ == "__main__":
    main()
