import pygame
import random

pygame.init()

class DrawInformation:
    BLACK = 0,0,0
    WHITE = 255,255,255
    GREEN = 0,255,0
    RED = 255,0,0
    BACKGROUND_COLOR = WHITE

    SIDE_PAD = 100
    TOP_PAD = 150

    GRADIENTS = [
        (128,128,128),                      #light grey 
        (160,160,160),                      #moderate grey
        (192,192,192)                       #dark grey
    ]

    FONT = pygame.font.SysFont('comicsans',30)
    LARGE_FONT = pygame.font.SysFont('comicsans', 40)
    def __init__(self,width,height,lst):
        self.width = width
        self.height = height

        self.window = pygame.display.set_mode((width,height))
        pygame.display.set_caption("SORTING ALGORITHM VISUALIZER")
        self.set_list(lst)

    def set_list(self,lst):
        self.lst = lst
        self.min_val = min(lst)
        self.max_val = max(lst)
        
        #to determine how much widht space does whole block
        self.block_width = int((self.width - self.SIDE_PAD) / len(lst))
        #to determine how much height required does the blocks require
        self.block_height = int((self.height - self.TOP_PAD ) / (self.max_val - self.min_val)) 
        self.start_x = self.SIDE_PAD//2

def draw(draw_info, algo_name, ascending):
    draw_info.window.fill(draw_info.BACKGROUND_COLOR)

    title = draw_info.LARGE_FONT.render(f"{algo_name} - {'Ascending' if ascending else 'Descending'}",1,draw_info.RED)
    draw_info.window.blit(title,(draw_info.width/2 - title.get_width()/2, 5)) 


    controls = draw_info.FONT.render("R - Reset | SPACE - Start Sorting | A - Ascending | D - Descending",1,draw_info.BLACK)
    draw_info.window.blit(controls,(draw_info.width/2 - controls.get_width()/2, 35)) #to get it to the center

    sorting = draw_info.FONT.render("I - Insertion Sort | B - Bubble Sort | Q - Quick Sort",1,draw_info.BLACK)
    draw_info.window.blit(sorting,(draw_info.width/2 - sorting.get_width()/2, 65))    
        
    draw_list(draw_info)
    pygame.display.update()

def draw_list(draw_info, color_positions = {}, clear_bg = False):
    lst = draw_info.lst

    if clear_bg: #for redrawing
        clear_rect = (draw_info.SIDE_PAD//2, draw_info.TOP_PAD, draw_info.width - draw_info.SIDE_PAD, draw_info.height - draw_info.TOP_PAD)
        pygame.draw.rect(draw_info.window, draw_info.BACKGROUND_COLOR, clear_rect)


    for i, val in enumerate(lst):
        x = draw_info.start_x + i * draw_info.block_width
        y = draw_info.height - (val - draw_info.min_val) * draw_info.block_height

        color = draw_info.GRADIENTS[i % 3]

        if i in color_positions:
            color = color_positions[i]

        pygame.draw.rect(draw_info.window, color, (x, y, draw_info.block_width, draw_info.height))

    if clear_bg:
        pygame.display.update()

#to generate a list of random integers
def generate_starting_list(n,min_val,max_val):
    lst = []
    for _ in range(1,n):
        val = random.randint(min_val, max_val)
        lst.append(val)

    return lst

def bubble_sort(draw_info, ascending = True):
    lst = draw_info.lst

    for i in range(len(lst)-1):
        for j in range(len(lst)-1-i):
            num1 = lst[j]
            num2 = lst[j+1]

            if (num1 > num2 and ascending) or (num1 < num2 and not ascending):
                lst[j] , lst[j+1] = lst[j+1] , lst[j]
                draw_list(draw_info, {j: draw_info.GREEN, j+1: draw_info.RED}, True)
                yield True

    return lst

def insertion_sort(draw_info, ascending=True):
    lst = draw_info.lst

    for i in range(1,len(lst)):
        curr = lst[i]

        while True:
            ascending_sort = i > 0 and lst[i-1] > curr and ascending
            descending_sort = i > 0 and lst[i-1] < curr and not ascending

            if not ascending_sort and not descending_sort:
                break

            lst[i] = lst[i-1]
            i = i-1
            lst[i] = curr
            draw_list(draw_info,{i-1:draw_info.GREEN, i:draw_info.RED}, True)
            yield True

    return lst

#QUICK SORT using Iterative approach
def partition(arr, l, h, ascending = True):
    i = (l - 1)
    x = arr[h]

    for j in range(l, h):
        if ((arr[j] <= x) and ascending) or ((arr[j] >= x) and not ascending):
            # increment index of smaller element
            i = i + 1
            arr[i], arr[j] = arr[j], arr[i]

    arr[i + 1], arr[h] = arr[h], arr[i + 1]
    return (i + 1)


def quicksort(draw_info, ascending = True):
    arr = draw_info.lst
    l = 0
    h = len(arr) -1

    size = h - l + 1
    stack = [0] * (size)


    top = -1


    top = top + 1
    stack[top] = l
    top = top + 1
    stack[top] = h

    i = 0
    # Keep popping from stack while is not empty
    while top >= 0:

        # Pop h and l
        h = stack[top]
        top = top - 1
        l = stack[top]
        top = top - 1

        # Set pivot element at its correct position in
        # sorted array
        p = partition(arr, l, h, ascending)

        # If there are elements on left side of pivot,
        # then push left side to stack
        if p - 1 > l:
            top = top + 1
            stack[top] = l
            top = top + 1
            stack[top] = p - 1

        # If there are elements on right side of pivot,
        # then push right side to stack
        if p + 1 < h:
            top = top + 1
            stack[top] = p + 1
            top = top + 1
            stack[top] = h

        draw_list(draw_info, {i: draw_info.GREEN, i+1: draw_info.RED}, True)
        i+=1
        yield True
    return arr

def main():
    run = True
    clock = pygame.time.Clock()

    n = 50
    min_val = 0
    max_val = 100

    lst = generate_starting_list(n, min_val, max_val)
    draw_info = DrawInformation(800,600,lst)
    sorting = False
    ascending = True

    sorting_algorithm = bubble_sort
    sorting_algo_name = "Bubble Sort"
    sorting_algo_generator = None
 
    
    while run:
        clock.tick(60)

        if sorting:
            try:
                next(sorting_algo_generator)

            except StopIteration:
                sorting = False
        
        else:
            draw(draw_info, sorting_algo_name, ascending)
        

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            if event.type != pygame.KEYDOWN:
                continue

            #reset the blocks
            if event.key == pygame.K_r:
                lst = generate_starting_list(n,min_val,max_val)
                draw_info.set_list(lst)
                sorting = False

            #to start sorting
            elif event.key == pygame.K_SPACE and sorting == False:
                sorting = True
                sorting_algo_generator = sorting_algorithm(draw_info, ascending)

            elif event.key == pygame.K_a and not sorting:
                ascending = True

            elif event.key == pygame.K_d and not sorting:
                ascending = False

            elif event.key == pygame.K_i and not sorting:
                sorting_algorithm = insertion_sort
                sorting_algo_name = "Insertion Sort"

            elif event.key == pygame.K_b and not sorting:
                sorting_algorithm = bubble_sort
                sorting_algo_name = "Bubble Sort"

            elif event.key == pygame.K_q and not sorting:
                sorting_algorithm = quicksort
                sorting_algo_name = "Quick Sort"

    pygame.quit()

if __name__=="__main__":
    main()
