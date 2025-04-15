from os import path,mkdir,remove
from json import load,dumps
from data.modules.log import LOG
from bitarray import bitarray

def xor(value,bit_index:int):
    return value ^ (1 << bit_index)
    
def xor_complex(value:bitarray) -> bitarray:
    num = int(value.to01(),2)
    for i in range(num.bit_length()):
        num = xor(num,i)
    return bitarray(f'{num:08b}')

from io import FileIO
class DataManagementBitarray:
    def __init__(self):
        pass
    def load(self,file_path:str) -> bitarray:
        ba = bitarray(0)
        with FileIO(file_path,'rb') as f_in:
            ba.fromfile(f_in)
        return ba
    def write(self,file_path:str, data:bitarray) -> None:
        
        with FileIO(file_path,'wb') as f_out:
            data.tofile(f_out)
    
    def encrypt(self,shift):
        pass
            
class DataManagement:
    """
    Many Modules for loading and saving files
    """
    def ine(value:str,default):
        if value != '':
            return value
        else:
            return default
    def ifane(value:str,default):
        "Is float and not empty"
        spl = value.split('.')
        if value != '' and spl.__len__() == 2:
            id = spl[0].replace('-','').isdecimal() + spl[1].isdecimal()
            lr = spl[0] == '' + spl[0] == ''
            
            if lr > 1 or id < 1:
                return default
            
            return float(value)
        else:
            if value.replace('-','').isdecimal():
                return float(value)
            return default
    
    def idane(value:str,default):
        "Is decimal and not empty"
        if value != '' and value.replace('-','').isdecimal():
            return int(value)
        else:
            return default
        
    def get_file_size(filePath:str):
        """
        Returns the fileSize in Bytes
        """
        
        if path.isfile(filePath):
            
            return path.getsize(filePath)
        
    def save(filePath:str,data:dict | tuple | list):
        """
        Saves the Data in JSON File Format With Indent 4
        """
        LOG.nlog(1,'save file: $',[filePath])
        with open(filePath,'w') as fOut:
            
            fOut.write(
                dumps(
                    data,
                    indent=4
                    )
                )
            
    def loads(filePath:str):
        """
        Reads the Data from JSON File Format and converts it to Dict or List
        """
        LOG.nlog(1,'load file: $',[filePath])
        with open(filePath,'r') as fIn:
            
            return load(fIn)
        
    def remove_file(filePath: str):
        if path.isfile(filePath):
            LOG.nlog(2,'Removed : $',[filePath])
            remove(filePath)
        else:
            LOG.nlog(3,'File not found : $',[filePath])
         
    def load_def(filePath:str,searchL:list | tuple,default):
        """
        Returns Specific Value in a JSON File if not existing return Default
        """
        
        with open(filePath,'r') as fIn:
            
            _ret = load(fIn)
            
            for key in searchL:
                
                if key in _ret:
                    
                    _ret = _ret[key]
                    
                else:
                    
                    return default
                    
            return _ret
        
    def load_save(filePath:str,data:dict | tuple | list):
        """
        Load, Edit & Save
        """
        
        _sav = load(filePath)
        
        _sav |= data
        
        DataManagement.save(filePath,_sav)
    def exist_file(filePath):
        if filePath is not None:
            return path.isfile(filePath)
    def create_folder(filePath):
        
        if not path.isdir(filePath):
            LOG.nlog(1,'created Folder: $',[filePath])
            mkdir(filePath)

DM = DataManagement
#! essentialFAFOnStart