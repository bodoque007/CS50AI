import sys

from crossword import *


class CrosswordCreator():

    def __init__(self, crossword):
        """
        Create new CSP crossword generate.
        """
        self.crossword = crossword
        self.domains = {
            var: self.crossword.words.copy()
            for var in self.crossword.variables
        }

    def letter_grid(self, assignment):
        """
        Return 2D array representing a given assignment.
        """
        letters = [
            [None for _ in range(self.crossword.width)]
            for _ in range(self.crossword.height)
        ]
        for variable, word in assignment.items():
            direction = variable.direction
            for k in range(len(word)):
                i = variable.i + (k if direction == Variable.DOWN else 0)
                j = variable.j + (k if direction == Variable.ACROSS else 0)
                letters[i][j] = word[k]
        return letters

    def print(self, assignment):
        """
        Print crossword assignment to the terminal.
        """
        letters = self.letter_grid(assignment)
        for i in range(self.crossword.height):
            for j in range(self.crossword.width):
                if self.crossword.structure[i][j]:
                    print(letters[i][j] or " ", end="")
                else:
                    print("█", end="")
            print()

    def save(self, assignment, filename):
        """
        Save crossword assignment to an image file.
        """
        from PIL import Image, ImageDraw, ImageFont
        cell_size = 100
        cell_border = 2
        interior_size = cell_size - 2 * cell_border
        letters = self.letter_grid(assignment)

        # Create a blank canvas
        img = Image.new(
            "RGBA",
            (self.crossword.width * cell_size,
             self.crossword.height * cell_size),
            "black"
        )
        font = ImageFont.truetype("assets/fonts/OpenSans-Regular.ttf", 80)
        draw = ImageDraw.Draw(img)

        for i in range(self.crossword.height):
            for j in range(self.crossword.width):

                rect = [
                    (j * cell_size + cell_border,
                     i * cell_size + cell_border),
                    ((j + 1) * cell_size - cell_border,
                     (i + 1) * cell_size - cell_border)
                ]
                if self.crossword.structure[i][j]:
                    draw.rectangle(rect, fill="white")
                    if letters[i][j]:
                        w, h = draw.textsize(letters[i][j], font=font)
                        draw.text(
                            (rect[0][0] + ((interior_size - w) / 2),
                             rect[0][1] + ((interior_size - h) / 2) - 10),
                            letters[i][j], fill="black", font=font
                        )

        img.save(filename)

    def solve(self):
        """
        Enforce node and arc consistency, and then solve the CSP.
        """
        self.enforce_node_consistency()
        self.ac3()
        return self.backtrack(dict())

    def enforce_node_consistency(self):
        """
        Update `self.domains` such that each variable is node-consistent.
        (Remove any values that are inconsistent with a variable's unary
         constraints; in this case, the length of the word.)
        """
        for var, domain in self.domains.items():
            to_remove = set()
            for word in domain:
                if len(word) != var.length:
                    to_remove.add(word)
            for word in to_remove:
                domain.remove(word)

    def revise(self, x, y):
        """
        Make variable `x` arc consistent with variable `y`.
        To do so, remove values from `self.domains[x]` for which there is no
        possible corresponding value for `y` in `self.domains[y]`.

        Return True if a revision was made to the domain of `x`; return
        False if no revision was made.
        """
        if self.crossword.overlaps[x, y] == None:
            return False
        # y is neighbor of x, we'll have to see if we'll change x's domain to respect arc cons.
        revision_made = False
        overlap = self.crossword.overlaps[x, y]
        to_remove = set()
        for x_word in self.domains[x]:
            # If any word in x's domain cannot have any word in y's domain such that they overlap with the same character, remove it from x's domain.
            should_remove_x_word = not any(y_word[overlap[1]] == x_word[overlap[0]] for y_word in self.domains[y])
            if should_remove_x_word:
                to_remove.add(x_word)
                revision_made = True
        for word in to_remove:
            self.domains[x].remove(word)
        return revision_made
        

    def ac3(self, arcs=None):
        """
        Update `self.domains` such that each variable is arc consistent.
        If `arcs` is None, begin with initial list of all arcs in the problem.
        Otherwise, use `arcs` as the initial list of arcs to make consistent.

        Return True if arc consistency is enforced and no domains are empty;
        return False if one or more domains end up empty.
        """
        queue = []
        if arcs != None:
            queue = arcs
        else:
            for x in self.crossword.variables:
                for y in self.crossword.neighbors(x):
                    queue.append((x, y))

        while queue:
            (x, y) = queue.pop(0)
            if self.revise(x, y):
                if len(self.domains[x]) == 0:
                    return False
                for z in self.crossword.neighbors(x) - {y}:
                    queue.append((z, x))
        return True

    def assignment_complete(self, assignment):
        """
        Return True if `assignment` is complete (i.e., assigns a value to each
        crossword variable); return False otherwise.
        """
        return len(assignment) == len(self.crossword.variables) 

    def consistent(self, assignment):
        """
        Return True if `assignment` is consistent (i.e., words fit in crossword
        puzzle without conflicting characters); return False otherwise.
        """
        # Checks for no duplicates
        if len(assignment) != len(set(assignment.values())):
            return False
        
        for var, word in assignment.items():
            if len(word) != var.length:
                return False
            for y in assignment.keys():
                if y == var or self.crossword.overlaps[var, y] == None:
                    continue
                # Checks if overlapping characters are the same
                overlapping_index_x = self.crossword.overlaps[var, y][0]
                overlapping_index_y = self.crossword.overlaps[var, y][1]
                if word[overlapping_index_x] != assignment[y][overlapping_index_y]:
                    return False
        return True


    def order_domain_values(self, var, assignment):
        """
        Return a list of values in the domain of `var`, in order by
        the number of values they rule out for neighboring variables.
        The first value in the list, for example, should be the one
        that rules out the fewest values among the neighbors of `var`.
        """
        def how_many_ruled_out(word):
            ruled_out = 0
            for neighbor in self.crossword.neighbors(var) - set(assignment.keys()):
                overlapping_index_var = self.crossword.overlaps[var, neighbor][0]
                overlapping_index_neighbor = self.crossword.overlaps[var, neighbor][1]
                for val in self.domains[neighbor]:
                    if word[overlapping_index_var] != val[overlapping_index_neighbor]:
                        ruled_out += 1
            return ruled_out

        ordered = list(self.domains[var])
        ordered.sort(key=how_many_ruled_out)
        return ordered

    def select_unassigned_variable(self, assignment):
        """
        Return an unassigned variable not already part of `assignment`.
        Choose the variable with the minimum number of remaining values
        in its domain. If there is a tie, choose the variable with the highest
        degree. If there is a tie, any of the tied variables are acceptable
        return values.
        """
        unassigned_variables = [var for var in self.crossword.variables if var not in assignment.keys()]
        # candidates will store variables with fewest number of remaining values in their domains
        
        min_domain = min(unassigned_variables, key=lambda var : len(self.domains[var]))
        candidates = [var for var in unassigned_variables if len(self.domains[var]) == len(self.domains[min_domain])]
        # No tie, return variable with minimum remaining values in its domain.
        if len(candidates) == 1:
            return candidates[0]
        else:
            # Tie, return variable with most neighbors (highest degree) among tied variables
            return max(candidates, key=lambda var : len(self.crossword.neighbors(var)))
    
    def backtrack(self, assignment):
        """
        Using Backtracking Search, take as input a partial assignment for the
        crossword and return a complete assignment if possible to do so.

        `assignment` is a mapping from variables (keys) to words (values).

        If no assignment is possible, return None.
        """
        if self.assignment_complete(assignment):
            return assignment

        var = self.select_unassigned_variable(assignment)
        for word in self.order_domain_values(var, assignment):
            new_assignment = assignment.copy()
            domains_copy = self.domains.copy()
            new_assignment[var] = word
            if self.consistent(new_assignment):
                inference = self.ac3([(y, var) for y in self.crossword.neighbors(var)])
                # This solution won't work, it's not necessary to calculate result.
                if not inference:
                    continue
                
                updated = True
                while updated:
                    # Keep making new inferences and assigning values to variables until no new inferences can be made (No domain has been reduced to one element)
                    updated = False
                    for x in (self.crossword.variables - set(new_assignment.keys())):
                        if len(self.domains[x]) == 1: 
                            updated = True
                            new_assignment[x] = list(self.domains[x])[0] 
                            self.ac3([(y, x) for y in self.crossword.neighbors(x) if y not in new_assignment.keys()]) 
                result = self.backtrack(new_assignment)
                if result != None:
                    return result
            self.domains = domains_copy
        return None

def main():

    # Check usage
    if len(sys.argv) not in [3, 4]:
        sys.exit("Usage: python generate.py structure words [output]")

    # Parse command-line arguments
    structure = sys.argv[1]
    words = sys.argv[2]
    output = sys.argv[3] if len(sys.argv) == 4 else None

    # Generate crossword
    crossword = Crossword(structure, words)
    creator = CrosswordCreator(crossword)
    assignment = creator.solve()

    # Print result
    if assignment is None:
        print("No solution.")
    else:
        creator.print(assignment)
        if output:
            creator.save(assignment, output)


if __name__ == "__main__":
    main()
