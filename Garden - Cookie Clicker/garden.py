from grid import Grid
from mutation import Mutation
from plant import Plant
from utils import num_to_word

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
