import clingo


class CustomClingoControl(clingo.Control):
    def __init__(self, asp_files, cmd_params=[]):
        super().__init__(cmd_params+['--warn=none'])
        # self.__solve_timeout=solve_timeout
        for file in asp_files:
            super().load(file)
    
    def set_models(self, models_no):
        self.configuration.solve.models = models_no

    def simple_ground(self, subprogram, *constants):
        constant_symbols = list(map(clingo.symbol.Number, constants))
        super().ground([(subprogram, constant_symbols)])        
    
    def assign_external(self, name, value):
        super().assign_external(clingo.Function(name, [clingo.symbol.Number(value)]), True) 
    
    def release_external(self, name, value):
        super().release_external(clingo.Function(name, [clingo.symbol.Number(value)]))

    def add_base(self, code):
        super().add('base', [], code)

    
    def get_constraints(self, program, external, step, predicates):
        self.simple_ground(program, step)
        self.assign_external(external, step)

        self.set_models(0)

        constraints = []

        with self.solve(yield_=True) as hnd:
            for m in hnd:
                # m.__str__().split()
                relevant_atoms = filter(lambda model: model.name in predicates and model.arguments[0] == clingo.Number(step), m.symbols(shown=True))



                constraints.append(':- ' + ', '.join(f'{atom.name}(_, {atom.arguments[1]})' for atom in relevant_atoms) + '.')
                    
                # print(m)   


            self.release_external(external, step)
            self.cleanup()
            self.set_models(-1)

            return constraints


    def get_constraints_assumptions(self, step, predicates):

        self.set_models(0)
        constraints = []

        with self.solve(yield_=True, assumptions=[(clingo.Function('opponentWon', [clingo.Number(step)]), True)]) as hnd:
            for m in hnd:
                relevant_atoms = filter(lambda model: model.name in predicates and model.arguments[0] == clingo.Number(step), m.symbols(shown=True))

                constraints.append(':- ' + ', '.join(f'{atom.name}(_, {atom.arguments[1]})' for atom in relevant_atoms) + '.')
                    
            self.set_models(-1)

            return constraints
        



    def is_safisfiable(self, program, external, step) -> bool:
        self.simple_ground(program, step)
        self.assign_external(external, step) # don't use externals but use assumptions - there will be no re-grounding
        # start_time = time.time()
        # with self.solve(async_=True, on_model=lambda m: print(f'Model: {m}')) as handle:
        with self.solve(async_=True) as handle:
            while not handle.wait(1.0):
                pass
                # time_elapsed = time.time() - start_time
                # if time_elapsed > self.__solve_timeout:
                    # handle.cancel()
                    # raise Exception(f'Timeout error')
                
            res = handle.get()
            self.release_external(external, step)
            self.cleanup()

            return res.satisfiable
        
    def is_satisfiable_assumptions(self, assumptions) -> bool:
        with self.solve(async_=True, assumptions=assumptions) as handle:
            while not handle.wait(1.0):
                pass
                # time_elapsed = time.time() - start_time
                # if time_elapsed > self.__solve_timeout:
                    # handle.cancel()
                    # raise Exception(f'Timeout error')
                
            res = handle.get()
            return res.satisfiable
        
    def enumerate_answer_sets(self):
        with self.solve(yield_=True) as handle:
            for i,m in enumerate(handle): 
                print(f"Answer {i}: {m.symbols(shown=True)}")
                #  handle.get()


    # def is_satisfiable