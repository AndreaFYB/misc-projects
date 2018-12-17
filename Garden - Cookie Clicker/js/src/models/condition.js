export default class Condition {
    // eslint-disable-next-line max-params
    constructor(plant, quantity=1, status="M", lessT = false, exact = false, to = -1){
        this.plant = plant;
        this.quantity = quantity;
        this.status = status;
        this.exact = exact;
        this.lessT = lessT;
        this.to = to <= quantity ? -1 : to;
    }

    static fromNotation(garden, notation){
        if(notation.includes("!!")){
            let split = notation.split("!!");

            let plant = garden.getPlant(split[0]);
            let quantity = split[1];
            let status = "M";

            if(quantity.includes("@")){
                split = quantity.split("@");
                quantity = split[0];
                status = split[1];
            }

            return new Condition(plant, quantity, status, false, true, undefined);
        }
        else if(notation.includes("!")){
            let split = notation.split("!");

            let plant = garden.getPlant(split[0]);
            let quantity = split[1];
            let status = "M";
            let lessT = false;

            if(quantity.includes("@")){
                let flags = quantity.split("@");
                quantity = flags[0];
                status = flags[1];
            }

            if(quantity.includes("<")){
                lessT = true;
                quantity = quantity.split("<")[1];
            }
            else if(quantity.includes("-")){
                let range = quantity.split("-");
                return new Condition(plant, range[0], status, lessT, false, range[1])
            }

            return new Condition(plant, quantity, status, lessT, false, undefined);
        }
        else if(notation.includes("@")){
            let split = notation.split("@");
            let plant = garden.getPlant(split[0]);
            return new Condition(plant, undefined, split[1]);
        }
        else{
            return new Condition(garden.getPlant(notation));
        }
    }
}