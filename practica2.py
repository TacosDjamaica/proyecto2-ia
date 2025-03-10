import pygame 
import numpy as np
import random
import sys
#constantes 
facil = 1
medio = 2
dificil = 3
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
pygame.display.set_caption("Practica 2") #nombre de la ventana


#Funciones 
def is_valid_location(board, col): # checa si un cuadro en la parte superior es vacía
     return board[ROW_COUNT -1][col] == 0


def get_next_open_row(board, col): # siguiente columna abierta 
     for r in range(ROW_COUNT):
          if board[r][col]==0:
               return r
          
def drop_piece(board, row, col, piece): #coloca una ficha en la matriz
    board[row][col] = piece # asigando valores en la matriz

def winning_move(board, piece): #checamos si un movimiento es ganador
     #checamos si hay 4 Horizontal 
     for r in range(ROW_COUNT):
          for c in range(COLUMN_COUNT -3):
               if board[r][c] == piece and board[r][c+1] == piece and board[r][c+2] == piece and board[r][c+3]==piece: 
                    return True #alguien 
               
     for c in range (COLUMN_COUNT): #checa si hay 4 verticales
          for r in range (ROW_COUNT -3): #-3 para que no se salga de la matriz
               if board [r][c] ==piece and board [r+1][c] == piece and board[r+2][c]==piece and board[r+3][c] == piece:
                    return True
     for r in range (ROW_COUNT -3): #checa si hay 4 diagonales
          for c in range(COLUMN_COUNT -3):
               if board[r][c] == piece and board[r+1][c+1] == piece and board[r+2][c+2] == piece and board[r+3][c+3] == piece:
                    return True
     for c in range(COLUMN_COUNT - 3): #checa si hay 4 diagonales
        for r in range(3, ROW_COUNT):
            if board[r][c] == piece and board[r - 1][c + 1] == piece and board[r - 2][c + 2] == piece and board[r - 3][c + 3] == piece:
                return True

     return False

def draw_board(board): #dibuja el tablero
    for c in range (COLUMN_COUNT):
        for r in range (ROW_COUNT):
            pygame.draw.rect(screen, BLUE, (c * SQUARE_SIZE, (r+1) * SQUARE_SIZE, SQUARE_SIZE,SQUARE_SIZE))#dibujamos un rectangulo
            pygame.draw.circle(screen, BLACK, (int(c * SQUARE_SIZE + SQUARE_SIZE / 2), int((r+1) * SQUARE_SIZE + SQUARE_SIZE / 2)), RADIUS)#dibujamos un circulo
    for c in range(COLUMN_COUNT):
        for r in range(ROW_COUNT):
            if board[r][c]==1:#contiene la ficha del jugador
                pygame.draw.circle(screen, RED, (int(c * SQUARE_SIZE + SQUARE_SIZE / 2), HEIGHT - int(r * SQUARE_SIZE + SQUARE_SIZE / 2)), RADIUS) #dibuja la ficha del jugador
            elif board[r][c]==2: #
                pygame.draw.circle(screen, YELLOW, (int(c * SQUARE_SIZE + SQUARE_SIZE / 2), HEIGHT - int(r * SQUARE_SIZE + SQUARE_SIZE / 2)), RADIUS)#dibuja la ficha del cpu
                pygame.display.update()     
                                

def cpu_player(board, piece, dificultad):#funcion que calcula el tiro de la cpu
    depth = 2 if dificultad == facil else (4 if dificultad == medio else 8)#asignamos la profundidad dependiendo de la dificultad
    fac = dificultad == facil #si la dificultad es facil asignamos True para hacer minimax facil
    best_score= -float('inf') #inicializar menos infinito
    best_col= random.choice([col for col in range (COLUMN_COUNT) if is_valid_location(board,col)]) #escoge una columna aleatoria si no hay ninguna disponible
    for col in range(COLUMN_COUNT):
         if is_valid_location(board, col):
               row = get_next_open_row(board,col)
               temp_board = board.copy()
               drop_piece(temp_board, row,col, piece)
               if fac: 
                    score = minimax_facil(temp_board, depth, False)
               else:
                    score=minimax(temp_board,depth,-float('inf'), float('inf'), False)
               if score> best_score:
                    best_score=score
                    best_col =col
    return best_col #columna con mejor score

