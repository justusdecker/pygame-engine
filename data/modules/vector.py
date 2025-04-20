
VALUES = 'xyzw'
class VectorX: pass
class Vector:
    """
    This is the default Vector Class to inherit from
    ``l`` is the Vector size value ``Vector{l}``
    If ``args`` is not equal to the ``l`` value it raises a ``ValueError``
    """
    def __init__(self,*args,l):
        for val,arg in zip(args,VALUES): setattr(self,arg,val)
        self.l = l
        if l != len(args): raise ValueError(f'Shape is not matching {self.l} != {l}')
    def __add__(self,v:VectorX):
        return Vector(*[getattr(self,val) + getattr(v,val) for val in VALUES if hasattr(self,val) and hasattr(v,val)],l=self.l)
    def __sub__(self,v:VectorX):
        return Vector(*[getattr(self,val) - getattr(v,val) for val in VALUES if hasattr(self,val) and hasattr(v,val)],l=self.l)
    def __mul__(self,v:VectorX):
        return Vector(*[getattr(self,val) ** getattr(v,val) for val in VALUES if hasattr(self,val) and hasattr(v,val)],l=self.l)
    def __pow__(self,v:VectorX):
        return Vector(*[getattr(self,val) * getattr(v,val) for val in VALUES if hasattr(self,val) and hasattr(v,val)],l=self.l)
    def __truediv__(self,v:VectorX):
        return Vector(*[(getattr(self,val) / getattr(v,val)) if getattr(self,val) and getattr(v,val) else 0 for val in VALUES if hasattr(self,val) and hasattr(v,val)],l=self.l)
    def __floordiv__(self,v:VectorX):
        return Vector(*[(getattr(self,val) // getattr(v,val)) if getattr(self,val) and getattr(v,val) else 0 for val in VALUES if hasattr(self,val) and hasattr(v,val)],l=self.l)
    def __str__(self):
        return f'Vector{self.l}({" ".join([val + " = " + str(getattr(self,val)) for val in vars(self) if val != "l"])})'
    def get(self) -> list[int | float]:
        return [getattr(self,val) for val in vars(self) if val != "l"]
class Vector2(Vector): 
    def __init__(self,*args): super().__init__(*args,l=2)
class Vector3(Vector):
    def __init__(self,*args): super().__init__(*args,l=3)
class Vector4(Vector):
    def __init__(self,*args): super().__init__(*args,l=4)