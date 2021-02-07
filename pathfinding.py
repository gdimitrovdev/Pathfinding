# system imports
import sys

# pip installed imports
import pygame

# imports from my files
import config
from bruteforce_algorithm import bruteforce
from a_star_algorithm import a_star

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
    for i in range(x):
        grid.append([])
        for j in range(y):
            rect = pygame.Rect((start_x, start_y), (20, 20))
            grid[i].append(rect)
            start_y += 20
        start_x += 20
        start_y = 0

    # coordinates for key points on the grid
    beginning = []
    end = []
    obstacles = {}

    # help message displayed on screen
    help_message = "Select a starting point."
    help_text = font.render(help_message, True, (0, 0, 0))

    # warning message displayed on screen
    warning_text_1 = font.render("Don't use bruteforce on", True, (0, 0, 0))
    warning_text_2 = font.render("grids larger than 8x8!", True, (0, 0, 0))

    # method ( 0 -> bruteforce, 1 -> A* )
    method = ""

    # start button after selecting end point
    # bruteforce
    start_button_brute_rect = pygame.Rect((615, 200), (170, 50))
    start_button_brute_text = font.render("Start with bruteforce", True, (255, 255, 255))

    # a* algorithm
    start_button_a_rect = pygame.Rect((615, 300), (170, 50))
    start_button_a_text = font.render("Start with A*", True, (255, 255, 255))

    # start over button
    start_over_rect = pygame.Rect((615, 400), (170, 50))
    start_over_text = font.render("Find another path", True, (255, 255, 255))

    # update
    while True:
        for event in pygame.event.get():
            # quit event
            if event.type == pygame.QUIT:
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                # choosing points event
                x1, y1 = event.pos
                # getting coordinates of clicked button
                x1, y1 = x1 // 20, y1 // 20
                if x1 < x and y1 < y:
                    # setting beginning point
                    if config.state == 0:
                        beginning = [x1, y1]
                        config.state = 1
                        help_message = "Select an ending point."
                        help_text = font.render(help_message, True, (0, 0, 0))
                    # setting ending point
                    elif config.state == 1 and (x1 != beginning[0] or y1 != beginning[1]):
                        end = [x1, y1]
                        config.state = 2
                        help_message = "Select obstacles."
                        help_text = font.render(help_message, True, (0, 0, 0))
                    # setting obstacles
                    elif config.state == 2 and (x1 != beginning[0] or y1 != beginning[1]) and (x1 != end[0] or y1 != end[1]):
                        obstacles[(x1, y1)] = True

                # start simulation events
                if start_button_brute_rect.collidepoint(event.pos) and config.state == 2:
                    config.state = 3
                    method = 0
                    # start looking for all possible paths
                    possible_paths = [[beginning]]
                if start_button_a_rect.collidepoint(event.pos) and config.state == 2:
                    config.state = 3
                    method = 1
                    # get all selected and not selected blocks you have access to
                    # assign a value to them showing how many turns it takes to get to them from the beginning
                    selected = {}
                    # for every point we remember coordinates, G and H values (look at algorithm file) and point it came
                    # from, and for the starting point we ignore where it came from (and the value becomes 9)
                    available = {
                        tuple(beginning): [0, abs(end[0]-beginning[0]) + abs(end[1]-beginning[1]), 0]
                    }

                # start over event
                if start_over_rect.collidepoint(event.pos):
                    home_screen()
        
        # white screen
        screen.fill((255, 255, 255))

        # display the grid
        for row in grid:
            for rect in row:
                pygame.draw.rect(screen, (0, 0, 0), rect, 1)

        # bruteforce algorithm
        if method == 0:
            if config.state == 3:
                bruteforce(screen, font, grid, obstacles, end, possible_paths, x, y)

        # A* algorithm
        if method == 1:
            if config.state == 3:
                a_star(screen, font, grid, obstacles, beginning, end, selected, available, x, y)

        # display the path if it has been found
        if config.state == 4:
            if method == 0:
                if config.found:
                    # the right path is always the last one as we break the while after it
                    for block_x, block_y in config.final_path[1:-1]:
                        pygame.draw.rect(screen, (128, 128, 128), grid[block_x][block_y])
                else:
                    # display a message that there is no right path
                    no_right_path = font.render("Path not possible!", True, (0, 0, 0))
                    screen.blit(no_right_path, (610, 500))
            if method == 1:
                if config.found:
                    for block, rest in config.final_path[1:-1]:
                        block = list(block)
                        block_x = block[0]
                        block_y = block[1]
                        pygame.draw.rect(screen, (128, 128, 128), grid[block_x][block_y])
                else:
                    # display a message that there is no right path
                    no_right_path = font.render("Path not possible!", True, (0, 0, 0))
                    screen.blit(no_right_path, (610, 500))

        # display starting, end points and obstacles if any
        if config.state >= 1:
            pygame.draw.rect(screen, (0, 255, 0), grid[beginning[0]][beginning[1]])
        if config.state >= 2:
            pygame.draw.rect(screen, (255, 0, 0), grid[end[0]][end[1]])
            for obstacle in obstacles:
                obstacle = list(obstacle)
                pygame.draw.rect(screen, (0, 0, 255), grid[obstacle[0]][obstacle[1]])

        # display help message
        screen.blit(help_text, (610, 20))

        # display warning message
        screen.blit(warning_text_1, (610, 100))
        screen.blit(warning_text_2, (610, 120))

        # display start button
        if config.state >= 2:
            pygame.draw.rect(screen, (0, 0, 0), start_button_brute_rect)
            screen.blit(start_button_brute_text, (700 - list(font.size("Start with bruteforce"))[0]/2, 225 - list(font.size("Start with bruteforce"))[1]/2))
            pygame.draw.rect(screen, (0, 0, 0), start_button_a_rect)
            screen.blit(start_button_a_text, (700 - list(font.size("Start with A*"))[0] / 2, 325 - list(font.size("Start with A*"))[1] / 2))

        # display play again button
        pygame.draw.rect(screen, (0, 0, 0), start_over_rect)
        screen.blit(start_over_text, (700 - list(font.size("Find another path"))[0] / 2, 425 - list(font.size("Find another path"))[1] / 2))

        # display menu line
        pygame.draw.line(screen, (0, 0, 0), (605, 0), (605, 600))

        # update frame
        pygame.display.flip()


home_screen()
