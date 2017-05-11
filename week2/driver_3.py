# import
import sys
from collections import deque

# Debug Mode
if len(sys.argv)>3 and sys.argv[3]=='1' :  DEBUG_VAR = 1
else : DEBUG_VAR = 0

# State definition
class State:
    def __init__(self,board,layer,parent,move):
        self.board = board
        self.value = 0
        for i in range(1,9):
            self.value += int(board[i])*i
        self.layer = layer
        self.par = parent
        self.parmove = move

# Utility to print the board (3x3)
if DEBUG_VAR :
    def pb(board):
        print(board[:3])
        print(board[3:6])
        print(board[6:9])

# Utility to expand nodes (require node and direction [0 for 'Up',1 for 'Right',2 for 'Down',3 for 'Left'])
def expnode(node,dir,i):
    global msd
    global explored
    global fronted
    global front
    if dir is 0:
        dirword = 'Up'
        offset = -3
    elif dir is 1:
        dirword = 'Right'
        offset = 1
    elif dir is 2:
        dirword = 'Down'
        offset = 3
    elif dir is 3:
        dirword = 'Left'
        offset = -1
    else:
        if DEBUG_VAR : print("Error: in expnode not valid direction")
        return
    newboard = node.board.copy()
    newboard[i+offset],newboard[i] = newboard[i],newboard[i+offset]
    new = State(newboard,node.layer+1,node,dirword)
    if not (new.value in explored or new.value in fronted):
        if DEBUG_VAR :
            print('new node generated from '+dirword+' (depth '+str(new.layer)+' ) move: ')
            pb(new.board)
        if new.layer > msd : msd = new.layer
        fronted[new.value]=new
        front.append(new)


# Utility to generate the output file (require a tuple with final state, explored nodes and maximum depth search)
def outgen(tuple):
    f = open('output.txt','w')
    path = ''
    s=tuple[0]
    layer = str(s.layer)
    exp=tuple[1]
    msd=tuple[2]
    while s.par is not None:
        path += "'"
        path += s.parmove
        path += "',"
        s = s.par
    path=path[:-1].split(',')
    path.reverse()
    pathstr="["
    for el in path:
        pathstr+=el
        pathstr+=','
    pathstr=pathstr[:-1]+']'
    output='path_to_goal: '+pathstr+'\ncost_of_path: '+layer+'\nnodes_expanded: '+str(exp)+'\nsearch_depth: '+layer+'\nmax_search_depth: '+str(msd)
    f.write(output)
    #f.write(('\nrunning_time: ',rt))
    #f.write(('\nmax_ram_usage: ',mu))

# implementation of Breadth First Search
def bfs():
    global front
    front = deque([inits])
    global exp
    global msd
    while len(front)>0:
        cur = front.popleft()

        if DEBUG_VAR :
            print('exp = ',exp)
            print('dequeued depth('+str(cur.layer)+')')
            pb(cur.board)

        if cur.value == solved:
            if DEBUG_VAR : print('solved (depth '+str(cur.layer)+') ',cur.board," node expanded ",exp," msd ",msd)
            return (cur,exp,msd)
        del fronted[cur.value]
        explored[cur.value] = cur
        exp += 1
        for i in range(len(cur.board)):
            if cur.board[i] == '0':
                if i>2:
                    #expand up
                    expnode(cur,0,i)
                if i<6:
                    #expand down
                    expnode(cur,2,i)
                if i in range(1,3) or i in range(4,6) or i in range(7,9):
                    #expand left
                    expnode(cur,3,i)
                if i in range(0,2) or i in range(3,5) or i in range(6,8):
                    #expand right
                    expnode(cur,1,i)
                break
    return None

# Depth First Search
def dfs():
    global front
    front = [inits]
    global exp
    global msd
    while len(front)>0:
        cur = front.pop();

        if DEBUG_VAR :
            print('exp = ',exp)
            print('dequeued depth('+str(cur.layer)+')')
            pb(cur.board)

        if cur.value == solved:
            if DEBUG_VAR : print('solved (depth '+str(cur.layer)+') ',cur.board," node expanded ",exp," msd ",msd)
            return (cur,exp,msd)
        del fronted[cur.value]
        explored[cur.value] = cur
        exp += 1
        for i in range(len(cur.board)):
            if cur.board[i] == '0':
                if i in range(0,2) or i in range(3,5) or i in range(6,8):
                    #expand right
                    expnode(cur,1,i)
                if i in range(1,3) or i in range(4,6) or i in range(7,9):
                    #expand left
                    expnode(cur,3,i)
                if i<6:
                    #expand down
                    expnode(cur,2,i)
                if i>2:
                    #expand up
                    expnode(cur,0,i)
                break
    return None


# A* Search with Manhattan heuristic
def ast():
    pass

# Main
if DEBUG_VAR : print("\n *** DEBUG MODE ***\n")
inits = State(sys.argv[2].split(','),0,None,'')
solved = 0
for i in range(1,9):
    solved += i*i
explored = {} # dictionary containing explored nodes
fronted = {inits.value : inits} # dictionary containing frontier nodes
front = [] # frontier
exp = 0 # number of explored nodes
msd = 0 # maximum search depth
if sys.argv[1] == 'bfs':
    if DEBUG_VAR : print('bfs calling:')
    solution = bfs()
elif sys.argv[1] == 'dfs':
    if DEBUG_VAR : print('dfs calling:')
    solution = dfs()
elif sys.argv[1] == 'ast':
    if DEBUG_VAR : print('ast calling:')
    solution = ast()
if solution is not None: outgen(solution)
