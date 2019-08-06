from render.base import base

CONTROL_TEMPLATE = 'tpl/parts/submit.html'

class formcontrol(base):

    def __init__(self, params={}):
        base.__init__(self, CONTROL_TEMPLATE)
        self.render_params = params
        return

    def set_var(self, name, val):
        self.render_params[name] = val

    
    def prerender(self):
        return





