'''
Your tasks:
1) instead of just printing out combinations, collect all possible combinations into a list (and then print out the list)
2) now use a function to choose the second color in the list
3) now choose three colors instead of two
4) now choose four colors instead of three
5) now choose as many colors as there are marbles.

'''
def chooseSecond(others,first):
    combos=list()
    for y in others:
        combos.append([first,y])
    return combos

def getAllCombosOfTwo(colors):
    combos=list()
    for x in colors:
        others = list(colors)
        others.remove(x)
        combos.extend(chooseSecond(others,x))
    return combos

        
colors = ["red","green","blue","yellow"]
combos = getAllCombosOfTwo(colors)
print(combos)

