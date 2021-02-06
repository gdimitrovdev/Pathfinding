# pip installed imports
import pygame


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
def a_star(screen, font, grid, state, obstacles, end, selected, available, x, y):
    pass
