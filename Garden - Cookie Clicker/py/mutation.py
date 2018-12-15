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
    def __init__(self, filename, level=None, dimensions=None):
        self.garden = {}
        self.load(filename)

    def get_plant(self, name):
        return self.garden[name.lower()]

    def best_layout(self, p1, p2):
        best_by_dimensions = {
            (2,2) : [(0,0,'a'), (1,1,'b')],
            (3,2) : [(1,0,'a'), (1,1,'b')],
            (3,3) : [(0,1,'a'), (1,1,'b'), (2,1,'a')],
            (4,3) : [(0,1,'a'), (1,1,'b'), (2,1,'a'), (3,1,'b')],
            (4,4) : [(0,0,'a'), (3,3,'a'), (0,3,'a'), (3,0,'a'), (1,1,'b'), (2,2,'b')],
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

        p1cost = p1.get_cost(self.cps)
        p2cost = p2.get_cost(self.cps)

        if(p1 == p2):
            for (x,y,_) in points:
                cost += p1cost
                plots.set(x,y, p1.code)
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
    
    def save_all_to_file(self):
        # backup file
        backup = open("garden.bak", "w+")
        file = open("garden.dat", "r+")

        backup.write("{:-^70}\n".format(" " + get_time() + " "))
        backup.write(file.read())
        backup.write("{:-^70}\n".format(" BACKUP DONE "))

        file = open("garden.dat", "w+")

        #empty file
        file.truncate(0)

        # WRITING GARDEN STATUS
        file.write("<-{:-^70}->\n".format(" GARDEN STATUS "))
        file.write("LEVEL : {}\n".format(self.level))
        file.write("DIMENSIONS : {}x{}\n".format(self.plots.dimensions[0], self.plots.dimensions[1]))
        file.write("CPS : {}\n".format(num_to_word(self.cps)))

        # WRITING PLANT DATA
        file.write("<-{:-^70}->\n".format(" PLANT DATA "))

        plants = [p for _,p in self.garden.items()]

        # name, mat, life, cps_cost, min_cost, code="PNT"):

        for plant in plants:
            file.write("{:15} @@ {:5} @@ {:5} @@ {:7} @@ {:22d} @@ {:4}\n".format(
                plant.name, plant.mat, plant.life, plant.cps_cost, plant.min_cost, plant.code
            ))

        muts = [(p.name, mut) for p in plants for mut in p.muts]

        # WRITING MUTATION DATA
        file.write("<-{:-^70}->\n".format(" MUTATION DATA "))

        for mut in muts:
            file.write("{:15} : {}\n".format(mut[0], mut[1].mutation_to_notation()))

        # WRITING PLANT HISTORY
        file.write("<-{:-^70}->\n".format(" PLANT HISTORY "))

        for plant in self.history:
            file.write("{}\n".format(plant))

    def load(self, name):
        data = open(name, "r+")

        data = data.read().split("->\n")

        gar_data = data[1].split("\n<-")[0]
        pla_data = data[2].split("\n<-")[0]
        mut_data = data[3].split("\n<-")[0]
        his_data = data[4]

        # Preparing garden data
        garden_d = [s.split(" : ") for s in gar_data.split("\n")]
        self.level = garden_d[0][1]
        dimensions = garden_d[1][1].split("x")
        self.plots = Grid(int(dimensions[0]), int(dimensions[1]), "-")
        cps = garden_d[2][1].split(" ")
        self.cps = word_to_num(float(cps[0]), cps[1])

        plants = [n.split("@@") for n in pla_data.split("\n")]
        mutations = [m.split(":") for m in mut_data.split("\n")]
        history = his_data.split("\n")

        pl_clean = []
        mut_clean = []

        for entry in plants:
            line = [s.strip() for s in entry]
            pl_clean += [line]

        for entry in mutations:
            line = [s.strip() for s in entry]
            mut_clean += [line]

        plants = pl_clean
        mutations = mut_clean

        for x in plants:
            self.garden[x[0].lower()] = Plant(x[0], int(x[1]), int(x[2]), int(x[3]), int(x[4]), x[5])

        for mutation in mutations:
            mutated = mutation[0] # The plant the mutation results in
            mut_info = mutation[1].split(" ==> ")
            mut_rate = mut_info[0] # The rate of mutation
            mut_nots = mut_info[1].split(" && ") # The conditions

            self.garden[mutated.lower()].created_from(Mutation(self, mut_nots, mut_rate))

        self.history = history
        self.received = [self.get_plant(n) for n in history if n != ""]
        self.remaining = [self.get_plant(n) for n in
            list(set([p.name for _,p in self.garden.items()]) -
                set([p.name for p in self.received]))
        ]

class Mutation:
    def __init__(self, garden, plants, mut_rate):
        self.mut_rate = float(mut_rate)
        self.conditions = []

        for x in plants:
            if "!" in x and "!!" not in x:
                xsplit = x.split("!")

                plant = garden.get_plant(xsplit[0])
                quantity = xsplit[1]
                status = "M"
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
                status = "M"

                if "@" in quantity:
                    xsplit2 = quantity.split("@")
                    quantity = xsplit2[0]
                    status = xsplit2[1]

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

    def mutation_to_notation(self):
        string = "{} ==> ".format(self.mut_rate)
        notations = []
        for con in self.conditions:
            details = {
                "name" : con.plant.name,
                "quan" : con.quantity,
                "stat" : con.status,
                "to"   : con.to
            }
            template = ""
            if con.lessT is False and con.exact is False and con.to == -1:
                template = "{d[name]}!{d[quan]}@{d[stat]}"
            elif con.lessT is True:
                template = "{d[name]}!<{d[quan]}@{d[stat]}"
            elif con.exact is True:
                template = "{d[name]}!!{d[quan]}@{d[stat]}"
            elif con.to > 0:
                template = "{d[name]}!{d[quan]}-{d[to]}@{d[stat]}"
            notations += [template.format(d=details)]
        
        string += " && ".join(notations)
        return string


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
def basic_garden(garden):
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
    bl = garden.best_layout(p1,p2)

    # Usable spaces are spaces that are both empty, AND do not have a chance of an unwanted mutation.
    usable_spaces = bl["usable"]

    # Calculates (loosely) total chance of achieving mutation.
    calculate_total_chance(wood_chips, p1, p2, usable_spaces, chosen_mut[1].mut_rate, chosen_mut[0].name)

    # Displays the best layout to the user.
    print("Best layout (-X- means a possible unwanted mutation)\n{}".format(bl["plot"]))

    # Displays the total cost of such a layout
    print("Total cost : {}".format(bl["cost"]))

def auto_garden(garden):
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

    bl = garden.best_layout(p1, p2)
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

    # Loading info from data file
    garden = Garden("garden.dat")

    while(True):
        # INFO header
        print("{:-^70}".format(" INFO "))

        print_time("Current time : ")
        print("CPS : {}".format(num_to_word(garden.cps)))
        print("Garden Level : {}".format(garden.level))
        print("Garden Dimensions : {}".format(garden.plots.dimensions))

        # MENU header
        print("{:-^70}".format(" MENU "))

        print("Pick a choice!")
        print("\t    1. Calculate mutation possibility (by entering plants)")
        print("\t    2. Calculate mutation possibility (by selecting mutation)")
        print("\t    3. Find out how to get plant")
        print("\t    4. Find out what plants remain")
        print("\t    5. Change CPS")
        # print("\t    5. Add achieved plant!")
        print("\tOther. Quit")
        choice = input("Choice : ")

        if choice == "1":
            basic_garden(garden)
            time.sleep(3)

        elif choice == "2":
            auto_garden(garden)
            time.sleep(3)

        elif choice == "3":
            get_mutations(garden)
            time.sleep(3)

        elif choice == "4":
            for p in garden.remaining:
                print("[{:^18}]".format(p.name))
                achievable = p.achievable_by(garden.received)
                ach_string = "YES" if achievable[1] else "REQUIRED => " + ", ".join(achievable[0])
                print("\tAchievable? : {}".format(ach_string))
            time.sleep(3)

        elif choice == "5":
            cps = input("Enter your CPS : ").split(" ")
            garden.cps = word_to_num(float(cps[0]), cps[1])
            time.sleep(2)

        # elif choice == "5":
        #     plant_achieved = input("Enter name of plant : ")
        #     p = garden.get_plant(plant_achieved)
        #     plant_history.write(p.name + "\n")
        #     print("Saved plant!")
        #     time.sleep(2)

        else:
            garden.save_all_to_file()
            break
#END