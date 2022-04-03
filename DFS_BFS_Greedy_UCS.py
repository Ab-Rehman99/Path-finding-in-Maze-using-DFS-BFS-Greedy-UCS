from __future__ import annotations

from typing import Callable, TypeVar,Generic,Optional,List,Deque,Dict
from collections import deque
from heapq import heappush, heappop


# for simplicity "S" is cell_positon


S=TypeVar('S') # for int, string any type


class Stack(Generic[S]):
    def __init__(self) -> None:
        self.L: List[S] = []

    @property
    def empty(self):
        if self.L:
            return False
        else:
            return True 

    def add(self, item: S) -> None:
        self.L.append(item)

    def p0p(self) -> S:
        return self.L.pop()  # LIFO

    def __repr__(self) -> str:
        return repr(self.L)

class Q(Generic[S]):
    def __init__(self) -> None:
        self.q: Deque[S]=deque()    
    @property
    def empty(self):
        if self.q:
            return False
        else:
            return True   

    def push_right(self, item: S) -> None:
        self.q.append(item)

    def p0p(self) -> S:
        return self.q.popleft() 

    def __repr__(self) -> str:
        return repr(self.q)
            
class PriorityQueue(Generic[S]):
    def __init__(self) -> None:
        self.l: List[S] = []

    @property
    def empty(self):
        if self.l:
            return False
        else:
            return True    

    def push(self, item: S) -> None:
        heappush(self.l, item)  # use in huaristic

    def pop(self) -> S:
        return heappop(self.l)  

    # def __repr__(self) -> str:
    #     return repr(self.l)

# node is some position in maze and parent is from where we get taht node
class box(Generic[S]):
    def __init__(self, state: S, p: Optional[box], cost = 0.0, h = 0.0) -> None:
        self.state = state
        self.p= p
        self.cost = cost
        self.h= h

    def __lt__(self, other: box) -> bool:
        return (self.cost + self.h) < (other.cost + other.h)

#helper function for backtracking using parent node
def goal_to_start(n: box[S]) -> List[S]:
    b_p: List[S] = [n.state]

    while n.p is not None:
        b_p.append(n.state)
        n=n.p
    b_p.reverse()
    return b_p

    
def DFS(start: S,check_end:Callable[[S], bool ],chck_next_node:Callable[[S], List[S] ]) -> Optional[box[S]]:

       
        my_stac = Stack()
        state=box(start, None)
        my_stac.add(state)
     
        visited: List[S] = [start]

        
        while  my_stac.empty == False:
            recent_box = my_stac.p0p()
            current_state = recent_box.state
            
            if check_end(current_state) == True: # if goal state has been reached.........
                return recent_box
            else:
                for elements in chck_next_node(current_state):
                    if elements in visited:  
                        continue
                    else:

                        visited.append(elements)
                        state=box(elements, recent_box)
                        my_stac.add(state)
        return None  




def BFS(start: S,check_end:Callable[[S], bool ],chck_next_node:Callable[[S], List[S] ]) -> Optional[box[S]]:

       
        my_stac = Q()
        state=box(start, None)
        my_stac.push_right(state)
     
        visited: List[S] = [start]

        
        while my_stac.empty == False:
            recent_box = my_stac.p0p()  ##first in first out 
            current_state = recent_box.state
            # if goal state has been reached.........
            if check_end(current_state) == True:
                return recent_box
            else:  # else traverse 
                for elements in chck_next_node(current_state):
                    if elements in visited:  
                        continue
                    else:

                        visited.append(elements)
                        sate=box(elements, recent_box)
                        my_stac.push_right(sate)
        return None  

def uniform(start: S, check_end: Callable[[S], bool], chck_next_node: Callable[[S], List[S]]) -> Optional[box[S]]:
    
    my_p_q = PriorityQueue()
    satte=box(start, None,0.0 )
    my_p_q.push(satte)

    visited: Dict[S, float] = {start: 0.0}

    while  my_p_q.empty== False:
        recent_box = my_p_q.pop()
        current_state = recent_box.state
      
        if check_end(current_state) == True:  # if goal state has been reached.........
            return recent_box
        else:
            for elements in chck_next_node(current_state):
                n_c = recent_box.cost + 1  

                if elements not in visited or  n_c < visited[elements] :
                    visited[elements] = n_c
                    state=box(elements, recent_box, n_c)
                    my_p_q.push(state)
    return None  


def best_first(initial: S, check_end: Callable[[S], bool], chck_next_node: Callable[[S], List[S]], h: Callable[[S], float]) -> Optional[box[S]]:


    my_p_q = PriorityQueue()
    state=box(initial, None, h(initial))
    my_p_q.push(state)
   
    visited: Dict[S, float] = {initial: 0.0}


    
    while  my_p_q.empty == False:
        recent_box = my_p_q.pop()
        current_state = recent_box.state
        
        if check_end(current_state) == True:  # if goal state has been reached.........
            return recent_box
        else:    
        
            for elements in chck_next_node(current_state):
                n_c = recent_box.cost + 0.0  

                if elements not in visited or n_c < visited[elements]:
                    visited[elements] = n_c
                    state:box=box(elements, recent_box, n_c, h(elements))
                    my_p_q.push(state)
    return None 


  



