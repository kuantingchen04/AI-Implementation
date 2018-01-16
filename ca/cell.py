from random import randint

def rules(left,mid,right):
    return ~mid & (left ^ right)
def print_CA(cell):
    s = ''
    for x in cell:
        s += '*' if x else '.'
    print (s)

def CA(num_cell,num_gen):
    # randomly seed the cell with 1's and 0's initially (except first & last)
    cell = [randint(0, 1) for x in range(num_cell-2)]     
    cell = [0] + cell + [0] 
    print_CA(cell)

    next_gen = [0] * num_cell
    for i_gen in range(num_gen):
        for i in range(1,num_cell-1): # first and last cells to be always empty
            next_gen[i] = rules(cell[i-1],cell[i],cell[i+1])
        #print (cell,next_gen)
        print_CA(next_gen)
        cell[:] = next_gen[:] # copy by value

if __name__ == '__main__':
    CA(10,5)
