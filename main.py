#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  main.py
#  
#  Copyright 2019 Jose De Armas
#  
#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 2 of the License, or
#  (at your option) any later version.
#  
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#  
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software
#  Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#  MA 02110-1301, USA.
#  
#Parámetros de entrada
# @vmin:    Tamaño min de cajas
# @vmax:    Tamaño max de cajas
# @con:     Volumen del contenedor
# @psp:     Espacios disponibles en zona inferior primera entrada
# @psr:     Espacios de reserva en segunda ala
# @solp:    Probabilidad de solvencia
# @locs:    Cantidad de destinos
# @cars:    Cantidad de vehiculos
# @carcap:  Capacidad de cada vehiculo
# @caros:   Tiempo de diferencia entre vehiculos


# @tb:      Tiempo promedio de descarga de una caja
# @tba:     Tiempo promedio de mover caja en almacen 
# @tbc:     Tiempo promedio de mover caja a vehiculo
# @tps:     Tiempo promedio de mover paleta a zona de espera
# @tpa:     Tiempo promedio de mover paleta a almacen
# @tpr:     Tiempo promedio de mover paleta a espacios de reserva
# @tpu:     Tiempo promedio de mover paleta a espacios superiores/otro almacen
# @tvs:     Tiempo promedio de verificar cajas


import procedures
import random
import math
import asyncio
import json



