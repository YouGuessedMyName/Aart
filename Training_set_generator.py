#! /usr/bin/python3
import os
from random import randrange, uniform, randint
import secrets
from math import pi, sin
from matplotlib.pyplot import plot, xlim, ylim, show, grid, axis
from numpy import arange
import pickle

# Function to clear screen with and print title with
def title():
    print(
        "\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n>>>>>>>>>>>>>>>>>>>>>>>>>>\nTraining set generator 2.0\n<<<<<<<<<<<<<<<<<<<<<<<<<<")


# Class to group all variable generation
class RandValsObj:

    def randvar_1(self):
        return randint(0, 9)

    def randvar_2(self, var1, var2):
        return randrange(var1 - 10, 10 - var2)

    def randvar_3(self):
        return uniform(0, 2 * pi)

    def randvar_4(self):
        return uniform(-pi, pi)

    def get_coord(self, u, var1, var2, var3, var4):
        return var1 * sin(var2 * u + var3) + var4


# Class to hold all data from one (1) image
# All variables should be lists of 10 integers each, representing all variables necessary to create an image
class ImageDataObj:

    def __init__(self):
        self.var_list = [[] for i in range(8)]
        # vars in one nested list instead of eight seperate ones
        # [[], [], ....]

    # Creates all variables necessary for an image
    def gen_imagedata(self):
        randvals = RandValsObj()
        for var in range(10):
            self.var_list[0].append(randvals.randvar_1())
            self.var_list[1].append(randvals.randvar_1())
            self.var_list[2].append(randvals.randvar_2((self.var_list[0])[var-1],(self.var_list[1])[var-1]))
            self.var_list[3].append(randvals.randvar_2((self.var_list[1])[var-1],(self.var_list[0])[var-1]))
            self.var_list[4].append(randvals.randvar_3())
            self.var_list[5].append(randvals.randvar_3())
            self.var_list[6].append(randvals.randvar_4())
            self.var_list[7].append(randvals.randvar_4())


    # Function which is called by plot in order to generate all coordinates
    def gen_coordinates(self):
        randvals = RandValsObj()
        u_arr = arange(0, 1, 0.01)
        # list of empty coords [[x, y], [x, y]......]
        
        coord_list = [
            [[], []] for i in range(10)
            ]

        for u in u_arr:
            n = 0
            for c in coord_list:
                x = c[0]
                y = c[1]
                x.append(randvals.get_coord(u,(self.var_list[0])[n], (self.var_list[4])[n], (self.var_list[6])[n], (self.var_list[2])[n]))
                y.append(randvals.get_coord(u, (self.var_list[1])[n], (self.var_list[5])[n], (self.var_list[7])[n], (self.var_list[3])[n]))
                n += 1

        # list of empty coords [[x, y], [x, y]......]
        coord_list.insert(0, u_arr)
        return coord_list

    # Method to plot the generated image with
    def plot_image(self):
        coordinatelist = self.gen_coordinates()
        xlim(-10, 10)
        ylim(-10, 10)
        
        for n in range(len(coordinatelist)-1):
            content = coordinatelist[n]
            x = content[0]
            y = content[1]
            plot(x, y)
        grid(b = None)
        axis("off")
        show()


# Class to hold all data from one (1) training set
# Datalist is a list of all variables used,
# Numlist is a list of all numbers assigned to the images
class DataSetObj:

    def __init__(self):
        self.datalist = []
        self.numlist = []

    # Method to append data and number
    def append_data(self, data, num):
        if type(data) == list and len(data) == 8 and type(num) == int:
            self.datalist.append(data)
            self.numlist.append(num)
        else:
            return "INVALID_FORMAT"

    # Method which dumps the trainingset as a pickle file
    def save_trainingset(self, name):
        folderpath = os.path.normpath(os.getcwd() + "/trainingsets")
        if os.path.isdir(folderpath) == False:
            os.makedirs(folderpath)
        path = os.path.normpath(folderpath + "/" + name)
        with open(path, "wb") as file:
            pickle.dump([self.datalist, self.numlist], file)

    # Method which reads a dumped trainingset in from a pickle file
    def read_trainingset(self, name):
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
                self.datalist,self.numlist = pickle.load(file)
        except:
            return "INVALID_FORMAT"


def gen_dataset(dataset):
    title()
    amount = input("How many pictures would you like to put in this new training set?\nIf you enter anything other than a number, you will return to the menu.\n")
    try:
        amount = int(amount)
        if amount < 0:
            raise Exception
    except:
        return dataset

    for n in range(amount):
        imagehandler = ImageDataObj()
        imagehandler.gen_imagedata()
        title()
        input("Press enter to see the image.\nWhen you are done reviewing it, close the window.\n")
        imagehandler.plot_image()
        num = input("On a scale of 1-10, how would you rate this image?\nYou can also press enter to discard.\n")
        try:
            num = int(num)
            if num < 1 or num > 10:
                raise Exception
        except:
            num = False
        if type(num) == int:
            check = dataset.append_data(imagehandler.var_list, num)
    return dataset


def read_dataset(dataset):
    title()
    name = input(
        "What is the name of the training set you want to read?\nYou can also press enter to return to the menu.\n")
    if name != "":
        check = dataset.read_trainingset(name)
        title()
        if check == "NO_FOLDER":
            input("The folder used to store all training sets does not exist.\nTherefore, there are no training sets.\nPress enter to return to the menu.\n")
        elif check == "NO_FILE":
            input("The filename you entered does not exist.\nPress enter to return to the menu.\n")
        elif check == "INVALID_FORMAT":
            input("The file you attempted to read does not have a valid format.\nPress enter to retrun to the menu.\n")
        else:
            input("The training set has been read succesfuly.\nPress enter to return to the menu.\n")
    return dataset


def save_dataset(dataset):
    title()
    if len(dataset.datalist) < 1:
        input("The current training set is empty.\nPlease put at least 1 picture in it first.\nPress enter to return to the menu.\n")
    else:
        name = input("What would you like to name the current training set?\nIf you pick a filename which already exists, it will be overwritten!\nYou can also press enter to return to the menu.\n")
        if name != "":
            dataset.save_trainingset(name)


# Start of main loop
mainloop = True
chosen_set = None
dataset = DataSetObj()
while mainloop:
    title()
    if dataset.datalist != []:
        print("The current dataset is " + str(len(dataset.datalist)) + " items long.")
    print("Do you want to:\n1) Create a new training set/Append to selected set\n2) Read a training set\n3) Save a training set\n4) Exit\n")
    choice = input()
    try:
        choice = int(choice)
    except:
        choice = 0
    if choice == 1:
        dataset = gen_dataset(dataset)
    elif choice == 2:
        dataset = read_dataset(dataset)
    elif choice == 3:
        save_dataset(dataset)
    elif choice == 4:
        mainloop = False
