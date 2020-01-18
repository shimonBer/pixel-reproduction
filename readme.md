#**Pixel Reproduction**

###This program simulates a reproduction of pixel population.
A pixel is an entity which carries the values of RGB (red, green, blue).
A population of pixels is a collection of pixels.
Pixels can reproduce in couples. This process takes two random pixels and create a third one by calculate the average 
of their values. The population initially consists of 2 or more pixels (up for the user to decide the initial amount).
The program simulates a few stages of reproduction (the number of stages is also up for the user to decide).
Time between one reproduction to another is measured by whole seconds and it is up for the user to decide.
A pixel can and will die after participating in several reproductions (again, up for the user to decide).

####Getting Started
In order to run the program run the following command:

     >pixel_production.py initial_pixels_amount, reproduction_interval, number_of_iterations, >reproductions_amount_till_death
All arguments are mandatory. Their values are explained above or via --help command.

####Prerequisites
argparse, numpy, time, random, multiprocessing 

####Installing
Run the following command:

    > pip install argparse numpy time random multiprocessing 

####About the code
The reproduction is achieved by using multiprocessing. Each process takes a couple of pixels to reproduce in order to
get an efficient and fast program.

####Authors
Shimon Berkovich
