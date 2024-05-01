import pygame
import sys


class Paz(object):
    # code function 'def __init__(self):' to set initial values of the game screen and character
    def __init__(self):
        # start the game
        pygame.init()
        # set the game state to be "started" to be True
        self.game_started = True

        # set the game screen size to 800x600
        self.screen = pygame.display.set_mode((800, 600))
        # get the width and height of the screen to use later
        self.screen_width, self.screen_height = self.screen.get_size()

        # set the initial position of the character to the center of screen by dividing both width and height of the screen by mod 2
        self.character_pos = [self.screen_width // 2, self.screen_height // 2]
        # set the size of the character as a circle to diameter of 50 pixels
        self.character_size = 50
        # set the speed of the character to be 1 pixel per frame
        self.character_speed = 1

    #code the function 'def draw_character(self):' to draw the character as a circle and lines
    def draw_character(self):

        # Draw a circle on the center of the screen as the character.
        # Character color is hot pink, radius of circle is character size//2, and speed is 1 pixel per frame
        pygame.draw.circle(self.screen, (255, 105, 180), self.character_pos, self.character_size//2, 1)

        # Draw a symmetrical vertical line on the circle
        pygame.draw.line(
            self.screen, (255, 105, 180),
            (self.character_pos[0], self.character_pos[1] - self.character_size//2),
            (self.character_pos[0], self.character_pos[1] + self.character_size//2),
            1
        )
        # Draw a symmetrical horizontal line on the circle
        pygame.draw.line(
            self.screen, (255, 105, 180),
            (self.character_pos[0] - self.character_size//2, self.character_pos[1]),
            (self.character_pos[0] + self.character_size//2, self.character_pos[1]),
            1
        )

    # code the function 'move_character' to move the character with arrow keys
    def move_character(self):
        # get the current state of the keyboard
        keys = pygame.key.get_pressed()
        # if the up arrow key is pressed, move the character up
        if keys[pygame.K_UP]:
            self.character_pos[1] -= self.character_speed
        # if the down arrow key is pressed, move the character down
        if keys[pygame.K_DOWN]:
            self.character_pos[1] += self.character_speed
        # if the left arrow key is pressed, move the character left
        if keys[pygame.K_LEFT]:
            self.character_pos[0] -= self.character_speed
        # if the right arrow key is pressed, move the character right
        if keys[pygame.K_RIGHT]:
            self.character_pos[0] += self.character_speed

        # make sure the character stays within the bounds of the screen (no test)
        self.character_pos[0] = max(
            min(self.character_pos[0], self.screen_width - self.character_size // 2),
            self.character_size // 2,
        )
        self.character_pos[1] = max(
            min(self.character_pos[1], self.screen_height - self.character_size // 2),
            self.character_size // 2,
        )

    #code the function "def game_loop(self):" to have a game loop based on other functions
    def game_loop(self):
        # code the main game loop that runs indefinitely until the game is quit
        while True:
            # iterate over all current events
            for event in pygame.event.get():
                # if the event is a keypress and the 'q' key was pressed, quit the game
                if event.type == pygame.KEYDOWN and event.key == pygame.K_q:
                    pygame.quit()
                    sys.exit()

            # if the game has started, clear the screen and perform game operations
            if self.game_started:
                # fill the whole game window with color black
                self.screen.fill((0, 0, 0))

                # draw the character on the screen
                self.draw_character()

                # update the character's position based on key presses
                self.move_character()

            # update the display to reflect any changes
            pygame.display.flip()


if __name__ == "__main__":
    # create a Paz object and start the game loop
    game = Paz()
    game.game_loop()
