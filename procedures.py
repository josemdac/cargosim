#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  procedures.py
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
#  
import box
import random
import paleta
import cars
import json

class Procedures:
    def __init__(self):
        self.params = {}
        self.boxes = []
        self.volume = 0
        self.result = {'messages' : []}
        
    def parse_args(self, args=[], argsw=[]):
        for i in range(0, len(args)):
            words = args[i].split('=')
            self.params[words[0]] = words[1]

        try:
            if self.params['reset'] == 'true':
                with open('output.json', "w") as fh:
                    fh.write('')
                    fh.close()
        except:
            pass
        
        try:
            self.parse_file()
        except:
            pass
        

        self.change_types()
        
    def parse_file(self):
        filename = self.params['filename']
        self.params = json.loads(self.read_file(filename))['params']    
        pass

    def read_file(self, filename):
        with open(filename, "r") as fh:
            json_str = fh.read()
            fh.close()
            
        return json_str
        
    def change_types(self):
        for p in self.params.keys():
            self.params[p] = int(self.params[p])
    
    def create_box(self):
        rnum = float(random.randint(1,100)/100)
        x = float(random.randint(1,100)/100)
        y = float(random.randint(1,100)/100)
        z = float(random.randint(1,100)/100)
        
        v = (self.params['vmax'] - self.params['vmin']) * rnum
        
        l = ( v /(x * y * z) ) ** (1./3)
        w = l * x
        h = l * y
        d = l * z
        
        locs = self.params['locs']
        boxc = box.Box(w, h, d)
        boxc.dest(locs)
        self.volume += boxc.get_vol()
        self.boxes.append(boxc)
        return
            
    def check_total_vol(self):
        
        #vols = list(map(lambda b: b.get_vol(), boxes))
        return self.volume
        
    def create_paleta(self):
        return paleta.Paleta()
        
    def add_m(self, m):
        print(m)
        self.result['messages'].append(m)


    def load_cars(self, boxes):
         # Cantidad de descargas en paleta
        carset = []
        pboxes = []
        nboxes = []
        
        car_num = 0
        #Cajas en contenedor
        while len(boxes) > 0:
            car = cars.Car(self.params['carcap'])
            car_num += 1

            #Carga de cajas en paleta
            while len(boxes) > 0:
                b = boxes.pop()
                if car.add_box(b):
                    pboxes.append(b)
                else:
                    nboxes.append(b)
                    
            boxes = nboxes
            nboxes = []
            carset.append(car)
        
        self.cars = carset
        self.trips = len(carset)
    
    def save(self, reset=False):
        
        filename = 'output.json'
        
        data = []
        
        if not reset:
            try:
                data = json.loads(self.read_file(filename))
            except:
                pass
        
        data.append(self.result)
        
        with open(filename, "w") as fh:
            fh.write(json.dumps(data))
            fh.close()
    
