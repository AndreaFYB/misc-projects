import Data from "../../garden.json";
import Garden from "../models/garden";
import $ from "jquery";

import PlantView from "../views/plant-view"

export default class GardenController{
    constructor(){
        console.log(Data);
        this.garden = new Garden(Data);
        this.view = new PlantView();
        this.view.setHeaders();
        this.view.viewPlants(this.garden.getPlants());
    }
}