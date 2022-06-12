import pygame
from pygame import mixer
pygame.init()

# window dimension
WIDTH = 1400
HEIGHT = 800

black = (0, 0, 0)
white = (255, 255, 255)
gray = (128, 128, 128)
green = (0,255, 0)
gold = (212, 175, 55)

screen = pygame.display.set_mode([WIDTH, HEIGHT])
pygame.display.set_caption("Drum-Machine")
label_font = pygame.font.Font('Roboto-Bold.ttf', 32)

fps = 60
timer = pygame.time.Clock()
beats = 16
instruments = 6
boxes = []
clicked = [[-1 for  _ in range(beats)] for _ in range(instruments)] # -1 is for those that are not selected
bpm = 240


def draw_grid(clicks):

    left_box = pygame.draw.rect(screen, gray, [0, 0, 200, HEIGHT-200], 5)
    bottom_box = pygame.draw.rect(screen, gray, [0, HEIGHT-200, WIDTH, 200], 5)

    boxes = []
    colors = [gray, white, gray]

    kick_text = label_font.render('Kick', True, white)
    screen.blit(kick_text, (30, 230))
    snare_text = label_font.render('Snare', True, white)
    screen.blit(snare_text, (30, 130))
    closed_hat_text = label_font.render("Hat", True, white)
    screen.blit(closed_hat_text, (30, 30))
    crash_text = label_font.render('Crash', True, white)
    screen.blit(crash_text, (30, 330))
    clap_text = label_font.render('Clap', True, white)
    screen.blit(clap_text, (30, 430))
    tom_text = label_font.render('Tom', True, white)
    screen.blit(tom_text, (30, 530))

# outer lines per instrument
    for i in range(instruments):
        pygame.draw.line(screen, gray, (0, (i*100)+100), (200, (i*100)+100), 3)

# grid for the sequencer
    for i in range(beats):
        for j in range(instruments):
            if clicks[j][i] == -1:
                color = gray
            else:
                color = green

            rect = pygame.draw.rect(screen, color, [i * ((WIDTH-200) // beats) + 205, (j*100)+5,
                                                   ((WIDTH-200)//beats)-10, ((HEIGHT-200) // instruments)-10], 0, 3)

            pygame.draw.rect(screen, gold, [i * ((WIDTH - 200) // beats) + 200, (j * 100),
                                             ((WIDTH - 200) // beats), ((HEIGHT - 200) // instruments)], 5, 10)

            pygame.draw.rect(screen, black, [i * ((WIDTH - 200) // beats) + 200, (j * 100),
                                                   ((WIDTH - 200) // beats), ((HEIGHT - 200) // instruments)], 2, 10)
            boxes.append((rect,(i,j)))

    return boxes



# main event loop
run = True
while run:
    timer.tick(fps)
    screen.fill(black)
    boxes = draw_grid(clicked)

    # event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            # if we clicked on any of the grid sequence rectangles
            for i in range(len(boxes)):
                if boxes[i][0].collidepoint(event.pos):
                    coords = boxes[i][1]
                    clicked[coords[1]][coords[0]] *= -1  # invert the thing when selected if -1 => 1 and vice versa

    beat_length = (fps*60) // bpm




    pygame.display.flip()

pygame.quit()
