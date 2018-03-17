import sys
import math

input_file = open("e_high_bonus.in", "r")

firstLine = input_file.readline()
firstLine = firstLine.replace("\n", "")
firstLine = firstLine.split(' ')

R = int(firstLine[0])  # rows
C = int(firstLine[1])  # columns
F = int(firstLine[2])  # cars
N = int(firstLine[3])  # rides
B = int(firstLine[4])  # bonus
T = int(firstLine[5])  # steps

class RideInfo:
    start_x = 0
    start_y = 0
    end_x = 0
    end_y = 0
    start_time = 0
    end_time = 0
    possible = 0
    trip_duration = 0

    def __init__(self, _start_x, _end_x, _start_y, _end_y, _start_time, _end_time, _possible, _trip_duration):
        self.start_x = _start_x
        self.start_y = _start_y
        self.end_x = _end_x
        self.end_y = _end_y
        self.start_time = _start_time
        self.end_time = _end_time
        self.possible = _possible
        self.trip_duration = _trip_duration

class CarInfo:
    current_x = 0
    current_y = 0
    available = 0
    number_of_trips_done = 0
    trips = []
    ticker = 0

    def __init__(self, _current_x, _current_y, _available, _number_of_trips_done, _trips, _ticker):
        self.current_x = _current_x
        self.current_y = _current_y
        self.available = _available
        self.number_of_trips_done = _number_of_trips_done
        self.trips = _trips
        self.ticker = _ticker

rides = []
cars = []

# filling in rides array
for i in range(N):
    line = input_file.readline()
    #line = line.replace("\n", "")
    line = line.split(' ')
    start_x, end_x, start_y, end_y, start_time, end_time = line
    start_x = int(start_x)
    end_x = int(end_x)
    start_y = int(start_y)
    end_y = int(end_y)
    start_time = int(start_time)
    end_time = int(end_time)
    trip_duration = abs(start_x - end_x) + abs(start_y - end_y)
    if trip_duration <= T and trip_duration <= (end_time - start_time):
        possible = 1
    else:
        possible = 0
    rides.append(RideInfo(start_x, end_x, end_x, end_y, start_time, end_time, possible, trip_duration))

# each car starts from (0, 0), available, without any trips done
for i in range(F):
    cars.append(CarInfo(0, 0, 1, 0, [], 0))

global_turn_id = 0  # first turn - zero
taken = 0 # number of rides assigned

# run the loop if there are steps or rides left
while global_turn_id < T or taken == N:
    for i in range(F):
        if (cars[i].available):
            dist = []
            for j in range(N):
                canStart = global_turn_id + abs(rides[j].start_x - cars[i].current_x) + abs(
                    rides[j].start_y - cars[i].current_y)
                if (rides[j].possible and canStart + rides[j].trip_duration <= rides[j].end_time):
                    dist.append(max(canStart, rides[j].start_time))
                else:
                    dist.append(20000000)

            min1 = dist[0]
            index = 0
            for m in range(1, len(dist)):
                if (min1 > dist[m] ):
                    min1 = dist[m]
                    index = m

            if min1 == 20000000:
                cars[i].available = 0
                cars[i].ticker = 20000000
                continue

            cars[i].number_of_trips_done += 1 # take the trip
            cars[i].available = 0 # assign car to the trip
            cars[i].trips.append(index) # adding the ride number to the trips for this car
            cars[i].current_x = rides[index].end_x # update car x location
            cars[i].current_y = rides[index].end_y # update car y location
            rides[index].possible = 0 # remove trip from the list
            cars[i].ticker = rides[index].trip_duration + min1  # set the time when the car will be available
            taken += 1

    if (taken == N):
        break

    # check the cars availability and make cars available if it is time
    for i in range(F):
        if cars[i].ticker == global_turn_id:
            cars[i].available = 1

    global_turn_id += 1

s = cars

f = open("e_high_bonus.txt", "w")
for car in range(len(cars)):
    f.write(str(cars[car].number_of_trips_done) + " ")
    for i in range(len(cars[car].trips)):
        f.write(str(cars[car].trips[i]) + " ")

    f.write("\n")

f.close()