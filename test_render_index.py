from render.index import index
from render.base import base

formdata = {
    'NAME'    : 'simulation_data',
    'inputs'  : [{ 
        'TYPE' : 'text',
        'NAME' : 'vmin',
        'LABEL' : 'Volumen minimo' 
        }, { 
        'TYPE' : 'text',
        'NAME' : 'vmax',
        'LABEL' : 'Volumen maximo' 
        }],
    'controls': [{
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
}

page = index()
page.add_form(formdata)
page.add_tpl('HEADER_PART', 'tpl/parts/header.html', {'TITLE': 'Simulador CargoSim'})
page.add_tpl('TOP_CONTROLS', 'tpl/parts/top_controls.html')
page.add_tpl('TIMELINE', 'tpl/parts/timeline.html')


lb = base('tpl/parts/list_box.html')
lb.render_params['NAME'] = 'list_box_table'

rt = base('tpl/parts/result_table.html')
rt.render_params['NAME'] = 'result_table'

page.add_tpl('LIST_BOX_PART','tpl/parts/list_box_part.html', {'TITLE': 'Simulaciones parciales', 'LIST_BOX': lb.render()})
page.add_tpl('RESULT_TABLE_PART','tpl/parts/result_table_part.html', {'TITLE': 'Resultado', 'RESULT_TABLE': rt.render()})


print(page.render())