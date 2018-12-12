import time

# classes
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
        
        self.level = (dimensions[0]-2)+(dimensions[1]-2)+1
        self.plots = Grid(dimensions[0], dimensions[1], "-")

        plants = [
            ["Baker's Wheat", 5, 13, 1, 30, "Bak"],
            ["Thumbcorn", 3, 15, 5, 100, "Thu"],
            ["Cronerice", 74, 134, 15, 250, "Cro"],
            ["Gildmillet", 15, 37, 15, 1500, "Gil"],
            ["Clover", 20, 58, 25, 77777, "Clo"],
            ["Golden Clover", 5, 10, 125, 777777777, "GCl"],
            ["Shimmerlily", 9, 13, 60, 777777, "Shi"],
            ["Elderwort", 164, 9999, 180, 100 * 10**6, "Eld"],
            ["Bakeberry", 34, 67, 45, 100 * 10**6, "Bkb"],
            ["Chocoroot", 7, 25, 15, 100 * 10**3, "Cho"],
            ["White Chocoroot", 7, 25, 15, 100 * 10**3, "WCh"],
            ["Meddleweed", 4, 8, 1, 10, "Med"],
            ["Whiskerbloom", 20, 34, 20, 1 * 10**6, "Whi"],
            ["Chimerose", 18, 58, 15, 242424, "Chi"],
            ["Nursetulip", 40, 64, 40, 1 * 10**9, "Nur"],
            ["Drowsyfern", 300, 1000, 90, 100 * 10**3, "Dro"],
            ["Wardlichen", 10, 15, 10, 10000, "War"],
            ["Keenmoss", 10, 16, 50, 1 * 10**6, "Kee"],
            ["Queenbeet", 67, 84, 90, 1 * 10**9, "Qbt"],
            ["Juicy Queenbeet", 1063, 1250, -1, -1, "JQB"],
            ["Duketater", 212, 223, 480, 1 * 10**12, "Duk"],
            ["Shriekbulb", 18, 29, 60, 4.444 * 10**12, "Shr"],
            ["Tidygrass", 80, 200, 90, 100 * 10**12, "Tid"],
            ["Everdaisy", 250, 9999, 180, 100 * 10**18, "Eve"],
            ["White Mildew", 5, 8, 20, 9999, "WhM"],
            ["Brown Mold", 5, 8, 20, 9999, "BrM"],
            ["Crumbspore", 15, 23, 10, 999, "Cru"],
            ["Doughshroom", 43, 50, 100, 100 * 10**6, "Dou"],
            ["Glovemorel", 7, 9, 30, 10000, "Glo"],
            ["Cheapcap", 3, 8, 40, 100000, "Che"],
            ["Fool Bolete", 3, 6, 15, 10000, "Foo"],
            ["Wrinklegill", 26, 40, 20, 1 * 10**6, "Wri"],
            ["Green Rot", 4, 6, 60, 1 * 10**6, "Gre"],
            ["Ichorpuff", 20, 58, 120, 987654321, "Ich"]
        ]

        for x in plants:
            self.garden[x[0].lower()] = Plant(x[0], x[1], x[2], x[3], x[4], x[5])

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

    def best_layout(self, p1, p2, cps):
        best_by_dimensions = {
            (2,2) : [(0,0,'a'), (1,1,'b')],
            (3,2) : [(1,0,'a'), (1,1,'b')],
            (3,3) : [(0,1,'a'), (1,1,'b'), (2,1,'a')],
            (4,3) : [(0,1,'a'), (1,1,'b'), (2,1,'a'), (3,1,'b')],
            (4,4) : [(0,0,'a'), (3,3,'a'), (0,3,'a'), (3,0,'a'), (1,2,'b'), (2,1,'b')],
            (5,4) : [(0,0,'a'), (3,0,'a'), (0,3,'a'), (3,3,'a'), (1,0,'b'), (4,0,'b'), (1,3,'b'), (4,3,'b')],
            (5,5) : [(0,0,'a'), (1,0,'b'), (3,0,'a'), (4,0,'b'), (0,3,'a'), (1,3,'b'), (3,3,'a'), (4,3,'b')],
            (6,5) : [(1,0,'a'), (1,1,'b'), (1,3,'a'), (1,4,'b'), (4,0,'a'), (4,1,'b'), (4,3,'a'), (4,4,'b')],
            (6,6) : [(0,1,'a'), (1,1,'b'), (3,1,'a'), (4,1,'b'), (5,1,'a'), (0,4,'a'), (1,4,'b'), (2,4,'a'), (4,4,'b'), (5,4,'a')]
        }

        unwanted_mutations = {
            (2,2) : [],
            (3,2) : [],
            (3,3) : [(1,0), (1,2)],
            (4,3) : [(1,0), (2,0), (1,2), (2,2)],
            (4,4) : [(1,2), (2,1)],
            (5,4) : [],
            (5,5) : [],
            (6,5) : [],
            (6,6) : [(4,0), (4,2), (1,3), (1,5)]
        }

        # p1 - even index, p2 - odd index

        dims = self.plots.dimensions
        points = best_by_dimensions[dims]
        points_X = unwanted_mutations[dims]

        plots = Grid(dims[0], dims[1], "---")

        cost = 0

        p1cost = p1.get_cost(cps)
        p2cost = p2.get_cost(cps)

        if(p1 == p2):
            for (x,y,_) in points:
                cost += p1cost
                plots.set(x,y, " P ")
        else:
            pcs = (p1.code, p2.code) if p1cost < p2cost else (p2.code, p1.code)
            for (x,y,z) in points:
                pc = None
                if z == "a":
                    pc = pcs[0]
                    cost += p1cost
                else:
                    pc = pcs[1]
                    cost += p2cost
                plots.set(x,y, pc)
            for (x,y) in points_X:
                plots.set(x,y, "-X-")

        return {
            "plot" : plots,
            "empty" : self.plots.area - len(points),
            "usable" : self.plots.area - len(points) - len(points_X),
            "unwanted" : len(points_X),
            "cost" : num_to_word(cost)
        }

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

