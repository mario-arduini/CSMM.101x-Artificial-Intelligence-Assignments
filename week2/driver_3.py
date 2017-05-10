import sys
from collections import deque
class State:
    def __init__(self,board,layer,parent,move):
        self.board = board
        self.value = 0
        for i in range(1,9):
            self.value += int(board[i])*i
        self.layer = layer
        self.par = parent
        self.parmove = move

def pb(board):
    print(board[:3])
    print(board[3:6])
    print(board[6:9])

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
    output='path _to_goal: '+pathstr+'\ncost_of_path: '+layer+'\nnodes_expanded: '+str(exp)+'\nsearch_depth: '+layer+'\nmax_search_depth: '+str(msd)
    f.write(output)
    #f.write(('\nrunning_time: ',rt))
    #f.write(('\nmax_ram_usage: ',mu))

def bfs():
    front = deque([inits])
    exp=0
    msd=0
    while len(front)>0:
        cur = front.popleft()
        exp += 1

        print('exp = ',exp)
        print('dequeued depth('+str(cur.layer)+')')
        pb(cur.board)

        if cur.value == solved:
            print('solved (depth '+str(cur.layer)+') ',cur.board," node expanded ",exp," msd ",msd)
            return (cur,exp,msd)
        del fronted[cur.value]
        explored[cur.value] = cur
        for i in range(len(cur.board)):
            if cur.board[i] == '0':
                if i>2:
                    #expand up
                    newboard = cur.board.copy()
                    swap=newboard[i-3]
                    newboard[i-3]=newboard[i]
                    newboard[i]=swap
                    new = State(newboard,cur.layer+1,cur,'Up')
                    if not (new.value in explored or new.value in fronted):
                        print('new node generated from "up" (depth '+str(new.layer)+' ) move: ')
                        pb(new.board)
                        if new.layer > msd : msd = new.layer
                        fronted[new.value]=new
                        front.append(new)
                if i<6:
                    #expand down
                    newboard = cur.board.copy()
                    swap=newboard[i+3]
                    newboard[i+3]=newboard[i]
                    newboard[i]=swap
                    new = State(newboard,cur.layer+1,cur,'Down')
                    if not (new.value in explored or new.value in fronted):
                        print('new node generated from "down" (depth '+str(new.layer)+' ) move: ')
                        pb(new.board)
                        if new.layer > msd : msd = new.layer
                        fronted[new.value]=new
                        front.append(new)
                if i in range(1,3) or i in range(4,6) or i in range(7,9):
                    #expand left
                    newboard = cur.board.copy()
                    swap=newboard[i-1]
                    newboard[i-1]=newboard[i]
                    newboard[i]=swap
                    new = State(newboard,cur.layer+1,cur,'Left')
                    if not (new.value in explored or new.value in fronted):
                        print('new node generated from "left" (depth '+str(new.layer)+' ) move: ')
                        pb(new.board)
                        if new.layer > msd : msd = new.layer
                        fronted[new.value]=new
                        front.append(new)
                if i in range(0,2) or i in range(3,5) or i in range(6,8):
                    #expand right
                    newboard = cur.board.copy()
                    swap=newboard[i+1]
                    newboard[i+1]=newboard[i]
                    newboard[i]=swap
                    new = State(newboard,cur.layer+1,cur,'Right')
                    if not (new.value in explored or new.value in fronted):
                        print('new node generated from "right" (depth '+str(new.layer)+' ) move: ')
                        pb(new.board)
                        if new.layer > msd : msd = new.layer
                        fronted[new.value]=new
                        front.append(new)
                break
    return None


def dfs():
    pass

def ast():
    pass

inits = State(sys.argv[2].split(','),0,None,'')
solved = 0
for i in range(1,9):
    solved += i*i
explored = {}
fronted = {inits.value : inits}
if sys.argv[1] == 'bfs':
    print('bfs calling:')
    solution = bfs()
elif sys.argv[1] == 'dfs':
    print('dfs calling:')
    solution = dfs()
elif sys.argv[1] == 'ast':
    print('ast calling:')
    solution = ast()
if solution is not None: outgen(solution)
