#!/usr/bin/env python

import math

class Question:
    """col and value"""
    def __init__(self, col, value, header_info):
        self.col = col
        self.value = value
        self.header_info = header_info

    def match(self, example):
        val = example[self.col]
        return val == self.value # if attrs are discrete

    def __repr__(self):
        return "Is %s == %s?" % (self.header_info[self.col]['name'], str(self.value))


def partition_by_a(data, col, header_info):
    """given colomn"""
    n = len(header_info[col]['values']) # num of piles
    all_partitions = [[] for _ in range(n)]

    for row in data:
        for i, val in enumerate(header_info[col]['values']):
            if row[col] == val:
                all_partitions[i].append(row)

    return all_partitions

def class_counts(rows):
    """Counts the number of each type of example in a dataset. (labels)"""
    counts = {}  # a dictionary of label -> count.
    for row in rows:
        # in our dataset format, the label is always the last column
        label = row[-1]
        if label not in counts:
            counts[label] = 0
        counts[label] += 1
    return counts

def entropy(data):
    counts = class_counts(data)
    entropy = 0
    for label in counts:
        prob_of_lbl = counts[label] / float(len(data))
        entropy -= prob_of_lbl * math.log(prob_of_lbl,2)
    return entropy

def info_gain_from_entropy(partitions, current_uncertainty):
    cnts = [ len(x) for x in partitions ]
    total = sum(cnts)
    res = current_uncertainty
    for i, cnt in enumerate(cnts):
        p = float(cnt)/total
        res = res - p * entropy(partitions[i])
    return res

# Find most important
def get_best_attr(data, header_info, idx_lst=None):
    best_gain = -float("inf")
    if not idx_lst:
        n = len(header_info) - 1 # exclude label
        idx_lst = [ i for i in range(n) ]

    current_uncertainty = entropy(data)
    for idx in idx_lst: # each feature

        partitions = partition_by_a(data, idx, header_info)
        gain = info_gain_from_entropy(partitions, current_uncertainty)
        log(idx, gain, [len(x) for x in partitions], current_uncertainty)
        if gain >= best_gain:
            best_gain, best_attr = gain, idx

    log(header_info[best_attr]['name'], idx_lst, best_attr, best_gain, len(data))
    return best_gain, best_attr


class Decision_Node:
    def __init__(self,attr, child_nodes=None):
        self.attr = attr
        if not child_nodes:
            self.child_nodes = []

class Leaf:
    def __init__(self, rows, val):
        self.predictions = class_counts(rows)
        self.examples = rows
        self.val = val

def decision_tree_learning(examples, attr_idxs, parent_examples, header_info):
    if len(examples) == 0:
        pr_cls_cnt = class_counts(parent_examples)
        return Leaf(parent_examples, max(pr_cls_cnt.values())) # PLURALITY-VALUE(parent examples)

    cls_cnt = class_counts(examples)

    if len(cls_cnt.keys())==1: # only 1 class
        return Leaf(examples, cls_cnt.values()[0])
    if not attr_idxs:
        return Leaf(examples, max(cls_cnt.values()))

    # pick best attr

    best_gain, best_attr_idx = get_best_attr(examples, header_info, attr_idxs)
    partitions = partition_by_a(examples, best_attr_idx, header_info)

    attr_idxs.remove(best_attr_idx)

    node = Decision_Node(best_attr_idx)
    for i, val in enumerate(header_info[best_attr_idx]['values']):
        child = decision_tree_learning(partitions[i], attr_idxs, examples, header_info)
        node.child_nodes.append(child)

    return node



def print_tree(node, header_info, spacing=""):
    if isinstance(node, Leaf):
        print spacing+"Leaf", node.predictions, node.examples
        return

    print spacing+ "Q: %s?" % header_info[node.attr]['name']

    for i, child in enumerate(node.child_nodes):
        print spacing + '-->' + header_info[node.attr]['values'][i] + ':'
        print_tree(child, header_info, spacing + "  ")


# Parsers
def read_decision_tree(fname):
    """"""

    with open(fname, 'r') as f:

        # Input Attributes
        header = []
        header_vals = [] # vals for each attributes

        f.readline()
        while True:
            line = f.readline().rstrip('\n').replace(' ','')
            if '%' in line:
                break
            attr_name, vals = line.split(':')
            header.append(attr_name)
            header_vals.append(vals.split(','))

        # Decision values (label)
        header.append("label")
        label_vals = f.readline().rstrip('\n').replace(' ','').split(',')
        header_vals.append(label_vals)

        # Data
        training_data = []
        f.readline()
        f.readline()
        while True:
            line = f.readline()
            if line == '':  # eof
                break
            line = line.rstrip('\n').replace(' ','').split(',')
            training_data.append(line)

    header_info = {}
    for i in range(len(header)):
        header_info[i] = {'name': header[i], 'values':header_vals[i]}
    return header_info, training_data


def partition_by_q(data, question):
    true_rows, false_rows = [], []
    for row in data:
        if question.match(row):
            true_rows.append(row)
        else:
            false_rows.append(row)
    return true_rows, false_rows


def gini(data):
    counts = class_counts(data)
    impurity = 1
    for lbl in counts:
        prob_of_lbl = counts[lbl] / float(len(data))
        impurity -= prob_of_lbl**2
    return impurity


def info_gain_from_gini(left, right, current_uncertainty):
    p = float(len(left)) / (len(left) + len(right))
    return current_uncertainty - p * gini(left) - (1 - p) * gini(right)

def get_best_question(data, header, header_vals):
    """Try all question and find the best"""
    best_gain = 0
    best_question = None
    current_uncertainty = gini(data)
    n_features = len(header_vals) - 1

    for i in range(n_features): # each feature

        for val in header_vals[i]: # possible val for each feature

            q = Question(i, val, header)
            true_rows, false_rows = partition_by_q(data, q)

            if len(true_rows) == 0 or len(false_rows) == 0:
                continue

            gain = info_gain_from_gini(true_rows, false_rows, current_uncertainty)

            if gain >= best_gain: # update
                best_gain, best_question = gain, q

    return best_gain, best_question



def log(*args):
    """For Debugging"""
    print(args)
    pass

def main():
    dt_file = "examples.txt"
    header_info, training_data = read_decision_tree(dt_file)
    log(header_info)

    # question
    q = Question(0, "Yes", header_info)
    print q
    print q.match(training_data[0])

    # # cal uncertain
    g = gini(training_data)
    e = entropy(training_data)
    print "origin:", g, e

    partitions = partition_by_a(training_data, 4, header_info)
    print "pick pat:", info_gain_from_entropy(partitions, e)

    best_gain, best_attr_idx = get_best_attr(training_data, header_info) # run all attr and get max gain
    print header_info[best_attr_idx]['name']

    print "---Start Run---"
    n = len(header_info) - 1
    node = decision_tree_learning(training_data, list(range(n)), training_data, header_info)


if __name__ == '__main__':
    main()