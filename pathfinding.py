# system imports
import sys

# pip installed imports
import pygame

# initializing pygame
pygame.init()
font = pygame.font.SysFont(None, 24)


# home screen
def home_screen(error_message=""):
    # initializing screen
    screen = pygame.display.set_mode((800, 600))
    pygame.display.set_caption("Home")

    # start button
    start_button_rect = pygame.Rect((300, 400), (200, 50))
    start_button_text = font.render("Start!", True, (255, 255, 255))

    # grid buttons
    grid_size_x = pygame.Rect((300, 200), (200, 50))
    grid_size_y = pygame.Rect((300, 300), (200, 50))

    # text above grid
    grid_size_text = font.render("Choose dimensions of the grid (both sides should be <=30 blocks long).", True, (0, 0, 0))

    # sizes entered by the user
    x = ""
    y = ""

    # sizes displayed on grid buttons
    grid_size_x_value = font.render(x, True, (255, 255, 255))
    grid_size_y_value = font.render(y, True, (255, 255, 255))

    # selected grid size button
    current_button = ""
    
    # error message displayed (if any)
    error_message_text = font.render(error_message, True, (255, 0, 0))
    
    # update
    while True:
        for event in pygame.event.get():
            # quit event
            if event.type == pygame.QUIT:
                sys.exit()
            
            if event.type == pygame.MOUSEBUTTONDOWN:
                # on click of the start button
                if start_button_rect.collidepoint(event.pos):
                    path(x, y)

                # on click of one of the grid buttons
                if grid_size_x.collidepoint(event.pos):
                    current_button = "x"
                if grid_size_y.collidepoint(event.pos):
                    current_button = "y"

            if event.type == pygame.KEYDOWN:
                # add text when typing
                char = pygame.key.name(event.key)
                # check if the pressed key is backspace
                if event.key == pygame.K_BACKSPACE:
                    if current_button == "x":
                        x = x[:-1]
                        grid_size_x_value = font.render(x, True, (255, 255, 255))
                    if current_button == "y":
                        y = y[:-1]
                        grid_size_y_value = font.render(y, True, (255, 255, 255))
                # check if the pressed key is enter
                elif event.key == pygame.K_RETURN:
                    path(x, y)
                # if it's a number
                elif char.isnumeric():
                    if current_button == "x":
                        x += char
                        grid_size_x_value = font.render(x, True, (255, 255, 255))
                    if current_button == "y":
                        y += char
                        grid_size_y_value = font.render(y, True, (255, 255, 255))
        
        # white screen
        screen.fill((255, 255, 255))

        # drawing the start button
        pygame.draw.rect(screen, (0, 0, 0), start_button_rect)
        screen.blit(start_button_text, (start_button_rect.centerx - list(font.size("Start!"))[0]/2, start_button_rect.centery - list(font.size("Start!"))[1]/2))

        # drawing the grid size customization
        if current_button == "x":
            pygame.draw.rect(screen, (0, 255, 0), grid_size_x)
        else:
            pygame.draw.rect(screen, (0, 0, 0), grid_size_x)
        if current_button == "y":
            pygame.draw.rect(screen, (0, 255, 0), grid_size_y)
        else:
            pygame.draw.rect(screen, (0, 0, 0), grid_size_y)
        screen.blit(grid_size_text, (400 - list(font.size("Choose dimensions of the grid (both sides should be <=30 blocks long)"))[0]/2, 100))
        screen.blit(grid_size_x_value, (400 - list(font.size(x))[0]/2, 225 - list(font.size(x))[1]/2))
        screen.blit(grid_size_y_value, (400 - list(font.size(y))[0]/2, 325 - list(font.size(y))[1]/2))

        # displaying error message
        screen.blit(error_message_text, (0, 0))

        # updating frames
        pygame.display.flip()


def path(x, y):
    # checking if the sizes of the grid are numbers
    try:
        x, y = int(x), int(y)
    except:
        home_screen("Please enter numbers for the sizes of the grid.")

    # checking if the numbers are between 1 and 30
    if x < 1 or x > 30 or y < 1 or y > 30:
        home_screen("Both sizes should  be numbers between 1 and 30.")

    # create the screen
    screen = pygame.display.set_mode((800, 600))
    pygame.display.set_caption("Pathfinder")

    # create the grid
    start_x = 0
    start_y = 0
    grid = []
    for i in range(y):
        grid.append([])
        for j in range(x):
            rect = pygame.Rect((start_x, start_y), (20, 20))
            grid[i].append(rect)
            start_x += 20
        start_y += 20
        start_x = 0

    # coordinates for key points on the grid
    beginning = []
    end = []
    obstacles = []

    # help message displayed on screen
    help_message = "Select a starting point."
    help_text = font.render(help_message, True, (0, 0, 0))

    # state ( 0 -> selecting starting point, 1 -> selecting end point, 2 -> drawing obstacles, 3 -> simulating)
    state = 0

    # start button after selecting end point
    start_button_rect = pygame.Rect((625, 200), (150, 50))
    start_button_text = font.render("Start simulation", True, (255, 255, 255))

    # update
    while True:
        for event in pygame.event.get():
            # quit event
            if event.type == pygame.QUIT:
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                # choosing points event
                y1, x1 = event.pos
                # getting coordinates of clicked button
                x1, y1 = x1 // 20, y1 // 20
                if y1 < x-1 and x1 < y-1:
                    # setting beginning point
                    if state == 0:
                        beginning = [x1, y1]
                        state = 1
                        help_message = "Select an ending point."
                        help_text = font.render(help_message, True, (0, 0, 0))
                    # setting ending point
                    elif state == 1:
                        end = [x1, y1]
                        state = 2
                        help_message = "Select obstacles."
                        help_text = font.render(help_message, True, (0, 0, 0))
                    # setting obstacles
                    elif state == 2:
                        obstacles.append([x1, y1])

                # start simulation event
                if start_button_rect.collidepoint(event.pos) and state >= 2:
                    state = 3
                    # start looking for all possible paths
                    possible_paths = [[beginning]]

            # use enter instead of the start button
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    state = 3
                    # start looking for all possible paths
                    possible_paths = [[beginning]]
        
        # white screen
        screen.fill((255, 255, 255))

        # display the grid
        for row in grid:
            for rect in row:
                pygame.draw.rect(screen, (0, 0, 0), rect, 1)

        # display starting, end points and obstacles if any
        if state >= 1:
            pygame.draw.rect(screen, (0, 255, 0), grid[beginning[0]][beginning[1]])
        if state >= 2:
            pygame.draw.rect(screen, (255, 0, 0), grid[end[0]][end[1]])
            for obstacle in obstacles:
                pygame.draw.rect(screen, (0, 0, 255), grid[obstacle[0]][obstacle[1]])

        # display help message
        screen.blit(help_text, (620, 20))

        # display start button
        if state >= 2:
            pygame.draw.rect(screen, (0, 0, 0), start_button_rect)
            screen.blit(start_button_text, (700 - list(font.size("Start simulation."))[0]/2, 225 - list(font.size("Start simulation."))[1]/2))

        # update frame
        pygame.display.flip()


home_screen()
