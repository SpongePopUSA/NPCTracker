import time
from typing import Callable

def decorate (*args, func:Callable, item:str = "~", num:int = 50, delay:float = 0.0, give_space:bool = True):
    print("") if give_space else print("", end = "")
    for i in range(0, num):
        print(item, end = "")
        time.sleep(delay)
    print("\n") if give_space else print("")

    params = []
    if len(args) == 0:
        func()
    else:
        for a in args:
            params.append(a)
        func(*params)

    print("") if give_space else print("", end = "")
    for i in range(0, num):
        print(item, end = "")
        time.sleep(delay)
    print("\n") if give_space else print("")