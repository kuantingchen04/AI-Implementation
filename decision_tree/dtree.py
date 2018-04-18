#!/usr/bin/env python

"""Implementation of Decision Tree Learning

namings
    - data: 2d array (lists of lists) with a label at the last column
    - attr: feature of the data, usually refers to its col_idx
    - val: possible value of each attr
    - partitions: list of data (splitted)

    - header_info: a dict storing { 0: {'values': ['Yes', 'No'], 'name': 'Alt'},
                                    1: {'values': ['Yes', 'No'], 'name': 'Bar'} }
"""

import math
import copy

TOLERANCE = 1e-8  # float comparison


def get_best_attr(data, header_info, idx_lst=None):
    """Find the best attr to split the data, return the best attr (idx)"""
    best_gain = -float("inf")
    if not idx_lst:
        n = len(header_info) - 1  # exclude label
        idx_lst = [i for i in range(n)]

    current_uncertainty = entropy(data)
    for idx in idx_lst:  # each feature

        partitions = partition_by_a(data, idx, header_info)
        gain = info_gain_from_entropy(partitions, current_uncertainty)
        log(idx, gain, [len(x) for x in partitions], [class_counts(x)
                                                      for x in partitions], current_uncertainty)
        if gain >= best_gain and abs(gain - best_gain) > TOLERANCE:
            best_gain, best_attr = gain, idx

    log(header_info[best_attr]['name'], idx_lst,
        best_attr, best_gain, len(data))
    return best_attr, best_gain


def partition_by_a(data, attr, header_info):
    """Given attr, split the data into list of data"""
    n = len(header_info[attr]['values'])  # num of piles
    partitions = [[] for _ in range(n)]

    for row in data:
        for i, val in enumerate(header_info[attr]['values']):
            if row[attr] == val:
                partitions[i].append(row)
    return partitions


def class_counts(data):
    """Given data, return the number of each class (label)"""
    counts = {}
    for row in data:
        label = row[-1]
        if label not in counts:
            counts[label] = 0
        counts[label] += 1
    return counts


def entropy(data):
    """Return entropy"""
    counts = class_counts(data)
    # print data,counts
    entropy = 0.0
    for label in counts:
        prob_of_lbl = counts[label] / float(len(data))
        entropy -= prob_of_lbl * math.log(prob_of_lbl, 2)
    return entropy


def gini(data):
    """Return gini, faster than entropy"""
    counts = class_counts(data)
    impurity = 1
    for lbl in counts:
        prob_of_lbl = counts[lbl] / float(len(data))
        impurity -= prob_of_lbl**2
    return impurity


def info_gain_from_entropy(partitions, current_uncertainty):
    """Sum up the entropy of each partiions and return gain increase"""
    cnts = [len(x) for x in partitions]
    total = sum(cnts)
    sum_e = 0.0
    for i, cnt in enumerate(cnts):
        p = float(cnt) / total
        sum_e += p * entropy(partitions[i])
        # print p, entropy(partitions[i])
    return current_uncertainty - sum_e


class Decision_Node:
    """Nodes that not done, having children leaf nodes"""

    def __init__(self, attr, child_nodes=None):
        self.attr = attr
        if not child_nodes:
            self.child_nodes = []


class Leaf_Node:
    """Nodes that calculate a prediction, no child"""

    def __init__(self, examples, pred):
        self.predictions = class_counts(examples)
        self.pred = pred

# Main Program


