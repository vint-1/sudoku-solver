from z3 import *

def main():
    pz_file = "puzzles.txt"
    pz_solver = SudokuSolver(pz_file)
    for i in range(25):
        pz_solver.solve()
        print("\n=========\n")

class SudokuSolver:
    
    def __init__(self,pz_file,pz_len=3):
        
        self.pz_file = pz_file
        self.model = None
        self.pz_len = pz_len
        self.pz_size = self.pz_len**2
        self.arr = [[Int("x{}_{}".format(i,j)) for j in range(self.pz_size)] for i in range(self.pz_size)]
        # this is defined here and maintained throughout the lifetime of SudokuSolver so that we don't have to start from scratched when finding multiple solutions
        self.s = Solver()
        self.f = open(pz_file,mode="r")
        
    def solve(self):
        """
        gets puzzle from pz_file, solves it
        returns 1 if answer is correct, 0 otherwise
        """
        self._new_puzzle()
        print("problem: ")
        self.print_pz(self.puzzle)

        self._set_sudoku_constraints()
        print("solving...")
        if self._solve_puzzle()==1:
            print("\nsolution found!")
        else:
            print("\ncould not find solution :(")
            return

        self.print_pz(self._stringify_soln())

    def _new_puzzle(self):
        # todo: write some code to catch exceptions
        self.puzzle = self.f.readline().strip()
        # if we get a new puzzle, the constraints will have to be reset
        self.s = Solver()
        assert len(self.puzzle)==self.pz_len**4, "self.pz_len and size of puzzle string don't match"

    def _set_sudoku_constraints(self):
        """
        applies sudoku constraints to solver (self.s)
        """
        assert self.puzzle is not None, "no puzzle found, must call _new_puzzle first"
        # numbers must be from [1,9]
        num_constraint = [ And(self.arr[i][j]>=1,self.arr[i][j]<=self.pz_size) for j in range(self.pz_size) for i in range(self.pz_size) ]
        # each row has unique numbers
        row_constraint = [ Distinct(self.arr[i]) for i in range(self.pz_size) ]
        # each column has unique numbers
        col_constraint = [ Distinct([self.arr[i][j] for i in range(self.pz_size)]) for j in range(self.pz_size) ]
        # each block has unique numbers
        blk_constraint = [ Distinct([self.arr[i][j] for i in range(corner_i,corner_i+self.pz_len) for j in range(corner_j,corner_j+self.pz_len)]) for corner_i in range(0,self.pz_size,self.pz_len) for corner_j in range(0,self.pz_size,self.pz_len)]
        # solution must match numbers already given
        pz_constraint = [ self.arr[i][j]==int(self.puzzle[j+i*self.pz_size]) if self.puzzle[j+i*self.pz_size] != '.' else True for i in range(self.pz_size) for j in range(self.pz_size) ]
        
        self.s.add(num_constraint + row_constraint + col_constraint + blk_constraint + pz_constraint)

    def _solve_puzzle(self):
        """
        solves sudoku encoded as string in self.puzzle. returns 1 if solution found, and -1 otherwise.
        updates self.model if solution found
        """
        # heavy lifting of solving puzzle goes here
        result = self.s.check().r
        if result != 1:
            return -1
        self.model = self.s.model()
        return 1
    
    def print_pz(self,puzzle):
        """
        prints, in a human-friendly format, a puzzle that's encoded as string
        """
        assert len(puzzle)==self.pz_len**4, "self.pz_len and size of puzzle string don't match"
        
        for i in range(self.pz_size):
            output = ""
            for j in range(self.pz_size):
                char=puzzle[j+i*self.pz_size]
                if(char=='.'):
                    output += "- "
                else:
                    output += str(char) + " "
            print(output)
    
    def _stringify_soln(self):
        """
        generates encoding of completed puzzle as a string (format similar to that of input puzzle)
        """
        assert self.model is not None, "no solution found. either puzzle is unsolvable or attempt hasn't been made"
        out_list = [str(self.model[self.arr[i][j]]) for i in range(self.pz_size) for j in range(self.pz_size)]
        return "".join(out_list) 


if __name__=="__main__":
    main()
