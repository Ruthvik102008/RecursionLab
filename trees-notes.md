# Trees: let every branch solve a smaller problem

 

A linked list has one rest. A tree can have many branches, and every branch is itself a tree. These notes follow your four videos in order. Each section has four original practice problems: first learn the representation, then combine branch results, carry information down paths, and finally count or select paths.

 

[1. Trees](#tree-structure)[2. Processing](#tree-processing)[3. Summing paths](#tree-paths)[4. Counting paths](#tree-counting) 

 | Your video | Concepts | Practice 

 | [Trees](https://www.youtube.com/watch?v=pTPDmMH9dbs) | Root, labels, branches, leaves, nodes; Tree dataclass | 1–4 

 | [Tree Processing](https://www.youtube.com/watch?v=u80l0ZdxjIs) | Fibonacci trees, leaf aggregation, constructing transformed trees | 5–8 

 | [Example: Summing Paths](https://www.youtube.com/watch?v=k0VmYzZS0Jw) | Carry an accumulated number or string from root to leaf | 9–12 

 | [Example: Counting Paths](https://www.youtube.com/watch?v=9jcoCFe9efA) | Root-to-any-node endpoints and remaining-target recursion | 13–16 

## 1. The representation: label plus branches

 

The root is the top node. A node’s direct descendants are its children, and the subtrees rooted at those children are its branches. A leaf has no branches. A path moves from a parent to one of its children at each step; it cannot jump between siblings.

 

```python
from dataclasses import dataclass, field

@dataclass
class Tree[T]:
    label: T
    branches: list['Tree[T]'] = field(default_factory=list)

def is_leaf(t):
    return not t.branches

t = Tree(2, [Tree(4), Tree(6, [Tree(8), Tree(10)])])
t.label                         # 2
t.branches[0].label             # 4
t.branches[1].branches[0].label  # 8
is_leaf(t)                      # False
is_leaf(t.branches[0])          # True
```

 

`t.branches` is a list of Tree objects, not a list of their labels. After indexing into that list, you have a Tree and can read its label or branches. The root exists even when branches is empty: `Tree(4)` is a one-node tree, not an empty tree.

 

`field(default_factory=list)` creates a fresh empty list for each instance whose branches are omitted. It avoids making all leaves share one mutable default list. `T` describes the label type; it does not perform runtime validation or change how you call the constructor.

 

The lecture’s printed trees put the root first and indent each child below it. Our `tree_shape` helper displays the same structure as nested `(label, branches)` pairs, so doctests do not depend on a display method. It is supplied for tests, not as an implementation shortcut.

 

Self-check: does Tree(5, [7]) represent a branch labeled 7?

No. The branch must be a tree: `Tree(5, [Tree(7)])`. Its branch list contains objects that support label and branches.

 

A Tree is never the empty linked-list sentinel (). Its stopping shape is a leaf whose branches list is empty.

 

## 2. Combine answers from branches

 

When you need a total, count, or extremum, let each recursive call answer the same question for one entire branch. The parent combines those answers. A branch may contain many nodes; reading only its root label is not enough to process everything underneath it.

 

```python
def count_nodes(t):
    return 1 + sum(count_nodes(b) for b in t.branches)

count_nodes(t)                   # 5
```

 

The current call counts its own node with 1. Every recursive call counts all nodes in a different branch. For a leaf, the generator visits no branches and `sum` gives 0, so the result is 1. This function has a base case through empty iteration even without a separate if.

 

Leaf-only calculations need a different contribution. A leaf contributes its label or one leaf count. An internal node combines its branches’ results without including its own label. For a largest-leaf calculation, a huge internal label must not win. Initializing the answer to zero also fails when all qualifying labels are negative.

 

The processing video builds Fibonacci trees: the base cases are leaves with labels 0 and 1; other nodes contain recursively built branches for n−2 and n−1, with their root labels added. The fact that its root equals the sum of its leaves is a property of those particular trees, not a rule for all trees.

 

A transformation that returns a new tree must construct a new root and recursively construct its branches. Reusing an input branch can give the right display while still sharing unwanted mutable nodes.

 

Self-check: should a tree traversal forbid all loops?

No. These videos use comprehensions and loops over branches while making recursive calls on those branches. The new exercises allow that pattern. Recursion is still required to handle arbitrary depth.

 

Say what each recursive call returns: an integer, a boolean, a list, or a Tree. Combine results using operations appropriate to that type.

 

## 3. Carry information downward

 

Some questions concern the labels along a path, rather than independent subtree totals. A helper parameter can carry the path accumulated so far. Add the current label, then either handle a leaf or pass the updated value to each branch.

 

```python
def show_paths(t, prefix=()):
    path = prefix + (t.label,)
    if is_leaf(t):
        print(path)
    else:
        for branch in t.branches:
            show_paths(branch, path)

show_paths(Tree(1, [Tree(2), Tree(3, [Tree(4)])]))
# (1, 2)
# (1, 3, 4)
```

 

Each sibling starts from its parent’s path. The path ending in 2 must not accidentally become the prefix for the branch beginning with 3. Tuples, numbers, and strings let each recursive call use its own updated value without mutating another branch’s accumulated state.

 

The Summing Paths video uses string labels to produce words. The same `+` expression adds numbers or concatenates strings, but the starting value must fit the labels: 0 for numeric sums and an empty string for text. Print at leaves when the requested endpoints are leaves, not at every intermediate node.

 

Printing and returning are different jobs. A printing traversal can return None and call every branch in order. A function returning a list of path results must combine those branch lists and return the combined list. Duplicate results correspond to different paths and usually remain unless the prompt says otherwise.

 

Self-check: why not use one global running total for every branch?

It would mix unrelated paths unless you carefully restored it. A helper argument passes exactly the parent’s accumulated value into each child call, making the responsibility explicit.

 

## 4. Count endpoints without losing later matches

 

The Counting Paths video counts root-to-any-node paths. The root by itself is a valid endpoint. An internal node can qualify even though it has branches. This differs from counting complete root-to-leaf paths.

 

```python
example = Tree(3, [Tree(0), Tree(1, [Tree(-1)])])
# Root-to-node sums: 3, 3, 4, 3.
# Three endpoints have sum 3; only two are leaves.
```

 

A remaining-target helper asks a branch to make up whatever total remains after using the current label. If the original target is 7 and the current label is 3, that branch must contribute 4. This is the same accounting idea as subtracting a selected part in partition problems.

 

Finding one match does not mean returning immediately. A descendant with label 0 could create another matching endpoint; a negative value could bring a larger sum back to the target. Do not stop merely because the target has been reached or the running sum has overshot when the labels may be negative.

 

For a requested sequence of labels, check the current root against the next expected value, then explore branches for the remaining sequence. A branch choice must keep the entire continuation together; selecting matching labels from different siblings is not a path.

 

The depth-copy challenge transfers this helper idea to a nonnegative depth budget. The root is at depth 0. When the remaining budget is zero, the new result root has no branches; the input subtree remains intact.

 

Self-check: can a leaf have branches=[] and still contribute one path?

Yes. A one-node tree has one root-to-leaf path containing its single label. Its zero branches do not make it a zero-node tree.

 

Before coding, identify the endpoint rule: any node or only a leaf. Then choose a helper state and decide whether matching at the current node should also continue into its branches.

 

Sources: your four linked videos (available auto-generated captions, checked against their Python concepts), [Python dataclasses and default factories](https://docs.python.org/3.12/library/dataclasses.html), and [the instructor’s tree reference](https://composingprograms.com/pages/23-sequences.html#trees). The workbook uses the dataclass representation from your videos, rather than the textbook’s list-based tree abstraction.
