#! /usr/bin/python3

#for basic os manipulation
import os

#for use in processing
from pickle import load as pickle_load
from pickle import dump as pickle_dump
from matplotlib.pyplot import xlim, ylim, plot, grid, axis, savefig, clf
from math import sin, pi
import numpy
import PIL
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

    def process_randvar_1(self, var):
        return var/9

    def process_randvar_2(self, var):
        return (var+10)/20
    
    def process_randvar_3(self, var):
        return var/(2*pi)
    
    def process_randvar_4(self, var):
        return (var+pi)/(2*pi)

    def reverse_process_randvar_1(self,var):
        return var*9
    
    def reverse_process_randvar_2(self,var):
        return (var*20)-10
    
    def reverse_process_randvar_3(self,var):
        return var*(2*pi)
    
    def reverse_process_randvar_4(self,var):
        return (var*(2*pi))-pi

    def process_dataset(self, dataset):
        
        if type(dataset) == numpy.array:
            print("WARN: Dataset is an array, attempting to convert to list for processing")
            try:
                dataset = list(dataset)
            except:
                print("ERROR: Converting to list failed, exiting")
                return "INVALID_FORMAT"
            
        for idx,sublist in enumerate(dataset):
            if type(sublist) == numpy.array:
                print("WARN: Element of dataset is an array, attempting to convert to list for processing")
                try:
                    dataset[idx] = list(sublist)
                except:
                    print("ERROR: Converting to list failed, exiting")
                    return "INVALID_FORMAT"

        for idx,var in enumerate(dataset[0]):
            dataset[0][idx] = self.process_randvar_1(var)
            
        for idx,var in enumerate(dataset[1]):
            dataset[1][idx] = self.process_randvar_1(var)
            
        for idx,var in enumerate(dataset[2]):
            dataset[2][idx] = self.process_randvar_2(var)
            
        for idx,var in enumerate(dataset[3]):
            dataset[3][idx] = self.process_randvar_2(var)
            
        for idx,var in enumerate(dataset[4]):
            dataset[4][idx] = self.process_randvar_3(var)
            
        for idx,var in enumerate(dataset[5]):
            dataset[5][idx] = self.process_randvar_3(var)
            
        for idx,var in enumerate(dataset[6]):
            dataset[6][idx] = self.process_randvar_4(var)

        for idx,var in enumerate(dataset[7]):
            dataset[7][idx] = self.process_randvar_4(var)
        
        for idx,sublist in enumerate(dataset):
            dataset[idx] = numpy.array(sublist)
        
        return dataset

    def reverse_process_dataset(self, dataset):
        return "WIP"

    def process_trainingset(self):
        return "WIP"

    def reverse_process_trainingset(self):
        return "WIP"
def main():
    
  # Setting argparser arguments
  parser = argparse.ArgumentParser()
  parser.add_argument("-i","--file_name", type=str, help="The name of the file you want to process.")

  parser.add_argument("-v","--verbosity", help="How much information the program will output about the process.", action="store_true")

  parser.add_argument("-o","--output_name", type=str, help="The name of the output file.")

  parser.add_argument("-pt","--process_trainingset", help="Sets a flag to indicate one entire trainingset should be processed.", action="store_true")

  parser.add_argument("-po","--process_one",help="Sets a flag to indicate one set of variables should be processed.", action = "store_true")

  parser.add_argument("-rp","--reverse_process",help="Sets a flag to indicate a trainigset should be processed to obtain the original variables.", action = "store_true")
  
  # Getting the args
  args = parser.parse_args()
  
  if args.file_name == None:
      print("ERROR: No file name was given!")
      return
  
  #Defaulting variables:
  if args.output_name == None:
    args.output_name = args.file_name

  if args.process_one and args.process_trainingset:
    print("WARN: -pt and -po cannot both be set, defaulting to -pt!")
    args.process_one = False
  
  #Creating imageconstructor instance
  image_constructor = ImageConstructor()

  error = image_constructor.read_trainingset(args.file_name)
  if type(error) == str:
    print("ERROR:"+error)
    return
  
  if args.verbosity:
    print("Trainingset read succesfully")

  input("WIP")

if __name__ == "__main__":
  main()
