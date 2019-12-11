#! /usr/bin/python3

#for basic os manipulation
import os

#for use in processing
from pickle import load as pickle_load
from matplotlib.pyplot import xlim, ylim, plot, grid, axis, savefig
from math import sin
import numpy
import PIL

#for future use
import argparse

class image_constructor:
    """
    Class used to reconstruct images from their variables for processing
    """
    
    def __init__(self):
        self.datalist = None
        self.numlist = None
        self.coord_list = None
        self.image_instance = None
        
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
        
        u_arr = numpy.arange(0, 1, 0.01)
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
        self.coord_list = coord_list
        
    def plot_and_save_img(self, figurename):
        """
        Method which saves one image to disk
        """
        
        xlim(-10,10)
        ylim(-10,10)
        for n in range(len(self.coord_list)-1):
            content = self.coord_list[n]
            plot(content[0],content[1], linewidth = float(10/2))
        grid(b = None)
        axis("off")
        savefig(figurename)

    def read_img(self, imgname):
        """
        Method to read one image using PIL
        """
        if not os.path.isfile(imgname):
            imgname = os.path.normpath(os.getcwd()+"/"+imgname)
            if not os.path.isfile(imgname):
                return "NO_FILE"

        try:
            image = PIL.Image.open(imgname)
        except:
            return "INVALID_FORMAT"
        
        self.image_instance = image

    def process_image(self, size_tuple):
        """
        Method which uses one image instance to process one image into pixel arrays
        """
        self.image_instance = self.image_instance.resize(size_tuple)
        image_array = numpy.array(self.image_instance, dtype= numpy.float)
        return image_array/255

    def process_trainingset(self):
        """
        Method which processes one entire trainingset for use in training
        """
        if self.datalist == None:
            return "NO_SET_LOADED"
        os.makedirs(os.path.normpath(os.getcwd()+"/temp_imgs"))
        n = 0
        final_array = []
        for trainingset in self.datalist:
            self.reconstruct_coords(trainingset)
            self.plot_and_save_img("/temp_imgs/img"+str(n))
            self.read_img("/temp_imgs/img"+str(n))
            trainingset_array = self.process_image((128,128))
            final_array.append(trainingset_array)
            n+=1
        final_array = numpy.array(final_array)
        return final_array

#Now we just need to build the parser around it
