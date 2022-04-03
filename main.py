from enum import Enum
from tkinter.ttk import *
from typing import NamedTuple, Optional,Callable,Set
from tkinter import *
from typing import List
from DFS_BFS_Greedy_UCS import BFS, box,DFS,goal_to_start,best_first,uniform
from DFS_BFS_Greedy_UCS import goal_to_start
import random
from collections import deque

# class for cell Position
class cell_positon(NamedTuple):  # namedtupes since use row and col as tuple
    r: int
    c: int

# cell class containg all the possiblities of a cell
class cell(str,Enum):
    path="*"
    staring_posi="S"
    ending_posi="E"
    obstracle="O"
    khali=" "

#class Grid
class grid:
    #default constructor:
    def __init__(self, row: int = 10, col: int = 10,start:cell_positon=cell_positon(9,0), end:cell_positon=cell_positon(0,9)) ->None:
        self.row: int = row
        self.col: int = col
        self.start: cell_positon = start
        self.end: cell_positon = end

        # fill the grid empty cells
        self.g : List[List[cell]]  =   [[cell.khali for col in range(col)] for r0ws in range(row)] 

        # generate random obstacles
        self.genaerate_obstacles(row,col)

        #setting start and ending position

        self.g[start.r][start.c]=cell.staring_posi
        self.g[end.r][end.c]=cell.ending_posi
    
    def genaerate_obstacles(self,row:int, col:int):
        a = 0.25  #filling only 20% of grid with obstacles
        for rows in range(row):
                for cols in range(col):
                    if random.uniform(0, 1.5) < a:
                        self.g[rows][cols] = cell.obstracle

    #outputting the 2D list

    def output_grid(self):
        for row in self.g:
            for elem in row:
                print(elem, end=' ')
            print()

    def __str__(self) -> str:
        result: str = ""
        for r in self.g:
            result += " ".join([elem.value for elem in r]) + "\n"
        return result

    

    def check_end(self,c_p:cell_positon)-> bool:
        return c_p == self.end
         
    #given a node(cell position) it will return a list containing the next nodes where u can go simplay checking obstacles and adding those nodes where uu can go
    def chck_next_node(self, c_p:cell_positon) -> List[cell_positon]:
        p: List[cell_positon]=[]
        # go one row down:
        if self.row > c_p.r + 1 and self.g[c_p.r +1][c_p.c] != cell.obstracle:
            p.append( cell_positon(c_p.r +1,c_p.c) )# append that cell which is not an obstracle
        
        # go one row up:
        if  c_p.r - 1 >=0 and self.g[c_p.r -1][c_p.c] != cell.obstracle:
            p.append( cell_positon(c_p.r -1,c_p.c) )# append that cell which is not an obstracle  

        # go one col up:
        if  self.col > c_p.c + 1  and self.g[c_p.r][c_p.c+1] != cell.obstracle:
            p.append( cell_positon(c_p.r,c_p.c+1) )# append that cell which is not an obstracle    

        # go one col down:
        if c_p.c -1 >= 0 and self.g[c_p.r][c_p.c - 1] != cell.obstracle:
            p.append(cell_positon( c_p.r,c_p.c-1) )   
       
        return p     
     # mark the path with "*""
    def mark_the_path(self, p:List[cell_positon]):

        for c_p in p:
            self.g[c_p.r][c_p.c]=cell.path

        self.g[self.start.r][self.start.c]=cell.staring_posi
        self.g[self.end.r][self.end.c]=cell.ending_posi


    def make_claer(self,p:List[cell_positon]):
        for items in p:
            self.g[items.r][items.c]=cell.khali

        self.g[self.start.r][self.start.c]=cell.staring_posi
        self.g[self.end.r][self.end.c]=cell.ending_posi

def manhattan_distance(goal: cell_positon) -> Callable[[cell_positon], float]:
    def distance(ml: cell_positon) -> float:
        xdist = abs(ml.c - goal.c)
        ydist = abs(ml.r - goal.r)
        return (xdist + ydist)
    return distance


def dfs(s_p: cell_positon):
    stack = deque()
    stack.append(s_p)
    explored: Set = {s_p}

    while not stack.empty:
            current_node: cell_positon = stack.pop()
            # current_state: T = current_node.state
            # if we found the goal, we're done
            if g.check_end(current_node):
                return current_node
            # check where we can go next and haven't explored
            for next in g.chck_next_node(current_node):
                if next in explored:  # skip children we already explored
                    continue
                explored.add(next)
                stack.push(next)
    return None  # went through everything and never found goal


     
if __name__ == "__main__":


    #DfS
    rows=int(input("Enter Number of Rows :"))
    cols=int(input("Enter Number of cols :"))
    s: cell_positon=cell_positon(rows-1,0)
    e:cell_positon=cell_positon(0,cols-1)

   
    g: grid=grid(rows,cols,s,e)
    print(g)
    #DFS

    res_DFS=DFS(g.start,g.check_end,g.chck_next_node) # passing two functions "check_end" "check_next_node"
    if res_DFS :
        print("----------------------------------------------")
        print("Path: DFS \n")
        way: List[cell_positon]=goal_to_start(res_DFS)
        g.mark_the_path(way)
        print(g)
        g.make_claer(way)
        
    else:
        print("Solution Does not exist for dFS ")


    # BFS 
    res_bfs=BFS(g.start,g.check_end,g.chck_next_node)
   
    if res_bfs :
        print("----------------------------------------------")
        print("Path: BFS \n")
        way_bfs: List[cell_positon]=goal_to_start(res_bfs)
        g.mark_the_path(way_bfs)
        print(g)
        g.make_claer(way_bfs)
       
    else:
        print("Solution Does not exist for BFS")


    #Uniform cost Search
    print("----------------------------------------------")
    print("Path: Uniform cost Search \n")

    res_UCS= uniform(g.start,g.check_end,g.chck_next_node)

    if res_UCS :
        way_UCS = goal_to_start(res_UCS)
        g.mark_the_path(way_UCS)
        print(g)
        g.make_claer(way_UCS)  
        
    else:
        print("No solution found using uniform cost")

    # Greedy (best first Search) *
    print("----------------------------------------------")
    print("Path: Greedy (best first Search) \n")
    distance = manhattan_distance(g.end)
    res_greedy = best_first(g.start,g.check_end,g.chck_next_node, distance)
    if res_greedy :
        way_greedy = goal_to_start(res_greedy)
        g.mark_the_path(way_greedy)
        print(g)
        g.make_claer(way_greedy)

        
    else:
        print("No solution found using best first")
 

