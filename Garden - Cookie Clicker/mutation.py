class Plant:
    def __init__(self, name, mat, life, cps_cost, min_cost):
        self.name = name
        self.mat = mat
        self.life = life
        self.cps_cost = cps_cost
        self.min_cost = min_cost
        self.mat_age = life-mat
        self.muts = []

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

    def get_cost(self, cps):
        total_cost = cps * self.cps_cost * 60
        return self.min_cost if total_cost < self.min_cost else total_cost

    def mutates_from(self, ingredients):
        for mut in self.muts:
            if mut.match_ingredients(ingredients) is True:
                return mut
        return False

class Grid:
    def __init__(self, x, y, elem=None):
        self.dimensions = (x,y)
        self.area = x*y

        self.grid = [[elem for x1 in range(x)] for y1 in range(y)]

    def set(self, x, y, elem):
        self.grid[y][x] = elem

    def get(self, x, y, elem):
        return self.grid[y][x]

    def __repr__(self):
        string = ""

        for horizarr in self.grid:
            string += "[" + " , ".join(horizarr) + "]\n"

        return string

class Garden:
    def __init__(self, level=None, dimensions=None):
        self.garden = {}

        level_grid_dict = {
            1 : (2,2),
            2 : (3,2),
            3 : (3,3),
            4 : (4,3),
            5 : (4,4),
            6 : (5,4),
            7 : (5,5),
            8 : (6,5),
            9 : (6,6)
        }

        if level is not None and dimensions is None:
            dimensions = level_grid_dict[level]
        elif (level is None and dimensions is None) or (level is not None and dimensions is not None):
            raise RuntimeError("Level OR dimensions required! Not both, not neither!")
        
        self.plots = Grid(dimensions[0], dimensions[1], "-")

        plants = [
            ["Baker's Wheat", 5, 13, 1, 30],
            ["Thumbcorn", 3, 15, 5, 100],
            ["Cronerice", 74, 134, 15, 250],
            ["Gildmillet", 15, 37, 15, 1500],
            ["Clover", 20, 58, 25, 77777],
            ["Golden Clover", 5, 10, 125, 777777777],
            ["Shimmerlily", 9, 13, 60, 777777],
            ["Elderwort", 164, 9999, 180, 100 * 10**6],
            ["Bakeberry", 34, 67, 45, 100 * 10**6],
            ["Chocoroot", 7, 25, 15, 100 * 10**3],
            ["White Chocoroot", 7, 25, 15, 100 * 10**3],
            ["Meddleweed", 4, 8, 1, 10],
            ["Whiskerbloom", 20, 34, 20, 1 * 10**6],
            ["Chimerose", 18, 58, 15, 242424],
            ["Nursetulip", 40, 64, 40, 1 * 10**9],
            ["Drowsyfern", 300, 1000, 90, 100 * 10**3],
            ["Wardlichen", 10, 15, 10, 10000],
            ["Keenmoss", 10, 16, 50, 1 * 10**6],
            ["Queenbeet", 67, 84, 90, 1 * 10**9],
            ["Juicy Queenbeet", 1063, 1250, -1, -1],
            ["Duketater", 212, 223, 480, 1 * 10**12],
            ["Shriekbulb", 18, 29, 60, 4.444 * 10**12],
            ["Tidygrass", 80, 200, 90, 100 * 10**12],
            ["Everdaisy", 250, 9999, 180, 100 * 10**18],
            ["White Mildew", 5, 8, 20, 9999],
            ["Brown Mold", 5, 8, 20, 9999],
            ["Crumbspore", 15, 23, 10, 999],
            ["Doughshroom", 43, 50, 100, 100 * 10**6],
            ["Glovemorel", 7, 9, 30, 10000],
            ["Cheapcap", 3, 8, 40, 100000],
            ["Fool Bolete", 3, 6, 15, 10000],
            ["Wrinklegill", 26, 40, 20, 1 * 10**6],
            ["Green Rot", 4, 6, 60, 1 * 10**6],
            ["Ichorpuff", 20, 58, 120, 987654321]
        ]

        for x in plants:
            self.garden[x[0].lower()] = Plant(x[0], x[1], x[2], x[3], x[4])

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

    def best_layout(self, dual=False):
        best_by_dimensions = {
            (2,2) : [(0,0), (1,1)],
            (3,2) : [(1,0), (1,1)],
            (3,3) : [(0,1), (1,1), (2,1)],
            (4,3) : [(0,1), (1,1), (2,1), (3,1)],
            (4,4) : [(0,0), (3,3), (0,3), (3,0), (1,2), (2,1)],
            (5,4) : [(0,0), (2,0), (4,0), (0,2), (1,2), (3,2), (4,2)],
            (5,5) : [(0,0), (1,0), (3,0), (4,0), (0,3), (1,3), (3,3), (4,3)],
            (6,5) : [(1,0), (1,1), (1,3), (1,4), (4,0), (4,1), (4,3), (4,4)],
            (6,6) : [(0,1), (1,1), (3,1), (4,1), (5,1), (0,4), (1,4), (2,4), (4,4), (5,4)]
        }

        dims = self.plots.dimensions
        points = best_by_dimensions[dims]

        plots = Grid(dims[0], dims[1], "-")

        for (x,y) in points:
            plots.set(x,y, "P")

        return {"plot" : plots, "empty" : self.plots.area - len(best_by_dimensions[dims])}

    def get_mutations_by_ingredients(self, ingredients):
        mutations = []
        for _,v in self.garden.items():
            mut = v.mutates_from(ingredients)
            if mut is not False:
                mutations += [(v,mut)]
    
        return mutations

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

    class Condition:
        def __init__(self, plant, quantity = 1, status = "M", lessT = False, exact = False, to = -1):
            self.plant = plant
            self.quantity = int(quantity)
            self.status = status
            self.exact = exact
            self.lessT = lessT
            self.to = -1 if to <= quantity else to

        def __repr__(self):
            status_str = ""

            if self.status == "M":
                status_str = "Mature "
            elif self.status == "Any":
                status_str = "Any "

            if self.exact is False and self.lessT is False:
                return "%s or more of %s%s" % (self.quantity, status_str, self.plant.name)
            elif self.exact is True:
                return "Exactly %s of %s%s" % (self.quantity, status_str, self.plant.name)
            elif self.lessT is True:
                return "Less than %s of %s%s" % (self.quantity, status_str, self.plant.name)

