import itertools
import random


class Minesweeper:
    """
    Minesweeper game representation
    """

    def __init__(self, height=8, width=8, mines=8):

        # Set initial width, height, and number of mines
        self.height = height
        self.width = width
        self.mines = set()

        # Initialize an empty field with no mines
        self.board = []
        for i in range(self.height):
            row = []
            for j in range(self.width):
                row.append(False)
            self.board.append(row)

        # Add mines randomly
        while len(self.mines) != mines:
            i = random.randrange(height)
            j = random.randrange(width)
            if not self.board[i][j]:
                self.mines.add((i, j))
                self.board[i][j] = True

        # At first, player has found no mines
        self.mines_found = set()

    def print(self):
        """
        Prints a text-based representation
        of where mines are located.
        """
        for i in range(self.height):
            print("--" * self.width + "-")
            for j in range(self.width):
                if self.board[i][j]:
                    print("|X", end="")
                else:
                    print("| ", end="")
            print("|")
        print("--" * self.width + "-")

    def is_mine(self, cell):
        i, j = cell
        return self.board[i][j]

    def nearby_mines(self, cell):
        """
        Returns the number of mines that are
        within one row and column of a given cell,
        not including the cell itself.
        """

        # Keep count of nearby mines
        count = 0

        # Loop over all cells within one row and column
        for i in range(cell[0] - 1, cell[0] + 2):
            for j in range(cell[1] - 1, cell[1] + 2):

                # Ignore the cell itself
                if (i, j) == cell:
                    continue

                # Update count if cell in bounds and is mine
                if 0 <= i < self.height and 0 <= j < self.width:
                    if self.board[i][j]:
                        count += 1

        return count

    def won(self):
        """
        Checks if all mines have been flagged.
        """
        return self.mines_found == self.mines


class Sentence:
    """
    Logical statement about a Minesweeper game
    A sentence consists of a set of board cells,
    and a count of the number of those cells which are mines.
    """

    def __init__(self, cells, count):
        self.cells = set(cells)
        self.count = count

    def __eq__(self, other):
        return self.cells == other.cells and self.count == other.count

    def __str__(self):
        return f"{self.cells} = {self.count}"

    def known_mines(self):
        """
        Returns the set of all cells in self.cells known to be mines.
        """
        if len(self.cells) == self.count:
            return self.cells
        else:
            return None

    def known_safes(self):
        """
        Returns the set of all cells in self.cells known to be safe.
        """
        if self.count == 0:
            return self.cells
        else:
            return None

    def mark_mine(self, cell):
        """
        Updates internal knowledge representation given the fact that
        a cell is known to be a mine.
        """
        if cell in self.cells:
            self.cells.remove(cell)
            self.count -= 1
        return self

    def mark_safe(self, cell):
        """
        Updates internal knowledge representation given the fact that
        a cell is known to be safe.
        """
        if cell in self.cells:
            self.cells.remove(cell)
        return self


