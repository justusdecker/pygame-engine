from time import perf_counter
from data.modules.kernel.log import LOG
class timings:
    def __init__(self):
        self.tims = []
    def add(self,n,t):
        self.tims.append((n,t))
    def clr(self):
        self.tims.clear()
T = timings()
def timein(func):
  
    def test(self):
        t = perf_counter()
        func(self)
        t = perf_counter() - t
        
        T.add(func.__name__,f'{t*1000:.2f}ms')
        #LOG.nlog(0,f"$ $ ms",[func.__name__,round(t * 1000,2)])
    return test