#! /usr/bin/python3

#for basic os manipulation
import os

#for use in processing
from pickle import load as pickle_load
from pickle import dump as pickle_dump
from math import sin, pi
import numpy
import argparse


class ProcessingObj:
    """
    Class used to reconstruct images from their variables for processing.
    """
    
    def __init__(self):
        self.datalist = None
        self.numlist = None
        
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
        
        if type(dataset) != list:
            print("WARN: Dataset is not a list, attempting to convert to list for processing")
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
            dataset[idx] = numpy.array(sublist, dtype =numpy.float64)
        
        return dataset

    def reverse_process_dataset(self, dataset):

        if type(dataset) != list:
            print("WARN: Dataset is not a list, attempting to convert to list for processing")
            try:
                dataset = list(dataset)
            except:
                print("ERROR: Converting to list failed, exiting")
                return "INVALID_FORMAT"


        for idx, sublist in enumerate(dataset):
            if type(sublist) != numpy.array:
                print("WARN: Element of dataset is not an array, is this a genuine dataset?")
                try:
                    sublist = list(sublist)
                except:
                    print("ERROR: Converting to list failed, exiting")
                    return "INVALID_FORMAT"
            else:
                sublist = list(sublist)
            dataset[idx] = sublist

        for idx,var in enumerate(dataset[0]):
            dataset[0][idx] = self.reverse_process_randvar_1(var)
            
        for idx,var in enumerate(dataset[1]):
            dataset[1][idx] = self.reverse_process_randvar_1(var)
            
        for idx,var in enumerate(dataset[2]):
            dataset[2][idx] = self.reverse_process_randvar_2(var)
            
        for idx,var in enumerate(dataset[3]):
            dataset[3][idx] = self.reverse_process_randvar_2(var)
            
        for idx,var in enumerate(dataset[4]):
            dataset[4][idx] = self.reverse_process_randvar_3(var)
            
        for idx,var in enumerate(dataset[5]):
            dataset[5][idx] = self.reverse_process_randvar_3(var)
            
        for idx,var in enumerate(dataset[6]):
            dataset[6][idx] = self.reverse_process_randvar_4(var)
            
        for idx,var in enumerate(dataset[7]):
            dataset[7][idx] = self.reverse_process_randvar_4(var)
        
        return dataset

    def process_trainingset(self):

        if self.datalist == None or self.numlist == None:
            print("ERROR: No trainingset is loaded, exiting")
            return "NO_SET"

        if type(self.datalist) == numpy.array:
            print("WARN: Trainingset is an array, attempting to convert to list for processing")
            try:
                self.datalist = list(self.datalist)
            except:
                print("ERROR: Converting to list failed, exiting")
                return "INVALID_FORMAT"
        
        for idx,dataset in enumerate(self.datalist):
            self.datalist[idx] = self.process_dataset(dataset)
        
        final_array = [numpy.array(self.datalist,dtype=numpy.float64),numpy.array(self.numlist,dtype =numpy.float64)]
        
        self.datalist = None
        self.numlist = None
        
        return final_array

    def reverse_process_trainingset(self):

        if type(self.datalist) == None or type(self.numlist) == None:
            print("ERROR: No trainingset is loaded, exiting")
            return "NO_SET"

        if type(self.datalist) != numpy.array:
            print("WARN: Trainingset is not an array, is this a genuine trainingset?")
            try:
                self.datalist = list(self.datalist)
            except:
                print("Converting to list failed, exiting")
                return "INVALID_FORMAT"
        else:
            self.datatlist = list(self.datalist)

        for idx,dataset in enumerate(self.datalist):
            self.datalist[idx] = self.reverse_process_dataset(dataset)

        raw_set = [self.datalist,self.numlist]
        
        self.datalist = None
        self.numlist = None
        return raw_set

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

    if os.path.isfile(args.output_name) == True or os.path.isfile(os.path.normpath(os.getcwd()+"/"+args.output_name)) == True:
        print("WARN: Output file name is already in use, file will be overwritten!")

    if args.process_one and args.process_trainingset:
        print("WARN: -pt and -po cannot both be set, defaulting to -pt!")
        args.process_one = False

    #Creating ProcessingObj instance
    variable_processor = ProcessingObj()

    error = variable_processor.read_trainingset(args.file_name)
    if type(error) == str:
        print("ERROR:"+error)
        return

    if args.verbosity:
        print("Trainingset read succesfully")

    
    if args.process_one:
        if args.verbosity:
            print("Processing dataset")
            
        if args.reverse_process:
            processed_set = variable_processor.reverse_process_dataset()
        else:
            processed_set = variable_processor.process_dataset()

    elif args.process_trainingset:
        if args.verbosity:
            print("Processing trainingset")
        
        if args.reverse_process:
            processed_set = variable_processor.reverse_process_trainingset()
        else:
            processed_set = variable_processor.process_trainingset()

    if args.reverse_process:
        suffix = ""
        if args.output_name[:-12] == ".trainingset":
            args.ouput_name = args.output_name[::-12]
    else:
        suffix = ".trainingset"

    if args.verbosity:
        print("Saving processed data")

    with open(os.path.normpath(os.getcwd()+"/"+args.output_name+suffix), "wb") as file:
        pickle_dump(processed_set,file)

    if args.verbosity:
        print("Processing finished")

if __name__ == "__main__":
  main()
