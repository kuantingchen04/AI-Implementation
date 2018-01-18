from random import randint

"""cellular automaton (CA) implementation"""


def rules(left, mid, right):
    """rule: current empty & only one of the neighbor is full -> full"""
    return ~mid & (left ^ right)

def print_CA(cell):  # 1:'*' ,0:'.c'
    s = ''
    for x in cell:
        s += '*' if x else '.'
    print(s)

# cell: Save current cell
# next_gen: cell for next generation using rules()

def CA(num_cell, num_gen):
    """Iteratively produce the generations"""
    # Check valid inputs
    if not (num_cell >= 2 and num_gen >= 0):
        raise ValueError("Check if num_cell >= 2 && num_gen >= 0!")
        # return
    if not (isinstance(num_cell, int) and isinstance(num_gen, int)):
        raise ValueError("Check if inputs are integers!")
        # return
    # Randomly seed the cell with 1/0 but exclude first/last cell
    cell = [randint(0, 1) for _ in range(num_cell - 2)]
    cell = [0] + cell + [0]
    print_CA(cell)  # initial state
    print "--------------------"

    next_gen = [0] * num_cell
    for _ in range(num_gen):  # generate generations
        for i in range(
                1, num_cell - 1):  # first/last cells should always be empty
            next_gen[i] = rules(cell[i - 1], cell[i], cell[i + 1])
        print_CA(next_gen)
        cell[:] = next_gen[:]  # copy by value

def main():
    """Prompt the user to enter # of cell & gen"""
    num_cell = input("Number of cell (n>= 2): ")
    num_gen = input("Number of gen (n>= 0): ")

    CA(num_cell, num_gen)

if __name__ == '__main__':

    main()
