from z3 import *
from basic_solve import SudokuSolver
import time

def main():
    pz_file = "adv_puzzles.txt"
    pz_solver = AdvSudokuSolver(pz_file)
    timings = []
    for i in range(25):
        t0 = time.time()
        result = pz_solver.solve()
        timings.append(time.time()-t0)
        if result == 0 or timings[-1] > 60.0:
            print("We have a problem!")
            print(timings)
            return
    print("time elapsed for solving each puzzle:")
    print(timings)

class AdvSudokuSolver(SudokuSolver):
        
    def solve(self,verbose=False):
        """
        solves advanced sudoku problem - 2 more constraints, 
        gets puzzle from pz_file, solves it, then submits solution to submit_endpt
        returns 1 if answer is correct, 0 otherwise

        Additional constraints for advanced problem:
        - On even rows, sum(even indices) > sum(odd indices)
        - On odd rows, sum(odd indices) > sum(even indices)
        - We have to find all solutions, not just 1 of them
        """
        print("problem: ")
        self._new_puzzle()
        self.print_pz(self.puzzle)

        print("solving...")
        self._set_sudoku_constraints()
        # additional constraints for advanced problem - on even rows, sum(even indices) > sum(odd indices); on odd rows, sum(odd indices) > sum(even indices)
        # we can combine these into 1 constraint (1-indexed): for each row, sum( even (row + column indices)) > sum( odd (row + column indices))
        # because we use 0-indexing in python, the parity flips 
        adv_constraint = [ (Sum([self.arr[i][j] for j in range(self.pz_size) if (i+j)%2==0]) > Sum([self.arr[i][j] for j in range(self.pz_size) if (i+j)%2==1])) for i in range(self.pz_size) ]
        self.s.add(adv_constraint)
        
        output = []

        # we run the solver until we cannot find any more distinct solutions
        while self._solve_puzzle() == 1:
            output.append(self._stringify_soln())

            # each solution must be differ from others in at least one element
            # we need to find all solutions, so each time we place a constraint that the next solution cannot be identical to the previous one
            distinct_constraint = Or([self.arr[i][j] != int(str(self.model.evaluate(self.arr[i][j]))) for i in range(self.pz_size) for j in range(self.pz_size)])
            self.s.add(distinct_constraint)
            print("\n{}th solution found!".format(len(output)))
            self.print_pz(self._stringify_soln())

        self.ans = " ".join(output)
        print("answer:\t",len(output)," solutions")


if __name__=="__main__":
    main()
