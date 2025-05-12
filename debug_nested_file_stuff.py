import os

class NestedFileStructure:
    def __init__(self):
        self.map = []
        self.paths = []
    def generate(self):
        """
        Generate two arrays
        ******
        .. map:: Paths
        .. files:: Filenames
        The values are stored like this: ``MAP_ID`` # ``filename``
        """
        self.map : list[str] = []
        self.files : list[str] = []

        for root, dirs, files in os.walk("."):
            path = os.getcwd() + '\\'.join(root.split('\\')[1:]) + '\\'
            if path not in self.map: self.map.append(path)
            map_index = self.map.index(path)
            self.files += [f'{map_index}#{file}' for file in files]
def getcwdasl() -> list:
    return os.getcwd().split('\\')
def cd_back_folder(ammount: int = 1):
    for i in range(ammount):
        os.chdir('\\'.join(getcwdasl()[:-1]))
def cd_foreward_folder(folder_name):
    folder = '\\'.join(getcwdasl()) + f'\\{folder_name}'
    if os.path.isdir(folder):
        os.chdir(folder)
print('\\'.join(getcwdasl()))