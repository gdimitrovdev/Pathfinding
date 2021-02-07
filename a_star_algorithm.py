# sys imports
from time import sleep

# pip installed imports
import pygame

# imports from my files
import config


# algorithm explanation
'''
This algorithm does not expand the path in every possible way
Instead it checks what is the most optimal block we can go to

The most optimal block should be the one that is both theoretically
closest to the end and practically closest to the beginning

So if G(x) is how many turns we practically took to get from the starting point to
the point x and H(x) is how many turns we will theoretically need to get to the end
starting from point x (theoretically = assuming there are no obstacles), then
we can introduce F(x) = G(x) + H(x) and we will call F the value of the point x

The more valuable points have a smaller F and therefore are optimal
'''
def a_star(screen, font, grid, obstacles, beginning, end, selected, available, x, y):
    # find the point(s) with optimal value that is(are) available and remember where they came from and their G and H
    optimal_value = float('inf')
    optimal_points = {}
    for key in available:
        s = available[key][0] + available[key][1]
        if s == optimal_value:
            optimal_points[key] = available[key]
        if s < optimal_value:
            optimal_value = s
            optimal_points = {key: available[key]}

    # for the found points check if they lead to a shorter path from the start to one of their adjacent points
    # if the point's adjacent points are not in the available list add them
    for point in optimal_points:
        point_left = (list(point)[0]-1, list(point)[1])
        point_right = (list(point)[0] + 1, list(point)[1])
        point_up = (list(point)[0], list(point)[1] - 1)
        point_down = (list(point)[0], list(point)[1] + 1)
        # left
        if point_left in available:
            if available[point_left][0] > optimal_points[point][0] + 1:
                available[point_left][0] = optimal_points[point][0] + 1
                available[point_left][2] = point
        elif list(point)[0] - 1 >= 0 and point_left not in selected and point_left not in obstacles:
            g = optimal_points[point][0]+1
            h = abs(end[0] - (list(point)[0] - 1)) + abs(end[1] - list(point)[1])
            available[point_left] = [g, h, point]
        # right
        if point_right in available:
            if available[point_right][0] > optimal_points[point][0] + 1:
                available[point_right][0] = optimal_points[point][0] + 1
                available[point_right][2] = point
        elif list(point)[0] + 1 < x and point_right not in selected and point_right not in obstacles:
            g = optimal_points[point][0] + 1
            h = abs(end[0] - (list(point)[0] + 1)) + abs(end[1] - list(point)[1])
            available[point_right] = [g, h, point]
        # up
        if point_up in available:
            if available[point_up][0] > optimal_points[point][0] + 1:
                available[point_up][0] = optimal_points[point][0] + 1
                available[point_up][2] = point
        elif list(point)[1] - 1 >= 0 and point_up not in selected and point_up not in obstacles:
            g = optimal_points[point][0] + 1
            h = abs(end[0] - list(point)[0]) + abs(end[1] - (list(point)[1] - 1))
            available[point_up] = [g, h, point]
        # down
        if point_down in available:
            if available[point_down][0] > optimal_points[point][0] + 1:
                available[point_down][0] = optimal_points[point][0] + 1
                available[point_down][2] = point
        elif list(point)[1] + 1 < y and point_down not in selected and point_down not in obstacles:
            g = optimal_points[point][0] + 1
            h = abs(end[0] - list(point)[0]) + abs(end[1] - (list(point)[1]+1))
            available[point_down] = [g, h, point]

        # make the point selected
        del available[point]
        selected[point] = optimal_points[point]

        # check if the point is the end
        if point == tuple(end):
            # trace back the path
            end_path = [[point, selected[point]]]
            while end_path[-1][0] != tuple(beginning):
                end_path.append([end_path[-1][1][2], selected[end_path[-1][1][2]]])
            config.state = 4
            config.found = True
            break

    # check if there are no more available points (then you can't get to the end)
    if len(available) == 0 and not config.found:
        config.state = 4

    # display the paths that have been tried
    if config.state >= 3:
        for point_s in selected:
            pygame.draw.rect(screen, (0, 255, 255), grid[list(point_s)[0]][list(point_s)[1]])
        for point_a in available:
            pygame.draw.rect(screen, (255, 255, 0), grid[list(point_a)[0]][list(point_a)[1]])
        # delay the app to help the user see the visualization better
        sleep(0.2)

    # set the final path
    if config.found:
        config.final_path = end_path.copy()
