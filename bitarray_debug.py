from data.modules.data_management import DataManagementBitarray,xor_complex
from bitarray import bitarray
DMBA = DataManagementBitarray()
DATA = bitarray("01001000")

print('Logic Gates Tests:')



DATA = DMBA.load('test.data')
print(DATA.to01())
print(xor_complex(DATA).to01())
    
DMBA.write('test.data',DATA)
input('rewrite')
DATA = DMBA.load('test.data')

DMBA.write('test.data',DATA)