Implementation of Decision Tree Learning

- namings
    - data: 2d array (lists of lists) with a label at the last column
    - attr: feature of the data, usually refers to its col_idx
    - val: possible value of each attr
    - partitions: list of data (splitted)

    - header_info: a dict storing { 0: {'values': ['Yes', 'No'], 'name': 'Alt'},
                                    1: {'values': ['Yes', 'No'], 'name': 'Bar'} }

- Usage
    - Run `python dtree.py`, you could specify input/output path in main() function