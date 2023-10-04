# package class with values required by assessment
class Package:
    def __init__(self, id, address, city, state, zipcode, deadline, weight, status, truck):
        self.id = id
        self.address = address
        self.city = city
        self.state = state
        self.zipcode = zipcode
        self.deadline = deadline
        self.weight = weight
        self.status = status
        self.departure_time = None
        self.delivery_time = None
        self.truck = truck

    # Returns package information and status
    def __str__(self):
        return 'Package %s: %s, %s, %s, %s, %s, %s, %s, %s, on %s' % (
            self.id, self.address, self.city, self.state, self.zipcode,
            self.deadline, self.weight, self.delivery_time,
            self.status, self.truck)

    # Updates current location of package
    def update_status(self, input_time):
        self.status = "At the hub"
        if self.delivery_time > input_time > self.departure_time:
            self.status = "En route"
        if self.delivery_time < input_time:
            self.status = "Delivered"