# utils
def word_to_num(num, extension):
    extensions = [
        "million", "billion", "trillion", "quadrillion",
        "quintillion", "sextillion", "septillion",
        "octillion", "nonillion", "decillion",
        "undecillion", "duodecillion", "tredecillion",
        "quattordecillion", "quindecillion", "sexdecillion"
    ]

    ext_nums = [10 ** r for r in range(6, 52, 3)]

    word_num = dict(zip(extensions, ext_nums))

    return num * float(word_num[extension])

def num_to_word(num):
    extensions = [
        "million", "billion", "trillion", "quadrillion",
        "quintillion", "sextillion", "septillion",
        "octillion", "nonillion", "decillion",
        "undecillion", "duodecillion", "tredecillion",
        "quattordecillion", "quindecillion", "sexdecillion"
    ]

    t_num = num / (10 ** 6)
    i = 0

    if t_num < 1: return num
    
    while(t_num / 1000 >= 1 and i <= 15):
        t_num /= 1000
        i += 1

    return "{:.3f} {}".format(t_num, extensions[i])      

def calculate_total_chance(wc, p1, p2, empty, mut_rate, mut_name):
    modifier = 3 if wc.lower() == "y" else 1

    max_ticks = 0
    instant = 0
    diff_matu_ticks = 0
    plant_earlier = None
    plant_later = None

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
                plant_later = p1
            else:
                instant = p2.mat_age - (p1.mat - p2.mat)
                plant_earlier = p1
                plant_later = p2
        else:
            instant = max_ticks

    max_chance = modifier * mut_rate * empty * max_ticks
    ins_chance = modifier * mut_rate * empty * instant if instant > 0 else 0

    print("{:-^70}".format(" Mutating {} ".format(mut_name)))
    print("Maximum chance = %.3f" % (max_chance))
    print("Maximum chance (if planted instantly) = %.3f" % (ins_chance))
    print("\nChance lost by being planted instantly = %.3f" % (max_chance - ins_chance))
    if(ins_chance != max_chance):
        print("In order to achieve maximum chance, plant %s %d ticks earlier." % (plant_earlier.name, diff_matu_ticks))

        print("In other words, plant %s at:" % (plant_later.name))
        print("\t{:15s} : {}".format("(Fertiliser)", get_time(3 * diff_matu_ticks * 60)))
        print("\t{:15s} : {}".format("(Clay)", get_time(15 * diff_matu_ticks * 60)))
        print("\t{:15s} : {}".format("(Other)", get_time(5 * diff_matu_ticks * 60)))
    print("{:-^70}".format(""))
    
