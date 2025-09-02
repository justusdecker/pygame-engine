from time import perf_counter
class DeltaTime:
    """
    Calculate the time between the start of a frame and the end.
    
    This Time is called DELTA(T).
    
    Use case
    ------
    
    ``DeltaTime.t`` is used to calculate position, rotation & other changes based on time.
    
    .. calculation::
        
        ``DeltaTime.t`` * ``speed``
    """
    def __init__(self) -> None: self.b, self.t = 0, 0
        
    def before(self) -> None: self.b = perf_counter()
        
    def after(self) -> None: self.t = perf_counter() - self.b
        
    def get(self) -> float: return self.t