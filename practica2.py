import pygame 
import numpy as np
import random

#constantes 

ROW_COUNT = 6 #numero de filas
COLUMN_COUNT = 7 # numero de las columnas
SQUARE_SIZE = 100 #tamano del cuadro
RADIUS = int(SQUARE_SIZE / 2- 5) #radio de la fichita
WIDTH = COLUMN_COUNT * SQUARE_SIZE #Anchura de la ventana
HEIGHT = (ROW_COUNT+1)*SQUARE_SIZE #Lo alto de la ventana 
BLUE = (0, 0, 255) #tablero
BLACK = (0,0,0) #Para el tablero
RED=(255,0,0) #fichas del jugador
YELLOW = (255, 255, 0) # fichas cpu

pygame.init() #inicia los modulos de pygame
screen = pygame.display.set_mode((WIDTH,HEIGHT)) # renderizar la ventana
pygame.display.set_caption("practica 02: Busqueda") #nombre de la ventana


#Funciones 
def is_valid_location(board, col): # checa si un cuadro en la parte superior es vacía
     return board[ROW_COUNT -1][col] == 0


def get_next_open_row(board, col):
     for r in range(ROW_COUNT):
          if board[r][col]==0:
               return r
          
def drop_piece(board, row, col, piece):
    board[row][col] = piece # asigando valores en la matriz

def winning_move(board, piece): #checamos si un movimiento es ganador
     #checamos si hay 4 Horizontal 
     for r in range(ROW_COUNT):
          for c in range(COLUMN_COUNT -3):
               if board[r][c] == piece and board[r][c+1] == piece and board[r][c+2] == piece and board[r][c+3]==piece: 
                    return True #alguien 
               
     for c in range (COLUMN_COUNT): 
          for r in range (ROW_COUNT -3):
               if board [r][c] ==piece and board [r+1][c] == piece and board[r+2][c]==piece and board[r+3][c] == piece:
                    return True
     for r in range (ROW_COUNT -3):
          for c in range(COLUMN_COUNT -3):
               if board[r][c] == piece and board[r+1][c+1] == piece and board[r+2][+2] == piece and board[r+3][c+3] == piece:
                    return True
     for c in range(COLUMN_COUNT - 3):
        for r in range(3, ROW_COUNT):
            if board[r][c] == piece and board[r - 1][c + 1] == piece and board[r - 2][c + 2] == piece and board[r - 3][c + 3] == piece:
                return True

     return False

def draw_board(board):
    for c in range (COLUMN_COUNT):
        for r in range (ROW_COUNT):
            pygame.draw.rect(screen, BLUE, (c * SQUARE_SIZE, (r+1) * SQUARE_SIZE, SQUARE_SIZE,SQUARE_SIZE))
            pygame.draw.circle(screen, BLACK, (int(c * SQUARE_SIZE + SQUARE_SIZE / 2), int((r+1) * SQUARE_SIZE + SQUARE_SIZE / 2)), RADIUS)#dibujamos un circulo
    for c in range(COLUMN_COUNT):
        for r in range(ROW_COUNT):
            if board[r][c]==1:#contiene la ficha del jugador
                pygame.draw.circle(screen, RED, (int(c * SQUARE_SIZE + SQUARE_SIZE / 2), HEIGHT - int(r * SQUARE_SIZE + SQUARE_SIZE / 2)), RADIUS)
            elif board[r][c]==2:
                pygame.draw.circle(screen, YELLOW, (int(c * SQUARE_SIZE + SQUARE_SIZE / 2), HEIGHT - int(r * SQUARE_SIZE + SQUARE_SIZE / 2)), RADIUS)
                pygame.display.update()     
                                