def print_time(prompt, offset=0):
    print("{}{}".format(prompt, get_time(offset)))

def get_time(offset=0):
    ctime = time.localtime(time.time() + offset)

    return "{:02d}:{:02d}:{:02d} - {:02d}/{:02d} - {}".format(
        ctime.tm_hour, ctime.tm_min, ctime.tm_sec,
        ctime.tm_mday, ctime.tm_mon, ctime.tm_year)

# menu funcs
def basic_garden(garden, cps):
    wood_chips = input("Are you using wood chips? (Y for yes, N for no) : ")

    inp1 = input("Enter Plant 1's name : ")
    inp2 = input("Enter Plant 2's name : ")

    p1 = garden.get_plant(inp1)
    p2 = garden.get_plant(inp2)

    # Gets mutations that can result from inputted plants
    mutps = garden.get_mutations_by_ingredients([p1,p2])

    # Displays possible mutations
    print("Possible mutations:\n\t- {}".format("\t- ".join(p[0].name + "\n" for p in mutps)))

    chosen_mut = None

    # Either
    #   - Aborts if no mutations are found
    #   - Automatically continues if only one mutation is found
    #   - Pops up prompt so that user can select proper mutation
    if len(mutps) == 0:
        print("ERROR - No mutations found.")
        return
    elif len(mutps) == 1:
        chosen_mut = mutps[0]
    else:
        chosen_mut = mutps[int(input("Enter the index (1-{}) of the mutation you'd like : ".format(len(mutps))))-1]

    # Stores the best layout for the garden using plants p1 and p2.
    # Also has additional information about such a layout.
    bl = garden.best_layout(p1,p2,cps)

    # Usable spaces are spaces that are both empty, AND do not have a chance of an unwanted mutation.
    usable_spaces = bl["usable"]

    # Calculates (loosely) total chance of achieving mutation.
    calculate_total_chance(wood_chips, p1, p2, usable_spaces, chosen_mut[1].mut_rate, chosen_mut[0].name)

    # Displays the best layout to the user.
    print("Best layout (-X- means a possible unwanted mutation)\n{}".format(bl["plot"]))

    # Displays the total cost of such a layout
    print("Total cost : {}".format(bl["cost"]))

