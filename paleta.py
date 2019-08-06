#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  paleta.py
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

PAL = [
   120,
   120,
   120
   ]

class Paleta:
    def __init__(self):
        self.w = PAL[0]
        self.h = PAL[1]
        self.d = PAL[2]
        self.boxes = []
    
    def add_box(self, b):
        if b.get_vol() < self.available_vol():
            self.boxes.append(b)
            return True
        else:
            return False
    
    def available_vol(self):
        bvol = 0
        for b in self.boxes:
            bvol = bvol + b.get_vol()
        
        pvol = self.w * self.h * self.d
        avol = pvol - bvol
        return avol
