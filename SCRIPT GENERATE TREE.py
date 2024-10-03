from random import randint

def around(x, y, cords, typetree):

    width = 0
    height = 0
    if typetree == '1':
        width = 64 * 2
        height = 128 * 2
    if typetree == '2':
        width = 80 * 2
        height = 124 * 2
    if typetree == '3':
        width = 152 * 2
        height = 156 * 2

    for i in cords:
        if i[0] in range(int(x), int(x) + width) and i[1] in range(int(y), int(y) + height):
            return False


    return True

def create(y1, y2, stx=100, end=3500):
    x = stx
    while int(x) < end:
        type_tree = str(randint(1,2))
        x = str(int(x) + 150)
        y = str(randint(y1, y2))

        print(x, y)

        types_trees.append(type_tree)
        cords.append((x, y))

cords = []
types_trees = []


create(3900, 4100)
create(3200, 3800)
create(2500, 3100)
create(1800, 2400)
create(1100, 1700)
create(3900, 4100, 4200, 5020)
create(3200, 3800, 4200, 5020)
create(2500, 3100, 4200, 5020)
create(1800, 2400, 4200, 5020)
create(1100, 1700, 4200, 5020)

with open('static/trees station.txt', 'w') as file:
    for trees in range(len(types_trees)):
        print(types_trees[trees], cords[trees])
        file.write(f'{types_trees[trees]}\n')
        file.write(f'{cords[trees][0]} {cords[trees][1]}\n')