import pygame
from pygame import mixer

pygame.init()

# window dimension
WIDTH = 1400
HEIGHT = 800

black = (0, 0, 0)
white = (255, 255, 255)
gray = (128, 128, 128)
dark_gray = (50, 50, 50)
green = (0, 255, 0)
gold = (212, 175, 55)
blue = (0, 255, 255)

screen = pygame.display.set_mode([WIDTH, HEIGHT])
pygame.display.set_caption("Drum-Machine")
label_font = pygame.font.Font('./public/Roboto-Bold.ttf', 32)
medium_font = pygame.font.Font('./public/Roboto-Bold.ttf', 24)

fps = 60
timer = pygame.time.Clock()
beats = 16
instruments = 6
boxes = []
clicked = [[-1 for _ in range(beats)] for _ in range(instruments)]  # -1 is for those that are not selected
bpm = 240*2
playing = True
active_length = 0
active_beat = 0
beat_changed = True

# load drum samples
hi_hat = mixer.Sound('.\public\sounds\hi hat.wav')
snare = mixer.Sound('.\public\sounds\snare.wav')
kick = mixer.Sound('.\public\sounds\kick.wav')
crash = mixer.Sound('.\public\sounds\crash.wav')
clap = mixer.Sound('.\public\sounds\clap.wav')
tom = mixer.Sound(".\public\sounds\\tom.wav")
pygame.mixer.set_num_channels(instruments * 3)


def play_notes():
    for i in range(len(clicked)):
        if clicked[i][active_beat] == 1:
            if i == 0:
                hi_hat.play()
            if i == 1:
                snare.play()
            if i == 2:
                kick.play()
            if i == 3:
                crash.play()
            if i == 4:
                clap.play()
            if i == 5:
                tom.play()


def draw_grid(clicks, beat):
    left_box = pygame.draw.rect(screen, gray, [0, 0, 200, HEIGHT - 200], 5)
    bottom_box = pygame.draw.rect(screen, gray, [0, HEIGHT - 200, WIDTH, 200], 5)

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
        pygame.draw.line(screen, gray, (0, (i * 100) + 100), (200, (i * 100) + 100), 3)

    # grid for the sequencer
    for i in range(beats):
        for j in range(instruments):
            if clicks[j][i] == -1:
                color = gray
            else:
                color = green

            rect = pygame.draw.rect(screen, color, [i * ((WIDTH - 200) // beats) + 205, (j * 100) + 5,
                                                    ((WIDTH - 200) // beats) - 10,
                                                    ((HEIGHT - 200) // instruments) - 10], 0, 3)

            pygame.draw.rect(screen, gold, [i * ((WIDTH - 200) // beats) + 200, (j * 100),
                                            ((WIDTH - 200) // beats), ((HEIGHT - 200) // instruments)], 5, 10)

            pygame.draw.rect(screen, black, [i * ((WIDTH - 200) // beats) + 200, (j * 100),
                                             ((WIDTH - 200) // beats), ((HEIGHT - 200) // instruments)], 2, 10)
            boxes.append((rect, (i, j)))
        active = pygame.draw.rect(screen, blue,
                                  [beat * ((WIDTH - 200) // beats) + 200, 0,
                                   ((WIDTH - 200) // beats), instruments * 100], 5, 3)
    return boxes


# main event loop
run = True
while run:
    timer.tick(fps)
    screen.fill(black)
    boxes = draw_grid(clicked, active_beat)

    # menu buttons
    play_pause = pygame.draw.rect(screen, gray, [50, HEIGHT - 150, 200, 100], 0, 5)
    play_text = label_font.render("Play/Pause", True, white)
    screen.blit(play_text, (70, HEIGHT - 130))

    if playing:
        play_text2 = medium_font.render("Playing", True, dark_gray)
    else:
        play_text2 = medium_font.render("Paused", True, dark_gray)
    screen.blit(play_text2, (70, HEIGHT - 100))


    # bpm
    bpm_rect = pygame.draw.rect(screen, gray, [300, HEIGHT-150, 75, 100],5, 5)
    bpm_text = medium_font.render("BPM", True, white)
    screen.blit(bpm_text, (310, HEIGHT - 130))
    bpm_text2 = label_font.render(f"{bpm}", True, white)
    screen.blit(bpm_text2, (310, HEIGHT - 100))


    # play note at every beat
    if beat_changed:
        play_notes()
        beat_changed = False

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
        if event.type == pygame.MOUSEBUTTONUP:
            if play_pause.collidepoint(event.pos):
                if playing:
                    playing = False
                elif not playing:
                    playing = True

    beat_length = (fps * 60) // bpm

    if playing:
        if active_length < beat_length:
            active_length += 1
        else:
            active_length = 0
            if active_beat < beats - 1:
                active_beat += 1
                beat_changed = True
            else:
                active_beat = 0
                beat_changed = True

    pygame.display.flip()

pygame.quit()
