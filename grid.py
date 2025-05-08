import numpy as np

class Grid:
    def __init__(self, width, height, cell_size):
        self.width = width
        self.height = height
        self.cell_size = cell_size
        self.grid = np.zeros((height, width), dtype=int)
        
    def is_valid_position(self, x, y):
        """Verilen koordinatların grid içinde olup olmadığını kontrol eder."""
        return 0 <= x < self.width and 0 <= y < self.height
    
    def get_cell(self, x, y):
        """Belirtilen koordinattaki hücrenin değerini döndürür."""
        if self.is_valid_position(x, y):
            return self.grid[y][x]
        return None
    
    def set_cell(self, x, y, value):
        """Belirtilen koordinattaki hücrenin değerini ayarlar."""
        if self.is_valid_position(x, y):
            self.grid[y][x] = value
            
    def clear(self):
        """Grid'i temizler."""
        self.grid.fill(0)
        
    def get_neighbors(self, x, y):
        """Verilen koordinatın komşu hücrelerini döndürür."""
        neighbors = []
        for dx, dy in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
            new_x, new_y = x + dx, y + dy
            if self.is_valid_position(new_x, new_y):
                neighbors.append((new_x, new_y))
        return neighbors 