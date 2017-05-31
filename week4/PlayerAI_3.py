from random import randint
from BaseAI_3 import BaseAI
import time
import math

directionVectors = (UP_VEC, DOWN_VEC, LEFT_VEC, RIGHT_VEC) = ((-1, 0), (1, 0), (0, -1), (0, 1))

# node_type: 0 for player, 1 for tile insertion
class State:
    def __init__(self,grid,move,node_type):
        self.grid = grid
        self.move = move
        self.type = node_type
    def canMove(self, dir): # dir in [0,3] up,down,left,right
        for x in range(self.grid.size):
            for y in range(self.grid.size):
                # If Current Cell is Filled
                if self.grid.map[x][y]:
                    # Look Ajacent Cell Value
                    move = directionVectors[dir]
                    adjCellValue = self.grid.getCellValue((x + move[0], y + move[1]))
                    # If Value is the Same or Adjacent Cell is Empty
                    if adjCellValue == self.grid.map[x][y] or adjCellValue == 0:
                        return True
                # Else if Current Cell is Empty
                elif self.grid.map[x][y] == 0:
                    return True
        return False
    def children(self): # ret list of State
        children = []
        if self.type == 0 :
            # expand player move
            for i in range(4):
                if self.canMove(i):
                    newgrid = self.grid.clone()
                    newgrid.move(i)
                    children.append(State(newgrid,i,1))
            return children
        if self.type == 1 :
            # expand tile insertion move
            for cell in self.grid.getAvailableCells():
                newgrid = self.grid.clone()
                newgrid.setCellValue(cell,2)
                children.append(State(newgrid,(cell,2),0))
                newgrid = self.grid.clone()
                newgrid.setCellValue(cell,4)
                children.append(State(newgrid,(cell,4),0))
            return children

class PlayerAI(BaseAI):
    def getMove(self, grid):
        startp = time.clock()
        inits = State(grid,None,0)
        termDepth = 2
        bestmove = 0
        while time.clock() - startp < 0.19:
            termDepth += 1
            state,util = self.maximize(inits,-1,2000,startp,0,termDepth) # -1,17 just for naive heur
            if util != None and state.move != None : bestmove = state.move
        return bestmove


    def heur(self,grid):
        # h1 num of available cells
        availableC = len(grid.getAvailableCells())
        if availableC > 4 : h1 = 100
        else : h1 = availableC*20
        # h2 max tile in the corner, h3 same value near
        h3 = 0

        maxT = grid.map[0][0]
        xMaxT, yMaxT = (0,0)
        for x in range(1,grid.size):
            if grid.map[x][0] > 4 and grid.map[x-1][0] != 0:
                adj = abs(math.log2(grid.map[x][0]/grid.map[x-1][0]))
                h3 += 7*math.log2(grid.map[x][0])-5*adj
            if grid.map[x][0] > maxT :
                maxT = grid.map[x][0]
                xMaxT, yMaxT = (x,0)
            for y in range(1,grid.size):
                if grid.map[x][y] > 4:
                    if grid.map[x][y-1] != 0:
                        adj1 = abs(math.log2(grid.map[x][y]/grid.map[x][y-1]))
                    else : adj1 = float("+inf")
                    if grid.map[x-1][y] != 0:
                        adj2 = abs(math.log2(grid.map[x][y]/grid.map[x-1][y]))
                    else : adj2 = float("+inf")
                    adj = min(adj1,adj2)
                    if adj != float("+inf"):
                        h3 += 10*math.log2(grid.map[x][y])-5*adj
                if grid.map[x][y] > maxT :
                    maxT = grid.map[x][y]
                    xMaxT, yMaxT = (x,y)

        h2 = 0
        if (xMaxT == 0 or xMaxT == grid.size-1) or (yMaxT == 0 or yMaxT == grid.size-1) : h2 = 150
        if (xMaxT == 0 or xMaxT == grid.size-1) and (yMaxT == 0 or yMaxT == grid.size-1) : h2 = 300

        return h1+h2+h3

    def maximize(self,state,a,b,startp,currDepth,maxDepth):
        if time.clock() - startp > 0.19 :
            return None,None
        if currDepth == maxDepth:
            return None,self.heur(state.grid)
        maxChild, maxUtil = state, float("-inf")
        for child in state.children():
            _, util = self.minimize(child,a,b,startp,currDepth+1,maxDepth)
            if util == None : return None,None # Check timeout
            if util > maxUtil : maxChild, maxUtil = child, util
            if maxUtil >= b: break
            if maxUtil > a: a = maxUtil
        return maxChild, maxUtil

    def minimize(self,state,a,b,startp,currDepth,maxDepth):
        if time.clock() - startp > 0.19 :
            return None,None
        if currDepth == maxDepth:
            return None,self.heur(state.grid)
        minChild, minUtil = state, float("inf")
        for child in state.children():
            _, util = self.maximize(child,a,b,startp,currDepth+1,maxDepth)
            if util == None : return None,None # Check timeout
            if util < minUtil : minChild, minUtil = child, util
            if minUtil <= a : break
            if minUtil < b : b = minUtil
        return minChild, minUtil
