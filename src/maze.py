import sys, time

class State:
    def __init__(self, label, reward, is_terminal = False):
        self.label = label
        self.reward = reward
        self.is_terminal = is_terminal
        self.successors = {}
    
    def add_successor(self, action, state):
        self.successors[action] = state
        
    def __hash__(self):
        return int(str(self.label[0]) + str(self.label[1]))

class Instance:
    def __init__(self, width, height):
        self.states = {}
        self.shape = (width, height)
        self.Q = [[0] * height] * width
        
        for i in range(0, width):
            for j in range(0, height):
                self.Q[i][j] = {(0, 1): 0, (0, -1): 0, (1, 0): 0, (-1, 0): 0}
        
    def add_state(self, i, j, reward, is_terminal = False):
        self.states[(i, j)] = State((i, j), reward, is_terminal)
        
    def add_successor(self, i, j, p, q, action):
        self.states[(i, j)].add_successor(action, self.states[(p, q)])

def create_instance(width, height, grid):
    instance = Instance(width, height)
    
    for i in range(0, width):
        for j in range(0, height):
            if grid[i][j] == '-':
                instance.add_state(i, j, -1)
            elif grid[i][j] == '0':
                instance.add_state(i, j, 10, True)
            elif grid[i][j] == '&':
                instance.add_state(i, j, -10, True)
            
    for i in range(0, width):
        for j in range(0, height):
            x_s, x_f = -1 if i > 0 else 0, 2 if i < height - 1 else 1
            y_s, y_f = -1 if j > 0 else 0, 2 if j < width - 1 else 1
            
            for x in range(x_s, x_f):
                for y in range(y_s, y_f):
                    if not (x == 0 and y == 0) and grid[i][j] != '#':
                        if grid[i + x][j + y] == '#':
                            instance.add_successor(i, j, i, j, (x, y))
                        else:
                            instance.add_successor(i, j, i + x, j + y, (x, y))
    
    return instance

def solve(instance): 
    pass

def main():
    raw_data = sys.argv
    
    if len(raw_data) != 5:
        print("usage: %s map alpha gama n" % raw_data[0])
        sys.exit(1)
    
    map_name, alpha, gama, n = raw_data[1:]
    
    with open(map_name, 'r') as file:
        data = file.readlines()
        
    width, height = data[0].split()
    grid = list(map(lambda l: list(l.rstrip()), data[1:]))
    
    instance = create_instance(int(width), int(height), grid)
    current_state = None
    
if __name__ == "__main__":
    main()