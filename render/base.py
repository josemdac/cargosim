class base:
    @staticmethod
    def get_tpl(path):
        with open(path, 'r') as fh:
            tpl = fh.read()
            fh.close()
        
        return tpl

    @staticmethod
    def tpl_vars(str, params):
        endstr = str
        vars = params.keys()
        for v in vars:
            endstr = endstr.replace('[{}]'.format(v), params[v])
        
        return endstr

    @staticmethod
    def parse_tpl(path, params):
        str = base.get_tpl(path)
        return base.tpl_vars(str, params)

    def __init__(self, template):
            self.inputs = []
            self.prerender_result = ''
            self.render_params = {}
            self.template = template
            return

    
    def prerender(self):
        return


    def render(self):
        self.prerender()
        html = base.parse_tpl(self.template, self.render_params)
        return html
    
    def prerender_items(self, items):
        prerender_result = ''
        for i in items:
            prerender_result += i.render()
        
        return prerender_result