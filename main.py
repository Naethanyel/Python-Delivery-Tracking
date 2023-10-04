# Naethanyel Nowakowski - ID: 011270595

import csv
import datetime
import Truck
import HashTable
import Package

# Read CSV files
with open("distances.csv") as distance_file:
    distance_list = list(csv.reader(distance_file))

with open("addresses.csv") as address_file:
    address_list = list(csv.reader(address_file))


# Create package and load objects from the package file into the hash table
def load_package_data(filename, packages):
    with open(filename) as package_info:
        package_data = csv.reader(package_info)
        for package in package_data:
            id = int(package[0])
            address = package[1]
            city = package[2]
            state = package[3]
            zipcode = package[4]
            deadline = package[5]
            weight = package[6]
            status = "At Hub"
            truck = ""
            package_info = Package.Package(id, address, city, state, zipcode, deadline, weight, status, truck)
            packages.insert(id, package_info)


# find distance between two locations
def find_distance(x_value, y_value):
    distance = distance_list[x_value][y_value]
    if distance == '':
        distance = distance_list[y_value][x_value]
    return float(distance)


# get address number from string of address
def get_address(address):
    for row in address_list:
        if address in row[2]:
            return int(row[0])


def ship_packages(truck, hash_table):
    to_deliver = []

    # finds package object based on package id in truck
    for package_id in truck.packages:
        package = hash_table.lookup(package_id)
        to_deliver.append(package)

    # Delivers packages from "to_deliver" until "to_deliver" is empty
    while to_deliver:
        next_address_distance = 100
        next_package = None
        
        # Orders packages to be delivered using nearest neighbor algorithm
        for package in to_deliver:
            if find_distance(get_address(truck.address), get_address(package.address)) <= next_address_distance:
                next_address_distance = find_distance(get_address(truck.address), get_address(package.address))
                next_package = package
                
                # updates package to show what truck it is on
                package.truck = truck.name

        truck.packages.append(next_package.id)
        to_deliver.remove(next_package)

        # update truck mileage, distance, and time
        truck.mileage += next_address_distance
        truck.address = next_package.address
        truck.time += datetime.timedelta(hours=next_address_distance / truck.speed)

        # update package time
        next_package.delivery_time = truck.time
        next_package.departure_time = truck.depart_time


class Main:
    # create hash table and load with package data
    packages = HashTable.HashTable()
    load_package_data("packages.csv", packages)

    # load truck1 with packages that have early deadlines or need shipped together
    truck1 = Truck.Truck(None, [1, 13, 14, 15, 16, 19, 20, 29, 30, 31, 34, 37, 40],
                         0.0, datetime.timedelta(hours=8), "Truck1")

    # load truck2 with packages that must be on truck 2, wait until correct address given for package 9
    truck2 = Truck.Truck(None, [3, 12, 17, 18, 21, 22, 23, 24, 26, 27, 35, 36, 38, 39],
                         0.0, datetime.timedelta(hours=10, minutes=20), "Truck2")

    ship_packages(truck1, packages)
    ship_packages(truck2, packages)

    # get distance between last stop for truck1 and the hub to calculate return
    # mileage and return time
    returnMileage = find_distance(0, 18)
    truck1.mileage += returnMileage
    truck1.time += datetime.timedelta(hours=returnMileage / truck1.speed)

    # load truck3 with late packages and early deadlines, ship when driver one has returned to hub
    truck3 = Truck.Truck(None, [2, 4, 5, 6, 7, 8, 9, 10, 11, 25, 28, 32, 33],
                         0.0, datetime.timedelta(hours=9, minutes=40), "truck3")

    # ship truck 3 when driver one has returned to hub
    ship_packages(truck3, packages)

    # present user with  text interface
    print("Welcome to the routing application \n")
    print("Truck1 drove " + str(round(truck1.mileage, 1)) + " miles")
    print("Truck2 drove " + str(truck2.mileage) + " miles")
    print("Truck3 drove " + str(truck3.mileage) + " miles")
    print("Total route mileage: " + str(truck1.mileage + truck2.mileage + truck3.mileage))
    print("Driver 1 finished Truck1 route and returned Truck1 to hub at " + str(truck1.time))
    print("Driver 2 finished Truck2 route at " + str(truck2.time))
    print("Driver 1 finished Truck3 route at " + str(truck3.time) + "\n")

    # options always available until user exits with "exit"
    while True:
        menu = """To perform an action type the number of the action. Or type \"exit\" to close the program
           1) Check status of all packages at a given time
           2) Check Status of one package at a given time
           """
        print(menu)

        text = input()

        if text == "exit":
            exit()

        if text == "1":
            print("Enter a time in 24 hour format. For example, to see 8:00AM type \"08:00\" with a leading zero"
                  " or to see 1:45PM type \"13:45\"\n")

            # format user input to convert time for package time
            (h, m) = input().split(":")
            input_time = datetime.timedelta(hours=int(h), minutes=int(m))

            for package_id in range(1, 41):
                package = packages.lookup(package_id)
                package.update_status(input_time)
                print(str(package))

            print("\n")

        if text == "2":
            package_id = input("Enter the ID number of the package\n")
            print("Enter a time in 24 hour format. For example, to see 8:00AM type \"08:00\" with a leading zero"
                  " or to see 1:45PM type \"13:45\"\n")

            # format user input to convert time for package time
            (h, m) = input().split(":")
            input_time = datetime.timedelta(hours=int(h), minutes=int(m))
            package = packages.lookup(int(package_id))
            package.update_status(input_time)
            print(str(package))
