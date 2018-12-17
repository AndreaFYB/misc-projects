import headerList from "./templates/header-list.hbs";
import plantList from "./templates/plant-list.hbs";

export default class TableView {
    updateHeaders(templateData){
        $("#plant-list-header-row").html(headerList(templateData));
    }

    updateRows(objData){
        $("#plant-list-body").html(plantList(objData));
    }
}