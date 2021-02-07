# system imports
from time import sleep

# pip installed imports
import pygame

# imports from my files
import config


# algorithm explanation
'''
this algorithm expands every possible path with 1 block in every possible 
direction on every cycle of the "while True:" in pathfinding.py

then on the next cycle of "while True:" we expand our new paths and so on until we either get to the end
point (1) or we are out of possible expansions for the path (2)

(1) if we get to the end point we know we have found the "best" path and we can stop the simulation 
(that's because every path gains 1 block of length on every cycle so the paths grow equally fast)

(2) if we can't expand any of the paths anymore and the state is still 3 (simulating) this means we haven't reacted
the final point and we are closed out by obstacles so we tell the user that a path can't be found
'''
def bruteforce(screen, font, grid, obstacles, end, possible_paths, x, y):
    # cycle through every currently possible path
    number_of_paths = len(possible_paths)
    while number_of_paths > 0:
        # get the end of the current path
        current_path = possible_paths[0]
        end_of_path = current_path[-1]
        end_x = end_of_path[0]
        end_y = end_of_path[1]

        # see to where the path can continue
        continuation = []
        # left
        if end_x - 1 >= 0 and (end_x - 1, end_y) not in obstacles and [end_x - 1, end_y] not in current_path:
            continuation.append([end_x - 1, end_y])
            # check if you have found the shortest path
            if [end_x - 1, end_y] == end:
                possible_paths.append(current_path.copy() + [[end_x - 1, end_y]])
                config.state = 4
                config.found = True
                break
        # right
        if end_x + 1 < x and (end_x + 1, end_y) not in obstacles and [end_x + 1, end_y] not in current_path:
            continuation.append([end_x + 1, end_y])
            # check if you have found the shortest path
            if [end_x + 1, end_y] == end:
                possible_paths.append(current_path.copy() + [[end_x + 1, end_y]])
                config.state = 4
                config.found = True
                break
        # up
        if end_y - 1 >= 0 and (end_x, end_y - 1) not in obstacles and [end_x, end_y - 1] not in current_path:
            continuation.append([end_x, end_y - 1])
            # check if you have found the shortest path
            if [end_x, end_y - 1] == end:
                possible_paths.append(current_path.copy() + [[end_x, end_y - 1]])
                config.state = 4
                config.found = True
                break
        # down
        if end_y + 1 < y and (end_x, end_y + 1) not in obstacles and [end_x, end_y + 1] not in current_path:
            continuation.append([end_x, end_y + 1])
            # check if you have found the shortest path
            if [end_x, end_y + 1] == end:
                possible_paths.append(current_path.copy() + [[end_x, end_y + 1]])
                config.state = 4
                config.found = True
                break

        # continue to the next step of the path
        for c in continuation:
            possible_paths.append(current_path.copy() + [[c[0], c[1]]])

        # go to the next path and remove the current one as it has already been expanded
        number_of_paths -= 1
        del possible_paths[0]

    # check if there are no more paths remaining (then it's impossible to find the correct one)
    if len(possible_paths) == 0:
        config.state = 4

    # display the paths that have been tried
    if config.state >= 3:
        for possibility in possible_paths:
            for block in possibility:
                pygame.draw.rect(screen, (0, 255, 255), grid[block[0]][block[1]])
        # delay the app to help the user see the visualization better
        sleep(0.2)

    # set the final path
    if config.found:
        config.final_path = possible_paths[-1].copy()
