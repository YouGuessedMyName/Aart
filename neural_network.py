#! /usr/bin/python3
# from tensorflow import keras
# even om lag te voorkomen
import os
import numpy
import pickle
from math import pi

def read_trainingset(name):
    """
    Function which reads a dumped trainingset in from a pickle file.

    :returns tuple OR str
    """
    folderpath = os.path.normpath(os.getcwd() + "/trainingsets")
    if os.path.isdir(folderpath) == False:
        os.makedirs(folderpath)
        return "NO_FOLDER"
    path = os.path.normpath(os.getcwd() + "/trainingsets/" + name)
    if os.path.isfile(path) == False:
        return "NO_FILE"
    try:
        with open(path, "rb") as file:
            datalist,numlist = pickle.load(file)
            return datalist, numlist
    except:
        return "INVALID_FORMAT"

def get_trainingset():
    """
    function with a UI interface that returns the trainingset.

    :returns list, list, filename
    """
    print("Please input file name.")
    filename = ""
    while True:
        filename = input()
        data = read_trainingset(filename)
        if type(data) == str:
            if data == "NO_FOLDER":
                print("ERROR, trainingset folder not found.")
            elif data == "NO_FILE":
                print("ERROR, file name not found.")
            elif data == "INVALID_FORMAT":
                print("ERROR, file has invalid format.")
            print("Please try again.")
        else:
            break
    return data[0], data[1], filename


def process_trainingset(input_list):
    """
    Function to process one input_list to alter all values to a range (0 - 1).
    """
    for set_idx,single_set in enumerate(input_list):
        for y in range(0,7):
            varlist = single_set[y]
            for idx,var in enumerate(varlist):
                if y == 0 or y == 1:
                    varlist[idx] = var/9
                elif y == 2 or y == 3:
                    varlist[idx] = (var+10)/20
                elif y == 4 or y == 5:
                    varlist[idx] = var/pi
                elif y == 6 or y == 7:
                    varlist[idx] = (var+pi)/2*pi
            single_set[y] = varlist
        input_list[set_idx] = single_set
    return input_list

def show_traningset(input_list, result_list, filename):
    """
    Function to clearly display trainingset data.

    :param input_list: list
    :param result_list: list
    :param filename: str
    """

    print("SHOWING TRAININGSET: ", filename)
    for n in range(0, len(result_list)):
        print("\nIMAGE", n+1)
        print("    Grade:", result_list[n])
        print("    Function data:\n    ", input_list[n])
        

def main():
    input_list, result_list, filename = get_trainingset()
    input_list = process_trainingset(input_list)
    show_traningset(input_list, result_list, filename)

if __name__ == "__main__":
    main()
