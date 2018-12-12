
def calculate_total_chance(wc, p1, p2, empty, mut):
    modifier = 3 if wc.lower() == "y" else 1

    max_ticks = 0
    instant = 0
    diff_matu_ticks = 0
    plant_earlier = None

    if p1 == p2 :
        max_ticks = p1.mat_age
        instant = max_ticks
        diff_matu_ticks = 0
    else:
        diff_matu_ticks = abs(p1.mat - p2.mat)
        quick_grower = "P1" if p1.compare_maturity(p2) < 0 else "P2"
        early_death = "P1" if p1.compare_lifespan(p2) < 0 else "P2"
        max_ticks = p1.mat_age if p1.compare_maturation_age(p2) <= 0 else p2.mat_age

        if quick_grower == early_death:
            if quick_grower == "P1":
                instant = p1.mat_age - (p2.mat - p1.mat)
                plant_earlier = p2
            else:
                instant = p2.mat_age - (p1.mat - p2.mat)
                plant_earlier = p1
        else:
            instant = max_ticks

    max_chance = modifier * mut * empty * max_ticks
    ins_chance = modifier * mut * empty * instant if instant > 0 else 0

    print("\n---------------------------------------------------------------------")
    print("Maximum chance = %.3f" % (max_chance))
    print("Maximum chance (if planted instantly) = %.3f" % (ins_chance))
    print("\nChance lost by being planted instantly = %.3f" % (max_chance - ins_chance))
    if(ins_chance != max_chance):
        print("In order to achieve maximum chance, plant %s %d ticks earlier." % (plant_earlier.name, diff_matu_ticks))
    print("---------------------------------------------------------------------")

class Plant:
    def __init__(self, name, mat, life):
        self.name = name
        self.mat = mat
        self.muts = []
        self.life = life
        self.mat_age = life-mat

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
        print("{:-^40}".format(" Mutated from "))

        if self.muts is []:
            print("[No mutations registered]")

        for x in range(0, len(self.muts)):
            print("%s" % (self.muts[x]))
            if(x < len(self.muts)-1):
                print()

        print("{:-^40}".format(""))

class Garden:
    def __init__(self):
        self.garden = {}

        plants = [
            ["Baker's Wheat", 5, 13],
            ["Thumbcorn", 3, 15],
            ["Cronerice", 74, 134],
            ["Gildmillet", 15, 37],
            ["Clover", 20, 58],
            ["Golden Clover", 5, 10],
            ["Shimmerlily", 9, 13],
            ["Elderwort", 164, 9999],
            ["Bakeberry", 34, 67],
            ["Chocoroot", 7, 25],
            ["White Chocoroot", 7, 25],
            ["Meddleweed", 4, 8],
            ["Whiskerbloom", 20, 34],
            ["Chimerose", 18, 58],
            ["Nursetulip", 40, 64],
            ["Drowsyfern", 300, 1000],
            ["Wardlichen", 10, 15],
            ["Keenmoss", 10, 16],
            ["Queenbeet", 67, 84],
            ["Juicy Queenbeet", 1063, 1250],
            ["Duketater", 212, 223],
            ["Shriekbulb", 18, 29],
            ["Tidygrass", 80, 200],
            ["Everdaisy", 250, 9999],
            ["White Mildew", 5, 8],
            ["Brown Mold", 5, 8],
            ["Crumbspore", 15, 23],
            ["Doughshroom", 43, 50],
            ["Glovemorel", 7, 9],
            ["Cheapcap", 3, 8],
            ["Fool Bolete", 3, 6],
            ["Wrinklegill", 26, 40],
            ["Green Rot", 4, 6],
            ["Ichorpuff", 20, 58]
        ]

        for x in plants:
            self.garden[x[0].lower()] = Plant(x[0], x[1], x[2])

    def get_plant(self, name):
        return self.garden[name.lower()]

    def include_mutations(self):
        g = self.garden

        mutations = [
                ["Baker's Wheat", 
                    [["Baker's Wheat!2"], 0.2],
                    [["Thumbcorn!2"], 0.05]
                ],
                ["Thumbcorn",
                    [["Baker's Wheat!2"], 0.05],
                    [["Thumbcorn!2"], 0.1],
                    [["Cronerice!2"], 0.02]
                ],
                ["Cronerice",
                    [["Baker's Wheat", "Thumbcorn"], 0.01]
                ],
                ["Bakeberry",
                    [["Baker's Wheat!2"], 0.001]
                ],
                ["Gildmillet",
                    [["Cronerice", "Thumbcorn"], 0.03]
                ],
                ["Clover",
                    [["Baker's Wheat", "Gildmillet"], 0.03],
                    [["Clover!2", "Clover!<5@Any"], 0.007]
                ],
                ["Golden Clover",
                    [["Baker's Wheat", "Gildmillet"], 0.0007],
                    [["Clover!2-4"], 0.0001],
                    [["Clover!4"], 0.0007]
                ],
                ["Shimmerlily",
                    [["Clover", "Gildmillet"], 0.02]
                ],
                ["Elderwort",
                    [["Shimmerlily", "Cronerice"], 0.01],
                    [["Wrinklegill", "Cronerice"], 0.002]
                ],
                ["Chocoroot",
                    [["Baker's Wheat", "Brown Mold@Any"], 0.1]
                ],
                ["White Chocoroot",
                    [["Chocoroot", "White Mildew@Any"], 0.1]
                ],
                ["Brown Mold",
                    [["White Mildew", "Brown Mold!<2@Any"], 0.5]
                ],
                ["White Mildew",
                    [["Brown Mold", "White Mildew!<2@Any"], 0.5]
                ],
                ["Meddleweed",
                    [["Meddleweed!1", "Meddleweed!<3@Any"], 0.15]
                ],
                ["Nursetulip",
                    [["Whiskerbloom!2"], 0.05]
                ],
                ["Whiskerbloom",
                    [["Shimmerlily", "White Chocoroot"], 0.01]
                ],
                ["Chimerose",
                    [["Shimmerlily", "Whiskerbloom"], 0.05],
                    [["Chimerose!2"], 0.005]
                ],
                ["Drowsyfern",
                    [["Chocoroot", "Keenmoss"], 0.005]
                ],
                ["Wardlichen",
                    [["Cronerice", "Keenmoss"], 0.005],
                    [["Cronerice", "White Mildew"], 0.005],
                    [["Wardlichen!!1"], 0.05]
                ],
                ["Keenmoss",
                    [["Green Rot", "Brown Mold"], 0.1],
                    [["Keenmoss!!1"], 0.05]
                ],
                ["Queenbeet",
                    [["Bakeberry", "Chocoroot"], 0.01]
                ],
                ["Juicy Queenbeet",
                    [["Queenbeet!8"], 0.001]
                ],
                ["Duketater",
                    [["Queenbeet!2"], 0.001]
                ],
                ["Crumbspore",
                    [["Crumbspore!!1"], 0.07],
                    [["Doughshroom!2"], 0.005]
                ],
                ["Glovemorel",
                    [["Crumbspore", "Thumbcorn"], 0.01]
                ],
                ["Cheapcap",
                    [["Crumbspore", "Shimmerlily"], 0.03]
                ],
                ["Fool Bolete",
                    [["Doughshroom", "Green Rot"], 0.02]
                ],
                ["Doughshroom",
                    [["Crumbspore!2"], 0.005],
                    [["Doughshroom!!1"], 0.07]
                ],
                ["Wrinklegill",
                    [["Crumbspore", "Brown Mold"], 0.06]
                ],
                ["Green Rot",
                    [["White Mildew", "Clover"], 0.05]
                ],
                ["Shriekbulb",
                    [["Wrinklegill", "Elderwort"], 0.001],
                    [["Elderwort!5"], 0.001],
                    [["Duketater!3@Any"], 0.005],
                    [["Doughshroom!4@Any"], 0.002],
                    [["Queenbeet!5"], 0.001],
                    [["Shriekbulb!!1"], 0.005]
                ],
                ["Tidygrass",
                    [["Baker's Wheat", "White Chocoroot"], 0.002]
                ],
                ["Everdaisy",
                    [["Tidygrass!3", "Elderwort!3"], 0.002]
                ],
                ["Ichorpuff",
                    [["Elderwort", "Crumbspore"], 0.002]
                ]
            ]

        for mutation in mutations:
            mutated = mutation[0]
            ingredients = mutation[1:]

            for ing in ingredients:
                g[mutated.lower()].created_from(Mutation(self, ing[0], ing[1]))

