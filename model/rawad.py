class RawAd:
    def __init__(self):
        self.price = None
        self.model = None
        self.release_year = None
        self.engine = None
        self.transmission = None
        self.mileage = None
        self.color = None
        self.body_type = None
        self.checkup = None
        self.city = None
        self.free_text = None

        self.secondary_features = list()

    def __str__(self):
        return str(self.__dict__)
