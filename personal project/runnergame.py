"""
Author: Zai Yang
Project: Alien Runner Game
This project implements an Alien Runner Game using the python programming language and Pygame.
"""

import pygame
from sys import exit
from random import randint, choice


class Player(pygame.sprite.Sprite):
    """A class to represent a Player"""
    
    def __init__(self)->None:
        """Initializes a Player object
        ---
        Attributes
        ---
        player_walk: list[Surface]
            A list containing both images of Player sprite walking
        player_idx: int
            Index that determines which surface in player_walk list is displayed
        player_jump: Surface
            Image of Player sprite jumping
        image: Surface
            Decides which walking image of Player sprite is displayed
        rect: Rect
            Rectangle object of image
        gravity: int
            value for gravity of player
        jump_sound: Sound
            Player's jumping sound effect"""        
        super().__init__()
        player_w1 = pygame.image.load("graphics1/Player/p1_walk/PNG/p1_walk02.png").convert_alpha()
        player_w2 = pygame.image.load("graphics1/Player/p1_walk/PNG/p1_walk03.png").convert_alpha()
        self.player_walk = [player_w1, player_w2]
        self.player_idx = 0
        self.image = self.player_walk[self.player_idx]
        self.rect = self.image.get_rect(midbottom = (80,300))        
        self.player_jump = pygame.image.load("graphics1/Player/p1_jump.png").convert_alpha()        
        self.gravity = 0
        self.jump_sound = pygame.mixer.Sound("audios/jump.ogg")
        
    def player_input(self)->None:
        """Plays a jumping sound effect and causes player sprite to jump if space bar is pressed"""
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE] and self.rect.bottom >= 300:
            self.gravity = -20
            self.jump_sound.play()
            
    def apply_gravity(self)->None:
        """This method creates a floor for the player to run on and controls the jump mechanics of the Player by moving it up 20 pixels and down 20 pixels but not below the floor"""
        self.gravity+=1
        self.rect.y+=self.gravity
        if self.rect.bottom >= 300:
            self.rect.bottom = 300
            
    def animation_state(self)->None:
        """Animates the player sprite:
        If player is not on floor, image of jumping player will be displayed
        If player is on floor, every ten frames the player's moving image that is displayed on screen will switch back and forth
        """
        if self.rect.bottom < 300:
            self.image = self.player_jump
        else:
            self.player_idx+=0.1
            if self.player_idx >= len(self.player_walk): 
                self.player_idx = 0
            self.image = self.player_walk[int(self.player_idx)]
            
    def update(self)->None:
        """Update the games according to player and game input"""
        self.player_input()
        self.apply_gravity()
        self.animation_state()


class Obstacle(pygame.sprite.Sprite):
    """A Class to represent an obstacle(Fly or Slime) sprite"""
    def __init__(self, type: str)->None:
        """Initializes an Obstacle Object based on the type inputted
        ---
        Attributes
        ---
        frames: list[Surface]
            A list containing 2 images of either a fly flying or a slime moving, depending on the type
        animation_index: int
            Index that determines which surface in frames list is displayed
        image: Surface
            Decides which moving image of obstacle sprite is displayed
        rect: Rect
            Rectangle object of image
        y_pos: int
            Y-coordinate of obstacle's location on surface
        """
        super().__init__()
        if type == "fly":
            fly_frame1 = pygame.image.load("graphics1/Enemies/flyFly1.png").convert_alpha()
            fly_frame2 = pygame.image.load("graphics1/Enemies/flyFly2.png").convert_alpha()
            self.frames = [fly_frame1, fly_frame2]
            y_pos = 195
        else:
            slime_frame1 = pygame.image.load("graphics1/Enemies/slime1.png").convert_alpha()
            slime_frame2 = pygame.image.load("graphics1/Enemies/slimeWalk2.png").convert_alpha()
            self.frames = [slime_frame1, slime_frame2]
            y_pos =300
        self.animation_index = 0
        self.image = self.frames[self.animation_index]
        self.rect = self.image.get_rect(midbottom = (randint(900,1100), y_pos))
        
    def animation_state(self)->None:
        """Animates the obstacle sprite:
        Every ten frames the obstacle moving image that is displayed on screen will switch back and forth
        """
        self.animation_index+=0.1
        if self.animation_index >= len(self.frames):
            self.animation_index = 0
        self.image = self.frames[int(self.animation_index)]
        
    def update(self)->None:
        """Update the games according to player and game input"""        
        self.animation_state()
        self.rect.x -= 5
        self.destroy()
    
    def destroy(self)->None:
        """Removes obstacle object from obstacle_group"""
        if self.rect.x <= -100:
            self.kill()
        
        

