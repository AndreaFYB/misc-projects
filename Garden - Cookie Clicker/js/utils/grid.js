export class Grid {
    constructor(x, y, elem=null){
        this.dimensions = {x: x, y: y};
        this.area = x*y;
        this.grid = new Array(y);

        for(let i = 0; i < y; i++){
            grid[i] = new Array(x);
            grid[i].fill(elem);
        }
    }

    set(x, y, elem){
        grid[y][x] = elem;
    }

    get(x,y){
        return grid[y][x];
    }

    render(){
        // to be implemented
    }
}