class MinesweeperAI:
    """
    Minesweeper game player
    """

    def __init__(self, height=8, width=8):

        # Set initial height and width
        self.height = height
        self.width = width

        # Keep track of which cells have been clicked on
        self.moves_made = set()

        # Keep track of cells known to be safe or mines
        self.mines = set()
        self.safes = set()

        # List of sentences about the game known to be true
        self.knowledge = []
        # Example of a knowledge representation:
        # self.knowledge = [Sentence({(0, 0), (0, 1), (1, 0), (1, 1)}, 1)]

    def mark_mine(self, cell):
        """
        Marks a cell as a mine, and updates all knowledge
        to mark that cell as a mine as well.
        """
        self.mines.add(cell)
        for sentence in self.knowledge:
            sentence.mark_mine(cell)

    def mark_safe(self, cell):
        """
        Marks a cell as safe, and updates all knowledge
        to mark that cell as safe as well.
        """
        self.safes.add(cell)
        for sentence in self.knowledge:
            sentence.mark_safe(cell)

    def add_knowledge(self, cell, count):
        """
        Called when the Minesweeper board tells us, for a given
        safe cell, how many neighboring cells have mines in them.

        This function should:
            1) mark the cell as a move that has been made
            2) mark the cell as safe
            3) add a new sentence to the AI's knowledge base
               based on the value of `cell` and `count`
            4) mark any additional cells as safe or as mines
               if it can be concluded based on the AI's knowledge base
            5) add any new sentences to the AI's knowledge base
               if they can be inferred from existing knowledge
        """
        # Move has been made
        self.moves_made.add(cell)

        # Mark cell as safe and update any sentences
        self.mark_safe(cell)

        # Add new sentence to knowledge base
        cells = set()
        for i in range(cell[0] - 1, cell[0] + 2):
            for j in range(cell[1] - 1, cell[1] + 2):
                # Ignore the cell itself
                if (i, j) == cell:
                    continue
                # Update count if cell in bounds and is mine
                if 0 <= i < self.height and 0 <= j < self.width:
                    if (i, j) not in self.moves_made and (i, j) not in self.mines:
                        cells.add((i, j))
                    elif (i, j) in self.mines:
                        count -= 1
        self.knowledge.append(Sentence(cells, count))

        # Mark any additional cells as safe or as mines
        for sentence in self.knowledge:
            if sentence.known_safes():
                for cell in sentence.known_safes().copy():
                    self.mark_safe(cell)
            if sentence.known_mines():
                for cell in sentence.known_mines().copy():
                    self.mark_mine(cell)

        # Inferred sentences from existing knowledge using set operations
        for sentence in self.knowledge:
            for other_sentence in self.knowledge:
                if sentence is other_sentence:
                    continue
                if sentence == other_sentence:
                    self.knowledge.remove(other_sentence)
                elif sentence.cells.issubset(other_sentence.cells):
                    new_cells = other_sentence.cells - sentence.cells
                    new_count = other_sentence.count - sentence.count
                    new_knowledge = Sentence(new_cells, new_count)
                    if new_knowledge not in self.knowledge:
                        self.knowledge.append(new_knowledge)

        # WORST VERSION PERFORMING :(
        # to_remove = []
        # for sentence, other_sentence in itertools.combinations(self.knowledge, 2):
        #     if sentence is other_sentence:
        #         continue
        #     if sentence == other_sentence:
        #         to_remove.append(other_sentence)
        #     elif sentence.cells.issubset(other_sentence.cells):
        #         new_cells = other_sentence.cells - sentence.cells
        #         new_count = other_sentence.count - sentence.count
        #         new_knowledge = Sentence(new_cells, new_count)
        #         if new_knowledge not in self.knowledge:
        #             self.knowledge.append(new_knowledge)

        # self.knowledge = [s for s in self.knowledge if s not in to_remove]

    def make_safe_move(self):
        """
        Returns a safe cell to choose on the Minesweeper board.
        The move must be known to be safe, and not already a move
        that has been made.

        This function may use the knowledge in self.mines, self.safes
        and self.moves_made, but should not modify any of those values.
        """
        for cell in self.safes:
            if cell not in self.moves_made:
                return cell
        return None

    def make_random_move(self):
        """
        Returns a move to make on the Minesweeper board.
        Should choose randomly among cells that:
            1) have not already been chosen, and
            2) are not known to be mines
        """
        cells = set()
        for i, j in itertools.product(range(self.height), range(self.width)):
            # Cartesian product of all cells
            # Ex: consider self.height = 3 and self.width = 4, range(self.height) = [0, 1, 2] and range(self.width) = [0, 1, 2, 3]
            # Result
            # cells = {(0, 0), (0, 1), (0, 2), (0, 3), (1, 0), (1, 1), (1, 2), (1, 3), (2, 0), (2, 1), (2, 2), (2, 3)}
            if (i, j) not in self.moves_made and (i, j) not in self.mines:
                cells.add((i, j))
        if cells:
            return random.choice(list(cells))
        else:
            return None
