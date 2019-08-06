// Empty JS for your own code to be here
var simulation_form = 'simulation_data'
var list_box = 'list_box_table tbody'

var theads = {
    "total_boxes": 	"Cajas generadas",
    "total_pallets":	"Paletas totales",
    "upsp" : "Espacios utilizados en zona #1",	
    "upsr" : "Espacios usados en zona #2",
    "rem" : "Espacios usados en reserva",
    "verified_boxes": "Cajas verificadas",
    "trips":"Viajes",
    "car_rounds": "Rondas",
    "boxes_to_cars": "Cajas movidas a vehiculo",
    "boxes_to_storage": "Cajas movidas a almacen",
    "ttb": "Tiempo total de descarga",
    "ttps": "Tiempo total de paletas a espera",
    "ttpa": "Tiempo total de paletas a zona #1",
    "ttpr": "Tiempo total de paletas a zona #2",
    "ttpu": "Tiempo total de paletas a reserva",
    "ttvs": "Tiempo total de verificacion de cajas",
    "ttbc": "Tiempo total de cajas a vehiculos",
    "tttt": "Tiempo total de viaje",
    "ttba": "Tiempo total de cajas insolventes",
    "tt": "Tiempo total"
}
$(document).ready(function(){

    $('button#add').click(function(){
        sim.add();
    });

    $('button#remove').click(function(){
        sim.remove();
    });

    $('button#load').click(function(){
        sim.load();
    });

    $('button#save').click(function(){
        sim.save();
    });

    $('a#simrun').click(function(){
        sim.runs();
    });

    $('a#saveresult').click(function(){
        sim.export_result();
    });
    
})
class sim {
    
    static get_data(){
        var target = simulation_form
        return $(`#${target}`).serializeArray();
    }

    static add(){
        var data = sim.get_data()
        sim.add_data(data)
    }
    static add_data(data){
        var vals = []
        var d = new Date()
        var id = d.getTime()
        for(var i in data){ vals[vals.length] = data[i].name + "=" + data[i].value}
        var col1 = `<td>${sim.checkbox(id, JSON.stringify(data))}</td>`
        var col2 =  `<td>${vals.join(', ')}</td>`
        var tpl = `<tr id=${id}><td>${col1}</td><td>${col2}</td></tr>`
        $(`#${list_box}`).append(tpl)
        sim.lb_itemdata(id)
    }

    static checkbox(id, value){
        var tpl = `<input type="checkbox" name="${id}" id="cb${id}" value='${value}'></input>`
        return tpl
    }

    static lb_itemdata(id){
        $(`tr#${id}`).click(function(){
            var a = $(`#cb${id}`).val();
            //console.log(a);
            var data = JSON.parse(a);
            for(var i in data){ $(`#${data[i].name}`).val(data[i].value);}
        })}
    
    static remove(){
        var obs = $(`#list_box_items`).find('input').serializeArray()
        for(var o in obs){ var id=obs[o].name; $(`tr#${id}`).remove() }

    }
        
    static save(){
        var obs = $(`#list_box_table`).find('input')
        var a = []; 
        for(var i=0; i<obs.length; i++){ a[a.length] = {"name" : obs[i].name, "value": obs[i].value }}
        var savedata = {"savedata": a}
        window.location = '/download?savedata=' + encodeURI(JSON.stringify(savedata))
    }

    static load(){
        var fr = new FileReader();
        var i = document.getElementById('openfile');
        var f = i.files[0];
        
        fr.readAsText(f);
        fr.onload = function(e) {
            var s = JSON.parse(JSON.parse(fr.result));
            s = s.savedata;
            $(`#list_box_table tbody`).html('');
            for(var i in s){
                var data = JSON.parse(s[i].value);
                sim.add_data(data);
            }
        }
        

    }

    static runs(){
        
        $(`#resultado_table tbody`).html('');
        var obs = $('#list_box_items').find('input')

        for(var i=0; i<obs.length; i++){ 
            var args = sim.get_args(JSON.parse(obs[i].value));
            sim.simulate(args)

        }

    }

    static get_args(data){
        var args =  {}; for(var v in data){
            args[data[v]['name']]= data[v]['value'];
        }
        return args
    }

    static simulate(data){
        $.ajax({
            method: 'POST',
            dataType: 'json',
            url: '/simulate',
            data : data,
            success: function(data){ 
                var result = data;
                console.log(result)
                sim.prompt(result.messages);
                sim.add_results(result);

            }
        })
    }

    static prompt(messages){
        var str = messages.join('<br />');
        $('#simlog').append('<br />' + str)
    }

    static add_results(result){
        var cols = []
        var h = []
        delete result.messages
        delete result.destinations

        for(var r in result){
            cols[cols.length] = `<td>${result[r]}</td>`
            h[h.length] = `<td><div><span>${theads[r]}</span></div></td>`
        }
        $(`#result_table thead`).html(`<tr>${h.join('')}</tr>`)
        $(`#result_table tbody`).append(`<tr>${cols.join('')}</tr>`)
    }

    static export_result(){
        $("#result_table").table2excel({
            exclude: ".noExl", 
            name: "Resultado", 
            filename: "resultado.xls", 
            fileext: ".xls"
        });
    }
}