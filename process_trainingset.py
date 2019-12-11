#! /usr/bin/python3

#for basic os manipulation
import os

#for use in processing
from pickle import load as pickle_load
from matplotlib.pyplot import xlim, ylim, plot, grid, axis, savefig
from math import sin
from numpy import array, arange

#for future use
import PIL
import argparse

class image_constructor:
    """
    Class used to reconstruct images from their variables for processing
    """
    
    def __init__(self):
        self.datalist = None
        self.numlist = None
        
    def read_trainingset(self, name):
        """
        Simple method which reads a trainingset in for processing
        """
        if not os.path.isfile(name):
            name = os.path.normpath(os.getcwd()+"/"+name)
            if not os.path.isfile(name):
                return "NO_FILE"

        try:
            with open(name,"rb") as file:
                datalist,numlist = pickle_load(file)
        except:
            return "INVALID_FORMAT"
        self.datalist = datalist
        self.numlist = numlist

    def get_coord(self, u, var1, var2, var3, var4):
        #Mainly used for readability
        return var1 * sin(var2 * u + var3) + var4 

    def reconstruct_coords(self, variablelist):
        """
        Method which reconstructs all coordinates from one picture
        """
        
        u_arr = arange(0, 1, 0.01)
        coord_list = [ [[], []] for i in range(10)]
        for u in u_arr:
            n = 0
            for c in coord_list:
                x = c[0]
                y = c[1]
                x.append(self.get_coord(u,(variablelist[0])[n], (variablelist[4])[n], (variablelist[6])[n], (variablelist[2])[n]))
                y.append(self.get_coord(u, (variablelist[1])[n], (variablelist[5])[n], (variablelist[7])[n], (variablelist[3])[n]))
                n += 1

        coord_list.insert(0, u_arr)
        return coord_list
        
    def plot_and_save_img(self, coord_list, figurename):
        """
        Method which saves one image to disk
        """
        
        xlim(-10,10)
        ylim(-10,10)
        for n in range(len(coord_list)-1):
            content = coord_list[n]
            plot(content[0],content[1], linewidth = float(7/2))
        grid(b = None)
        axis("off")
        savefig(figurename)

    def read_img(self, imgname):
        """
        Method to read one image using PIL
        """
        return "WIP"

    def process_trainingset(self):
        """
        Method which processes one entire trainingset for use in training
        """
        return "WIP"

