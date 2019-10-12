from render.base import base
from render.forminput import forminput
from render.formcontrol import formcontrol

FORM_TEMPLATE = 'tpl/parts/form.html'

class form(base):

    def __init__(self, paramset={}):
        base.__init__(self, FORM_TEMPLATE)
        self.inputs = []
        self.controls = []
        self.prerender_result = ''

        # Getting inputs
        try:
            inputset = paramset['inputs']
            self.add_inputs(inputset)
            paramset.pop('inputs', None)
        except:
            pass

        # Getting inputs
        try:
            controlset = paramset['controls']
            self.add_controls(controlset)
            paramset.pop('controls', None)
        except:

            pass
        self.render_params = paramset

        return
    

    def add_input(self, paramset):
        i = forminput(paramset)
        self.inputs.append(i) 

    def prerender(self):
        prerender_result = ''
        for i in self.inputs:
            prerender_result += str(i.render())

        self.render_params['FIELDS'] = prerender_result

        prerender_result = ''
        for c in self.controls:
            prerender_result += str(c.render())

        self.render_params['FIELD_CONTROLS'] = prerender_result
        return

    def add_inputs(self, inputs):
        for i in inputs:
            self.add_input(i)

    def add_control(self, paramset):
        c = formcontrol(paramset)
        self.controls.append(c)

    def add_controls(self, controls):
        for c in controls:
            self.add_control(c)

        




