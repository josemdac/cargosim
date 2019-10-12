from render.base import base
from render.form import form

INDEX_TEMPLATE = 'tpl/index.html'
HEADER_TEMPLATE = 'tpl/header.html'

class index(base):

    def __init__(self):
        base.__init__(self, INDEX_TEMPLATE)
        self.forms = []
        self.prerender_result = ''
        self.render_params = {}
        return
    

    def add_form(self, paramset):
        f = form(paramset)
        self.forms.append(f)

    def add_tpl(self, name, template, paramset={}):
        tpl = base(template)
        tpl.render_params = paramset
        self.render_params[name] = tpl.render()
    



    
    def prerender(self):
        #Getting the forms
        forms_html = self.prerender_items(self.forms)
        self.render_params['FORM'] = forms_html

        return
        




