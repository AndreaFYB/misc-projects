export class Grid {
    constructor(x, y, elem=null){
        this.dimensions = {x: x, y: y};
        this.area = x*y;
        this.grid = new Array(y);

        for(let i = 0; i < y; i++){
            this.grid[i] = new Array(x);
            this.grid[i].fill(elem);
        }
    }

    set(x, y, elem){
        this.grid[y][x] = elem;
    }

    get(x,y){
        return this.grid[y][x];
    }

    render(){
        // to be implemented
    }
}