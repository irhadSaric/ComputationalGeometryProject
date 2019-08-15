import pygame

# === CONSTANS === (UPPER_CASE names)

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

SCREEN_WIDTH = 600
SCREEN_HEIGHT = 400

BLOCK_SIZE = 50
CIRCLE_RADIUS = int(BLOCK_SIZE / 2)

# === CLASSES === (CamelCase names)

'''
class Button():
'''

# === FUNCTIONS === (lower_case names)

# empty

# === MAIN === (lower_case names)

# --- (global) variables ---

# --- init ---

pygame.init()

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
screen_rect = screen.get_rect()

# --- objects ---

'''
button = Button(...)
'''

rects = []
rects.append(pygame.Rect(SCREEN_WIDTH // 2 - CIRCLE_RADIUS, SCREEN_HEIGHT // 2 - CIRCLE_RADIUS, BLOCK_SIZE, BLOCK_SIZE))
rects.append(pygame.Rect(0, 0, BLOCK_SIZE, BLOCK_SIZE))

selected = None

# --- mainloop ---

clock = pygame.time.Clock()
is_running = True
moves_counter = 1

while is_running:
    # --- events ---

    for event in pygame.event.get():

        # --- global events ---

        if event.type == pygame.QUIT:
            is_running = False

        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                is_running = False

        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                for i, r in enumerate(rects):
                    # Pythagoras a^2 + b^2 = c^2
                    dx = r.centerx - event.pos[0]  # a
                    dy = r.centery - event.pos[1]  # b
                    distance_square = dx ** 2 + dy ** 2  # c^2

                    if distance_square <= CIRCLE_RADIUS ** 2:  # c^2 <= radius^2
                        selected = i
                        selected_offset_x = r.x - event.pos[0]
                        selected_offset_y = r.y - event.pos[1]

        elif event.type == pygame.MOUSEBUTTONUP:
            moves_counter += 1
            for circle in rects:
                print(circle)
            rects.append(pygame.Rect(0, 0, BLOCK_SIZE, BLOCK_SIZE))
            if event.button == 1:
                selected = None

        elif event.type == pygame.MOUSEMOTION:
            if selected is not None:  # selected can be `0` so `is not None` is required
                # move object
                rects[selected].x = event.pos[0] + selected_offset_x
                rects[selected].y = event.pos[1] + selected_offset_y

        # --- objects events ---

        '''
       button.handle_event(event)
       '''

    # --- updates ---

    # empty

    # --- draws ---

    screen.fill(BLACK)


    pygame.draw.circle(screen, GREEN, (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2), 200)
    '''
    button.draw(screen)    
    '''

    # draw rect
    for r in rects:
        pygame.draw.circle(screen, RED, r.center, CIRCLE_RADIUS)

    pygame.draw.line(screen, WHITE, (SCREEN_WIDTH // 2, 0), (SCREEN_WIDTH // 2, SCREEN_HEIGHT))
    pygame.draw.line(screen, WHITE, (0, SCREEN_HEIGHT // 2), (SCREEN_WIDTH, SCREEN_HEIGHT // 2))
    pygame.display.update()

    # --- FPS ---

    clock.tick(25)

# --- the end ---

pygame.quit()