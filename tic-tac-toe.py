#!/usr/bin/python


#import necessary modules
import os, sys
import pygame
from pygame.locals import *
import sqlite3
import random
from bots import minmax

#check for pygame fonts and sounds
if not pygame.font: print ('Warning, fonts disabled')
if not pygame.mixer: print ('Warning, sound disabled')

#set path variables
main_dir = os.path.split(os.path.abspath(__file__))[0]
img_dir = os.path.join(main_dir,'Assets','Images')
sound_dir = os.path.join(main_dir,'Assets','Sounds')



# Define some colors
BLACK    = (   0,   0,   0)
WHITE    = ( 255, 255, 255)
GREEN    = (  50, 255,  60)
RED      = ( 255,  120,  50)
BLUE     = (   0,   0, 255)

# Defining Button
class button:
    def __init__(self,surf,message,x,y,w,h,ic):
        self.rectangle = pygame.draw.rect( surf, ic, (x, y, w, h))
        font = pygame.font.Font(None, 32)
        text = font.render(message, 1, BLACK)
        textpos = text.get_rect()
        textpos.centerx = x+w/2
        textpos.centery = y+h/2
        surf.blit(text, textpos)

# Function to load sound
def load_sound(name):
    class NoneSound:
        def play(self): pass
    if not pygame.mixer or not pygame.mixer.get_init():
        return NoneSound()
    fullname = os.path.join(sound_dir, name)
    try:
        sound = pygame.mixer.Sound(fullname)
    except pygame.error:
        print ('Cannot load sound: %s' % fullname)
        raise SystemExit(str(geterror()))
    return sound



#Prepare Game Objects
clock = pygame.time.Clock()
fps = 60
app_size = (360,360)
extraspace = 60
click_sound = load_sound('Menu Choice.mp3')


# Checks whether the game is finished or not
def game_finished(state):
    if state[0]==state[1]==state[2]!=0 or state[3]==state[4]==state[5]!=0 or state[6]==state[7]==state[8]!=0 or \
        state[0]==state[3]==state[6]!=0 or state[1]==state[4]==state[7]!=0 or state[2]==state[5]==state[8]!=0 or \
        state[0]==state[4]==state[8]!=0 or state[2]==state[4]==state[6]!=0 :
        return 'Won'
    if state.count(0) == 0:
        return 'Draw'


# Displays menu
def menu(screen):
    # Add background
    try:
        background = pygame.image.load(os.path.join(img_dir,'Backgrounds','board_2.png')).convert_alpha()
        background = pygame.transform.scale(background, app_size)
    except:
        print("couldn't load the board.... exitting!!!")
        sys.exit()

    # Blit everything to the screen
    screen.blit(background, (0, 0))
    pygame.display.flip()

    #defining buttons
    #Start = button(surf,message,x,y,w,h,ic,ac)
    button1   =   button(screen,"Play with Bot",app_size[0]*0,app_size[1]*4/10,150,30,RED)
    button2 =   button(screen,"Play with other person",app_size[0]*0,app_size[1]*5/10,250,30,GREEN)

    # Event loop'
    running = True
    while running:

        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
                return
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = event.pos  # gets mouse position

                # checks if mouse position is over the button
                if button1.rectangle.collidepoint(mouse_pos):
                    click_sound.play()
                    game(screen)
                    running = False


                if button2.rectangle.collidepoint(mouse_pos):
                    click_sound.play()
                    game(screen,False)
                    running = False

        pygame.display.update()
        clock.tick(fps)


# Actual Game function
def game(surf, AI = True):
    symbols = ['X','O']
    player = symbols[random.randint(0,1)]
    opponent = symbols[1-symbols.index(player)]
    board = [0]*9
    section_size = int(app_size[0]//3)
    surf.fill(WHITE)

    try:
        background = pygame.image.load(os.path.join(img_dir,'boards','board_1.png')).convert_alpha()
        background = pygame.transform.scale(background, app_size)
    except:
        print("couldn't load the board.... exitting!!!")
        sys.exit()
    surf.blit(background,(0,0))
    turn = symbols[0]
    running = True
    result=str()
    while running:
        for event in pygame.event.get():
            if event.type == QUIT:
                return
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = event.pos  # gets mouse position
                if turn == player:
                    pos = int((mouse_pos[0]//section_size)*3 + mouse_pos[1]//section_size)
                    if board[pos] == 0:
                        board[pos] = player
                        #try to add image if not add simple text
                        symbol_image = pygame.image.load(os.path.join(img_dir,player,'i.png')).convert_alpha()
                        symbol_image = pygame.transform.scale(symbol_image, (section_size,section_size))
                        loc = (pos//3 * section_size, pos%3 *section_size)
                        surf.blit(symbol_image,loc)
                        pygame.display.update()
                        pygame.time.delay(400)
                        if game_finished(board) == 'Won':
                            result = turn+" has won"
                            running = False
                        if game_finished(board)=='Draw':
                            result = "It's a DRAW !!!!"
                            running = False
                        turn = opponent
                if turn == opponent and AI == False:
                    pos = int((mouse_pos[0]//section_size)*3 + mouse_pos[1]//section_size)
                    if board[pos] == 0:
                        board[pos] = opponent
                        #try to add image if not add simple text
                        symbol_image = pygame.image.load(os.path.join(img_dir,opponent,'i.png')).convert_alpha()
                        symbol_image = pygame.transform.scale(symbol_image, (section_size,section_size))
                        loc = (pos//3 * section_size, pos%3 *section_size)
                        surf.blit(symbol_image,loc)
                        pygame.display.update()
                        pygame.time.delay(400)
                        if game_finished(board) == 'Won':
                            result = turn+" has won"
                            running = False
                        if game_finished(board)=='Draw':
                            result = "It's a DRAW !!!!"
                            running = False
                        turn = player

            if turn == opponent and running == True and AI == True:
                pos = minmax.move(board,opponent)
                board[pos] = opponent
                symbol_image = pygame.image.load(os.path.join(img_dir,opponent,'i.png')).convert_alpha()
                symbol_image = pygame.transform.scale(symbol_image, (section_size,section_size))
                loc = (pos//3 * section_size, pos%3 *section_size)
                surf.blit(symbol_image,loc)
                if game_finished(board) == 'Won':
                    result = turn+" has won"
                    running = False
                if game_finished(board)=='Draw':
                    result = "It's a DRAW !!!!"
                    running = False
                turn = player

        pygame.display.update()
        clock.tick(fps)

    font = pygame.font.Font(None, 36)
    text = font.render(result, 1, (10, 10, 10))
    surf.blit(text, (0,app_size[1]+10))
    pygame.display.update()
    font = pygame.font.Font(None, 18)
    text = font.render("press any key to continue...", 1, (10, 10, 10))
    surf.blit(text, (0,app_size[1]+40))
    pygame.display.update()

    while not running:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                surf.fill(WHITE)
                return
        clock.tick(fps)



def main():
    # Initialise screen
    pygame.init()
    screen = pygame.display.set_mode((app_size[0],app_size[1]+extraspace))
    pygame.display.set_caption('Tic-Tac-Toe')
    screen.fill(WHITE)
    # Event loop'
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == QUIT:
                return
        menu(screen)
        clock.tick(fps)
    pygame.quit()
    sys.exit()


if __name__ == '__main__' : main()
