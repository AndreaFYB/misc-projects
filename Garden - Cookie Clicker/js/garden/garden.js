import Grid from "../utils/grid"
import Mutation from "./mutation"
import Plant from "./plant"

export class Garden {
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
        mutations = [];
        for(let plant of garden.values()){
            let mut = plant.mutatesFrom(ingredients)
            if(mut != false) mutations.push({plant: plant, mutation: mut});
        }

        return mutations;
    }

    saveAllToFile(){
        // to be implemented
    }

    load(filename){
        // to be implemented
    }
}