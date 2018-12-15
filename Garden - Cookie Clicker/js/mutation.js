import moment from moment;

class Plant {
    constructor(name, mat, life, cps_cost, min_cost, code="PNT"){
        this.name = name;
        this.mat = mat;
        this.life = life;
        this.mat_age = life-mat;
        this.cps_cost = cps_cost;
        this.min_cost = min_cost;
        this.muts = [];
        this.code = code;
    }

    equalTo(plant){
        return plant.name === this.name;
    }

    createdFrom(mutation){
        this.muts.push(mutation);
    }

    printDetails(){
        // to be implemented
    }

    printMuts(){
        // to be implemented
    }

    getCost(cps){
        let total = cps * this.cps_cost * 60;
        return total >= min_cost ? total : min_cost;
    }

    mutatesFrom(ingredients){
        // to be implemented
    }

    achievableBy(plants){
        // to be implemented
    }
}

class Grid {
    constructor(x, y, elem=null){
        this.dimensions = {x: x, y: y};
        this.area = x*y;
        this.grid = new Array(y);

        for(let i = 0; i < y; i++){
            grid[i] = new Array(x);
            grid[i].fill(elem);
        }
    }

    set(x, y, elem){
        grid[y][x] = elem;
    }

    get(x,y){
        return grid[y][x];
    }

    render(){
        // to be implemented
    }
}

class Garden {
    constructor(filename){
        this.garden = {};
        this.load(filename);
    }

    getPlant(pname){
        return garden[pname.toLowerCase()];
    }

    bestLayout(p1, p2){
        let dims = `${this.plots.dimensions["x"]}x${this.plots.dimensions["y"]}`;

        let bestByDim = {
            "2x2" : {"a": [[0,0]],                                    "b": [[0,1]]},
            "3x2" : {"a": [[1,0]],                                    "b": [[1,1]]},
            "3x3" : {"a": [[0,1], [2,1]],                             "b": [[1,1]]},
            "4x3" : {"a": [[0,1], [2,1]],                             "b": [[1,1], [3,1]]},
            "4x4" : {"a": [[0,0], [3,3], [0,3], [3,0]],               "b": [[1,1], [2,2]]},
            "5x4" : {"a": [[0,0], [3,0], [0,3], [3,3]],               "b": [[1,0], [4,0], [1,3], [4,3]]},
            "5x5" : {"a": [[0,0], [3,0], [0,3], [3,3]],               "b": [[1,0], [4,0], [1,3], [4,3]]},
            "6x5" : {"a": [[1,0], [1,3], [4,0], [4,3]],               "b": [[1,1], [1,4], [4,1], [4,4]]},
            "6x6" : {"a": [[0,1], [5,1], [2,4], [0,4], [5,4], [3,1]], "b": [[1,1], [4,4], [1,4], [4,1]]}
        }

        let unwantedMuts = {
            "2x2" : [],
            "3x2" : [],
            "3x3" : [[1,0], [1,2]],
            "4x3" : [[1,0], [2,0], [1,2], [2,2]],
            "4x4" : [[1,2], [2,1]],
            "5x4" : [],
            "5x5" : [],
            "6x5" : [],
            "6x6" : [[4,0], [4,2], [1,3], [1,5]],
        }

        let pointsAB = bestByDim[dims];
        let pointsXX = unwantedMuts[dims];
        let tplot = new Grid(this.plots.dimensions["x"], this.plots.dimensions["y"], "---")

        let cost = 0;

        let plants = {
            "a" : {
                "plant" : (p1cost >= p2cost) ? p2 : p1
            }, 
            "b" : {
                "plant" : (p1cost >= p2cost) ? p1 : p2
            }
        }

        plants.a["cost"] = plants.a.plant.getCost(this.cps);
        plants.b["cost"] = plants.b.plant.getCost(this.cps);

        fillInGrid = (arr, elem, pcost) => {
            cost = 0;
            arr.forEach(p => {
                tplot.set(p[0], p[1], elem);
                pcost += cost;
            })
            return cost;
        }

        let costA = fillInGrid(pointsAB["a"], plants.a.plant.code, plants.a.cost);
        let costB = fillInGrid(pointsAB["b"], plants.b.plant.code, plants.b.cost);
        fillInGrid(pointsXX, "-X-");

        return {
            "plot" : tplot,
            "empty" : self.plots.area - pointsAB["a"] - pointsAB["b"],
            "usable" : self.plots.area - pointsAB["a"] - pointsAB["b"] - pointsXX.length,
            "unwanted" : pointsXX.length,
            "cost" : numToWord(costA+costB)
        }
    }

    getMutsByIngs(ingredients){
        // to be implemented
    }

    saveAllToFile(){
        // to be implemented
    }

    load(filename){
        // to be implemented
    }
}

class Mutation {
    constructor(garden, plants, mutRate){
        // to be implemented
    }

    matchIngredients(ingredients){
        let ingnames = ingredients.map(p => p.name);

        let count = {}

        ingnames.forEach(name => {
            count[name] = count[name] ? count[name]+1 : 1;
        })

        this.conditions.forEach(con => {
            if(!con.plant.name in count) return false;
            let countP = count[con.plant.name];
            if(con.lessT) if(countP >= con.quantity) return false;
            else if(con.exact) if(countP !== con.quantity) return false;
            else if(countP < con.quantity) return false;
        })

        return true;
    }

    achievableBy(plants){
        let required = this.conditions.map(con => con.plant);

        for(let i in required){
            if (!required[i] in plants) return required[i].name;
        }

        return true;
    }

    toNotation(){
        let str = `${this.mutRate} ==> `;
        let notations = []

        conditions.forEach(con => {
            lessT = con.lessT ? "<" : "";
            exact = con.exact ? "!" : "";
            to    = con.to > 0 ? `-${con.to}` : "";
            
            notations.push(`${con.plant.name}!${exact}${lessT}${con.quantity}${con.to}@${con.status}`);
        })

        str += notations.join(" && ");

        return str;
    }
}

class Condition {
    constructor(plant, quantity=1, status="M", lessT = false, exact = false, to = -1){
        this.plant = plant;
        this.quantity = quantity;
        this.status = status;
        this.exact = exact;
        this.lessT = lessT;
        this.to = to <= quantity ? -1 : to;
    }
}

const extensions = [
    "million", "billion", "trillion", "quadrillion",
    "quintillion", "sextillion", "septillion",
    "octillion", "nonillion", "decillion",
    "undecillion", "duodecillion", "tredecillion",
    "quattordecillion", "quindecillion", "sexdecillion"
]

numToWord = function(num){
    sNum = num / (10 ** 6)

    if (sNum < 1) return num;

    let i;

    for(i = 0; sNum / 1000 >= 1 && i <= 15; i++){
        sNum /= 1000;
    }

    return `${sNum.toFixed(3)} ${extensions[i]}`
}

wordToNum = function(num, extension){
    let exps = []

    for(let i = 6; i <= 52; i+=3){
        exps.push(10 ** i);
    }

    let obj = {}

    for(let i in extensions){
        obj[extensions[i]] = exps[i];
    }

    return num * obj[extension];
}

calculateTotalChance = function(wc, p1, p2, empty, mutRate, mutName){
    // to be implemented
}

getTime = function(prompt, offset=0){
    return `${prompt}${moment().add(offset, 'seconds').format("MMMM Do YYYY, hh:mm:ss")}`
}

basicGarden = function(garden){
    // to be implemented
}

autoGarden = function(garden){
    // to be implemented
}

getMutations = function(garden){
    // to be implemented
}

// main function omitted.

