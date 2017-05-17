# import
import sys
from collections import deque
import time
from heapq import heappush, heappop
#import resource

# time-check
start_time = time.time()

# Debug Mode
if len(sys.argv)>3 and sys.argv[3]=='1' :  DEBUG_VAR = 1
else : DEBUG_VAR = 0

# State definition
class State:
    def __init__(self,board,layer,parent,move):
        self.board = board
        self.value = ''.join(str(i) for i in board)
        self.layer = layer
        self.par = parent
        self.parmove = move
        self.heu = 0
        for i in range(1,9):
            self.heu += tile_dist(i,self.board.index(str(i)))
        if DEBUG_VAR : print(self.value)

# Utility to evaluate distance of a tile from it's position
def tile_dist(value,position):
    pcoord = (position // 3 , position % 3)
    vcoord = (value // 3 , value % 3)
    return abs(pcoord[0]-vcoord[0])+abs(pcoord[1]-vcoord[1])


# Utility to print the board (3x3)
if DEBUG_VAR :
    def pb(board):
        print(board[:3])
        print(board[3:6])
        print(board[6:9])

# Utility to expand nodes (require node, direction [0 for 'Up',1 for 'Right',2 for 'Down',3 for 'Left'], '0' offset and 1 if A*)
def expnode(node,dir,i,is_ast):
    global msd, explored, fronted, front
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
        if is_ast : heappush(front,(new.heu+new.layer,new.value))
        else : front.append(new)


# Utility to generate the output file (require a tuple with final state, explored nodes and maximum depth search)
def outgen(s):
    global exp, msd, start_time
    cost = 0
    f = open('output.txt','w')
    path = ''
    while s.par is not None:
        cost += 1
        path += "'"+s.parmove+"',"
        s = s.par
    path=path[:-1].split(',')
    path.reverse()
    pathstr="["
    for el in path :  pathstr+= el+','
    pathstr=pathstr[:-1]+']'
    output='path_to_goal: '+pathstr+'\ncost_of_path: '+str(cost)+'\nnodes_expanded: '+str(exp)+'\nsearch_depth: '+str(cost)+'\nmax_search_depth: '+str(msd)+'\nrunning_time: '+str(time.time()-start_time)
    f.write(output)
    #f.write("\nmax_ram_usage: "+str(resource.getrusage(resource.RUSAGE_SELF).ru_maxrss))

# implementation of Breadth First Search
def bfs():
    global exp, msd, front, fronted, explored
    fronted[inits.value] = inits
    front = deque([inits])
    while len(front)>0:
        cur = front.popleft()
        if DEBUG_VAR :
            print('exp = ',exp)
            print('dequeued depth('+str(cur.layer)+')')
            pb(cur.board)
        if cur.value == solved:
            if DEBUG_VAR : print('solved (depth '+str(cur.layer)+') ',cur.board," node expanded ",exp," msd ",msd)
            return cur
        del fronted[cur.value]
        explored[cur.value] = cur
        exp += 1
        i = cur.board.index('0')
        if i>2: expnode(cur,0,i,0) #expand up
        if i<6: expnode(cur,2,i,0) #expand down
        if i in range(1,3) or i in range(4,6) or i in range(7,9): expnode(cur,3,i,0) #expand left
        if i in range(0,2) or i in range(3,5) or i in range(6,8): expnode(cur,1,i,0) #expand right
    return None

# Depth First Search
def dfs():
    global exp, msd, front, fronted, explored
    fronted[inits.value] = inits
    front = [inits]
    while len(front)>0:
        cur = front.pop();
        if DEBUG_VAR :
            print('exp = ',exp)
            print('dequeued depth('+str(cur.layer)+')')
            pb(cur.board)
        if cur.value == solved:
            if DEBUG_VAR : print('solved (depth '+str(cur.layer)+') ',cur.board," node expanded ",exp," msd ",msd)
            return cur
        del fronted[cur.value]
        explored[cur.value] = cur
        exp += 1
        i = cur.board.index('0')
        if i in range(0,2) or i in range(3,5) or i in range(6,8): expnode(cur,1,i,0) #expand right
        if i in range(1,3) or i in range(4,6) or i in range(7,9): expnode(cur,3,i,0) #expand left
        if i<6: expnode(cur,2,i,0) #expand down
        if i>2: expnode(cur,0,i,0) #expand up
    return None


# A* Search with Manhattan heuristic
def ast():
    global exp, msd, front, fronted, explored
    heappush(front,(inits.heu+inits.layer,inits.value))
    fronted[inits.value] = inits
    if DEBUG_VAR : print("init heu: "+str(inits.heu))
    while len(front)>0:
        next = heappop(front);
        cur = fronted[next[1]]
        if DEBUG_VAR :
            print('exp = ',exp)
            print('dequeued depth('+str(cur.layer)+')')
            pb(cur.board)
        if cur.value == solved:
            if DEBUG_VAR : print('solved (depth '+str(cur.layer)+') ',cur.board," node expanded ",exp," msd ",msd)
            return cur
        del fronted[cur.value]
        explored[cur.value] = cur
        exp += 1
        i = cur.board.index('0')
        if i>2: expnode(cur,0,i,1) #expand up
        if i<6: expnode(cur,2,i,1) #expand down
        if i in range(1,3) or i in range(4,6) or i in range(7,9): expnode(cur,3,i,1) #expand left
        if i in range(0,2) or i in range(3,5) or i in range(6,8): expnode(cur,1,i,1) #expand right
    return None



# Main
if DEBUG_VAR : print("\n *** DEBUG MODE ***\n")
inits, solved = State(sys.argv[2].split(','),0,None,''), 0
solved = '012345678'
explored = {} # dictionary containing explored nodes
fronted = {} # dictionary containing frontier nodes
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
