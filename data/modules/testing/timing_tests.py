from time import perf_counter
from data.modules.kernel.log import LOG
def timein(func):
  
    def test(self):
        t = perf_counter()
        func(self)
        t = perf_counter() - t
        LOG.nlog(0,f"$ $ ms",[func.__name__,round(t * 1000,2)])
    return test