from random import randint

def rules(left,mid,right):
    return left ^ right
def print_AC(cell):
    s = ''
    for x in cell:
        s += '*' if x else '.'
    print (s)

def run_AC(num_cell,num_gen):
    cell = [randint(0, 1) for x in range(num_cell)]
    print_AC(cell)

    next_gen = [0] * num_cell
    for i_gen in range(num_gen):
        for i in range(num_cell):
            left = cell[i-1] if i != 0 else 0
            right = cell[i+1] if i != (num_cell-1) else 0
            mid = cell[i]
            next_gen[i] = rules(left,mid,right)
        print_AC(next_gen)
        cell = next_gen[:] # copy by value

if __name__ == '__main__':
    run_AC(10,10)
