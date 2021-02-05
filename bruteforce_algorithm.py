# system imports
from time import sleep

# pip installed imports
import pygame


def bruteforce(screen, font, grid, state, obstacles, end, possible_paths, x, y):
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
                state = 4
                found = True
                break
        # right
        if end_x + 1 < x and (end_x + 1, end_y) not in obstacles and [end_x + 1, end_y] not in current_path:
            continuation.append([end_x + 1, end_y])
            # check if you have found the shortest path
            if [end_x + 1, end_y] == end:
                possible_paths.append(current_path.copy() + [[end_x + 1, end_y]])
                state = 4
                found = True
                break
        # up
        if end_y - 1 >= 0 and (end_x, end_y - 1) not in obstacles and [end_x, end_y - 1] not in current_path:
            continuation.append([end_x, end_y - 1])
            # check if you have found the shortest path
            if [end_x, end_y - 1] == end:
                possible_paths.append(current_path.copy() + [[end_x, end_y - 1]])
                state = 4
                found = True
                break
        # down
        if end_y + 1 < y and (end_x, end_y + 1) not in obstacles and [end_x, end_y + 1] not in current_path:
            continuation.append([end_x, end_y + 1])
            # check if you have found the shortest path
            if [end_x, end_y + 1] == end:
                possible_paths.append(current_path.copy() + [[end_x, end_y + 1]])
                state = 4
                found = True
                break

        # continue to the next step of the path
        for c in continuation:
            possible_paths.append(current_path.copy() + [[c[0], c[1]]])

        # go to the next path and remove the current one as it has already been expanded
        number_of_paths -= 1
        del possible_paths[0]

    # check if there are no more paths remaining (then it's impossible to find the correct one)
    if len(possible_paths) == 0:
        state = 4

    # display the paths that have been tried
    if state >= 3:
        for possibility in possible_paths:
            for block in possibility:
                pygame.draw.rect(screen, (0, 255, 255), grid[block[0]][block[1]])
        # delay the app to help the user see the visualization better
        sleep(0.5)

    # if the path has been found display it
    if state == 4:
        if found:
            # the right path is always the last one as we break the while after it
            right_path = possible_paths[-1]
            for block_x, block_y in right_path[1:-1]:
                pygame.draw.rect(screen, (128, 128, 128), grid[block_x][block_y])
        else:
            # display a message that there is no right path
            no_right_path = font.render("Path not possible!", True, (0, 0, 0))
            screen.blit(no_right_path, (610, 500))
