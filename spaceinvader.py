import pygame

# pygame setup
pygame.init()
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Space Invaders")
clock = pygame.time.Clock()

# Player class
class Player(object):
    def __init__(self):
        self.x = 370
        self.y = 480
        self.x_change = 0
        self.y_change = 0
        self.lives = 3

    def draw(self):
        # Draw a simple triangular spaceship
        pygame.draw.polygon(screen, (0, 255, 0), [(self.x, self.y), (self.x - 20, self.y + 40), (self.x + 20, self.y + 40)])

# Initialize player
player = Player()

# Main game loop
running = True
while running:
    # Fill the screen with black
    screen.fill((0, 0, 0))

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
            if event.key == pygame.K_UP:
                player.y_change = -5
            if event.key == pygame.K_DOWN:
                player.y_change = 5
        if event.type == pygame.KEYUP:
            if event.key in [pygame.K_LEFT, pygame.K_RIGHT]:
                player.x_change = 0
            if event.key in [pygame.K_UP, pygame.K_DOWN]:
                player.y_change = 0

    # Update player position
    player.x += player.x_change
    player.y += player.y_change

    # Ensure the player stays within screen bounds
    player.x = max(20, min(player.x, 780))
    player.y = max(0, min(player.y, 560))

    # Draw the player
    player.draw()

    # Update the display
    pygame.display.update()

    # Limit FPS to 60
    clock.tick(60)

pygame.quit()