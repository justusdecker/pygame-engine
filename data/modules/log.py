from pygame import Color



class Log:
    """
    The Logging Module
    """
    def __init__(self,
                 file:str='log.txt') -> None:
        """Create & Clean the Log File"""
        with open('log.txt','w') as f:
            f.write('')
    def get_default_module_info(self):
        return {
            'version': '02102024:1.6',
            'name': 'log',
            'state': 'isFinished',
            'copyright': 'Justus Decker'
        }
    def init_log(self,__module__:dict):
        """
        This is a predefined Log Message for loading Modules
        """
        self.log(msg= f"Loaded Version: ${__module__['version']} of Module: ${__module__['name']} State: ${__module__['state']}")
    def get_rgb(self,col,text):
        col = Color(col)
        return f'\033[38;2;{col.r};{col.g};{col.b}m{text}\033[0m'
    def clog(self,id:int=0,msg:str='',vars: list | tuple = [],ind: list | tuple = []):
        "⚠❗💠💬"
        """
        Checks value is identical with...
        Prints & Write custom Log Messages to the logfile: {file}
        [0] Debug Log
        [1] Info Log
        [2] Warning Log
        [3] Error Log
        """

        #$ Declares a variable
        
        color_map = [
            '#CCFF99',
            '#FFCC99',
            '#FF9999',
            '#99FFFF',
            '#FFFF99',
            '#FF99FF',
            '#9999FF',
            '#FF99CC',
            '#FFCC00'
        ]
        
        entry = msg.split(' ')
        output = ''
        var_step = 0
        for idx,word in enumerate(entry):
            if word == '$' and var_step <= len(vars) - 1:
                #print(vars[var_step])
                color_picker = [
                isinstance(vars[var_step],int),
                isinstance(vars[var_step],str),
                isinstance(vars[var_step],bool),
                isinstance(vars[var_step],float),
                isinstance(vars[var_step],dict),
                isinstance(vars[var_step],tuple),
                isinstance(vars[var_step],list),
                isinstance(vars[var_step],bytes)].index(True)
                
                
                
                word = self.get_rgb(color_map[color_picker],vars[var_step])
                
                if vars[idx-1] == ind[idx-1]:
                    beg = '✅'
                else:
                    beg = '❌'
                word = f'[{beg} | {word} == {ind[idx-1]}]'
                var_step += 1
            elif var_step > len(vars) - 1:
                word = '[NULL]'

            output += ' ' + word
        

        print('[' + ('\033[34;1;1m','\033[32;1;1m','\033[33;1;1m','\033[31;1;1m')[id] + ('DEB','INF','WAR','ERR')[id] + '\033[0m]❗ ' + output  + '\033[0m')
        msg = msg.replace('μ','n')
        with open('log.txt','a') as f:
            f.write(f'[{id}]:   {msg}\n')
            
    def tlog(self,msg:str='',version: str = '',r='',f='',l=''):
        """
        Prints & Write custom Todo Log Messages to the logfile: {file}
        [0] Debug Log
        [1] Info Log
        [2] Warning Log
        [3] Error Log
        """
        f,r,l = self.get_rgb(Color('#FFCC00'),f),self.get_rgb(Color('#CCFF99'),r),self.get_rgb(Color('#FF9999'),l)
        ver = self.get_rgb(Color('#9999FF'),version)
        msg_p = self.get_rgb(Color('#FFCC99'),msg)
        
        print(f'[{ver}] {msg_p} {l} {r} {f}\033[0m')
        msg = msg.replace('μ','n')
        with open('todo.txt','w') as f:
            f.write(f'[{version}]:   {msg}\n')
            
    def nlog(self,id:int=0,msg:str='',vars: list | tuple = []):
        """
        Prints & Write custom Log Messages to the logfile: {file}
        [0] Debug Log
        [1] Info Log
        [2] Warning Log
        [3] Error Log
        """

        #$ Declares a variable
        
        color_map = [
            '#CCFF99',
            '#FFCC99',
            '#FF9999',
            '#99FFFF',
            '#FFFF99',
            '#FF99FF',
            '#9999FF',
            '#FF99CC',
            '#FFCC00'
        ]
        
        entry = msg.split(' ')
        output = ''
        var_step = 0
        for idx,word in enumerate(entry):
            if word == '$' and var_step <= len(vars) - 1:
                #print(vars[var_step])
                if vars[var_step] is not None:
                    color_picker = [
                    isinstance(vars[var_step],int),
                    isinstance(vars[var_step],str),
                    isinstance(vars[var_step],bool),
                    isinstance(vars[var_step],float),
                    isinstance(vars[var_step],dict),
                    isinstance(vars[var_step],tuple),
                    isinstance(vars[var_step],list),
                    isinstance(vars[var_step],bytes)].index(True)
                else:
                    color_picker = 2
                
                
                if color_picker == 1:
                    if vars[var_step].startswith('#') and vars[var_step].__len__() == 7:

                        word = self.get_rgb(vars[var_step],vars[var_step])
                    else:
                        word = self.get_rgb(color_map[color_picker],vars[var_step])
                else:
                    word = self.get_rgb(color_map[color_picker],vars[var_step])
                var_step += 1
            elif var_step > len(vars) - 1 and word == '$':
                word = '[NULL]'
            output += ' ' + word
        

        print('[' + ('\033[34;1;1m','\033[32;1;1m','\033[33;1;1m','\033[31;1;1m')[id] + ('DEB','INF','WAR','ERR')[id] + '\033[0m] ' + output  + '\033[0m')
        msg = msg.replace('μ','n')
        with open('log.txt','a') as f:
            f.write(f'[{id}]:   {msg}\n')
            
    def log(self,id:int=0,msg:str=''):
        """
        Prints & Write custom Log Messages to the logfile: {file}
        [0] Debug Log
        [1] Info Log
        [2] Warning Log
        [3] Error Log
        """
        msg_l = msg.split(' ')
        for idx,word in enumerate(msg_l):
            if word.startswith('$'):
                msg_l[idx] = '\033[35;1;4m' + word.replace('$','') + '\033[0m'
        print('[' + ('\033[34;1;1m','\033[32;1;1m','\033[33;1;1m','\033[31;1;1m')[id] + ('DEB','INF','WAR','ERR')[id] + '\033[0m] ' + ' '.join(msg_l)  + '\033[0m')
        msg = msg.replace('μ','n')
        with open('log.txt','a') as f:
            f.write(f'[{id}]:   {msg}\n')

LOG = Log()#- Outsource