def basic_garden(garden):
    wood_chips = input("Are you using wood chip? (Y for yes, N for no) : ")

    inp1 = input("Enter Plant 1's name : ")
    inp2 = input("Enter Plant 2's name : ")

    p1 = garden.get_plant(inp1)
    p2 = garden.get_plant(inp2)

    mutps = garden.get_mutations_by_ingredients([p1,p2])

    print("Possible mutations:\n\t- {}".format("\t- ".join(p[0].name + "\n" for p in mutps)))

    chosen_mut = None

    if len(mutps) == 0:
        print("ERROR - No mutations found.")
    elif len(mutps) == 1:
        chosen_mut = mutps[0]
    else:
        chosen_mut = mutps[int(input("Enter the index (1-{}) of the mutation you'd like : ".format(len(mutps))))-1]

    empty_spaces = garden.best_layout()["empty"]
    mutation_rate = chosen_mut[1].mut_rate

    calculate_total_chance(wood_chips, p1, p2, empty_spaces, mutation_rate)

def get_mutations(garden):
    name = input("Which plant do you want to get? : ")
    plant = garden.get_plant(name)
    plant.print_mutations()

def get_best_layout(garden):
    dual = input("Different plants (Y) or same plant (N)? : ")
    print(garden.best_layout(True if dual == "Y" else False)[0])

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


if __name__ == "__main__":
    garden = None

    g_size = input("Enter the level (1..9+) or dimensions (2x2...) of your garden : ")
    if "x" in g_size:
        spl = g_size.split("x")
        garden = Garden(dimensions=(int(spl[0]), int(spl[1])))
    else:
        garden = Garden(level=int(g_size))

    garden.include_mutations()

    print("Pick a choice!")
    print("\t1. Calculate mutation possibility")
    print("\t2. Find out how to get plant")
    print("\t3. Get best layout")
    choice = int(input("Choice : "))

    if choice == 1:
        basic_garden(garden)
    elif choice == 2:
        get_mutations(garden)
    elif choice == 3:
        get_best_layout(garden)