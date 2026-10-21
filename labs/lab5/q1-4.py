from collections import defaultdict
# q1   
L = [["CIV", 92], ["180", 98], ["103", 99], ["194", 95]]
print(L[2][1])

# q2

def get_nums(L):
    res = []
    for _, j in L:
        res.append(j)
    return res

print(get_nums(L))


# q3

def lookup(L, num):
    for i, j in L:
        if j == num:
            return i
    return None

# QUESTION 7. PERSONAL FINANCES
# You decide to track your spending habits using two lists – the first list contains store names
# associated with a purchase and the second list contains the value of a particular purchase:
# recent_stores = ["Store A", "Store B", "Store A", "Store C"]
# recent_purchases = [15, 20, 10, 8]
# This means you made a $15 purchase at Store A, a $20 purchase at Store B, a $10 purchase at
# Store A and an $8 purchase at Store C. Stores may appear in the list more than once if multiple
# purchases are made there.
# Write a function that returns a dictionary, with keys for each store and values corresponding to the
# total amount spent there.
# Example returned dictionary for the above example:
# {"Store A": 25, "Store B": 20, "Store C": 8}


recent_stores = ["Store A", "Store B", "Store A", "Store C"]
recent_purchases = [15, 20, 10, 8]
# assume same len
def purchase_dict(recent_stores, recent_purchases):
    res = defaultdict(int)
    n = len(recent_stores)
    for i in range(n):
        res[recent_stores[i]] += recent_purchases[i]
    return res

# could make a dict but who cares
print(purchase_dict(recent_stores, recent_purchases))

#
# TIC TAC TOE TIME!!!!!!!!1
#


