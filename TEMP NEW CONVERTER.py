#! /usr/bin/python3

#for basic os manipulation
import os

print("HIHI")

#for use in processing
from pickle import load as pickle_load
from matplotlib.pyplot import xlim, ylim, plot, grid, axis, savefig
from math import sin
import numpy
# import PIL Installig PIL in repl.it failed.
import argparse
from shutil import rmtree


class ImageConstructor:
    """
    Class used to reconstruct images from their variables for processing.
    """
    
    def __init__(self):
        self.datalist = None
        self.numlist = None
        self.coord_list = None
        self.image_instance = None
        
    def read_trainingset(self, name):
        """
        Simple method which reads a trainingset in for processing

        :param name: str

        :return str "NO_FILE", "INVALID_FORMAT"
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
        # Mainly used for readability
        return var1 * sin(var2 * u + var3) + var4 

    def reconstruct_coords(self, variable_list):
        """
        Method which reconstructs all coordinates from one picture.

        :param variable_list: list
        """
        
        u_arr = numpy.arange(0, 1, 0.01)
        coord_list = [ [[], []] for i in range(10)]
        for u in u_arr:
            n = 0
            for c in coord_list:
                x = c[0]
                y = c[1]
                x.append(self.get_coord(u,(variable_list[0])[n], (variable_list[4])[n], (variable_list[6])[n], (variable_list[2])[n]))
                y.append(self.get_coord(u, (variable_list[1])[n], (variable_list[5])[n], (variable_list[7])[n], (variable_list[3])[n]))
                n += 1

        coord_list.insert(0, u_arr)
        self.coord_list = coord_list
        
    def plot_and_save_img(self, figurename):
        """
        Method which saves one image to disk
        """
        if self.coord_list == None:
            return "NO_COORD_LOADED"
        
        xlim(-10,10)
        ylim(-10,10)
        grid(b = None)
        axis("off")
        
        for n in range(len(self.coord_list)-1):
            content = self.coord_list[n]
            plot(content[0],content[1], linewidth = float(10/2))
            
        savefig(figurename)
        
        self.coord_list = None
        
    def read_img(self, image_name):
        """
        Method to read one image using PIL

        :param image_name: str
        """
        if not os.path.isfile(image_name):
            image_name = os.path.normpath(os.getcwd()+"/"+image_name)
            if not os.path.isfile(image_name):
                return "NO_FILE"

        try:
            # Commented out temporarily
            # image = PIL.Image.open(image_name)
            pass
        except:
            return "INVALID_FORMAT"
        
        self.image_instance = image

    def process_image(self, size_tuple):
        """
        Method which uses one image instance to process one image into pixel arrays.

        :param size_tuple: tuple (x, y)
        """
        if self.image_instance == None:
            return "NO_IMAGE_LOADED"

        self.image_instance = self.image_instance.resize(size_tuple)
        image_array = numpy.array(self.image_instance, dtype= numpy.float)
        
        self.image_instance = None
        
        return image_array/255

    def process_trainingset(self):
        """
        Method which processes one entire trainingset for use in training.
        """
        if self.datalist == None and self.numlist == None:
            return "NO_SET_LOADED\nNO_NUMLIST_LOADED"
        elif self.datalist == None:
            return "NO_SET_LOADED"
        elif self.numlist == None:
            return "NO_NUMLIST_LOADED"
        
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
        final_array = [final_array,self.numlist]
        
        rmtree(os.path.normpath(os.getcwd()+"/temp_imgs"), ignore_errors=True)
        
        self.numlist = None
        self.datalist = None
        
        return final_array

def main():
  # LOL this code is probably flawed but can't test it cause
  # command line running doesn't seem to be working.

  # Setting argparser arguments
  parser = argparse.ArgumentParser()
  parser.add_argument("file_name", type=str, help="The name of the file you want to process.")
  parser.add_argument("action", type=str, help="What you would like to do with the file.")
  parser.add_argument("--verbosity", type=str, help="How much information the program will output about the process.")
  # I don't think this argument is set properly but it works.

  # Getting the args
  args, leftovers = parser.parse_args()

  # Making vars for better readability, idk could be undone later.
  file_name = args.file_name
  action = args.action

  verbosity = False
  if args.verbosity == "--v" or "--verbosity":
    verbosity = True

  image_constructor = ImageConstructor()

  # Reading trainingset
  error = image_constructor.read_traningset
  if error != None:
    sys.exit("ERROR in ImageConstructor.read_trainingset: " + error)
  if verbosity:
    print("Read trainingset succesfully")
  
  


if __name__ == "__main__":
  main()
