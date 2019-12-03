# from tensorflow import keras
# even om lag te voorkomen
import os
import numpy
import pickle


def read_trainingset(name):
    """
    Function which reads a dumped trainingset in from a pickle file.

    :return tuple OR str
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
            content = pickle.load(file)
            datalist, numlist = content
            return (datalist, numlist)
    except:
        return "INVALID_FORMAT"

def get_trainingset():
    """
    function with a UI interface that returns the trainingset.

    :return list, list, filename
    """
    run = True
    print("Please input file name.")
    filename = ""
    while run:
        filename = input()
        data = read_trainingset(filename)
        if data == "NO_FOLDER":
            print("ERROR, trainingset folder not found.")
        if data == "NO_FILE":
            print("ERROR, file name not found.")
        if data == "INVALID_FORMAT":
            print("ERROR, file has invalid format.")
        if data == "NO_FOLDER" or data == "NO_FILE" or data == "INVALID_FORMAT":
            print("Please try again.")
        else:
            run = False
    return data[0], data[1], filename

def show_traningset(input_list, result_list, filename):
    """
    Function to clearly display trainingset data.

    :param input_list: list
    :param result_list: list
    :param filename: str
    """

    print("SHOWING TRAININGSET: ", filename)
    for n in range(0, len(result_list)):
        print("\nIMAGE", n)
        print("    Grade:", result_list[n])
        print("    Function data:\n    ", input_list[n])

def main():
    input_list, result_list, filename = get_trainingset()
    show_traningset(input_list, result_list, filename)

if __name__ == "__main__":
    main()
