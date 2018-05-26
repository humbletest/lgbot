__pragma__("kwargs")

class Test1:
    def __init__(self, fixarg, one = 1, two = 2):
        print(fixarg, one, two)

__pragma__("nokwargs")

class Test2:
    def __init__(self, fixarg, one = 1, two = 2):
        print(fixarg, one, two)
        
Test1(0)
Test1(4, 5, 6)
Test1(15, 25)
Test1(9, one = 4)
Test1(9, two = 6)
Test1(9, two = 11, one = 34)
Test1(9, 2, one = 34)

print("")

Test2(0)
Test2(4, 5, 6)
Test2(15, 25)
Test2(9, one = 4)
Test2(9, two = 6)
Test2(9, two = 11, one = 34)
Test2(9, 2, one = 34)