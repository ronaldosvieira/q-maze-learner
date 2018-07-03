import sys, time, random
from operator import attrgetter

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
                
    actions = {(0, -1): '^', (0, 1): 'v', (1, 0): '>', (-1, 0): '<'}
            
    for i in range(0, width):
        for j in range(0, height):
            if grid[i][j] != '#':
                for (dx, dy), action in actions.items():
                    if grid[i + dx][j + dy] == '#':
                        instance.add_successor(i, j, i, j, action)
                    else:
                        instance.add_successor(i, j, i + dx, j + dy, action)
    
    return instance

def main():
    raw_data = sys.argv
    
    if len(raw_data) != 5:
        print("usage: %s map alpha gama n" % raw_data[0])
        sys.exit(1)
    
    map_name, alpha, gama, n = raw_data[1:]
    
    alpha, gama, n = float(alpha), float(gama), int(n)
    epsilon = 0.9
    
    with open(map_name, 'r') as file:
        data = file.readlines()
        
    height, width = map(int, data[0].split())
    grid = list(map(lambda l: list(l.rstrip()), data[1:]))
    grid = [list(row) for row in zip(*grid)]
    
    instance = create_instance(width, height, grid)
    Q = {}
    state = None
    
    for i in range(0, width):
        for j in range(0, height):
            Q[(i, j)] = {'^': 0, 'v': 0, '>': 0, '<': 0}
    
    for i in range(0, n):
        if state is None:
            state = random.choice(list(filter(lambda s: not s.is_terminal, instance.states.values())))
        
        # chooses action
        if random.random() < epsilon:
            action = max(state.successors.keys(), key = lambda a: Q[state.label][a])
        else:
            action = random.choice(list(state.successors.keys()))
            
        new_state = state.successors[action]
        
        # updates Q-table
        current = Q[state.label][action]
        reward = new_state.reward
        max_val = max(Q[new_state.label].values())
        
        Q[state.label][action] = current + alpha * (reward + (gama * max_val) - current)
        
        #print(state.label, action, new_state.label, Q[state.label][action], (current, reward, max_val))
        
        if new_state.is_terminal: state = None
        else: state = new_state
    
    '''for s in sorted(instance.states.values(), key = attrgetter('label')):
        print(s.label, list(map(lambda a: str(a[0]) + ': ' + str(a[1]), Q[s.label].items())))'''
    
    for j in range(0, height):
        for i in range(0, width):
            if grid[i][j] != '-':
                print(grid[i][j], end="")
            else:
                print(max(Q[(i, j)].keys(), key = lambda a: Q[(i, j)][a]), end = "")
                
        print()
    
if __name__ == "__main__":
    main()