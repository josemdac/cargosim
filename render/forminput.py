from render.base import base

INPUT_TEMPLATE = 'tpl/parts/input.html'

class forminput(base):

    def __init__(self, params={}):
        base.__init__(self, INPUT_TEMPLATE)
        self.render_params = params
        return

    def set_var(self, name, val):
        self.render_params[name] = val

    
    def prerender(self):
        return





