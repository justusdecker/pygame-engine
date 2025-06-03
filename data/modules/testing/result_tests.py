from data.modules.kernel.log import LOG
def surfarray_result_check(func):
  
    def test(self,*args,**kwargs):
        
        ret = func(self,*args,**kwargs)
        
        LOG.nlog(0,f"$ $",[func.__name__,self.array.tolist()])
        return ret
    return test