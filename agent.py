import random
from enum import Enum

class Strategy(Enum):
    RANDOM = "random"
    GREEDY = "greedy"
    DEFENSIVE = "defensive"
    PATROL = "patrol"

class Agent:
    def __init__(self, x, y, strategy, color, grid):
        self.x = x
        self.y = y
        self.strategy = strategy
        self.color = color
        self.grid = grid
        self.score = 0
        self.patrol_points = []
        self.current_patrol_index = 0
        self.image = None  # Add image attribute
        
    def move(self, other_agents):
        """Ajanın stratejisine göre hareket etmesini sağlar."""
        if self.strategy == Strategy.RANDOM:
            self._move_random()
        elif self.strategy == Strategy.GREEDY:
            self._move_greedy(other_agents)
        elif self.strategy == Strategy.DEFENSIVE:
            self._move_defensive(other_agents)
        elif self.strategy == Strategy.PATROL:
            self._move_patrol()
            
    def _move_random(self):
        """Rastgele hareket stratejisi."""
        neighbors = self.grid.get_neighbors(self.x, self.y)
        if neighbors:
            self.x, self.y = random.choice(neighbors)
            
    def _move_greedy(self, other_agents):
        """En yakın hedefe doğru hareket stratejisi."""
        if not other_agents:
            self._move_random()
            return
            
        closest_agent = min(other_agents, 
                          key=lambda a: abs(a.x - self.x) + abs(a.y - self.y))
        
        dx = closest_agent.x - self.x
        dy = closest_agent.y - self.y
        
        if abs(dx) > abs(dy):
            new_x = self.x + (1 if dx > 0 else -1)
            if self.grid.is_valid_position(new_x, self.y):
                self.x = new_x
        else:
            new_y = self.y + (1 if dy > 0 else -1)
            if self.grid.is_valid_position(self.x, new_y):
                self.y = new_y
                
    def _move_defensive(self, other_agents):
        """Diğer ajanlardan uzaklaşma stratejisi."""
        if not other_agents:
            self._move_random()
            return
            
        # En yakın ajanı bul
        closest_agent = min(other_agents, 
                          key=lambda a: abs(a.x - self.x) + abs(a.y - self.y))
        
        # En yakın ajanın tersi yönünde hareket et
        dx = self.x - closest_agent.x
        dy = self.y - closest_agent.y
        
        if abs(dx) > abs(dy):
            new_x = self.x + (1 if dx > 0 else -1)
            if self.grid.is_valid_position(new_x, self.y):
                self.x = new_x
        else:
            new_y = self.y + (1 if dy > 0 else -1)
            if self.grid.is_valid_position(self.x, new_y):
                self.y = new_y
                
    def _move_patrol(self):
        """Belirli noktalar arasında devriye gezme stratejisi."""
        if not self.patrol_points:
            # Devriye noktalarını oluştur
            self.patrol_points = [
                (0, 0),
                (self.grid.width-1, 0),
                (self.grid.width-1, self.grid.height-1),
                (0, self.grid.height-1)
            ]
            
        target_x, target_y = self.patrol_points[self.current_patrol_index]
        
        # Hedef noktaya ulaşıldıysa bir sonraki noktaya geç
        if self.x == target_x and self.y == target_y:
            self.current_patrol_index = (self.current_patrol_index + 1) % len(self.patrol_points)
            target_x, target_y = self.patrol_points[self.current_patrol_index]
            
        # Hedef noktaya doğru hareket et
        dx = target_x - self.x
        dy = target_y - self.y
        
        if abs(dx) > abs(dy):
            new_x = self.x + (1 if dx > 0 else -1)
            if self.grid.is_valid_position(new_x, self.y):
                self.x = new_x
        else:
            new_y = self.y + (1 if dy > 0 else -1)
            if self.grid.is_valid_position(self.x, new_y):
                self.y = new_y 