from minesweeper import *


sentence1 = Sentence({(1, 1), (1, 2)}, 1)
sentence2 = Sentence({(1, 3), (1, 4)}, 2)
sentence3 = Sentence({(1, 5), (1, 6), (2, 1)}, 4)

sentence4 = Sentence({(0,0), (0,1)}, 2)
sentence5 = Sentence({(0,0), (0,1), (0,2)}, 3)

print(sentence4.cells.intersection(sentence5.cells))
print(sentence4.cells.difference(sentence5.cells))
print(sentence4.count - sentence5.count)

print(sentence5.cells.intersection(sentence4.cells))
print(sentence5.cells.difference(sentence4.cells))

ai = MinesweeperAI()
ai.add_knowledge((1, 1), 0)
# ai.add_knowledge((1, 2), 1)

# print(ai.safes)

# for sentence in ai.knowledge:
#     print(sentence.cells, sentence.count)


        # sentence1 = Sentence({(0,0), (0,1)}, 2) and sentence2 = Sentence({(0,0), (0,1), (0,2)}, 3)
        # intersect = sentence1.cells.intersection(sentence2.cells) = {(0,0), (0,1)}
        # Cells that are unique to sentence1 and not in sentence2
        # new_cells = sentence1.cells.difference(intersect) = set()
        # Similarly, new_cells = sentence2.cells.difference(intersect) = {(0,2)}    