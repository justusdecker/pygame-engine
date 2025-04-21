from bs4 import BeautifulSoup
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
        for line in HTML.splitlines():
            
            #get child if existing
            
            for x in line:
                if not x.isspace(): break
                depth += 1
            
        return HTML
html = '<button element_name="test" background_colors="[]" text_colors="[]" x="width" y="height"><button element_name="test" background_colors="[]" text_colors="[]" x="width" y="height">test</button></button>'



print(HTMLWRAPPER(html).unpack_html())