class Mutation:
    def __init__(self, garden, plants, mut_rate):
        self.mut_rate = mut_rate
        self.conditions = []

        for x in plants:
            if "!" in x and "!!" not in x:
                xsplit = x.split("!")

                plant = garden.get_plant(xsplit[0])
                quantity = xsplit[1]
                status = None
                lessT = None

                if "@" in quantity:
                    flags = quantity.split("@")
                    quantity = flags[0]
                    status = flags[1]

                if "<" in quantity:
                    lessT = True
                
                self.conditions += [self.Condition(plant, quantity, status, lessT)]
            
            elif "!!" in x:
                xsplit = x.split("!!")

                plant = garden.get_plant(xsplit[0])
                quantity = xsplit[1]

                self.conditions += [self.Condition(plant, quantity, exactT = True)]

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

    class Condition:
        def __init__(self, plant, quantity = 1, status = "M", lessT = False, exactT = False):
            self.plant = plant
            self.quantity = quantity
            self.status = status
            self.exactF = False
            self.lessT = False

        def __repr__(self):
            status_str = ""

            if self.status == "M":
                status_str = "Mature "
            elif self.status == "Any":
                status_str = "Any "

            if self.exactF is False and self.lessT is False:
                return "%s or more of %s%s" % (self.quantity, status_str, self.plant.name)
            elif self.exactF is True:
                return "Exactly %s of %s%s" % (self.quantity, status_str, self.plant.name)
            elif self.lessT is True:
                return "Less than %s of %s%s" % (self.quantity, status_str, self.plant.name)

def basic_garden(garden):
    wood_chips = input("Are you using wood chip? (Y for yes, N for no) : ")

    inp1 = input("Enter Plant 1's name : ")
    inp2 = input("Enter Plant 2's name : ")

    p1 = garden.get_plant(inp1)
    p2 = garden.get_plant(inp2)

    empty_spaces = int(input("How many empty spaces are there? : "))
    mutation_rate = float(input("Chance of mutation : "))

    calculate_total_chance(wood_chips, p1, p2, empty_spaces, mutation_rate)

def get_mutations(garden):
    name = input("Which plant do you want to get? : ")
    plant = garden.get_plant(name)
    plant.print_mutations()

if __name__ == "__main__":
    garden = Garden()
    garden.include_mutations()

    print("Pick a choice!")
    print("\t1. Calculate mutation possibility")
    print("\t2. Find out how to get plant")
    choice = int(input("Choice : "))

    if choice == 1:
        basic_garden(garden)
    elif choice == 2:
        get_mutations(garden)