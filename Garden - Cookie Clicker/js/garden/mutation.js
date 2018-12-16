export class Mutation {
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

        for(let plant of required){
            if (!plant in plants) return plant.name;
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