import argparse
import numpy
import time
import random
from multiprocessing import Pool

MIN_PIXEL_RANGE = 0
MAX_PIXEL_RANGE = 255


class Pixel:

    def __init__(self, red, green, blue):
        self.red = red
        self.green = green
        self.blue = blue
        self.reproductions_amount = 0

    def __repr__(self):
        return '(Red= {0}, Green= {1}, Blue= {2})'.format(self.red, self.green, self.blue)

    def get_values(self):
        return self.red, self.green, self.blue

    def get_reproduction_amount(self):
        return self.reproductions_amount

    def increment_reproduction_amount(self):
        self.reproductions_amount += 1

    @staticmethod
    def get_random_pixel():
        red = random.randint(MIN_PIXEL_RANGE, MAX_PIXEL_RANGE)
        green = random.randint(MIN_PIXEL_RANGE, MAX_PIXEL_RANGE)
        blue = random.randint(MIN_PIXEL_RANGE, MAX_PIXEL_RANGE)
        return Pixel(red, green, blue)



class Population:

    def __init__(self, initial_amount, interval, iterations, amount_till_death):
        self.community = numpy.empty((initial_amount,), dtype=Pixel)
        for i in range(initial_amount):
            self.community[i] = Pixel.get_random_pixel()
        self.reproduction_interval = interval
        self.number_of_iterations = iterations
        self.reproductions_amount_till_death = amount_till_death
        self.cur_stage = 0
        print(self)

    def __repr__(self):
        return 'Stage {0}: Current population holds {1} Pixels\nSee details below:\n{2}\n'.format(self.cur_stage,
                                                                                                  self.community.size,
                                                                                                  self.community)


    def increment_stage(self):
        self.cur_stage += 1

    @staticmethod
    def reproduce_couple(couple):
        first_values = couple[0].get_values()
        second_values = couple[1].get_values()

        couple[0].increment_reproduction_amount()
        couple[1].increment_reproduction_amount()

        return Pixel((first_values[0] + second_values[0]) // 2, (first_values[1] + second_values[1]) // 2,
                     (first_values[2] + second_values[2]) // 2)

    def population_dilution(self):
        young_indexes = []
        for index, pixel in numpy.ndenumerate(self.community):
            if pixel.get_reproduction_amount() < self.reproductions_amount_till_death:
                young_indexes.append(index[0])
        self.community = self.community[young_indexes]


    def reproduce(self):
        next_call = time.time()
        for i in range(self.number_of_iterations):
            self.increment_stage()
            cur_population_size = len(self.community) if len(self.community) % 2 == 0 else len(self.community) - 1
            shuffled_population = numpy.random.choice(a=self.community, size=cur_population_size, replace=False)
            couples = [(shuffled_population[i], shuffled_population[i + 1]) for i in range(0, cur_population_size, 2)]
            p = Pool()
            baby_pixels = p.map(self.reproduce_couple, couples)
            self.community = numpy.concatenate((self.community, numpy.array(baby_pixels)), axis=0)
            for pixel in shuffled_population:
                pixel.increment_reproduction_amount()
            self.population_dilution()
            print(self)

            next_call += self.reproduction_interval
            time.sleep(next_call - time.time())


def main(arguments):
    pixel_population = Population(arguments.initial_pixels_amount, arguments.reproduction_interval,
                                  arguments.number_of_iterations, arguments.reproductions_amount_till_death)
    pixel_population.reproduce()


if __name__ == '__main__':
    parser = argparse.ArgumentParser(usage="This program simulates the reproduction of pixels. "
                                                           "Call it with the 4 mandatory arguments explained below")

    parser.add_argument("initial_pixels_amount", help="How many pixels you would like to begin "
                                                      "with. Must be greater then 2 in order to reproduce", type=int)

    parser.add_argument("reproduction_interval", help="How much time (seconds) between one reproduction to another",
                        type=int)


    parser.add_argument("number_of_iterations", help="How many reproductions you would like to simulate", type=int)


    parser.add_argument("reproductions_amount_till_death", help="How many reproductions a pixel can participate before"
                                                                "death. Must be greater then 2 in order to reproduce",
                        type=int)

    args = parser.parse_args()
    main(args)
