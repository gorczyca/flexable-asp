import clingo


class CustomClingoControl(clingo.Control):
    def __init__(self, *asp_files):
        super().__init__(['--warn=none'])
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