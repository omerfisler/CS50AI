import itertools
import random


class Minesweeper():
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


class Sentence():
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
            #All the cells in sequence are mines.
            return self.cells
        else:
            return set() #empty set object

    def known_safes(self):
        """
        Returns the set of all cells in self.cells known to be safe.
        """
        if self.count == 0:
            return self.cells
        else:
            return set()

    def mark_mine(self, cell):
        """
        Updates internal knowledge representation given the fact that
        a cell is known to be a mine.
        """
        if cell in self.cells:
            self.count = self.count-1
            self.cells.discard(cell) #
        return

    def mark_safe(self, cell):
        """
        Updates internal knowledge representation given the fact that
        a cell is known to be safe.
        """
        if cell in self.cells:
            self.cells.discard(cell)
        return

class MinesweeperAI():
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
        """
        Called when the Minesweeper board tells us, for a given safe cell, 
        how many neighboring cells have mines in them.

        This function should:
        
        1) Mark the cell as one of the moves made in the game.
        - Add the cell to self.moves_made to track that this cell has been played.

        2) Mark the cell as a safe cell, updating any sentences that contain the cell as well.
        - Use self.mark_safe(cell) to mark the cell as safe.
        - Update any existing sentences that include this cell to reflect that the cell is known to be safe.

        3) Add a new sentence to the AI’s knowledge base based on the value of `cell` and `count`.
        - Create a new sentence to indicate that `count` of the `cell`’s neighbors are mines.
        - Ensure that the sentence only includes neighboring cells whose state is still undetermined (neither safe nor marked as a mine).
        - Add this new sentence to self.knowledge.

        4) If, based on any of the sentences in self.knowledge, new cells can be marked as safe or as mines, then the function should do so.
        - Iterate over the sentences in self.knowledge.
        - If a sentence can lead to marking new cells as safe, call self.mark_safe for those cells.
        - If a sentence can lead to marking new cells as mines, call self.mark_mine for those cells.

        5) If, based on any of the sentences in self.knowledge, new sentences can be inferred (using the subset method described in the Background),
        then those sentences should be added to the knowledge base as well.
        - Look for subset relationships between sentences.
        - If sentence1 is a subset of sentence2, create a new inferred sentence using the difference of sets and counts, 
        and add it to self.knowledge if it’s new.

        Note:
        - Any time you make any change to your AI’s knowledge, it may be possible to draw new inferences that weren’t possible before.
        - Be sure that those new inferences are added to the knowledge base if it is possible to do so.
        """
        ### ONE OF THE MAKE_SAFE Not Working properly.

        self.moves_made.add(cell) # 1

        self.mark_safe(cell)      # 2  

        cell_neighbors = set()     # 3
        minus_count = 0 # will be used for update the count in initial sentence.
        for row in range(cell[0] - 1, cell[0] + 2):
            for col in range(cell[1] - 1, cell[1] + 2):
                if not(row < 0 or row == self.height) and not(col < 0 or col == self.width):
                    if (row, col) not in self.safes:
                        if (row, col) not in self.mines:
                            cell_neighbors.add((row, col))
                        else: # if row,col in mines:
                            minus_count -= 1 # I used -= optionally.
        newSentence = Sentence(cell_neighbors,count + minus_count)
        # newSentence.mark_safe(cell) # that will remove the cell in sentence that we create right here. Also can be expressed in if condition as a new operation with extra an and not operator: and(row !=cell[0] or col != cell[1])
        self.knowledge.append(newSentence) ##

        for checking_sentence in self.knowledge: # 4 \in cleaner and more effective way:
            if checking_sentence.known_safes():
                for safe_cell in checking_sentence.known_safes().copy():
                    self.mark_safe(safe_cell)
            if checking_sentence.known_mines():
                for mine_cell in checking_sentence.known_mines().copy():
                    self.mark_mine(mine_cell)
        # self.mines.add(checking_sentence.known_mines)
        # self.safes.add(checking_sentence.known_safes)

        for sentence1 in self.knowledge:
            for sentence2 in self.knowledge:
                if sentence1 == sentence2:
                    continue  # Skipped for same sentences.

                # Check subsets
                if sentence1.cells.issubset(sentence2.cells):
                    new_cells = sentence2.cells - sentence1.cells
                    new_count = sentence2.count - sentence1.count

                    # Only add new sentence if it has new information
                    if new_cells and new_count >= 0:
                        new_sentence = Sentence(new_cells, new_count)
                        if new_sentence not in self.knowledge:
                            self.knowledge.append(new_sentence) 




    def make_safe_move(self):
        """
        Returns a safe cell to choose on the Minesweeper board.
        The move must be known to be safe, and not already a move
        that has been made.

        This function may use the knowledge in self.mines, self.safes
        and self.moves_made, but should not modify any of those values.
        """
        for selected_cell in self.safes:
            if selected_cell not in self.moves_made and selected_cell not in self.mines:
                # print(f"SAFE_MOVE: selected {selected_cell} cell.")
                return selected_cell
        
        return None

    def make_random_move(self):
        """
        Returns a move to make on the Minesweeper board.
        Should choose randomly among cells that:
            1) have not already been chosen, and
            2) are not known to be mines
        """
        all_pairs = [(x, y) for x in range(self.height) for y in range(self.width) if (x, y) not in self.moves_made and (x, y) not in self.mines]
        if all_pairs:
            random.shuffle(all_pairs)  # Shuffle to randomize \not necessary
            # print(f"RAND_MOVE: selected {all_pairs[0]} cell.")
            return all_pairs[0]
        else:
            return None