

hist = [0]
#  hist = [1,3,4,5,3]
mem = 0

def display_current_value():
    global hist
    print(f"cur: {hist[-1]}")
def add(to_add):
    global hist
    res = hist[-1] + to_add
    hist.append(res)

    print(res)
def mult(to_mult):
    global hist
    res = hist[-1] * to_mult
    hist.append(res)
    print(res)

def div(to_div):
    global hist
    if to_div == 0:
        print("Can't divide by zero")
        return
    res = hist[-1] / to_div
    hist.append(res)
    print(res)

def save():
    global mem
    mem = len(hist) - 1
    print("saved")
def recall():
    global hist
    hist.append(hist[mem])
    print(f"recalled value: {hist[mem]}")
def undo():
    global hist
    hist.append(hist[-2])
    print(f"undid! current value: {hist[-1]}")
def undo2():
    global hist
    hist.append(hist[-3])
    print(f"undid! current value: {hist[-1]}")
if __name__ == "__main__":
    print("Welcome to the calculator program")
    print("Current value: 0")
    add(5)
    display_current_value()
    mult(5)
    div(3)
    div(0)
    save()
    add(1)
    add(1)
    recall()
    mult(2)
    undo()
    undo()
    undo()
    undo2()
