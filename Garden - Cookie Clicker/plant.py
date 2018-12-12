class Plant:
    def __init__(self, name, mat, life, cps_cost, min_cost, code="PNT"):
        self.name = name
        self.mat = mat
        self.life = life
        self.cps_cost = cps_cost
        self.min_cost = min_cost
        self.mat_age = life-mat
        self.muts = []
        self.code = code

    def __eq__(self, plant):
        return (self.compare_maturity(plant) == 0 and self.compare_lifespan(plant) == 0 and self.compare_maturation_age(plant) == 0)

    @staticmethod
    def compare(var1, var2):
        if var1 == var2: return 0
        elif var1 < var2: return -1
        else : return 1

    def compare_maturity(self, other):
        return self.compare(self.mat, other.mat)

    def compare_lifespan(self, other):
        return self.compare(self.life, other.life)

    def compare_maturation_age(self, other):
        return self.compare(self.mat_age, other.mat_age)

    def created_from(self, mutation):
        self.muts += [mutation]

    def print_details(self):
        print("%s" % (self.name))
        print("Matures in %d ticks" % (self.mat))
        print("Dies in %d ticks" % (self.life))
        print("Stays mature for %d\n" % (self.mat_age))

        self.print_mutations()

    def print_mutations(self):
        print("{:-^70}".format(" Mutated from "))

        if self.muts is []:
            print("[No mutations registered]")

        for x in range(0, len(self.muts)):
            print("%s" % (self.muts[x]))
            if(x < len(self.muts)-1):
                print()

        print("{:-^70}".format(""))

    def get_cost(self, cps):
        total_cost = cps * self.cps_cost * 60
        return self.min_cost if total_cost < self.min_cost else total_cost

    # Utilises all constraints and features of Conditions
    # to find whether the exact list can mutate this plant
    def mutates_from(self, ingredients):
        for mut in self.muts:
            if mut.match_ingredients(ingredients) is True:
                return mut
        return False

    # Very general function to see whether this plant
    # can be mutated given the following list of availiable plants
    def achievable_by(self, plants):
        missing = []
        for mut in self.muts:
            achieved = mut.achievable_by(plants)
            if achieved is True:
                return (mut, True)
            else:
                missing += [achieved]
        return (missing, False)
