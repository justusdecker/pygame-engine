from data.modules.constants import CRYPT_KEY
from bitarray import bitarray
from cryptography.fernet import Fernet
FERNET = Fernet(CRYPT_KEY)
class DataManagementBitArray:
    def encrypt_and_write(file_path:str,data:bitarray):
        data = FERNET.encrypt(data.tobytes())
        with open(file_path,'wb') as f_out:
            f_out.write(data)
    def read_and_decrypt(file_path:str) -> bitarray:
        with open(file_path,'rb') as f_in:
            data = FERNET.decrypt(f_in.read())
        ba = bitarray(0)
        ba.frombytes(data)
        return ba
    def write(file_path:str,data:bitarray):
        with open(file_path,'wb') as f_out:
            f_out.write(data.tobytes())
    def read(file_path:str) -> bitarray:
        ba = bitarray(0)
        with open(file_path,'rb') as f_in:
            data = f_in.read()
            ba.frombytes(data)
        return ba
DMBA = DataManagementBitArray