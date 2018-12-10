
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

def init_garden():
    garden = {}

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
        ["Fool's Bolete", 3, 6],
        ["Wrinklegill", 26, 40],
        ["Green Rot", 4, 6],
        ["Ichorpuff", 20, 58]
    ]

    for x in plants:
        garden[x[0].lower()] = Plant(x[0], x[1], x[2])

    return garden

wood_chips = input("Are you using wood chip? (Y for yes, N for no) : ")

inp1 = input("Enter Plant 1's name : ")
inp2 = input("Enter Plant 2's name : ")

garden = init_garden()

p1 = garden[inp1.lower()]
p2 = garden[inp2.lower()]

empty_spaces = int(input("How many empty spaces are there? : "))
mutation_rate = float(input("Chance of mutation : "))

calculate_total_chance(wood_chips, p1, p2, empty_spaces, mutation_rate)