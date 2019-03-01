#!/usr/bin/python3

import random

def fail(which, key, b, correct, value):
    print("%s failed %d with key %d correct is %d value %d" % (which, b, key, correct, value))

def wiki_search(array, key, correct):
    b = 0
    e = len(array) - 1
    cmp = 0

    while b <= e:
        k = (b + e) >> 1
        cmp += 1
        if array[k] < key:
            b = k + 1
        else:
            cmp += 1
            if array[k] > key:
                e = k - 1
            else:
                b = k
                break

    if b != correct:
        fail("wiki", key, b, correct, array[correct])
    return cmp

classic_less = 0;
classic_equal = 0;
classic_more = 0;

#
# Classic search
#

def classic_search(array, key, correct):
    global classic_less, classic_equal, classic_more

    b = 0
    e = len(array)
    cmp = 0

    # Invarient preserved during search:
    #
    # array[b] <= key < array[e]
    #

    # Terminate when the length of the search space is 1 or less
    #
    # Using b < e is a common mistake here and causes the loop to
    # not terminate when e = b + 1 and key >= array[b]
    #

    while e - b > 1:
        k = (b + e) >> 1
        cmp += 1
        if key < array[k]:
            e = k               # key < array[e]
        else:
            b = k               # array[b] <= key

    if array[b] < key:
        classic_less += 1
    elif array[b] == key:
        classic_equal += 1
    else:
        classic_more += 1

    #
    # Correct the search to ensure the returned location is not
    # before the key. This is required only if the miss case
    # is required to have the discovered location have a
    # consistent relation to the key.
    #

    cmp += 1
    if array[b] < key:
        b += 1
    if b != correct:
        fail("classic", key, b, correct, array[correct])
    return cmp

#
# Classic search to find matching entries only
#

def classic_find_search(array, key, correct):
    b = 0
    e = len(array)
    cmp = 0

    # Invarient preserved during search:
    #
    # array[b] <= key < array[e]
    #

    # Terminate when the length of the search space is 1 or less
    #
    # Using b < e is a common mistake here and causes the loop to
    # not terminate when e = b + 1 and key >= array[b]
    #

    while e - b > 1:
        k = (b + e) >> 1
        cmp += 1
        if key < array[k]:
            e = k               # key < array[e]
        else:
            b = k               # array[b] <= key

    if b != correct and correct < len(array) and key == array[correct]:
        fail("classic", key, b, correct, array[correct])
    return cmp

# Reduce the search space faster by taking advantage of the knowledge
# that the compare gives us

def new_search(array, key, correct):
    # Requires signed values to support dim(array) == 0
    b = 0;
    e = len(array) - 1
    cmp = 0

    # Invarient preserved during the search:
    #
    # array[b] <= key <= array[e]
    #
    # Terminate when the search space is empty.
    #
    # This always halts because the search space is always
    # shrunk at each iteration

    while b <= e:
        k = (b + e) >> 1
        cmp += 1
        if array[k] < key:
           b = k + 1
        else:
           e = k - 1

    if b != correct:
        fail("new", key, b, correct, array[correct])
    return cmp

# Take the new search and bias the end value by one so that it is
# always non-negative

def new_unsigned_search(array, key, correct):
    b = 0
    e = len(array)
    cmp = 0

    while b < e:
        k = (b + e - 1) >> 1
        cmp += 1
        if array[k] < key:
           b = k + 1
        else:
           e = k

    if b != correct:
        fail("new_unsigned", key, b, correct, array[correct]);
    return cmp

# Search from wikipedia labeled 'leftmost'


def leftmost_search(array, key, correct):
    b = 0
    e = len(array)
    cmp = 0

    while b < e:
        k = (b + e) >> 1
        cmp += 1
        if array[k] < key:
           b = k + 1
        else:
           e = k

    if b != correct:
        fail("leftmost", key, b, correct, array[correct]);
    return cmp

def do_searches(min_size, max_size):

    searches = [
        {
            'name': "classic",
            'search': classic_search,
            'compares': 0
        },
        {
            'name': "classic-find",
            'search': classic_find_search,
            'compares': 0
        },
        {
            'name': "wiki",
            'search': wiki_search,
            'compares': 0
        },
        {
            'name': "new",
            'search': new_search,
            'compares': 0
        },
        {
            'name': "new-unsigned",
            'search': new_unsigned_search,
            'compares': 0
        },
        {
            'name': "leftmost",
            'search': leftmost_search,
            'compares': 0
        }
    ]

    totals = {}

    print("%5s" % "size", end='')
    for search in searches:
        print("%13s" % search['name'], end='')
        totals[search['name']] = 0
    print("")

    for size in range(min_size, max_size):
        array = list(range(size))
        tries = 0
        for miss in [False, True]:
            if miss:
                array = \
                    list(range(key)) + \
                    list(range(key + 1, size + 1))
            for search in searches:
                # Set up array and run all searches.
                for key in range(0, size):
                        # print("trying", size, key, miss)
                        search['compares'] += \
                            search['search'](array, key, key);
                        tries += 1

        # Record and report results.
        print("%5d" % size, end='')
        for search in searches:
            print("%13.1f" % (search['compares'] / tries), end='')
            totals[search['name']] += search['compares']
            search['compares'] = 0
        print("")

    print("%5s" % "total", end='')
    for search in searches:
        print("%13d" % totals[search['name']], end='')
    print('')
    print("classic less %d equal %d more %d" % (classic_less, classic_equal, classic_more))

do_searches(1, 1024)
