from random import randint
from BaseAI_3 import BaseAI
import time

class PlayerAI(BaseAI):
    def getMove(self, grid):
        startp = time.clock()
        termDepth = 2
        bestmove = 0
        while time.clock() - startp < 0.19:
            termDepth += 1
            move,grid,ut = self.maximize(grid,float('-inf'),float('+inf'),startp,0,termDepth)
            if move != -1 : bestmove=move
        return bestmove


    def heur(self,grid):
        return len(grid.getAvailableCells())

    def maximize(self,grid,a,b,startp,currDepth,maxDepth):
        if time.clock() - startp > 0.19 :
            return -1,-1,-1
        if currDepth == maxDepth: # play safe
            return 0,grid,self.heur(grid)
        moveToChoose,maxC, maxU = 0,grid,float("-inf")
        moves = grid.getAvailableMoves()
        for move in moves:
            newgrid = grid.clone()
            newgrid.move(move)
            genMove, minC, util = self.minimize(newgrid,a,b,startp,currDepth+1,maxDepth)
            if minC == -1 : return -1,-1,-1 # Check timeout
            if util > maxU : moveToChoose, maxC, maxU = move, minC, util
            if maxU >= b: break
            if maxU > a: a=maxU
        return moveToChoose,maxC,maxU

    def minimize(self,grid,a,b,startp,currDepth,maxDepth):
        if time.clock() - startp > 0.19 :
            return -1,-1,-1
        if currDepth == maxDepth: # play safe
            return 0,grid,self.heur(grid)
        moveToChoose,minC, minU = 0,grid,float("inf")
        moves = grid.getAvailableCells()
        for move in moves:
            newgrid = grid.clone()
            newgrid.setCellValue(move,2)
            genMove, maxC, util = self.maximize(newgrid,a,b,startp,currDepth+1,maxDepth)
            if maxC == -1 : return -1,-1,-1 # Check timeout
            if util < minU : moveToChoose, minC, minU = move,maxC, util
            if minU <= a: break
            if minU < b: b=minU

            newgrid = grid.clone()
            newgrid.setCellValue(move,4)
            genMove, maxC, util = self.maximize(newgrid,a,b,startp,currDepth+1,maxDepth)
            if maxC == -1 : return -1,-1,-1 # Check timeout
            if util < minU : moveToChoose, minC, minU = move, maxC, util
            if minU <= a: break
            if minU < b: b=minU
        return moveToChoose,minC,minU




            #, self.getNewTileValue())
