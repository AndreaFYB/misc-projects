from plant import Plant

class Mutation:
    def __init__(self, garden, plants, mut_rate):
        self.mut_rate = mut_rate
        self.conditions = []

        for x in plants:
            if "!" in x and "!!" not in x:
                xsplit = x.split("!")

                plant = garden.get_plant(xsplit[0])
                quantity = xsplit[1]
                status = False
                lessT = False

                if "@" in quantity:
                    flags = quantity.split("@")
                    quantity = flags[0]
                    status = flags[1]

                if "<" in quantity:
                    lessT = True
                    quantity = quantity.split("<")[1]

                if "-" in quantity:
                    rangeQ = quantity.split("-")
                    self.conditions += [self.Condition(plant, rangeQ[0], status, lessT, to=rangeQ[1])]
                    continue
                
                self.conditions += [self.Condition(plant, quantity, status, lessT)]
            
            elif "!!" in x:
                xsplit = x.split("!!")

                plant = garden.get_plant(xsplit[0])
                quantity = xsplit[1]

                self.conditions += [self.Condition(plant, quantity, exact = True)]

            elif "@" in x:
                xsplit = x.split("@")

                plant = garden.get_plant(xsplit[0])

                self.conditions += [self.Condition(plant, status = xsplit[1])]

            else:
                self.conditions += [self.Condition(garden.get_plant(x))]

    def __repr__(self):
        string = ""

        string += "Mutation rate = %.4lf" % (self.mut_rate)

        for con in self.conditions:
            string += "\n%s" % (con)

        return string

    def match_ingredients(self, ingredients):
        ingnames = [p.name for p in ingredients]
        plant_types = list(set(ingnames))
        count = {}

        for ptype in plant_types:
            count[ptype] = ingnames.count(ptype)

        for con in self.conditions:
            if con.plant.name not in count: return False
            if con.lessT:
                if count[con.plant.name] >= con.quantity: return False
            elif con.exact:
                if count[con.plant.name] != con.quantity: return False
            else:
                if count[con.plant.name] < con.quantity: return False

        return True

    def achievable_by(self, plants):
        required_plants = [con.plant for con in self.conditions]
        for plant in required_plants:
            if plant not in plants : return plant.name
        return True

    class Condition:
        def __init__(self, plant, quantity = 1, status = "M", lessT = False, exact = False, to = -1):
            self.plant = plant
            self.quantity = int(quantity)
            self.status = status
            self.exact = exact
            self.lessT = lessT
            self.to = -1 if int(to) <= int(quantity) else int(to)

        def __repr__(self):
            status_str = ""

            if self.status == "M":
                status_str = "Mature "
            elif self.status == "Any":
                status_str = "Any "

            if self.exact is False and self.lessT is False and self.to == -1:
                return "%s or more of %s%s" % (self.quantity, status_str, self.plant.name)
            elif self.exact is True:
                return "Exactly %s of %s%s" % (self.quantity, status_str, self.plant.name)
            elif self.lessT is True:
                return "Less than %s of %s%s" % (self.quantity, status_str, self.plant.name)
            elif self.to > -1:
                return "Between %s and %s of %s%s" % (self.quantity, self.to, status_str, self.plant.name)
