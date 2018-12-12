import time

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
