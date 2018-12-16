import "./css/main.css";
import Data from "../garden.json";
import Garden from "./garden/garden";

console.log(Data);
let garden = new Garden(Data);
console.log(garden);
