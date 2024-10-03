from random import randint


def generate_tiles():
    list_tiles = []
    for height in range(69):
        width_list = []
        for width in range(80):
            width_list.append(randint(1, 4))

        list_tiles.append(width_list)

    return list_tiles

with open('static/zetta_tiles.txt', 'w', encoding='utf-8') as file:
    result = ''
    for i in generate_tiles():
        tiles = f'{i}'.replace('[', '')
        tiles = tiles.replace(']', '')
        tiles = tiles.replace(' ', '')

        result += tiles + ',\n'

    file.write(result)