def decision_tree_learning(examples, parent_examples,
                           header_info, attr_lst, fix_expand_order=False):
    """Recursive call of tree learning"""

    # Invalid
    if len(examples) == 0:  # PLURALITY-VALUE(parent examples)
        pr_cls_cnt = class_counts(parent_examples)
        pred = max(pr_cls_cnt, key=lambda k: pr_cls_cnt[k])
        return Leaf_Node(parent_examples, pred)

    cls_cnt = class_counts(examples)

    # Success
    if len(cls_cnt.keys()) == 1:  # only 1 class -> predict
        pred = cls_cnt.keys()[0]
        return Leaf_Node(examples, pred)

    if not attr_lst:  # No more choice, PLURALITY-VALUE(examples)
        pred = max(cls_cnt, key=lambda k: cls_cnt[k])
        return Leaf_Node(examples, pred)

    # pick best attr if expansion order is not given
    if not fix_expand_order:
        best_attr, _ = get_best_attr(examples, header_info, attr_lst)
    else:
        best_attr = attr_lst[0]

    attr_lst.remove(best_attr)
    partitions = partition_by_a(examples, best_attr, header_info)
    node = Decision_Node(best_attr)

    for i, attr_val in enumerate(header_info[best_attr]['values']):
        _attr_lst = copy.copy(attr_lst)
        child = decision_tree_learning(
            partitions[i],
            examples,
            header_info,
            _attr_lst,
            fix_expand_order)
        node.child_nodes.append(child)

    return node


def print_tree(node, header_info, spacing=""):
    """For debugging"""
    if isinstance(node, Leaf_Node):
        s = spacing + "[Leaf_Node]", node.predictions, node.pred
        print(s)
        return

        # Decision node
        s = spacing + "Q: %s?" % header_info[node.attr]['name']
        print(s)

    for i, child in enumerate(node.child_nodes):
        s = spacing + '-->' + header_info[node.attr]['values'][i] + ':'
        print(s)
        print_tree(child, header_info, spacing + "  ")


def write_tree(node, header_info, fname):
    """Output the tree by traversing each nodes"""
    def helper(node, header_info):
        if isinstance(node, Leaf_Node):
            return

        for i, child in enumerate(node.child_nodes):
            if isinstance(child, Leaf_Node):
                s = "%s? %s, %s\n" % (
                    header_info[node.attr]['name'], header_info[node.attr]['values'][i], child.pred)
                f.write(s)

            if isinstance(child, Decision_Node):
                s = "%s? %s, %s?\n" % (header_info[node.attr]['name'],
                                       header_info[node.attr]['values'][i],
                                       header_info[child.attr]['name'])
                f.write(s)

            helper(child, header_info)

    with open(fname, 'w') as f:
        f.write("% Format: decision? value, next node (leaf value or next decision?)\n" +
                "% Use question mark and comma markers as indicated below.\n")
        helper(node, header_info)

# Parser


def read_decision_tree(fname):
    """Read the input file, return data and header info"""

    with open(fname, 'r') as f:

        # Input Attributes
        header = []
        header_vals = []  # vals for each attributes

        f.readline()
        while True:
            line = f.readline().rstrip('\n').replace(', ', ',')
            if '%' in line:
                break
            attr, vals = line.split(': ')
            header.append(attr)
            header_vals.append(vals.split(','))

        # Decision values (label)
        header.append("label")
        label_vals = f.readline().rstrip('\n').replace(', ', ',').split(',')
        header_vals.append(label_vals)

        # Data
        training_data = []
        f.readline()
        f.readline()
        while True:
            line = f.readline()
            if line == '':  # eof
                break
            line = line.rstrip('\n').replace(', ', ',').split(',')
            training_data.append(line)

    header_info = {}
    for i in range(len(header)):
        header_info[i] = {'name': header[i], 'values': header_vals[i]}
    return header_info, training_data


def log(*args):
    """For Debugging"""
    # print(args)
    pass


def main():
    """Read file, run program and write file"""

    dt_file = "examples2.txt"
    out_file = "dtree.txt"

    header_info, training_data = read_decision_tree(dt_file)
    log(header_info)

    n = len(header_info) - 1  # not include label column
    node = decision_tree_learning(training_data, training_data, header_info, list(range(n)))

    # write_tree(node, header_info, out_file)

    # For debugging
    # best_attr, best_gain = get_best_attr(training_data, header_info)
    # partitions = partition_by_a(training_data, best_attr, header_info)
    # node = decision_tree_learning(training_data, training_data, header_info, [2, 0, 1], fix_expand_order=True)
    print_tree(node, header_info)


if __name__ == '__main__':
    main()
