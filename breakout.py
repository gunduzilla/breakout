import math
import pygame
# rgb colors
black = (0, 0, 0)
white = (255, 255, 255)
blue = (0, 0, 255)
# block size
block_width = 23
block_height = 15
class Block(pygame.sprite.Sprite):
    # the blocks the ball will knock out
    def __init__(self, color, x, y):
        # constructor, passes color and coordinates
        super().__init__() # superclass (Sprite) constructor
        self.image = pygame.Surface([block_width, block_height]) # block image with list for width and height
        self.image.fill(color) # fill image with color
        self.rect = self.image.get_rect() # fetch the right (same dimensions) rectangle object for the image
        # move rectangle to x, y (coordinates are the top left corner of the object)
        self.rect.x = x
        self.rect.y = y
class Ball(pygame.sprite.Sprite):
    # the ball
    speed = 10.0 # pixels per cycle
    # float location of ball
    x = 0.0
    y = 180.0
    direction = 200 # degrees
    # dimensions of ball
    width = 10
    height = 10
    # constructor, passes color and coordinates
    def __init__(self):
        super().__init__() # superclass (Sprite) constructor
        self.image = pygame.Surface([self.width, self.height]) # image of ball
        self.image.fill(white) # fill the ball with the previously defined rgb color white
        self.rect = self.image.get_rect() # get rectangle object that shows where the image is
        # store height and width of screen
        self.screenheight = pygame.display.get_surface().get_height()
        self.screenwidth = pygame.display.get_surface().get_width()
    def bounce(self, diff):
        # bounce ball off of a horizontal surface
        self.direction = (180 - self.direction) % 360 # set the direction to 180 - current direction (remainder after 360(s))
        self.direction -= diff #subtract the differential from the new direction
    def update(self):
        # update ball position
        # convert to degrees to use trig functions (sin and cos)
        direction_radians = math.radians(self.direction)
        # change coordinates based on speed and direction
        self.x += self.speed * math.sin(direction_radians)
        self.y -= self.speed * math.cos(direction_radians)
        # move image to x, y
        self.rect.x = self.x
        self.rect.y = self.y
        # bouncing off...
        # top?
        if self.y <= 0:
            self.bounce(0)
            self.y = 1
        # left?
        if self.x <= 0:
            self.direction = (360 - self.direction) % 360
            self.x = 1
        # right?
        if self.x > self.screenwidth - self.width:
            self.direction = (360 - self.direction) % 360
            self.x = self.screenwidth - self.width - 1
        # bottom (fail)
        if self.y > 600:
            return True
        else:
            return False
class Player(pygame.sprite.Sprite):
    # the bar at the bottom
    def __init__(self):
        super().__init__() # call superclass constructor
        self.width = 75
        self.height = 15
        self.image = pygame.Surface([self.width, self.height])
        self.image.fill((white))
        # pass in the top left corner
        self.rect = self.image.get_rect()
        self.screenheight = pygame.display.get_surface().get_height()
        self.screenwidth = pygame.display.get_surface().get_width()
        self.rect.x = 0
        self.rect.y = self.screenheight-self.height
    def update(self):
        # update player position
        pos = pygame.mouse.get_pos() # get mouse position
        self.rect.x = pos[0] # set left side of bar to mouse position
        if self.rect.x > self.screenwidth - self.width: # when the paddle's x coordinate exceeds the screen width - the paddle's width (goes off the right side)
            self.rect.x = self.screenwidth - self.width # set it back to the screen width - the paddle's width (the furthest it can go without going off screen)
pygame.init() # initialize pygame library
screen = pygame.display.set_mode([800, 600]) # create screen with dimensions 800x600
pygame.display.set_caption('Breakout') # window title
pygame.mouse.set_visible(0) # mouse disappears when over the window
font = pygame.font.Font(None, 36) # set font to 36pt default
background = pygame.Surface(screen.get_size()) # create surface/background the same size as the screen (800x600) to draw objects on
# sprite lists
blocks = pygame.sprite.Group()
balls = pygame.sprite.Group()
allsprites = pygame.sprite.Group()
# initialize player
player = Player()
allsprites.add(player)
# initialize ball
ball = Ball()
allsprites.add(ball)
balls.add(ball)
top = 80 # top of block (y)
blockcount = 32
# make the blocks with nested for loops
for row in range(5): # 32 columns
    for column in range(0, blockcount): # create block (color, x, y)
        block = Block(blue, column * (block_width + 2) + 1, top)
        blocks.add(block)
        allsprites.add(block)
    top += block_height + 2 # move top y coord of the next line down 2 to accomodate the line we just made (height being 2)
clock = pygame.time.Clock() # clock to limit speed
game_over = False # whether the game is over
exit_program = False # whether to exit the program
while not exit_program: # main loop
    clock.tick(30) # 30 fps limit
    screen.fill(black) # fill screen with black
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit_program = True
    if not game_over: # as long as the game's not over
        # update player and ball positions
        player.update()
        game_over = ball.update()
    if game_over: # if the game is over
        # print game over message
        text = font.render("Game Over", True, white)
        textpos = text.get_rect(centerx=background.get_width()/2)
        textpos.top = 300
        screen.blit(text, textpos)
    if pygame.sprite.spritecollide(player, balls, False): # if the ball hits the player paddle
        # use diff to bounce ball left/right based on position of impact on paddle
        diff = (player.rect.x + player.width/2) - (ball.rect.x+ball.width/2)
        # set ball y for edge hits
        ball.rect.y = screen.get_height() - player.rect.height - ball.rect.height - 1
        ball.bounce(diff)
    # collisions btwn ball and blocks
    deadblocks = pygame.sprite.spritecollide(ball, blocks, True)
    if len(deadblocks) > 0: # if block hit
        ball.bounce(0) # bounce
        if len(blocks) == 0: # if all the blocks are gone
            game_over = True # the game's over
    allsprites.draw(screen) # draw all sprites
    pygame.display.flip() # flip screens to show the drawings
pygame.quit() # quit the program
