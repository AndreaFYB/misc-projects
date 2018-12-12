import time

# classes
from garden import Garden

# utils
from utils import num_to_word, calculate_total_chance, print_time, word_to_num

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