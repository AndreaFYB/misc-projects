class Grid:
    def __init__(self, x, y, elem=None):
        self.dimensions = (x,y)
        self.area = x*y

        self.grid = [[elem for x1 in range(x)] for y1 in range(y)]

    def set(self, x, y, elem):
        self.grid[y][x] = elem

    def get(self, x, y, elem):
        return self.grid[y][x]

    def __repr__(self):
        string = ""

        for horizarr in self.grid:
            string += "[" + " , ".join(horizarr) + "]\n"

        return string
