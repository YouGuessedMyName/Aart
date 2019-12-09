# Tensorflow-Art
TINKERLAB

Authors: Ivo Melse, Alex Feenstra

Acknowledgements:
Judith van Es, Michiel van Duin


Ranges of randvar 1-4:
1.  (0,9)
2.  (-10,10)
3.  (0, 2pi)
4.  (-pi,pi)


Possible processing:

randvar1: x/9

randvar2: (x+10)/20

randvar3: x/2pi

randvar4: (x+pi)/2pi



Possible processing function:

def process_trainingset(input_list):
  for idx,x in enumerate(input_list):
    for y in range(0,7):
      a = x[y]
      a[0] = a[0]/9
      a[1] = a[1]/9
      a[2] = (a[2]+10)/20
      a[3] = (a[3]+10)/20
      a[4] = a[4]/pi
      a[5] = a[5]/pi
      a[6] = (a[6]+pi)/2pi
      a[7] = (a[7]+pi)/2pi
      x[y] = a
    input_list[idx] = x
  return input_list