def minimax(board, depth, alpha,beta, maximizing_player):#parametros: tablero, profundidad, alpha, beta, si es el turno del cpu
#casos base
     if depth==0 or winning_move(board, 1) or winning_move(board, 2): #si se exploro todo el arbol o hay un  ganador
          if winning_move(board,2): #si el CPU gana
               return 1000000000 #garantiza que el cpu gané
          elif winning_move(board, 1):
               return -1000000000 #no debemos tener este movimiento
          else:
               return 0 #empate
     if maximizing_player: #si es turno de la cpu/max
          max_eval=-float('inf')#inicializamos el maximo valor en menos infinito
          for col in range(COLUMN_COUNT): #dfs
                    if is_valid_location(board, col):#si la columna esta vacia
                         row=get_next_open_row(board, col)#gavedad 
                         temp_board=board.copy()#copiamos el tablero
                         drop_piece(temp_board, row, col,2)#tiramos una ficha del cpu
                         eval1 = minimax(temp_board, depth -1, alpha,beta, False) #llamamos recursivamente minimax

                         max_eval = max(max_eval,eval1)#asignamos el maximo valor de max_eval 
                         alpha = max(alpha, eval1)#asignamos el maximo valor de alpha 
                         if alpha>=beta:
                              break #aqui se realiza la poda beta
          return max_eval #regresamos el maximo valor
     else: #turno del jugador 
          min_eval = float("inf") 
          for col in range(COLUMN_COUNT): #DFS
                    if is_valid_location(board,col):#si la columna esta vacia
                         row=get_next_open_row(board, col)#gavedad 
                         temp_board=board.copy()
                         drop_piece(temp_board, row, col,1)
                         eval1 =minimax(temp_board, depth -1, alpha, beta, True) #llamamos recursivamente minimax
                         min_eval=min(min_eval,eval1)#asignamos el minimo valor de min_eval
                         beta = min(beta,eval1)#asignamos el minimo valor de beta
                         if alpha>=beta:
                                   break #aqui se realiza la poda Beta
          return min_eval

#funcion minmax sin poda alfa beta     
def minimax_facil(board, depth,  maximizing_player):#parametros: tablero, profundidad, si es el turno del cpu
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
                         eval1 = minimax_facil(temp_board, depth -1, False)

                         max_eval = max(max_eval,eval1)
                              
          return max_eval
     else: #turno del jugador
          min_eval = float("inf")
          for col in range(COLUMN_COUNT): #DFS
                    if is_valid_location(board,col):
                         row=get_next_open_row(board, col)
                         temp_board=board.copy()
                         drop_piece(temp_board, row, col,1)
                         eval1 =minimax_facil(temp_board, depth -1, True)
                         min_eval=min(min_eval,eval1)
          return min_eval
     
def obtener_dificultad():
    if len(sys.argv) > 1:  # Si  pasa un argumento
        dificultad_arg = sys.argv[1].lower()  # Convertir a minúsculas para evitar errores
        if dificultad_arg in ["facil", "medio", "dificil"]:
            dificultad_map = {"facil": facil, "medio": medio, "dificil": dificil}
            return dificultad_map[dificultad_arg]
#Main
def main():
    dificultad = obtener_dificultad()
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
                              print("jugador ha ganado!")
                              game_over = True
                         turn = 1 #turno del cpu
                         draw_board(board)

          if turn == 1 and not game_over: #si el turno es del cpu y no se ha terminado el juego 
               col = cpu_player(board, 2, dificultad) #Aqui se calcula el tiro de CPU
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
                                        