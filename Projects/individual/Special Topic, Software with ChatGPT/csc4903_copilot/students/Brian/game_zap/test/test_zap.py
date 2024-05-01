import unittest
from unittest.mock import patch
import pygame

from zap import Paz


class TestPaz(unittest.TestCase):
    def setUp(self):
        pygame.init()
        self.game = Paz()

    def test_init(self): # test init function
        self.assertEqual(self.game.game_started, True)  # verifies if game is running
        self.assertEqual(self.game.screen.get_size(), (800, 600)) # make sure the screen size is 800x600
        self.assertEqual(self.game.character_pos, [400, 300]) # check if the character at center
        self.assertEqual(self.game.character_size, 50) # make sure character size = 50 pixels
        self.assertEqual(self.game.character_speed, 1) # make sure character speed = 1 pixel per frame

    # This test checks if 'pygame.draw.circle' and 'pygame.draw.line' are called with the correct arguments when draw_character is called.
    # However, it doesn't confirm that the correct image was drawn to the screen. Better to test it by running the game!
    def test_draw_character(self):
        with patch('pygame.draw.circle') as mock_circle, patch('pygame.draw.line') as mock_line:
            self.game.draw_character()

        # check if circle was drawn with expected arguments
        mock_circle.assert_called_once_with(
            self.game.screen, (255, 105, 180), self.game.character_pos, self.game.character_size // 2, 1)

        # check if lines were drawn with expected arguments
        assert mock_line.call_count == 2
        mock_line.assert_any_call(
            self.game.screen, (255, 105, 180),
            (self.game.character_pos[0], self.game.character_pos[1] - self.game.character_size // 2),
            (self.game.character_pos[0], self.game.character_pos[1] + self.game.character_size // 2),
            1
        )
        mock_line.assert_any_call(
            self.game.screen, (255, 105, 180),
            (self.game.character_pos[0] - self.game.character_size // 2, self.game.character_pos[1]),
            (self.game.character_pos[0] + self.game.character_size // 2, self.game.character_pos[1]),
            1
        )

    # test for character movement with arrow keys
    # 'mock' the key press with patch
    # missing test for out of bounds
    def test_move_character(self):
        # make a copy of character position to reset after each input
        original_pos = self.game.character_pos.copy()

        # create a dictionary to simulate key presses
        keys = {pygame.K_UP: True, pygame.K_DOWN: False, pygame.K_LEFT: False, pygame.K_RIGHT: False}

        # simulate pressing the up arrow key
        with patch('pygame.key.get_pressed', return_value=keys):
            self.game.move_character()
        assert self.game.character_pos[1] == original_pos[1] - self.game.character_speed

        # reset character position
        self.game.character_pos = original_pos.copy()

        # simulate pressing the down arrow key
        keys[pygame.K_UP] = False
        keys[pygame.K_DOWN] = True
        with patch('pygame.key.get_pressed', return_value=keys):
            self.game.move_character()
        assert self.game.character_pos[1] == original_pos[1] + self.game.character_speed

        # reset character position
        self.game.character_pos = original_pos.copy()

        # simulate pressing the left arrow key
        keys[pygame.K_DOWN] = False
        keys[pygame.K_LEFT] = True
        with patch('pygame.key.get_pressed', return_value=keys):
            self.game.move_character()
        assert self.game.character_pos[0] == original_pos[0] - self.game.character_speed

        # reset character position
        self.game.character_pos = original_pos.copy()

        # simulate pressing the right arrow key
        keys[pygame.K_LEFT] = False
        keys[pygame.K_RIGHT] = True
        with patch('pygame.key.get_pressed', return_value=keys):
            self.game.move_character()
        assert self.game.character_pos[0] == original_pos[0] + self.game.character_speed

    # test if the game loop is running correctly
    def test_game_loop(self):
        # make game_started True for testing
        self.game.game_started = True

        # mock the pygame's event.get, display.flip methods
        # and your draw_character and move_character methods
        with patch('pygame.event.get', side_effect=[[pygame.event.Event(pygame.KEYDOWN, key=pygame.K_a)],
                                                    [pygame.event.Event(pygame.KEYDOWN, key=pygame.K_q)]]), \
                patch('pygame.display.flip') as mock_flip, \
                patch.object(self.game, 'draw_character') as mock_draw_char, \
                patch.object(self.game, 'move_character') as mock_move_char:

            # run the game_loop in try-except block to catch SystemExit
            try:
                self.game.game_loop()
            except SystemExit:
                print("Game loop exited successfully on 'q' key press event")

            # check if draw_character and move_character methods were called once
            mock_draw_char.assert_called_once()
            mock_move_char.assert_called_once()

            # check if display.flip was called once
            mock_flip.assert_called_once()


if __name__ == "__main__":
    unittest.main()