def auto_garden(garden, cps):
    wood_chips = input("Are you using wood chips? (Y/N) : ")

    pl_name = input("Enter the plant you want : ")

    pl1 = garden.get_plant(pl_name)

    # Shows the mutations that lead to the creation of this plant.
    pl1.print_mutations()

    chosen_mut = None

    # Either:
    #   - Aborts if no mutations are found
    #   - Automatically continues if only one mutation is found
    #   - Prompts user to select correct mutation
    if(len(pl1.muts) == 0):
        print("ERROR : No possible options were found.")
        print("Most likely a bug. Please contact the developer (me)")
        return
    elif(len(pl1.muts) == 1):
        chosen_mut = pl1.muts[0]
    else:
        mut_i = int(input("Select which mutation you'd like (1-{}) : ".format(len(pl1.muts))))
        chosen_mut = pl1.muts[mut_i-1]

    # The ridiculous naming is on purpose.
    # It's to show that this feature isn't 100% complete.
    # For example, for a Juicy Queenbeet, this won't work properly, due to its complex mutation.
    # This only works (accurately) for plants with 2 ingredients, either of the same plant, or different plants.
    b___plants = []

    for con in chosen_mut.conditions:
        b___plants += [con.plant]*con.quantity

    # It only selects the first two plants in the list.
    # In the future, the entire list should be made use of.
    # It will show the total list of ingredients required for the mutation.
    p1, p2 = b___plants[0], b___plants[1]

    bl = garden.best_layout(p1, p2, cps)
    usable = bl["usable"]

    calculate_total_chance(wood_chips, p1, p2, usable, chosen_mut.mut_rate, pl_name.title())
    print("Best layout (-X- means a possible unwanted mutation)\n{}".format(bl["plot"]))
    print("Total cost : {}".format(bl["cost"]))

def get_mutations(garden):
    name = input("Which plant do you want to get? : ")
    plant = garden.get_plant(name)
    plant.print_mutations()

# main
if __name__ == "__main__":
    # Used as clear
    print("\n"*100)

    garden = None

    # Displays current time
    print_time("Current time : ")

    # Accepts size of garden
    g_size = input("Enter the level (1..9+) or dimensions (2x2...) of your garden : ")

    # Accepts CPS note
    cps = input("Enter your CPS : ").split(" ")

    # Converts from word notation to number
    cps = word_to_num(float(cps[0]), cps[1])

    # Initialises Garden object
    if "x" in g_size:
        spl = g_size.split("x")
        garden = Garden(dimensions=(int(spl[0]), int(spl[1])))
    else:
        garden = Garden(level=int(g_size))

    # Includes mutations in garden
    garden.include_mutations()

    # Opens file for plant history
    # Creates list of achieved plants, and list of unachieved plants.
    plant_history = open("plants.grdn", "r+")
    received = [garden.get_plant(n) for n in plant_history.read().split("\n")[:-1]]
    remaining = [garden.get_plant(n) for n in
        list(set([p.name for _,p in garden.garden.items()]) -
            set([p.name for p in received]))
    ]

    while(True):
        # INFO header
        print("{:-^70}".format(" INFO "))

        print_time("Current time : ")
        print("CPS : {}".format(num_to_word(cps)))
        print("Garden Level : {}".format(garden.level))
        print("Garden Dimensions : {}".format(garden.plots.dimensions))

        # MENU header
        print("{:-^70}".format(" MENU "))

        print("Pick a choice!")
        print("\t    1. Calculate mutation possibility (by entering plants)")
        print("\t    2. Calculate mutation possibility (by selecting mutation)")
        print("\t    3. Find out how to get plant")
        print("\t    4. Find out what plants remain")
        print("\t    5. Add achieved plant!")
        print("\tOther. Quit")
        choice = int(input("Choice : "))

        if choice == 1:
            basic_garden(garden, cps)
            time.sleep(3)

        elif choice == 2:
            auto_garden(garden, cps)
            time.sleep(3)

        elif choice == 3:
            get_mutations(garden)
            time.sleep(3)

        elif choice == 4:
            for p in remaining:
                print("[{:^18}]".format(p.name))
                achievable = p.achievable_by(received)
                ach_string = "YES" if achievable[1] else "REQUIRED => " + ", ".join(achievable[0])
                print("\tAchievable? : {}".format(ach_string))
            time.sleep(3)

        elif choice == 5:
            plant_achieved = input("Enter name of plant : ")
            p = garden.get_plant(plant_achieved)
            plant_history.write(p.name + "\n")
            print("Saved plant!")
            time.sleep(2)

        else:
            break
#END