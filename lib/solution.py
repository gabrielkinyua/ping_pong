import pygame
import json

pygame.init()

WIDTH, HEIGHT = 700, 500
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Ping Pong")

FPS = 60

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
PADDLE_WIDTH, PADDLE_HEIGHT = 20, 100
BALL_RADIUS = 6


SCORE_FONT = pygame.font.SysFont("comicsans", 40)
WINNING_SCORE = 10

def save_score(left_score, right_score):
    scores = {"Left": left_score, "Right": right_score}
    with open("scores.json", "w") as file:
        json.dump(scores, file)

def load_score():
    try:
        with open("scores.json", "r") as file:
            return json.load(file)
    except FileNotFoundError:
        return {"Left": 0, "Right": 0}

def reset_score():
    save_score(0, 0)


class Paddle:
    COLOR = WHITE
    VELOCITY = 4

    def __init__(self, x, y, width, height):
        self.x = self.original_x = x
        self.y = self.original_y = y
        self.width = width
        self.height = height

    def draw(self, win):
        pygame.draw.rect(win, self.COLOR, (self.x, self.y, self.width, self.height))

    def move(self, up=True):
        if up:
            self.y -= self.VELOCITY
        else:
            self.y += self.VELOCITY

    def reset(self):
        self.x = self.original_x
        self.y = self.original_y

class Ball:
    COLOR = WHITE
    MAX_VEL = 5

    def __init__(self, x, y, radius):
        self.x = self.original_x = x
        self.y = self.original_y = y
        self.radius = radius
        self.x_vel = self.MAX_VEL
        self.y_vel = 0

    def draw(self, win):
        pygame.draw.circle(win, self.COLOR, (self.x, self.y), self.radius)

    def move(self):
        self.x += self.x_vel
        self.y += self.y_vel

    def reset(self):
        self.x = self.original_x
        self.y = self.original_y
        self.x_vel *= -1
        self.y_vel = 0


def draw(win, paddles, ball, left_score, right_score):
    win.fill(BLACK)

    left_score_text = SCORE_FONT.render(F"Score: {left_score}", 1, WHITE)
    right_score_text = SCORE_FONT.render(F"Score: {right_score}", 1, WHITE)
    win.blit(left_score_text, (WIDTH//4 - left_score_text.get_width()//2, 10))
    win.blit(right_score_text, (WIDTH//4 * 3 - right_score_text.get_width()//2, 10))
    
    for paddle in paddles:
        paddle.draw(win)

    for i in range (10, HEIGHT, HEIGHT//20):
        if i % 2 ==1:
            continue
        pygame.draw.rect(win, WHITE, (WIDTH//2 - 5, i, 10, HEIGHT//20))
    
    ball.draw(win)
    pygame.display.update()

def handle_collision(ball, left_paddle, right_paddle):
    if ball.y + ball.radius >= HEIGHT:
        ball.y_vel *= -1
    elif ball.y - ball.radius <= 0:
        ball.y_vel *= -1

    if ball.x_vel < 0:
        if ball.y >= left_paddle.y and ball.y <= left_paddle.y + left_paddle.height:
            if ball.x - ball.radius <= left_paddle.x + left_paddle.width:
                ball.x_vel *= -1

                middle_y = right_paddle.y + right_paddle.height//2
                difference_in_y = middle_y - ball.y
                reduction_factor = (right_paddle.height//2) / ball.MAX_VEL
                y_vel = difference_in_y / reduction_factor
                ball.y_vel = -1 * y_vel

    else:
        if ball.y >= right_paddle.y and ball.y <= right_paddle.y + right_paddle.height:
            if ball.x + ball.radius >= right_paddle.x:
                ball.x_vel *= -1




def handle_paddle_movement(keys, left_paddle, right_paddle):
    if keys[pygame.K_w] and left_paddle.y - left_paddle.VELOCITY > 0:
        left_paddle.move(up=True)
    if keys[pygame.K_s] and left_paddle.y + left_paddle.height + left_paddle.VELOCITY < HEIGHT:
        left_paddle.move(up=False)
    if keys[pygame.K_UP] and right_paddle.y - right_paddle.VELOCITY > 0:
        right_paddle.move(up=True)
    if keys[pygame.K_DOWN] and right_paddle.y + right_paddle.height + right_paddle.VELOCITY < HEIGHT:
        right_paddle.move(up=False)

def main():
    run = True
    clock = pygame.time.Clock()

    left_paddle = Paddle(10, HEIGHT//2 - PADDLE_HEIGHT//2, PADDLE_WIDTH, PADDLE_HEIGHT) 
    right_paddle = Paddle(WIDTH - 10 - PADDLE_WIDTH, HEIGHT//2 - PADDLE_HEIGHT//2, PADDLE_WIDTH, PADDLE_HEIGHT) 

    ball = Ball(WIDTH//2, HEIGHT//2, 10)

    scores = load_score()
    left_score =  scores["Left"]
    right_score = scores["Right"]


    while run:
        clock.tick(FPS)
        draw(WIN, [left_paddle, right_paddle], ball, left_score, right_score)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                break

        keys = pygame.key.get_pressed()
        handle_paddle_movement(keys, left_paddle, right_paddle)

        ball.move()
        handle_collision(ball, left_paddle, right_paddle)

        if ball.x < 0:
            right_score += 1
            ball.reset()
        elif ball.x > WIDTH:
            left_score += 1
            ball.reset()

        save_score(left_score, right_score)

        won = False
        if left_score == WINNING_SCORE:
            won = True
            win_text = "Left player won"
        elif right_score == WINNING_SCORE:
            won = True
            win_text = "Right player won"

        if won:
            text = SCORE_FONT.render(win_text, 1, WHITE)
            WIN.blit(text, (WIDTH//2 - text.get_width()//2, HEIGHT//2 - text.get_height()//2))
            pygame.display.update()
            pygame.time.delay(5000)
            ball.reset()
            reset_score()
            left_paddle.reset()
            right_paddle.reset()
            left_score = 0
            right_score = 0


    pygame.quit()

if __name__ == "__main__":
    main()
        
