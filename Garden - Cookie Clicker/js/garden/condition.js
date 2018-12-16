export class Condition {
    // eslint-disable-next-line max-params
    constructor(plant, quantity=1, status="M", lessT = false, exact = false, to = -1){
        this.plant = plant;
        this.quantity = quantity;
        this.status = status;
        this.exact = exact;
        this.lessT = lessT;
        this.to = to <= quantity ? -1 : to;
    }
}