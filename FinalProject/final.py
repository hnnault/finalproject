import sys
import pygame
import json
import random
import time
from threading import Thread

pygame.font.init()

# pygame setup
pygame.init()
screen_width = 720
screen_height = 720
screen = pygame.display.set_mode((screen_width, screen_height))
clock = pygame.time.Clock()
running = True
dt = 0

# Things like buttons and fruits
objects = []
fruits = []
fruitOnScreen = 0

# Load save data
with open("CS1/FinalProject/Save/save.json", "r") as in_file: # find and open json file
    saveData = json.load(in_file) # load json file

# fruit ninja game setup
RoundInProgress = False
font = pygame.font.SysFont('Arial', 32)
appleImage = pygame.image.load("CS1/FinalProject/Images/apple.png")

highscore = [p['highscore'] for p in saveData['playerStats']]
totalScore = [p['totalscore'] for p in saveData['playerStats']]

# button class
class Button():
    def __init__(self, x, y, width, height, buttonText='Button', onclickFunction=None, onePress=False):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.onclickFunction = onclickFunction
        self.onePress = onePress
        self.alreadyPressed = False

        #different colors for different scenarios

        self.fillColors = {
            'normal': '#808080',
            'hover': '#666666',
            'pressed': '#333333',
        }

        self.buttonSurface = pygame.Surface((self.width, self.height))
        self.buttonRect = pygame.Rect(self.x, self.y, self.width, self.height)

        self.buttonSurf = font.render(buttonText, True, (255, 255, 255))
        objects.append(self) # add the button to the "objects" array

    # Button pressed add effects
    def processButton(self):
        mousePos = pygame.mouse.get_pos()
        self.buttonSurface.fill(self.fillColors['normal'])
        if self.buttonRect.collidepoint(mousePos):
            self.buttonSurface.fill(self.fillColors['hover'])
            if pygame.mouse.get_pressed(num_buttons=3)[0]:
                self.buttonSurface.fill(self.fillColors['pressed'])
                if self.onePress:
                    self.onclickFunction()
                elif not self.alreadyPressed:
                    self.onclickFunction()
                    self.alreadyPressed = True
            else:
                self.alreadyPressed = False
        
        self.buttonSurface.blit(self.buttonSurf, [
            self.buttonRect.width/2 - self.buttonSurf.get_rect().width/2,
            self.buttonRect.height/2 - self.buttonSurf.get_rect().height/2
        ])
        screen.blit(self.buttonSurface, self.buttonRect)

# create fruits
class createFruit:
    def __init__(self, image, x, y, width, height):
        self.image = image
        self.width = width
        self.height = height
        self.x = x
        self.y = y
        self.rect = pygame.Rect(x,y,width,height)
        #self.callback = callback

        self.buttonSurface = pygame.Surface((self.width, self.height))
        self.buttonRect = pygame.Rect(self.x, self.y, self.width, self.height)

        fruits.append(self)

    def clicked(self):
        mousePos = pygame.mouse.get_pos()
        if self.rect.collidepoint(mousePos):
            print("test")
            #self.callback(self)

    def processButton(self):
        screen.blit(self.buttonSurface, self.buttonRect)

    def fruitfall(self):
        self.y += 5
        self.buttonSurface = pygame.Surface((self.width, self.height))
        self.buttonRect = pygame.Rect(self.x, self.y, self.width, self.height)


# Function that will run when the button is pressed
def playFunc():
    global RoundInProgress 
    RoundInProgress = True

    for object in objects:
        print(objects)
        objects.remove(object)
    
# Add fruits to the game 
def addFruits():
    global fruitOnScreen
    if fruitOnScreen <= 1:
        for fruit in fruits:
            fruit.processButton()
            fruit.fruitfall()
        btn = createFruit(appleImage, random.randrange(0,screen_width),10,64,64) 

        fruitOnScreen += 1

def helpFunc():
    print('Button Pressed')

# Setup Menu
Button(screen_width/2-100, screen_height/2+25, 200, 50, 'Play', playFunc)
Button(screen_width/2-100, screen_height/2+100, 200, 50, 'Help', helpFunc)

title_text = font.render("fruit ninja but it's in python", False, (0, 0, 0))
totalPoints_text = font.render(f"Total Points: {totalScore}", False, (0, 0, 0))
highScore_text = font.render(f"High Score: {highscore}", False, (0, 0, 0))


# Game Loop
while running:
    for event in pygame.event.get(): #check if game is closed
        if event.type == pygame.QUIT:
            running = False # if they quit the game break the loop

    
    #background color
    screen.fill((255,255,255))

    # Load Menu
    for object in objects:
        object.processButton()


    screen.blit(title_text, (screen_width/2-180, screen_height/4))
    screen.blit(totalPoints_text, (screen_width/2-100, screen_height/3))
    screen.blit(highScore_text, (screen_width/2-100, screen_height/3+45))

    if RoundInProgress == True:
        addFruits()
        

    pygame.display.flip() # display

    # limits FPS to 60
    dt = clock.tick(60) / 1000

pygame.quit()