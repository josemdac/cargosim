from flask import Flask
from flask import request
from flask import make_response
from render.index import index
from render.base import base
import json
import urllib.parse
from main import main

app = Flask(__name__)

@app.route('/')
def front_end():
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
                }, { 
                'TYPE' : 'text',
                'NAME' : 'con',
                'LABEL' : 'Volumen total' 
                }, { 
                'TYPE' : 'text',
                'NAME' : 'psp',
                'LABEL' : 'Espacios en zona #1' 
                }, { 
                'TYPE' : 'text',
                'NAME' : 'psr',
                'LABEL' : 'Espacios en zona #2' 
                }, { 
                'TYPE' : 'text',
                'NAME' : 'solp',
                'LABEL' : 'Probabilidad de solvencia' 
                }, { 
                'TYPE' : 'text',
                'NAME' : 'cars',
                'LABEL' : 'Vehiculos' 
                }, { 
                'TYPE' : 'text',
                'NAME' : 'carcap',
                'LABEL' : 'Capacidad de vehiculos' 
                }, { 
                'TYPE' : 'text',
                'NAME' : 'caros',
                'LABEL' : 'Retardo entre vehiculos' 
                }, { 
                'TYPE' : 'text',
                'NAME' : 'tb',
                'LABEL' : 'Descarga de caja (tiempo)' 
                }, { 
                'TYPE' : 'text',
                'NAME' : 'tba',
                'LABEL' : 'Mover caja insolvente (tiempo)' 
                }, { 
                'TYPE' : 'text',
                'NAME' : 'tbc',
                'LABEL' : 'Mover caja a vehiculo (tiempo)' 
                }, { 
                'TYPE' : 'text',
                'NAME' : 'tps',
                'LABEL' : 'Paleta a zona de espera (tiempo)' 
                }, { 
                'TYPE' : 'text',
                'NAME' : 'tpa',
                'LABEL' : 'Paleta a zona #1 (tiempo)' 
                }, { 
                'TYPE' : 'text',
                'NAME' : 'tpr',
                'LABEL' : 'Paleta a zona #2 (tiempo)' 
                }, { 
                'TYPE' : 'text',
                'NAME' : 'tpu',
                'LABEL' : 'Paleta a reserva (tiempo)' 
                }, { 
                'TYPE' : 'text',
                'NAME' : 'tvs',
                'LABEL' : 'Verificación de una caja (tiempo)' 
                }, { 
                'TYPE' : 'text',
                'NAME' : 'locs',
                'LABEL' : 'Número de destinos de entrega' 
                }, { 
                'TYPE' : 'text',
                'NAME' : 'triptime',
                'LABEL' : 'Duración de viaje' 
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
                'LABEL' : 'Guardar parámetros' 
                }
        ]
        }

        page = index()
        page.add_form(formdata)
        page.add_tpl('HEADER_PART', 'tpl/parts/header.html', {'TITLE': 'Simulador CargoSim, para Next Cargo'})
        page.add_tpl('TOP_CONTROLS', 'tpl/parts/top_controls.html')
        page.add_tpl('TIMELINE', 'tpl/parts/timeline.html')


        lb = base('tpl/parts/list_box.html')
        lb.render_params['NAME'] = 'list_box_table'

        rt = base('tpl/parts/result_table.html')
        rt.render_params['NAME'] = 'result_table'

        page.add_tpl('LIST_BOX_PART','tpl/parts/list_box_part.html', {'TITLE': 'Simulaciones parciales', 'LIST_BOX': lb.render()})
        page.add_tpl('RESULT_TABLE_PART','tpl/parts/result_table_part.html', {'TITLE': 'Resultado', 'RESULT_TABLE': rt.render()})
        page.render_params['TITLE'] = 'Cargo Sim'

        return page.render()
    
    
@app.route('/scripts/<path>')
def get_scripts(path):
        with open('tpl/{}'.format(path), 'r') as fh:
                fdata = fh.read()
                fh.close()  
        return fdata


@app.route('/download', methods=['GET'])
def generate_download():
        data = json.dumps(request.args.get('savedata'))
        print(data)
        resp = make_response(data, 200)
        resp.headers.set('Content-Disposition', ' attachment; filename="{}"'.format('data.json'))
        resp.headers.set('Content-type','application/json; charset=utf-8')
        resp.headers.set('Cache-Control','private')
        resp.headers.set('Pragma','private')
        resp.headers.set('Expires', 'Mon, 26 Jul 1997 05:00:00 GMT')
        return resp

@app.route('/simulate', methods=['POST'])
def simulate():

        raw = str(request.get_data(), 'utf-8')
        #data = json.loads()
        #for k in data.keys():
        #        data[k] = data[k][0]
        args = urllib.parse.unquote_plus(raw)
        args = args.split("&")
        print(args)
        try:
                print('Procesando...')
                result = main(args)
                print(result)
                return json.dumps(result)
        except:
                return json.dumps({'messages': []})
        #return ""

