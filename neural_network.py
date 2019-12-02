from tensorflow import keras
import os
import numpy

def read_trainingset(name):
    """
    Function which reads a dumped trainingset in from a pickle file.
    """
    folderpath = os.path.normpath(os.getcwd() + "/trainingsets")
    if os.path.isdir(folderpath) == False:
        os.makedirs(folderpath)
        return "NO_FOLDER"
    path = os.path.normpath(os.getcwd() + "/trainingsets/" + name)
    if os.path.isfile(path) == False:
        input(path)
        return "NO_FILE"
    try:
        with open(path, "rb") as file:
            content = pickle.load(file)
            datalist = content[0]
            numlist = content[1]
            return datalist, numlist
            # datalist = [[[3, 6, ...], ...], ...]           numlist = [0, 4, 6, 9, ...]
    except:
        return "INVALID_FORMAT"

def main():
    name = input("Gimme da file name!!!!\n")
    input_list, result_list = read_trainingset(name)
    

if __name__ == "__main__":
    main()