def main(args):
    p = procedures.Procedures()
    # Parámetros de entrada

    p.parse_args(args)
    
    # Paso 1
    boxes = []
    while p.check_total_vol() < p.params['con']:
        p.create_box()
        
    
    p.boxes.pop()
    boxes = p.boxes
    total_boxes = len(boxes)
    p.result['total_boxes'] = total_boxes

    p.add_m('Total volume: {}'.format(p.check_total_vol()))
    
    # Paso 2
    # Cantidad de descargas en paleta
    paletas = []
    pboxes = []
    nboxes = []
    
    palet_num = 0
    #Cajas en contenedor
    while len(boxes) > 0:
        pal = p.create_paleta()
        palet_num += 1
        p.add_m('Creada paleta #{}'.format(palet_num))
        #Carga de cajas en paleta
        while len(boxes) > 0:
            b = boxes.pop()
            if pal.add_box(b):
                pboxes.append(b)
            else:
                nboxes.append(b)
                
        boxes = nboxes
        nboxes = []
        paletas.append(pal)
    
    p.add_m('Total pallets: ' + str(len(paletas)))
    p.result['total_pallets'] = len(paletas)
    
    #Paso 3
    #Mover paletas a los espacios disponibles
    total_paletas = len(paletas)
    
    #Uso de espacios en primera ala
    if (p.params['psp'] - total_paletas) <= 0:
        upsp = p.params['psp']
        rem = total_paletas - upsp
    else:
        upsp = total_paletas
        rem = 0
    #Uso de espacios en segunda ala
    
    if rem >= 0:
        #Uso de espacios superiores o segundo almacen
        if p.params['psr'] < rem:
            p.add_m('Menor')
            upsr = p.params['psr']
            rem = rem - upsp
        else:
            upsr = rem
            rem = 0
    
    p.add_m('upsp : {}, upsr: {}, rem: {}'.format(upsp, upsr, rem))
    p.result['upsp'] = upsp
    p.result['upsr'] = upsr
    p.result['rem'] = rem
    
    #Paso 4
    checked_boxes = len(pboxes)
    p.add_m('Boxes verified: {}'.format(checked_boxes))
    p.result['verified_boxes'] = checked_boxes
    
    #Paso 5
    moved_to_car = 0
    car_boxes = []
    moved_to_storage = 0
    delivery = {}
    
    for l in range(1, int(p.params['locs']+1)):
        delivery[l] = []
    
    #Cajas solventes
    for b in pboxes:
        if random.randint(0, 100) < p.params['solp']:
            b.sol()
            moved_to_car += 1
            car_boxes.append(b)
            delivery[b.dest].append(b)
            
        else:
            b.insol()
            moved_to_storage += 1
    
    trips = 0
    p.result['destinations'] = {}
    for l in range(1, int(p.params['locs']+1)):
        p.load_cars(delivery[l])
        p.result['destinations'][str(l)] = math.ceil(p.trips)
        p.add_m('Total trips for destination {}:{}'.format(l, math.ceil(p.trips)))
        trips += p.trips
    
    p.add_m('Total trips: {}, Car rounds: {}'.format(trips, trips / p.params['cars']))
    p.add_m('Boxes moved to car: {}'.format(moved_to_car))
    p.add_m('Boxes moved to storage: {}'.format(moved_to_storage))
    
    p.result['trips'] = trips
    p.result['car_rounds'] = trips / p.params['cars']
    p.result['boxes_to_cars'] = moved_to_car
    p.result['boxes_to_storage'] = moved_to_storage
    
    #Paso 6
    #Calculo de tiempos totales
    # @tb:      Tiempo promedio de descarga de una caja
    # @tbp:     Tiempo promedio de mover caja a paleta 
    # @tbc:     Tiempo promedio de mover caja a vehiculo
    # @tps:     Tiempo promedio de mover paleta a zona de espera
    # @tpa:     Tiempo promedio de mover paleta a almacen
    # @tpr:     Tiempo promedio de mover paleta a espacios de reserva
    # @tpu:     Tiempo promedio de mover paleta a espacios superiores/otro almacen
    # @tvb:     Tiempo promedio de verificar cajas
    
    times = []
    #Tiempo total de descarga del contenedor
    ttb  = total_boxes * p.params['tb']
    times.append(ttb)
    p.result['ttb'] = ttb
    p.add_m('Descarga del contenedor {}'.format(ttb))
    
    #Tiempo total de mover paletas a zona de espera
    ttps =  len(paletas) * p.params['tps']
    times.append(ttps)
    p.result['ttps'] = ttps
    p.add_m('Mover paletas a zona de espera {}'.format(ttps))
    
    #Tiempo total de mover paletas a almacen (ala 1)
    ttpa =  upsp * p.params['tpa']
    times.append(ttpa)
    p.result['ttpa'] = ttpa
    p.add_m('Mover paletas a paletas a almacen (ala 1) {}'.format(ttpa))
    
    #Tiempo total de mover paletas a almacen (ala 2)
    ttpr =  upsr * p.params['tpr']
    times.append(ttpr)
    p.result['ttpr'] = ttpr
    p.add_m('Mover paletas a paletas a almacen (ala 2) {}'.format(ttpr))
    
    #Tiempo total de mover paletas a almacen (otros espacios)
    ttpu =  rem * p.params['tpu']
    times.append(ttpu)
    p.result['ttpu'] = ttpu
    p.add_m('Mover paletas a paletas a almacen (otros espacios) {}'.format(ttpu))
    
    #Tiempo de verificacion de cajas
    ttvs =  checked_boxes * p.params['tvs']
    times.append(ttvs)
    p.result['ttvs'] = ttvs
    p.add_m('Verificacion de cajas {}'.format(ttvs))
    
    #Tiempo de carga de vehiculos
    ttbc =  moved_to_car * p.params['tbc']
    times.append(ttbc)
    p.result['ttbc'] = ttbc
    p.add_m('Carga de vehiculos {}'.format(ttvs))
    
    #Tiempo de viaje y preparacion de vehiculos
    tttt =  trips * (p.params['caros']) + p.result['car_rounds']
    times.append(tttt)
    p.result['tttt'] = tttt
    p.add_m('Viajes de entrega {}'.format(tttt))
    
    #Tiempo de mover cajas insolventes a almacen
    ttba =  moved_to_storage * p.params['tba']
    times.append(ttba)
    p.result['ttba'] = ttba
    p.add_m('Guardar cajas insolventes {}'.format(ttba))
    
    #Tiempo total de Descarga y entrega a vehiculos
    tt = round(sum(times) / 3600, 3)
    hours = int(tt)
    mins = round((tt-hours)*60)
    p.result['tt'] = sum(times)
    p.add_m('Tiempo total de Descarga y entrega a vehiculos {}Horas, {}mins'.format(hours, mins))
    #p.add_m(args)
    #p.save()
    
    return p.result

if __name__ == '__main__':
    import sys
    sys.exit(main(sys.argv))
