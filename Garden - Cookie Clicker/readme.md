# A Garden helper for Cookie Clicker
This project aims to serve as a sort of helper for the garden involved in cookie clicker. It helps a lot with knowing mutations, and optimising them.

## How to use
When you run `mutation.py`, the first input you'll be asked is about your garden size. Specifically your level or dimension. You can enter either. For example if your garden is at level 4 (and hence has dimensions 4x3), you can either enter `4`, or `4x3`. Whichever you feel is simpler.

After that, you are directed to a menu. In this menu you can:
- Calculate your chances at a mutation
- Find how to achieve a certain mutation
- Get the best layout for your garden.

### Calculating your chances
For this you need to know (and input) these things:
- Whether you're using wood chips.
- The 2 plants you want to use.
- Which mutation you want.

The first thing you'll be asked is whether you are going to use wood chips. After that, you'll be prompted for the two plants you want to use. If you need to use 2 of the same plant, then you can type the same name twice.

For now this is still relatively simple, so complicated mutations that include more than 2 total ingredients aren't calculated as accurately as simpler ones. For example the chances of getting a Juicy Queenbeet will be greatly inflated and inaccurate.

After that, you'll be shown a list of possible mutations resulting from the plants you've entered. If there's only one mutation it will be automatically picked, however if there's more than one, you should choose the one that you want.

After that, the script will show you the chances of you achieving that mutation. It will also tell you which plant you should plant first, and how many ticks you should wait before planting the other plant for the maximum chance.

### Getting mutations
For this, all you need to know is the name of the plant you want to get. After you enter that, you'll get a list of possible mutations, as well as their mutation rate.

### Getting the best layout
For this, just enter whether you're looking for the best layout with different plants, or with the same plant. For now though, only the best layout with the same plant is being considered.

## Docs
There are multiple classes here, namely:
- `Plant`
- `Grid`
- `Garden`
- `Mutation`
    - `Condition`

### Grid
This class is very simple, and mostly used as a utility class. It serves as an interface for creating a 2D array (hence a grid). Has specific `set` and `get` functions, and a representation via `__repr__`, and may get additional functions in the future.

### Plant
A plant needs:
- A name
- Number of ticks till maturity
- Number of ticks during its lifespan
- Cost to plant relative to cps (in minutes)
- Minimum cost of plant

It has multiple `compare` functions that compare 2 plants'
maturities, lifespans, or duration of maturity.

The function `created_from` accepts a **`Mutation`** object, and will add said mutation to `muts`. Any **`Mutation`** in `muts` is one that will result in the plant it belongs to.

There are two printing functions:
- `print_details` : Prints all the details of a plant.
- `print_mutations` : Prints all mutations that can create the plant.

`get_cost` simply retrieves the cost to plant the plant, and takes the `cps` as the parameter.

`mutates_from` has a parameter `ingredients`, which is simply a list of plants. This is a boolean function that will return `True` if the plants in `ingredients` can result in this plant. For example,

`Baker_Wheat.mutates_from([Baker_Wheat, Baker_Wheat])` 

...will return True, as a Baker Wheat plant can be created from 2 Baker Wheat plants. In this scenario, `Baker_Wheat` is a `Plant` object related to Baker Wheat.

### Mutation
A mutation needs:
- A `Garden` object
- A list of plant names in Mutation Notation.
- The mutation rate.

The garden object is useful as it is used to retrieve `Plant` objects using the list of plant names that was passed.

Before explaining Mutation Notation, let's explain what `match_ingredients` does.

It accepts a list of `Plant` objects as parameter, and if this list satisfies the *conditions* for the mutation, it will return `True`.

An example of a plant name in Mutation Notation is as follows:

`Brown Mold!2@Any`

The above means "*Any 2 Brown Mold plants*"

An explanation of the notation:
- In every name, there must be the actual plant name, which will come first.
- If there is a quantity constraint, it must be shown via a symbol after the name:
    - `!n` : n or more of this plant.
    - `!!n` : exactly n of this plant.
    - `!<n` : less than n of this plant.
    - Without an explicitly mentioned quantity constraint, it will be assumed to be *1 or more*.
- There can be a status constraint, which shows whether the plant needs to be Mature, or more.
    - `@M` : Mature
    - `@Any` : Any (Mature and below)
    - Without an explicitly mentioned status constraint, it will be assumed to be *Mature*
- Status constraints come **after** quantity constraints.

More examples of the notation:
- Exactly 3 of Cronerice = `Cronerice!!3`
- 2 or more of Thumbcorn = `Thumbcorn!2`
- Less than 5 of any Brown Mold = `Brown Mold!<5@Any`

Every plant name in Mutation Notation will be converted into a `Condition` object. A `Mutation` object will contain a list of these conditions, and the mutation rate.

### Condition
A `Condition` is only used within a `Mutation` object, in order to store the prerequisites for the Mutation. Every condition specifies certain amount of parameters:
- `plant` : The plant required.
- `quantity` : The quantity required. By default, this means that `quantity` or more of `plant` are required, though this meaning can change according to other flags.
- `status` : `"M"` or `"Any"`. Specifies the status of the plant.
- `lessT` : A flag. If `True`, then there need to be less than `quantity` of `plant`.
- `exactT` : A flag. If `True`, then there need to be exactly `quantity` of `plant`.
- `to`  : A sort-of flag. If set to a value higher than `quantity` then a range of quantities is specified for the plant.

Some examples to explain it better.
- `Condition(plant=P, quantity=4, lessT=True)` : Less than 4 of the Mature plant `P` are required.
- `Condition(plant=P, quantity=2, to=4)` : 2 to 4 of the Mature plant `P` are required.
- `Condition(plant=P, quantity=3, exact=True)` : Exactly 3 of plant `P` are required.
- `Condition(plant=P, quantity=2, status="Any")` : 2 or more of Any plant `P` are required.

### Garden
The largest object, for good reason. 

To create one, you require either the `level` or the `dimensions`. The `level` would be a number 1 or above. The `dimensions` would be a string like `2x2`. Only one of these parameters should be passed. If neither or both are passed, an Runtime Error will be thrown.

The initialiser creates a `Garden` object, with a `Grid` that has the same dimensions as `dimensions`, or as a Garden with level `level`. For example, `level=4` maps to `dimensions=(4,3)`.

All the plants, as well as their details, will also be added to the garden. All of the plant data is stored in the `plants` variable in `__init__`.

`Garden.garden` contains a dictionary of all the plants.

`get_plant` simply gets the `Plant` object with the same name as `name`.

`include_mutations` includes mutation data in the `Garden`. It will add all information regarding which plants mutate into which plants, mutation rates, and more. All the mutation data is stored in the `mutations` variable in this function.

In order to add a `Plant` or a `Mutation`, you would need to modify the source code for the time being. For ease of use, you can add an element to the `plants` or `mutations` array as follows:

```Python
plants += [Name, TicksToMaturity, TicksTillDeath, CPSCost, MinimumCost]
```

```Python
mutation += [Name,
    [[NameInMutationNotation, ...], MutationRate],
    ...
]
```

`best_layout` returns a dictionary that stores a grid representing the garden and which layout should be used with the key `plot`, and the number of empty spots in the grid with the key `empty`.

`get_mutations_by_ingredients` returns all the mutations that result from the list of `Plant`s `ingredients`. 

# In the future
- Update this README more thoroughly
- Add support for more complex mutations
- Include plant descriptions
- Add plant effects
- ~~Find which plant mutations are currently achievable~~