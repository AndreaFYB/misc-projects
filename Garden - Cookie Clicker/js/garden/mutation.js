export class Mutation {
    // constructor(garden, plants, mutRate){
    //     // to be implemented
    // }

    matchIngredients(ingredients){
        let ingnames = ingredients.map(p => p.name);

        let count = {};

        ingnames.forEach(name => {
            count[name] = count[name] ? count[name]+1 : 1;
        });

        // eslint-disable-next-line consistent-return
        this.conditions.forEach(con => {
            if(!(con.plant.name in count)) return false;
            let countP = count[con.plant.name];
            if(con.lessT) if(countP >= con.quantity) return false;
            else if(con.exact) if(countP !== con.quantity) return false;
            else if(countP < con.quantity) return false;
        });

        return true;
    }

    achievableBy(plants){
        let required = this.conditions.map(con => con.plant);

        for(let plant of required){
            if (!(plant in plants)) return plant.name;
        }

        return true;
    }

    toNotation(){
        let str = `${this.mutRate} ==> `;
        let notations = [];

        this.conditions.forEach(con => {
            let lessT = con.lessT ? "<" : "";
            let exact = con.exact ? "!" : "";
            let to    = con.to > 0 ? `-${con.to}` : "";
            
            notations.push(`${con.plant.name}!${exact}${lessT}${con.quantity}${to}@${con.status}`);
        });

        str += notations.join(" && ");

        return str;
    }
}