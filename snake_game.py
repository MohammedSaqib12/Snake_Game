import pygame
from pygame.locals import *
import time
import random

SIZE= 55
background_color=(255,255,255)

class apple:
    def __init__(self,parent_screen):
        self.apple=pygame.image.load("apple(p).jpg")
        self.parent_screen=parent_screen
        self.x=SIZE*3
        self.y=SIZE*3

    def draw(self):
        self.parent_screen.blit(self.apple,(self.x,self.y))
        pygame.display.flip()

    def move(self):
        self .x = random.randint(0,15)*SIZE
        self .y = random.randint(0,13)*SIZE

class snake:
    def __init__(self, parent_screen , length):
        self.length=length
        self.parent_screen=parent_screen 
        self.block=pygame.image.load("blue1.jpg")

        self.x=[SIZE]*length
        self.y=[SIZE]*length
        self.direction = 'down'

    def increment(self):
        self.length+=1
        self.x.append(-1)
        self.y.append(-1)

    def move_left(self):
        self.direction='left'

    def move_right(self):
        self.direction='right'

    def move_up(self):
        self.direction='up'

    def move_down(self):
        self.direction='down'
    
    def walk(self):

        for i in range(self.length-1,0,-1):
            self.x[i]=self.x[i-1] 
            self.y[i]=self.y[i-1]
        if self.direction=='left':
            self.x[0] -= SIZE
        if self.direction=='right':
            self.x[0] += SIZE
        if self.direction=='up':
            self.y[0] -= SIZE
        if self.direction=='down':
            self.y[0] += SIZE

        self.draw()
    
    def draw(self):
         for i in range(self.length):
            self.parent_screen.blit(self.block,(self.x[i],self.y[i]))

         pygame.display.flip()
class Game:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption("Snake and Apple Game")
        pygame.mixer.init()

        self.play_background()

        self.surface= pygame.display.set_mode((1000,800))
        self.snake=snake(self.surface,1)
        self.snake.draw()
        self.apple=apple(self.surface)
        self.apple.draw()

    def play_background(self):
        pygame.mixer.music.load("background.mp3")
        pygame.mixer.music.play(-1,0)

    def is_collision(self , x1 , y1, x2 , y2):
        if x1 >= x2 and x1 < x2+SIZE:
             if y1 >= y2 and y1 < y2+SIZE:
                return True

        return False
    
    def play_sound(self,soundname):
        if soundname=="crash2":
            sound=pygame.mixer.Sound("crash2.mp3")
        if soundname=="swallow":
            sound=pygame.mixer.Sound("swallow.mp3")

        pygame.mixer.Sound.play(sound)

    def render_background(self):
        bg= pygame.image.load("greentex.jpg")
        self.surface.blit(bg,(0,0))
    
    def play(self):
         self.render_background()
         pygame.display.flip()
         self.snake.walk()
         self.apple.draw()
         self.display_score()
         pygame.display.flip()
        

        #  for i in range(self,snake.length):
         if self.is_collision(self.snake.x[0], self.snake.y[0], self.apple.x , self.apple.y):
             self.play_sound("swallow")
             self.snake.increment()
             self.apple.move()

         for i in range (3,self.snake.length):
             if self.is_collision(self.snake.x[0] , self.snake.y[0] , self.snake.x[i] , self.snake.y[i]):
                 self.play_sound("crash2")
                 pygame.display.flip()
                 raise "Game Over"

         if not (0<=self.snake.x[0]<=1000 and 0<=self.snake.y[0]<=800):
             self.play_sound("crash")
             raise "hit the boundry error"

    def display_score(self):
        font = pygame.font.SysFont("arial",30)
        score = font.render(f"score:{self.snake.length}",True,(0,0,0))
        self.surface.blit(score,(800,10))

    def show_game_over(self):
        self.render_background()
        font = pygame.font.SysFont("arial",30)
        line1=font.render(f"Game is Over : Your Score is : {self.snake.length}",True,(200,200,200))
        self.surface.blit(line1,(300,300))
        line2=font.render(f"To play again press Enter. To Exit press Escape:",True,(200,200,200))
        self.surface.blit(line2,(230,350))
        pygame.mixer.music.pause()
        pygame.display.flip()

    def reset(self):
        self.snake=snake(self.surface,1)
        self.apple=apple(self.surface)
        
    def run(self):
        running=True
        pause = False

        while running:
             for event in pygame.event.get():
                 if event.type==KEYDOWN:
                    if event.key==K_ESCAPE:
                         running=False

                    elif event.key == K_RETURN:
                        pygame.mixer.music.unpause()
                        pause=False
                    if not pause:

                        if event.key==K_UP:
                            self.snake.move_up()

                        elif event.key==K_DOWN: 
                            self.snake.move_down()

                        elif event.key==K_LEFT:
                            self.snake.move_left()

                        elif event.key==K_RIGHT:
                            self.snake.move_right()

                 elif event.type==QUIT:
                      running=False
             try:
                if not pause:
                    self.play()
             except Exception as e:
                self.show_game_over()
                pause = True
                self.reset()

             time.sleep(.2) 
   
if __name__=="__main__":
    game = Game()
    game.run()
   