def display_score()->int:
    """Calculates and displays the current score on screen and returns the current score"""
    current_time = pygame.time.get_ticks()//1000 - start_time #sets score to 0 every time game is restarted
    score_surface = test_font.render(f'Score: {current_time}', False, (64,64,64))
    score_rect = score_surface.get_rect(center = (400,50))
    screen.blit(score_surface, score_rect)
    return current_time
    

def collision_sprite()->bool:
    """Removes all obstacles from obstacle_group and plays a death bell sound everytime a collision between the player and obstacle is detected.
    Returns False if collision is detected and True if not, in order to determine the status of game_active
    """
    if pygame.sprite.spritecollide(player.sprite, obstacle_group, True):
        obstacle_group.empty()
        pygame.mixer.Sound("audios/death.wav").play()        
        return False
    else: 
        return True

#Initializing the game
pygame.init()
screen = pygame.display.set_mode((800,400))
pygame.display.set_caption("Alien Dash Game")
test_font = pygame.font.Font("Pixeltype.ttf", 50) 
clock = pygame.time.Clock()
start_time = 0   #start time of every new game started
score = 0
game_active = False #Controls the state of the game & which screen is shown
sky_surface = pygame.image.load("graphics2/Backgrounds/desert.png").convert_alpha()
ground_surface = pygame.image.load("ground.png").convert_alpha()

#Initializing Player and Obstacle groups and Player Object
player = pygame.sprite.GroupSingle()
player.add(Player())
obstacle_group = pygame.sprite.Group()

#Background Music
bg_music = pygame.mixer.Sound("audios/retromusic.wav")
bg_music.set_volume(0.5)
bg_music.play(loops = -1)

#Intro screen before game begins
player_stand = pygame.image.load("graphics1/Player/p1_front.png").convert_alpha()
player_stand = pygame.transform.rotozoom(player_stand,0,2)
player_stand_rect = player_stand.get_rect(center = (400,200))

#Timer that controls how often obstacles are generated
obstacle_timer = pygame.USEREVENT+1
pygame.time.set_timer(obstacle_timer, 1500)

#Game Loop
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            """Exits game"""
            pygame.quit()
            exit()
        if game_active:
            if event.type == obstacle_timer:
                """Creates new obstacles: 75% chance it's a slime, 25% chance it's a fly """
                obstacle_group.add(Obstacle(choice(['fly','slime','slime','slime'])))
        else:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                """Restarts game and collects start time used to calculate game score"""
                game_active = True
                start_time = pygame.time.get_ticks()//1000
        
    if game_active:
        screen.blit(sky_surface, (0,0))
        screen.blit(ground_surface, (0,300))
        score = display_score()
        
        """Updates the player and obstacles drawn on screen"""
        player.draw(screen)  
        player.update()
        obstacle_group.draw(screen)
        obstacle_group.update()
        
        game_active = collision_sprite()
    else:
        screen.fill((94,129,162))
        screen.blit(player_stand, player_stand_rect)
        
        game_text = test_font.render("Alien Dash", False, "Blue")
        game_text_rect = game_text.get_rect(center = (400,80))
        screen.blit(game_text, game_text_rect)           
        
        play_msg = test_font.render("Press Space to run", False, "Blue")
        play_msg_rect = play_msg.get_rect(center = (400, 330))    
        
        
        score_msg = test_font.render(f'Your Score: {score}', False, "Blue")
        score_msg_rect = score_msg.get_rect(center = (400,330))
        

        if score == 0: 
            """Intro screen before game is played"""
            screen.blit(play_msg, play_msg_rect)
        else:
            """Screen after player dies and wants to restart game"""
            screen.blit(score_msg, score_msg_rect) 
            play_msg_rect.center = (350, 370)
            play_msg = test_font.render("(Press Space to run again)", False, "Blue")
            screen.blit(play_msg, play_msg_rect)
    pygame.display.update()
    clock.tick(60)
