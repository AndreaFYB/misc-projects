export class Plant {
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
        for(let mut of muts){
            if(mut.matchIngredients(ingredients)){
                return mut;
            }
        }
        return false;
    }

    achievableBy(plants){
        missing = [];
        for(mut of this.muts){
            achieved = mut.achievableBy(plants);
            if(achieved) return {mutation: mut, achievable: true, missing: null};
            else missing.push(achieved);
        }

        return {mutation: null, achievable: false, missing: missing};
    }
}