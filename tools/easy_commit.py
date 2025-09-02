from subprocess import run
from os import getcwd, system, remove, chdir
from json import load, dumps

PINFO_PATH = 'src/pinfo.json'

def json_read(filepath : str) -> dict | list:
    with open(filepath, 'r') as f:
        return load(f)

def json_write(filepath : str, data : dict | list):
    with open(filepath, 'w') as f:
        f.write(dumps(data))
def read_file(filepath : str):
    with open(filepath, 'r') as f:
        return f.read()


def get_terminal_result(cmd: str) -> str:
    return run(cmd, capture_output=True, text=True).stdout
     
def get_commit_hash(idm : int = 1) -> str:
    """ Gets the commit hash """
    return get_terminal_result(f"git log --pretty=format:'%h' -n {idm}").replace("\'",'')

def update_pinfo() -> str:
    """
    The new version format will be:
    {MAJOR}.{MINOR}.{MICRO}:{COMMIT_HASH}

    combined:
    1.0.4:abc123
    """
    #    chdir('..')
    data = json_read(PINFO_PATH)

    run('git add -A')
    
    old, new = get_commit_hash(2).split("\n")[1], get_commit_hash()
    
    t_res: list[str] = get_terminal_result(f'git diff --shortstat {old} {new}').split(',')

    #changes = sum([int(ch.split(' ')[1]) for ch in t_res])
    
    data['micro'] += 1
    
    #print(changes,t_res)
    
    msg = read_file('tools/cm.i')
    
    data['hash'] = new
    
    cmtmsg = f"\"{data['major']}.{data['minor']}.{data['micro']}:{new} - {msg}\""
    
    remove('tools/cm.i')
    
    json_write(PINFO_PATH,data)
    run('git add -A')
    run(f'git commit -m {cmtmsg}')
    run(f'git push')
if __name__ == '__main__':
    chdir('tools/')
    system('get_current_commit_msg.vbs')
    chdir('..')
    get_commit_hash()
    update_pinfo()



