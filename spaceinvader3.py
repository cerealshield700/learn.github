import pygame
import random
# pygame setup
pygame.init()
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Space Invaders")

# Load background image
background = pygame.image.load("background.png")

# Clock for controlling FPS
clock = pygame.time.Clock()

# Player class
class Player(object):
    def __init__(self):
        self.img = pygame.image.load("player.png")
        self.x = 370
        self.y = 480
        self.x_change = 0
        self.y_change = 0
        self.lives = 3

    def draw(self):
        screen.blit(self.img, (self.x, self.y))

# Enemy class
class Alien(object):
    def __init__(self):
        # Load the original alien image
        original_img = pygame.image.load("alien.png")
        
        # Scale the image to 5% of its original size
        self.img = pygame.transform.scale(original_img, 
                                          (int(original_img.get_width() * 0.025), 
                                           int(original_img.get_height() * 0.025)))
        
        # Spawn at a random position
        self.x = random.randint(0, 735)
        self.y = random.randint(50, 250)
        self.x_change = random.choice([-3, 3])  # Random horizontal direction
        self.y_change = 10

    def move(self):
        # Update position
        self.x += self.x_change

        # Reverse direction if hitting screen boundaries
        if self.x <= 0 or self.x >= 800 - self.img.get_width():
            self.x_change *= -1
            self.y += self.y_change  # Move down when changing direction

    def draw(self):
        screen.blit(self.img, (self.x, self.y))

class Bullet(object):
    def __init__(self):
        # Load and scale the bullet image
        original_img = pygame.image.load("bullet.png")
        self.img = pygame.transform.scale(original_img, (10, 20))  # Adjust width and height as needed
        self.x = 0
        self.y = 480
        self.y_change = 10
        self.state = "ready"  # "ready" means the bullet is not visible, "fired" means it is moving

    def fire(self, x, y):
        self.state = "fired"
        self.x = x + 16  # Align bullet with the center of the player
        self.y = y

    def move(self):
        if self.state == "fired":
            self.y -= self.y_change
        if self.y <= 0:  # Reset bullet when it goes off-screen
            self.state = "ready"

    def draw(self):
        if self.state == "fired":
            screen.blit(self.img, (self.x, self.y))

def is_collision(enemy, bullet):
    # Check if the bullet hits the enemy
    distance = ((enemy.x - bullet.x) ** 2 + (enemy.y - bullet.y) ** 2) ** 0.5
    return distance < 27  # Collision threshold

# Initialize player, bullet, and enemies
player = Player()
bullet = Bullet()

num_of_enemies = 6
enemies = [Alien() for _ in range(num_of_enemies)]

# Fire rate control
fire_cooldown = 5  # Cooldown in milliseconds (e.g., 500ms = 0.5 seconds)
last_fire_time = pygame.time.get_ticks()  # Initialize with the current time

# Main game loop
running = True
while running:
    # Draw the background
    screen.blit(background, (0, 0))

    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        # Check for key presses
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                player.x_change = -5
            if event.key == pygame.K_RIGHT:
                player.x_change = 5
            if event.key == pygame.K_SPACE and bullet.state == "ready":
                current_time = pygame.time.get_ticks()
                if current_time - last_fire_time >= fire_cooldown:  # Check cooldown
                    bullet.fire(player.x, player.y)
                    last_fire_time = current_time  # Update the last fire time
        if event.type == pygame.KEYUP:
            if event.key in [pygame.K_LEFT, pygame.K_RIGHT]:
                player.x_change = 0

    # Update player position
    player.x += player.x_change
    player.x = max(0, min(player.x, 800 - player.img.get_width()))

    # Update and draw enemies
    for alien in enemies[:]:  # Use a copy of the list to safely remove items
        alien.move()
        alien.draw()

        # Check for collision
        if is_collision(alien, bullet):
            bullet.state = "ready"  # Reset bullet
            bullet.y = 480
            enemies.remove(alien)  # Remove the enemy from the list

    # Update and draw bullet
    bullet.move()
    bullet.draw()

    # Draw the player
    player.draw()

    # Update the display
    pygame.display.update()

    # Limit FPS to 60
    clock.tick(60)

pygame.quit()