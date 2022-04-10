class Node:
    def __init__(self, data):
        self.adj = []  #lista de adjacencia, inicialmente esta vazia
        self.data = data  #infomacao que esta no nó
        self.dist = 0 # eh a distancia ate a raiz
        self.visit = False
        self.dad = None
        self.finalized = False

                                   
def create_tree(T):
    tree = {}

    for tupl in T:
        if not tupl[0] in tree : 
            v = Node(tupl[0] )
            tree[ tupl[0] ] = v
        if not tupl[1] in tree :
            u = Node(tupl[1] )
            tree[ tupl[1] ] = u

        tree[tupl[0]].adj.append(tupl[1]) 

    return tree
    

def dfs(G, v, tree, dist) :
    v.visit = True
    if(v.data == 's'): #se for a raiz
        v.dist = 0 
        v.dad = None
    else: 
        v.dist = v.dad.dist + G.edge_label( v.dad.data , v.data)
        

    dist[v.data] = v.dist 
    
    for w in v.adj :
        if(tree[w].visit == False) :
            tree[w].dad = v
            dfs(G, tree[w], tree, dist)

    v.finalized = True

def is_smaller_tree(G, T):
    tree =  create_tree(T)
    dist = {}
    dfs(G, tree['s'], tree, dist) 
   
    for u, v, w in G.edge_iterator():
        if dist[v] > dist[u] + w : #se precisa relaxar
	        return False  # T nao eh SPT
       
    return True 
        

G = DiGraph({'s':{'u':10,'x':5},
'u':{'v':1,'x':2},
'v':{'y':4},
'x':{'u':3,'v':9,'y':2},
"y":{"s":7,"v":6}})

T =[('s', 'x'),
('x', 'u'),
('x', 'y'),
('u', 'v')]

print(is_smaller_tree(G, T))