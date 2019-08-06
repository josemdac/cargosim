from render.form import form
from render.forminput import forminput


f = form()


# Testing with some inputs


inputset = [{ 
    'TYPE' : 'text',
    'NAME' : 'vmin',
    'LABEL' : 'Volumen minimo' 
    }, { 
    'TYPE' : 'text',
    'NAME' : 'vmax',
    'LABEL' : 'Volumen maximo' 
    }]

controlset = [{
    'NAME'  : 'add',
    'LABEL' : 'Agregar' 
    },{
    'NAME'  : 'remove',
    'LABEL' : 'Quitar' 
    },{
    'NAME'  : 'load',
    'LABEL' : 'Cargar' 
    },{
    'NAME'  : 'save',
    'LABEL' : 'Guardar' 
    }
]

f.add_inputs(inputset)
f.add_controls(controlset)

print(f.render())


formdata = {
    'NAME'    : 'simulation_data',
    'inputs'  : inputset,
    'controls': controlset
}

f1 = form(formdata)

print(f1.render())