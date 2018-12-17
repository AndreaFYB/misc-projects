export default class Plant {
    // eslint-disable-next-line max-params
    constructor(name, mat, life, cpsCost, minCost, code="PNT"){
        this.name = name;
        this.mat = mat;
        this.life = life;
        this.matAge = life-mat;
        this.cpsCost = cpsCost;
        this.minCost = minCost;
        this.muts = [];
        this.code = code;
    }

    equalTo(plant){
        return plant.name === this.name;
    }

    createdFrom(mutation){
        this.muts.push(mutation);
    }

    // TODO: Implement
    printDetails(){
    }

    // TODO: Implement
    printMuts(){
    }

    getCost(cps){
        let total = cps * this.cps_cost * 60;
        return total >= this.min_cost ? total : this.min_cost;
    }

    mutatesFrom(ingredients){
        for(let mut of this.muts){
            if(mut.matchIngredients(ingredients)){
                return mut;
            }
        }
        return false;
    }

    achievableBy(plants){
        let missing = [];
        for(let mut of this.muts){
            let achieved = mut.achievableBy(plants);
            if(achieved == true){
                return {mutation: mut, achievable: true, missing: null};
            // eslint-disable-next-line no-else-return
            } else missing.push(achieved);
        }

        return {mutation: null, achievable: false, missing: missing};
    }
}