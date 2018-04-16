#!/usr/bin/env python

import math

TOLERANCE = 1e-8

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
    # print data,counts
    entropy = 0.0
    for label in counts:
        prob_of_lbl = counts[label] / float(len(data))
        entropy -= prob_of_lbl * math.log(prob_of_lbl,2)
    return entropy

def gini(data): # faster than entropy
    counts = class_counts(data)
    impurity = 1
    for lbl in counts:
        prob_of_lbl = counts[lbl] / float(len(data))
        impurity -= prob_of_lbl**2
    return impurity

def info_gain_from_entropy(partitions, current_uncertainty):
    cnts = [ len(x) for x in partitions ]
    total = sum(cnts)
    sum_e = 0.0
    for i, cnt in enumerate(cnts):
        p = float(cnt)/total
        sum_e += p * entropy(partitions[i])
        # print p, entropy(partitions[i])
    return current_uncertainty - sum_e

# Find most important
def get_best_question(data, header_info, idx_lst=None):
    best_gain = -float("inf")
    if not idx_lst:
        n = len(header_info) - 1 # exclude label
        idx_lst = [ i for i in range(n) ]

    current_uncertainty = entropy(data)
    for idx in idx_lst: # each feature

        partitions = partition_by_a(data, idx, header_info)
        gain = info_gain_from_entropy(partitions, current_uncertainty)
        log(idx, gain, [len(x) for x in partitions], [class_counts(x) for x in partitions], current_uncertainty)
        if gain >= best_gain and abs(gain-best_gain) > TOLERANCE:
            best_gain, best_attr = gain, idx

    log(header_info[best_attr]['name'], idx_lst, best_attr, best_gain, len(data))
    return best_gain, best_attr


class Decision_Node:
    def __init__(self, pr_q, pr_attr, q, child_nodes=None):
        self.pr_q = pr_q
        self.pr_attr = pr_attr
        self.q = q
        if not child_nodes:
            self.child_nodes = []

class Leaf:
    def __init__(self, rows, pr_q, pr_attr, pred):
        self.examples = rows
        self.predictions = class_counts(rows)
        self.pr_q = pr_q
        self.pr_attr = pr_attr
        self.pred = pred

# Main Program
def decision_tree_learning(examples, parent_examples, header_info, q_idxs, pr_q=None, pr_attr=None):

    # Invalid
    if len(examples) == 0:
        pr_cls_cnt = class_counts(parent_examples)
        pred = max(pr_cls_cnt, key=lambda k: pr_cls_cnt[k])
        return Leaf(parent_examples, pr_q, pr_attr, pred) # PLURALITY-VALUE(parent examples)

    cls_cnt = class_counts(examples)

    # Success
    if len(cls_cnt.keys())==1: # only 1 class
        pred = cls_cnt.keys()[0]
        return Leaf(examples, pr_q, pr_attr, pred)

    if not q_idxs:
        pred = max(cls_cnt, key=lambda k: cls_cnt[k])
        return Leaf(examples, pr_q, pr_attr, pred)

    # pick best q
    best_gain, best_q = get_best_question(examples, header_info, q_idxs)
    partitions = partition_by_a(examples, best_q, header_info)

    q_idxs.remove(best_q)

    node = Decision_Node(pr_q,pr_attr,best_q)

    for i, attr_val in enumerate(header_info[best_q]['values']):
        child = decision_tree_learning(partitions[i], examples, header_info, q_idxs, best_q, attr_val)
        node.child_nodes.append(child)

    return node


def print_tree(node, header_info, spacing=""):
    if isinstance(node, Leaf):
        print spacing+"[Leaf]", node.predictions, node.pred
        return

    print spacing+ "Q: %s?" % header_info[node.q]['name'] # Decision node

    for i, child in enumerate(node.child_nodes):
        print spacing + '-->' + header_info[node.q]['values'][i] + ':'
        print_tree(child, header_info, spacing + "  ")

def print_tree_2(node, header_info, fname):

    def print_tree_helper(node, header_info, parent=None):
        if isinstance(node, Leaf):
            print >> fn, "%s? %s, %s" % (header_info[node.pr_q]['name'], node.pr_attr, node.pred) # print LEAF
            return

        if node.pr_q: # neglect first decision node
            print >> fn, "%s? %s, %s?" % (header_info[node.pr_q]['name'], node.pr_attr, header_info[node.q]['name'])# print DECISION

        for i, child in enumerate(node.child_nodes):
            print_tree_helper(child, header_info, node)

    with open(fname, 'w') as fn:
        print_tree_helper(node, header_info)

# Parser
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

def log(*args):
    """For Debugging"""
    # print(args)
    pass

def main():
    dt_file = "examples.txt"
    out_file = "dtree.txt"

    header_info, training_data = read_decision_tree(dt_file)
    log(header_info)

    # # cal uncertain
    g = gini(training_data)
    e = entropy(training_data)
    log("entropy:", g, e)

    best_gain, best_q = get_best_question(training_data, header_info) # run all attr and get max gain
    partitions = partition_by_a(training_data, best_q, header_info)
    log(header_info[best_q]['name'])

    n = len(header_info) - 1
    node = decision_tree_learning(training_data, training_data, header_info, list(range(n)))
    # print_tree(node, header_info)
    print_tree_2(node, header_info, out_file)


if __name__ == '__main__':
    main()