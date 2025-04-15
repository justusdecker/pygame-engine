from data.modules.data_management import DataManagementBitarray,xor_complex,get_checksum,validate_checksum
from bitarray import bitarray
DMBA = DataManagementBitarray()
print('Logic Gates Tests:')

DATA = bitarray('1011011110110111')

print(DATA)
DATA = xor_complex(DATA)

print(DATA)
ch = get_checksum(DATA,16)
print(f'{ch=} {DATA=}')
DATA = DATA + ch
print(DATA)


print(f'vc: {validate_checksum(DATA,16)}')