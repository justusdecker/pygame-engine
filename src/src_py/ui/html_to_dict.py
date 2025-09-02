from bs4 import BeautifulSoup
from json import dumps
class HTMLWRAPPER:
    def __init__(self,html_text:str):
        self.html_text = html_text
    def unpack_html(self):
        ui_elements:list = []
        #IF NOT EVEN THE AMMOUNT SOMETHING IS BROKEN
        assert not self.html_text.count('>') % 2 and not self.html_text.count('<') % 2

        BS = BeautifulSoup(self.html_text,'html.parser')
        HTML = BS.prettify()
        for ends in ['</button>']:
            HTML = HTML.replace(ends,'')
        HTML = '\n'.join([x for x in HTML.splitlines() if x and not x.isspace()])
        sp_l = HTML.splitlines()
        for idx,line in enumerate(sp_l):
            print(line)
            truncated = (''.join([i for i in line if not i.isspace()])).startswith('<')
            if truncated:
                args = line.replace('<','').replace('>','').split(' ')[2:]
                UIE = {arg.split('=')[0]:arg.split('=')[1].replace('\"','') for arg in args}
                
                UIE['child'] = idx+1 if idx + 1 <= len(sp_l) else None
                ui_elements.append(UIE)
            else:
                UIE['text'] = idx+1 if idx + 1 <= len(sp_l) else None
        return ui_elements
html = '<button element_name="test" background_colors="[]" text_colors="[]" x="width" y="height"><button element_name="test" background_colors="[]" text_colors="[]" x="width" y="height">test</button></button>'



print(dumps(HTMLWRAPPER(html).unpack_html(),indent=4))