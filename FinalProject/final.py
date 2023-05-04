import pygame
import json
import random

pygame.font.init()

# pygame setup
pygame.init()
screen_width = 720
screen_height = 720
screen = pygame.display.set_mode((screen_width, screen_height))
clock = pygame.time.Clock()
running = True
dt = 0

# Things like buttons and the fruit
objects = []
fruitSpeed = 3
isFruitClicked = False
fruitHitFloor = False

fruit_yPos = 0
fruit_xPos = random.randint(0,screen_width-64)
fruit_image = pygame.image.load("CS1/FinalProject/Images/Apple.png")
fruit_type = "Fruit"

# Setup player Health and points
player_Health = 100
round_Points = 0

# All Fruit types
fruitTypes = {
    "Fruit": {
        "Image": "CS1/FinalProject/Images/Apple.png",
        "Rarity": 3,
        "Points": 50,
        "Health": 0,
        "HitFloorHealth": -10,
    },
    "Bonus": {
        "Image": "CS1/FinalProject/Images/Bonus.png",
        "Rarity": 15,
        "Points": 150,
        "Health": 0,
        "HitFloorHealth": 0,
    },
    "Bomb": {
        "Image": "CS1/FinalProject/Images/Bomb.png",
        "Rarity": 6,
        "Points": -75,
        "Health": -15,
        "HitFloorHealth": 0,
    },
    "Health": {
        "Image": "CS1/FinalProject/Images/Health.png",
        "Rarity": 20,
        "Points": 0,
        "Health": 25,
        "HitFloorHealth": 0
    }
}
# Load save data
with open("CS1/FinalProject/Save/save.json", "r+") as in_file: # find and open json file
    saveData = json.load(in_file) # load json file

# fruit ninja game setup
RoundInProgress = False
font = pygame.font.SysFont('Arial', 32)
font_Small = pygame.font.SysFont('Arial', 24)

bgImg = pygame.image.load("CS1/FinalProject/Images/sky.png")
imgsmall = pygame.transform.scale(bgImg, (screen_width, screen_height))

# Load Player Data
highscore = 0
totalScore = 0

for p in saveData['playerStats']:
    highscore = p['highscore']
    totalScore = p['totalscore']

# button class
class Button():
    def __init__(self, x, y, width, height, buttonText='Button', onclickFunction=None):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.onclickFunction = onclickFunction

        self.alreadyPressed = False

        #different colors for different scenarios

        self.fillColors = {
            'normal': '#808080', #default color 
            'hover': '#666666', # hovering over UI
            'pressed': '#333333', # clicked UI
        }

        self.buttonSurface = pygame.Surface((self.width, self.height)) # position 
        self.buttonRect = pygame.Rect(self.x, self.y, self.width, self.height) # position and size

        self.buttonSurf = font.render(buttonText, True, (255, 255, 255)) # add button text to button
        objects.append(self) # add the button to the "objects" array

    # Button pressed add effects
    def processButton(self):
        mousePos = pygame.mouse.get_pos()
        self.buttonSurface.fill(self.fillColors['normal'])
        if self.buttonRect.collidepoint(mousePos): # if hovering over
            self.buttonSurface.fill(self.fillColors['hover'])
            if pygame.mouse.get_pressed(num_buttons=3)[0]:
                self.buttonSurface.fill(self.fillColors['pressed'])
                if not self.alreadyPressed:
                    self.onclickFunction() # run function
                    self.alreadyPressed = True # prevent spam clicking by accident
            else:
                self.alreadyPressed = False # button is done being pressed
        
        #set the text position onto the button
        self.buttonSurface.blit(self.buttonSurf, [ 
            self.buttonRect.width/2 - self.buttonSurf.get_rect().width/2,
            self.buttonRect.height/2 - self.buttonSurf.get_rect().height/2
        ])

        #set the position of the button itself
        screen.blit(self.buttonSurface, self.buttonRect)

 
# Help button
def helpFunc():
    print('Button Pressed')
    

# Function that will run when the button is pressed
def playFunc():
    global RoundInProgress 
    RoundInProgress = True # round started
    
#   __  __                            _   _   ___ 
# |  \/  |   ___   _ __    _   _    | | | | |_ _|
# | |\/| |  / _ \ | '_ \  | | | |   | | | |  | | 
# | |  | | |  __/ | | | | | |_| |   | |_| |  | | 
# |_|  |_|  \___| |_| |_|  \__,_|    \___/  |___|

def setupMenu():
    title_text = font.render("fruit ninja but it's in python", False, (0, 0, 0)) # title
    totalPoints_text = font.render(f"Total Points: {totalScore}", False, (0, 0, 0)) # total points
    highScore_text = font.render(f"High Score: {highscore}", False, (0, 0, 0)) # highscore

    # add text to scene
    screen.blit(title_text, (screen_width/2-180, screen_height/4)) 
    screen.blit(totalPoints_text, (screen_width/2-100, screen_height/3))
    screen.blit(highScore_text, (screen_width/2-100, screen_height/3+45))

# Create menu buttons
Button(screen_width/2-100, screen_height/2+25, 200, 50, 'Play', playFunc)
Button(screen_width/2-100, screen_height/2+100, 200, 50, 'Help', helpFunc)



#  ____    _                     _   _   ___ 
# |  _ \  | |   __ _   _   _    | | | | |_ _|
# | |_) | | |  / _` | | | | |   | | | |  | | 
# |  __/  | | | (_| | | |_| |   | |_| |  | | 
# |_|     |_|  \__,_|  \__, |    \___/  |___|
#                      |___/                 