def cpu_player(board, piece):
    best_score= -float('inf') #inicializar menos infinito
    best_col= random.choice([col for col in range (COLUMN_COUNT) if is_valid_location(board,col)]) 
    for col in range(COLUMN_COUNT):
         if is_valid_location(board, col):
               row = get_next_open_row(board,col)
               temp_board = board.copy()
               drop_piece(temp_board, row,col, piece)
               score=minimax(temp_board,15,-float('inf'), float('inf'), False)
               if score> best_score:
                    best_score=score
                    best_col =col
    return best_col #columna con mejor score

def minimax(board, depth, alpha,beta, maximizing_player):
#casos base
     if depth==0 or winning_move(board, 1) or winning_move(board, 2): #si se exploro todo el arbol o encontramos un movimiento ganador
          if winning_move(board,2): #El CPU gana
               return 1000000000 #garantiza que el cpu gané
          elif winning_move(board, 1):
               return -1000000000 #no debemos tener este movimiento
          else:
               return 0 #empate
     if maximizing_player: #turno de la cpu/max
          max_eval=-float('inf')
          for col in range(COLUMN_COUNT): #dfs
                    if is_valid_location(board, col):
                         row=get_next_open_row(board, col)
                         temp_board=board.copy()
                         drop_piece(temp_board, row, col,2)
                         eval1 = minimax(temp_board, depth -1, alpha,beta, False)

                         max_eval = max(max_eval,eval1)
                         beta = max(alpha, eval1)
                         if alpha>=beta:
                              break #aqui se realiza la poda beta
          return max_eval
     else: #turno del jugador
          min_eval = float("inf")
          for col in range(COLUMN_COUNT): #DFS
                    if is_valid_location(board,col):
                         row=get_next_open_row(board, col)
                         temp_board=board.copy()
                         drop_piece(temp_board, row, col,1)
                         eval1 =minimax(temp_board, depth -1, alpha, beta, True)
                         min_eval=min(min_eval,eval1)
                         beta = min(alpha,eval1)
                         if alpha>=beta:
                                   break #aqui se realiza la poda Beta
          return min_eval
                    

#Main
def main():
    board = np.zeros((ROW_COUNT, COLUMN_COUNT))
    game_over = False
    turn = 0 #0 para usuario y 1 para la cpu

    #draw borad (board)
    pygame.display.update()
    while not game_over: #Mientras no haya ganador 
          for event in pygame.event.get(): 
        #Eventos
               if event.type == pygame.QUIT: #cerramos el juego
                    pygame.quit()
                    return
               if event.type == pygame.MOUSEMOTION: #Movimineto del mous
                    pygame.draw.rect(screen, BLACK, (0,0,WIDTH, SQUARE_SIZE))
                    posx = event.pos[0]
                    if turn == 0:  #si el turno es del jugador
                         pygame.draw.circle(screen,RED, (posx, int(SQUARE_SIZE /2)), RADIUS) #Dibuja la fichita del jugador
                    pygame.display.update() #actualizamos cada movimiento del mouse

               if event.type == pygame.MOUSEBUTTONDOWN and turn == 0:
                    posx =event.pos[0]
                    col = int(posx // SQUARE_SIZE)
                    if is_valid_location (board, col):
                         row = get_next_open_row(board, col)
                         drop_piece(board, row, col, 1)# tiramos una ficha del jugador
                         if winning_move(board, 1): #Checamos si gano
                              print("jugador a ganador!")
                              game_over = True
                         turn = 1 #turno del cpu
                         draw_board(board)

          if turn == 1 and not game_over: #si el turno es del cpu y no se ha terminado el juego 
               col = cpu_player(board, 2) #Aqui se calcula el tiro de CPU
               if is_valid_location(board, col):
                    row = get_next_open_row(board,col)# gavedad
                    drop_piece(board, row, col, 2)
                    if winning_move(board, 2):
                         print ("cpu ha ganado!")
                         game_over=True         
                    turn = 0 #Cedemos turno a jugador
                    draw_board(board)

          if game_over: 
               pygame.time.wait(3000) #espera 3 segundos
if __name__ == "__main__":
     main() #correr el juego                         
                                        