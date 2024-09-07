#!/usr/bin/env python
# -*- coding: utf-8 -*-
#  __  __ ____ _  __ ____ ___ __  __
#  \ \/ // __// |/ //  _// _ |\ \/ /
#   \  // _/ /    /_/ / / __ | \  / 
#   /_//___//_/|_//___//_/ |_| /_/  
# 
#   2024 Yeniay Uav Flight Control Systems
#   Research and Development Team


import math

Blank =[0, 0, 0]

Easy =[
    [-2, 0, 0],
    [ 2, 0, 0]
]

Triangle = [
    [   0,    1, 0],
    [-0.8, -0.4, 0],
    [ 0.8, -0.4, 0]
]

Shapes={
    0 : Easy,
    1 : Triangle,
}

Shape_names={
    'Easy'      : 0,
    'Triangle'  : 1,
}

class Shape:

    def __init__(self, pos=Blank, rot=Blank, scale=1, index=0):
        self.pos   = pos
        self.rot   = rot
        self.scale = scale
        self.type  = index
        self.abs_points = Shapes[self.type]
        self.points = self.getShape()
    
    def rotater(self, pcloud, rot):
        pcl = []
        x = math.radians(rot[0])
        y = math.radians(rot[1])
        z = math.radians(rot[2])
        
        for p in pcloud:

            p = [p[0],(p[1]*math.cos(x))-(p[2]*math.sin(x)),(p[1]*math.sin(x))+(p[2]*math.cos(x))]
            p = [(p[0]*math.cos(y))+(p[2]*math.sin(y)),p[1],(p[2]*math.cos(y))-(p[0]*math.sin(y))]
            p = [(p[0]*math.cos(z))-(p[1]*math.sin(z)),(p[0]*math.sin(z))+(p[1]*math.cos(z)),p[2]]

            p[0]= round(p[0], 5)
            p[1]= round(p[1], 5)
            p[2]= round(p[2], 5)

            pcl.append(p)
        
        return pcl

    def scaler(self,pcloud,scl):
        pcl = []
        for p in pcloud:
            p = [p[0]*scl,p[1]*scl,p[2]*scl]
            p[0]= round(p[0],5)
            p[1]= round(p[1],5)
            p[2]= round(p[2],5)
            pcl.append(p)
        return pcl
    
    def poser(self,pcloud,pos):
        pcl = pcloud
        for p in pcl:
            p[0]=round(pos[0]+p[0],5)
            p[1]=round(pos[1]+p[1],5)
            p[2]=round(pos[2]+p[2],5)
        return pcl

    def getShape(self):
        pcl = self.abs_points
        pcl = self.rotater(pcl,self.rot)
        pcl = self.scaler(pcl,self.scale)
        pcl = self.poser(pcl,self.pos)
        return pcl
    

