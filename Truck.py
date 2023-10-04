# Truck class with default values provided by "assessment assumptions"
#    default values 16 package capacity, 18 mph speed, starting address at hub

class Truck:
    def __init__(self, load, packages, mileage, depart_time, name):
        self.capacity = 16
        self.speed = 18
        self.load = load
        self.packages = packages
        self.mileage = mileage
        self.address = "4001 South 700 East"
        self.depart_time = depart_time
        self.time = depart_time
        self.name = name
