#!/usr/bin/env python
import pygame
from pygame.locals import *
import time
import random
import tkinter as tk
from tkinter import filedialog, messagebox

SIZE = 40


class Cavatappi:
    def __init__(self, parent_screen, image_path):
        self.image = pygame.image.load(image_path).convert()
        self.image = pygame.transform.scale(self.image, (40, 40))  # Resize to 40x40
        self.parent_screen = parent_screen
        self.x = SIZE*3
        self.y = SIZE*3

    def draw(self):
        self.parent_screen.blit(self.image, (self.x, self.y))
        pygame.display.flip()

    def move(self):
        self.x = random.randint(1, 24) * SIZE
        self.y = random.randint(1, 19) * SIZE


class Snake:
    def __init__(self, parent_screen, length, body_image_path, head_image_path):
        self.length = length
        self.parent_screen = parent_screen
        self.body_block = pygame.image.load(body_image_path).convert()
        self.body_block = pygame.transform.scale(self.body_block, (40, 40))  # Resize body to 40x40
        self.head_block = pygame.image.load(head_image_path).convert()
        self.head_block = pygame.transform.scale(self.head_block, (40, 40))  # Resize head to 40x40
        self.x = [SIZE]*length
        self.y = [SIZE]*length
        self.direction = 'down'

    def increase_length(self):
        self.length += 1
        self.x.append(-1)
        self.y.append(-1)

    def draw(self):
        # Draw the head
        self.parent_screen.blit(self.head_block, (self.x[0], self.y[0]))

        # Draw body
        for i in range(1, self.length):
            self.parent_screen.blit(self.body_block, (self.x[i], self.y[i]))
        pygame.display.flip()

    def move_left(self):
        if self.direction != 'right':  # Prevent moving left if currently moving right
            self.direction = 'left'

    def move_right(self):
        if self.direction != 'left':  # Prevent moving right if currently moving left
            self.direction = 'right'

    def move_up(self):
        if self.direction != 'down':  # Prevent moving up if currently moving down
            self.direction = 'up'

    def move_down(self):
        if self.direction != 'up':  # Prevent moving down if currently moving up
            self.direction = 'down'

    def walk(self):
        for i in range(self.length-1, 0, -1):
            self.x[i] = self.x[i-1]
            self.y[i] = self.y[i-1]

        if self.direction == 'up':
            self.y[0] -= SIZE
        if self.direction == 'down':
            self.y[0] += SIZE
        if self.direction == 'left':
            self.x[0] -= SIZE
        if self.direction == 'right':
            self.x[0] += SIZE

        self.draw()


class Game:
    def __init__(self, snake_body_image, snake_head_image, cavatappi_image):

        # Store the image paths for use in the reset function
        self.snake_body_image = snake_body_image
        self.snake_head_image = snake_head_image
        self.cavatappi_image = cavatappi_image

        pygame.init()
        pygame.mixer.init()
        self.play_background_music()
        self.surface = pygame.display.set_mode((1000, 800))
        self.snake = Snake(self.surface, 3, snake_body_image, snake_head_image)
        self.snake.draw()
        self.cavatappi = Cavatappi(self.surface, cavatappi_image)
        self.cavatappi.draw()

    def is_collision(self, x1, y1, x2, y2):
        if abs(x1 - x2) < SIZE and abs(y1 - y2) < SIZE:
            return True
        return False

    def past_limit(self, x, y):
        if 0 > x or x >= 1000 or 0 > y or y >= 800:
            return True
        return False

    def play_background_music(self):
        pygame.mixer.music.load("resources/snake_music.mp3")
        pygame.mixer.music.set_volume(0.2)
        pygame.mixer.music.play()

    def play_sound(self, sound):
        sound = pygame.mixer.Sound(f"resources/{sound}.mp3")
        pygame.mixer.Sound.play(sound)

    def render_background(self):
        bg = pygame.image.load("resources/background.jpeg")
        self.surface.blit(bg, (0,0))

    def play(self):
        self.render_background()
        self.snake.walk()
        self.cavatappi.draw()
        self.display_score()
        pygame.display.flip()

        # snake colliding with cavatappi
        if self.is_collision(self.snake.x[0], self.snake.y[0], self.cavatappi.x, self.cavatappi.y):
            self.snake.increase_length()
            self.cavatappi.move()
            self.play_sound("nomnom")

        # snake collision with self
        for i in range(3, self.snake.length):
            if self.is_collision(self.snake.x[0], self.snake.y[0], self.snake.x[i], self.snake.y[i]):
                self.play_sound("yummy")
                raise "Collision Occurred"

        # snake passes limit
        if self.past_limit(self.snake.x[0], self.snake.y[0]):
            self.play_sound("yummy")
            raise "Collision Occurred"

    def display_score(self):
        font = pygame.font.SysFont('arial', 30)
        score = font.render(f"Score: {self.snake.length - 3}", True, (255, 255, 255))
        self.surface.blit(score, (800, 10))

    def show_game_over(self):
        self.render_background()
        font = pygame.font.SysFont('arial', 30)
        line1 = font.render(f"The Snake is Satisfied! She ate: {self.snake.length} cavatappi noodles!", True, (255, 255, 255))
        self.surface.blit(line1, (200,300))
        line2 = font.render("To play again press Enter. To exit press Escape", True, (255, 255, 255))
        self.surface.blit(line2, (200, 400))
        pygame.display.flip()
        pygame.mixer.music.pause()

    def reset(self):
        self.snake = Snake(self.surface, 3, self.snake_body_image, self.snake_head_image)
        self.cavatappi = Cavatappi(self.surface, self.cavatappi_image)

    def run(self):
        running = True
        pause = False

        while running:
            for event in pygame.event.get():
                if event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                        running = False

                    if event.key == K_RETURN:
                        pygame.mixer.music.unpause()
                        pause = False

                    if not pause:
                        if event.key == K_UP:
                            self.snake.move_up()

                        if event.key == K_DOWN:
                            self.snake.move_down()

                        if event.key == K_LEFT:
                            self.snake.move_left()

                        if event.key == K_RIGHT:
                            self.snake.move_right()

                elif event.type == QUIT:
                    running = False

            try:
                if not pause:
                    self.play()
            except Exception as e:
                self.show_game_over()
                pause = True
                self.reset()

            time.sleep(0.1)

def start_game():
    def select_images():
        # Initialize tkinter
        root = tk.Tk()
        root.withdraw()  # Hide the main window

        # Ask the user if they want to use custom images or default ones
        use_default = messagebox.askyesno("Use Default Images", "Do you want to use the default blocks?")

        if use_default:
            # Use default images
            snake_body_image = "resources/BodyDefault.jpg"
            snake_head_image = "resources/HeadDefault.jpeg"
            cavatappi_image = "resources/defaultMouse.jpeg"
        else:
            # Let the user select images
            snake_body_image = filedialog.askopenfilename(title="Select Snake Body Image")
            snake_head_image = filedialog.askopenfilename(title="Select Snake Head Image")
            cavatappi_image = filedialog.askopenfilename(title="Select Food Image")
        return snake_body_image, snake_head_image, cavatappi_image

    snake_body_image, snake_head_image, cavatappi_image = select_images()
    game = Game(snake_body_image, snake_head_image, cavatappi_image)
    game.run()


if __name__ == '__main__':
    start_game()
