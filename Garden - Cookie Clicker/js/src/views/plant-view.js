import TableView from "./table-view";

export default class PlantView extends TableView{
    setHeaders(){
        const headerData = {
            headers : [
                {
                    id : "plantName",
                    displayName : "Plant Name"
                },
                {
                    id : "maturityTicks",
                    displayName : "To Mature (ticks)"
                },
                {
                    id : "lifespanTicks",
                    displayName : "Lifespan (ticks)"
                },
                {
                    id : "cpsCost",
                    displayName : "Cost (mins of CPS)"
                },
                {
                    id : "minCost",
                    displayName : "Minimum Cost"
                }
            ]
        }

        this.updateHeaders(headerData);
    }

    viewPlants(plants){
        const plantData = {
            rows : []
        }

        plants.forEach(plant => {
            plantData.rows.push({
                id : plant.code,
                name : plant.name,
                mat : plant.mat,
                life : plant.life,
                ccost : plant.cpsCost,
                mcost : plant.minCost
            })
        })

        this.updateRows(plantData);
    }
}