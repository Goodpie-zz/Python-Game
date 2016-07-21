class DiamondSquare:
    def __init__(self, size, roughness):

        self.size = (2 ** size) + 1
        self.max = self.size - 1
        self.roughness = roughness
        self.make_grid(self.size)
        self.divide(self.max)  # Start

    # Sets x,y position in self.grid
    def set(self, x, y, val):
        self.grid[x + self.size * y] = val

    # Get's value of x, y in self.grid
    def get(self, x, y):
        if x < 0 or x > self.max or y < 0 or y > self.max:
            return -1
        return self.grid[x + self.size * y]

    # Clamps x between min and max
    def clamp(self, x, min, max):

        if (x < min):
            x = min
        elif (x > max):
            x = max

        return x

    # Main iteration
    def divide(self, size):

        x = size / 2
        y = size / 2
        half = size / 2
        scale = self.roughness * size

        if (half < 1):
            return

        # Square
        for y in range(half, self.max, size):
            for x in range(half, self.max, size):
                s_scale = random.uniform(0, 1) * scale * 2 - scale
                self.square(x, y, half, s_scale)

        # Diamond
        for y in range(0, self.max + 1, half):
            for x in range((y + half) % size, self.max + 1, size):
                d_scale = random.uniform(0, 1) * scale * 2 - scale
                self.diamond(x, y, half, d_scale)

        self.divide(size / 2)

    def square(self, x, y, size, scale):

        top_left = self.get(x - size, y - size)
        top_right = self.get(x + size, y - size)
        bottom_left = self.get(x + size, y + size)
        bottom_right = self.get(x - size, y + size)

        average = ((top_left + top_right + bottom_left + bottom_right) / 4)
        self.set(x, y, self.clamp(average + scale, 0, 1))

    def diamond(self, x, y, size, scale):

        top = self.get(x, y - size)
        right = self.get(x + size, y)
        bottom = self.get(x, y + size)
        left = self.get(x - size, y)

        average = ((top + right + bottom + left) / 4)
        self.set(x, y, self.clamp(average + scale, 0, 1))

    def make_grid(self, size):

        self.grid = []

        # Make the grid
        for x in range(size * size):
            self.grid.append(-1)

        # Base value
        self.set(0, 0, 1)
        self.set(self.max, 0, 0.5)
        self.set(self.max, self.max, 0)
        self.set(0, self.max, 0.5)

    # Returns a 2D array of the grid
    # Used for easier readability and manipulation
    def get_grid_2D(self):
        grid_2d = [self.grid[x:x + self.size] for x in range(0, len(self.grid), self.size)]
        return grid_2d
