from typing import Dict, List, Optional

from clingo import Control, PropagateControl




MODEL = List[str]
NOGOOD = List[int]

class Solver:
    def __init__(self, lp: str, horizon: int = 10, hspec: str = "#const horizon=") -> None:
        self.lp = lp
        self.hspec: str = hspec

        if not self.hspec in lp:
            print(f"specify horizon constant in lp by: {HSPEC}")
            return

        ctl = Control([str(0)])

        ctl.add("base", [], lp)
        ctl.ground([("base", [])])
        
        # TODO: specify horizon constant in ctl

        self.literal_mappings: Dict[str, int] = {
            #str(atom.symbol): atom.literal
            atom.symbol: atom.literal
            for atom in ctl.symbolic_atoms
        }


    #def model2nogood(self, model: str) -> NOGOOD:
    #    self.literal_mappings =


    def run(self, nogood: NOGOOD) -> NOGOOD:
        xs = []
        with self.ctl.solve(assumptions=nogood, yield_=True) as handle:
            models = [model.symbols() for model in handle]
            print(models)
            
                

if __name__ == "__main__":
    import sys

    lp = open(sys.argv[1], "r").read()
    h = sys.argv[2]
    ng = []
    solver = Solver(lp, horizon=h)
    ng = solver.run([])

    # NOTE: run recursively, maybe with memoization?