# Setup Game UI
def gameInterface():
    health_Text = font_Small.render("Health", False, (0, 0, 0))
    points_Text = font_Small.render(f"Points: {round_Points}", False, (0, 0, 0))
    speed_Text = font_Small.render(f"Speed: {round(fruitSpeed,2)}", False, (0, 0, 0))

    healthBarBg = pygame.Rect(10, 690, 200, 20)
    healthBar = pygame.Rect(10, 690, player_Health*2, 20)

    pygame.draw.rect(screen, (100,100,100), healthBarBg)
    pygame.draw.rect(screen, (0,255,0), healthBar)
    
    screen.blit(health_Text, (10, 660))
    screen.blit(points_Text, ((screen_width/2-50, 20)))
    screen.blit(speed_Text, (575, 690))


# Add fruits to the game 
def createFruit():
    global isFruitClicked, player_Health, hasClicked

    screen.blit(fruit_image, (fruit_xPos, fruit_yPos)) # add the fruit into the scene

    # Tell what the position and the size is (only used in line 153)
    fruitImageRect = pygame.Rect(fruit_xPos, fruit_yPos,64,64)

    # Detect if fruit has been clicked
    if pygame.mouse.get_pressed()[0] and fruitImageRect.collidepoint(pygame.mouse.get_pos()) and not isFruitClicked:
        isFruitClicked = True
        resetFruit()

# Detect if fruit hit the floor
def check_hitFloor():
    global fruit_yPos, player_Health, fruitHitFloor
    if fruit_yPos > screen_height - 64: # if fruit hit the floor
        #detect if they missed an apple
        fruitHitFloor = True
        resetFruit() # change the type of fruit, subtract/add player health or points

# Reset the fruit to be reused for the next fruit
def resetFruit():
    global fruit_xPos, fruit_yPos, fruit_image, fruit_type, isFruitClicked, round_Points, player_Health, fruitHitFloor, fruitSpeed # get all variables needed to change

    # Fruit Rarities 
    isBomb = random.randint(1, fruitTypes["Bomb"]["Rarity"])
    isHealth = random.randint(1, fruitTypes["Health"]["Rarity"])
    isBonus = random.randint(1, fruitTypes["Bonus"]["Rarity"])

    # 1 in x chance 
    if isBomb == 1:
        randFruit = "Bomb"
    elif isHealth == 1:
        randFruit = "Health"
    elif isBonus == 1:
        randFruit = "Bonus"
    else:
        randFruit = "Fruit"

    #randFruit = random.choice(list(fruitTypes)) # random fruit
    fruit_image =  pygame.image.load(fruitTypes[randFruit]["Image"]) # fruit image

    fruitBonus = fruitTypes[fruit_type]["Points"]
    fruitHealth = fruitTypes[fruit_type]["Health"]

    fruit_xPos = random.randint(0,screen_width-64)
    fruit_yPos = 0
    
    if fruitHitFloor:
        if fruit_type == "Fruit":
            player_Health -= 15
            
        fruitHitFloor = False
    else:
        if fruit_type == "Fruit" or fruit_type == "Bonus" and not fruitHitFloor:
            round_Points += fruitBonus # add/subtract fruit points

        if fruit_type == "Bomb" and not fruitHitFloor:
            player_Health += fruitHealth # add/subtract fruit health
            round_Points += fruitBonus
        
        if fruit_type == "Health" and not fruitHitFloor:
            if player_Health >= 85 and player_Health <= 100:
                player_Health = 100 # if the health is less than 100 but greater than 85 just make it  100
            else:
                player_Health += 15 # add 15 health

        fruitSpeed += 0.05 # increase fruit fall speed to add difficulty

    fruit_type = randFruit # fruit name

    
    
    # add/subtract fruit health from it hitting the floor
    isFruitClicked = False # so the player can click the fruit again

def game_Over():
    global RoundInProgress, player_Health, fruitSpeed, round_Points, totalScore, highscore

    # Reset Variables back to normal
    player_Health = 100 
    totalScore += round_Points 
    if highscore < round_Points:
        highscore = round_Points

    round_Points = 0
    fruitSpeed = 3
    RoundInProgress = False # game is over

#    ____                                _                             
#  / ___|   __ _   _ __ ___     ___    | |       ___     ___    _ __  
# | |  _   / _` | | '_ ` _ \   / _ \   | |      / _ \   / _ \  | '_ \ 
# | |_| | | (_| | | | | | | | |  __/   | |___  | (_) | | (_) | | |_) |
#  \____|  \__,_| |_| |_| |_|  \___|   |_____|  \___/   \___/  | .__/ 
#                                                              |_|    

while running:
    for event in pygame.event.get(): #check if game is closed
        if event.type == pygame.QUIT:
            running = False # if they quit the game break the loop
    
    #background color
    screen.fill((255,255,255))
    screen.blit(imgsmall, (0, 0))


    if RoundInProgress == True:
        gameInterface()
        createFruit() # create the fruit
        fruit_yPos += fruitSpeed # make the fruit fall
        check_hitFloor() # check if fruit hit the floor

        if player_Health <= 0: # if player died the game is over
            game_Over()
    else: # if the round is over then setup the menu again
        setupMenu()
        for object in objects:
            object.processButton()

    pygame.display.flip() # display

    # limits FPS to 60
    dt = clock.tick(60) / 1000

pygame.quit()