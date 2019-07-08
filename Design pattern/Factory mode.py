class Store(object):

    # factory model
    def select_car(self):
        pass
    def order(self, car_type):
        return self.select_car(car_type)


class BMWCarStore(Store):

    # # simple factory model
    # def __init__(self):
    #     self.factory = BMWFactory()

    def select_car(self,car_type):
        return self.factory.select_car_by_type(car_type)

# uncoupling the store and car

class BMWFactory (object):
    def select_car_by_type(self,car_type):
        if car_type=="MINI":
            return MINI()


class Car(object):
    def move(self):
        print("moving")

class MINI(Car):
    pass


bmw_store = BMWCarStore()
bmw = bmw_store.order("MINI")
bmw.move()