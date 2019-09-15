# -*- coding: utf-8 -*-
"""
Created on Fri Sep  6 23:29:54 2019

@author: user

NAME: SAURAV VIRMANI
ID: 2017A7PS0090P
"""
"""
    importing the necessary libraries
    tkinter for GUI
    matplotlib for Graphs
    sys for calculating size of objects
    random for generating random states
    timeit for calculating the time of execution
    priority queue for implementing uniform cost search
    
"""
import random
import sys
import timeit
import time

# for Graphical User interface
import tkinter
from tkinter import *
from tkinter import ttk

from matplotlib.backends.backend_tkagg import (
    FigureCanvasTkAgg, NavigationToolbar2Tk)
# Implement the default Matplotlib key bindings.
from matplotlib.backend_bases import key_press_handler
from matplotlib.figure import Figure
import matplotlib.pyplot as plt


#from collections import deque
from queue import PriorityQueue


#this will throw an error whenever a faulty action is taken

class WrongActionError(Exception):
    pass


"""
    the structure of the node
    it contains the state
    the action through which it is generated
    the cost of reaching this state
    number of nodes at a particular time
    number of total nodes generated
"""
class Node():
    
    number=0
    number_generated=0
    def __init__(self,state,parent,cost,parent_action):
        self.parent=parent
        self.state=state
        self.cost=cost
        self.parent_action=parent_action
        Node.number+=1
        Node.number_generated+=1
    def __lt__(self,other):
        #print("HERE2")
        return self.cost<other.cost
    
    def __del__(self):
        Node.number-=1

rows=0
cols=0
grid_dirt=0
goal_states=()
node_generated_IDS=0
node_generated_BFS=0
memory_allocated_IDS=0
memory_allocated_BFS=0
length_queue=0
total_cost_BFS=0
total_cost_IDS=0
time_IDS=0
time_BFS=0
root_node=()

BFS_count=[]
IDS_count=[]


#generation of goal states to be stored in global variable
def generateGoalStates():
    global goal_states
    goal_states=[(0,0),(rows-1,0),(rows*cols-1,0),(rows*(cols-1),0)]
    return goal_states

#function to generate dirt randomily
def generateDirt(p):
    count_present=0
    count_final=p*rows*cols//100
    grid_dirt=0 
    while(count_present!=count_final):
        row=int(random.random()*rows)
        col=int(random.random()*cols)
        if(grid_dirt & int(2**(col*rows+row))==0):
            count_present+=1
            grid_dirt |=int(2**(col*rows+row))
    return grid_dirt

#function to check whether the current state is the goal state or not
def isGoalReached(current_node):
    for state in goal_states:
        if(state[0]==current_node.state[0] and state[1]==current_node.state[1]):
            return 1
    return 0

#function to generate the successor of the current node
def successor(current_node,action):
    
    current_state=current_node.state;
    next_state=();
    cost=current_node.cost
    
    if(action==5):# 5 represent action none
        next_state=current_state
    elif(action==4):# 4 represent action clean tile
        current_position=current_state[0]
        next_grid_dirt=current_state[1] & ~(int)(2**current_position)
        next_state=(current_position,next_grid_dirt)
        cost+=1
        #print("Next State = ",next_state)
    elif(action==0):#0 represent right move
        if(current_state[0]>=rows*cols-rows and current_state[0]<rows*cols):#boundary cases
            next_state=current_state
        else:
            next_grid_dirt=current_state[1]
            next_state=(current_state[0]+rows,next_grid_dirt)
            cost+=2
            
    elif(action==1):#1 represent left move
        if(current_state[0]>=0 and current_state[0]<rows):#boundary cases
            next_state=current_state
        else:
            next_grid_dirt=current_state[1]
            next_state=(current_state[0]-rows,next_grid_dirt)
            cost+=2
            
    elif(action==2):#2 represent up move
        if(current_state[0]%rows==(rows-1)):#boundary cases
            next_state=current_state
        else:
            next_grid_dirt=current_state[1]
            next_state=(current_state[0]+1,next_grid_dirt)
            cost+=2
    
    elif(action==3):#3 represent down move
        if(current_state[0]%rows==0):#boundary
            next_state=current_state
        else:
            next_grid_dirt=current_state[1]
            next_state=(current_state[0]-1,next_grid_dirt)
            cost+=2
    else:
            raise WrongActionError()

    next_node=Node(next_state,current_node,cost,action)
    return next_node

#function to create a root node
def createRoot(grid_dirt):
    initial_position=int(random.random()*rows*cols)
    root_node=Node((initial_position,grid_dirt),None,0,0)
    return root_node

#BFS implementation
def findFinalBFS(root_node):
    global length_queue
    Node.number_generated=0
    node_pq=PriorityQueue()
    node_pq.put(root_node)
    dict_states={}    
    
    length_queue=0
    
    if(isGoalReached(root_node)):
        #print("Yes Goal State Reached")
        return root_node
            
    else:
        node_pq.put(root_node)
        while not node_pq.empty():
            #try:
            current_node=node_pq.get()
            try:
                dict_states[current_node.state]
            except KeyError:
                dict_states[current_node.state]=1;
                #print("Minimum cost till now =",current_node.cost)
                #except IndexError:
                #print("No Solution Exist For This Problem")
                
                for action in range(5):
                    successor_node=successor(current_node,action)
                    #print("Cost to reach the successor gnerated is",successor_node.cost)
                    #print("Total number of nodes in memory for bfs = ",Node.number)
                    BFS_count.append(Node.number)
                    node_pq.put(successor_node)
                    if(length_queue<node_pq.qsize()):
                        length_queue=node_pq.qsize()
                    if(isGoalReached(successor_node)):
                        #print("Yes Goal State Reached")
                        #print("Total number of nodes in memory for bfs = ",Node.number)
                        return successor_node

#recursive limited cost DFS implementation
def findFinalDFSLimited(root_node,cost,dict_states):
    #print()    
    cost_action=[2,2,2,2,1,0]
    if(cost<0):
        return None
    elif(isGoalReached(root_node)):
        return root_node
    else:
        for action in range(5):
            successor_node=successor(root_node,action)
            #print("Total number of nodes in memory for ids",Node.number)
           
            try:
                if(dict_states[successor_node.state]>successor_node.cost):
                    dict_states[successor_node.state]=successor_node.cost
                    leaf_node=findFinalDFSLimited(successor_node,cost-cost_action[action],dict_states)
                    IDS_count.append(Node.number)
                    if(leaf_node==None):
                        del successor_node
                    else:
                        return leaf_node
                    
            except KeyError:
                dict_states[successor_node.state]=successor_node.cost
                   #print(dict_states)
                leaf_node=findFinalDFSLimited(successor_node,cost-cost_action[action],dict_states)
                if(leaf_node==None):
                    del successor_node
                else:
                    return leaf_node
        return None
    
#driving function of Iterative Deepening Search
def findFinalIDS(root_node):
    Node.number_generated=0    
    cost=0;
    while(True):
        dict_states={}
        leaf_node=findFinalDFSLimited(root_node,cost,dict_states)
        if(leaf_node!=None):
            return leaf_node
        cost+=1
        #print(cost)


def performIDS():
    
    global IDS_count
    print("")
    global rows
    global cols
    global grid_dirt
    global memory_allocated_IDS
    global node_generated_IDS
    global total_cost_IDS
    global time_IDS
    
    
    IDS_count=[]
    print("GOAL STATES = ",goal_states)
    
    print("ROOT NODE = ",root_node.state)
        
    start=timeit.default_timer()
    
    leaf_node=findFinalIDS(root_node)

    end=timeit.default_timer()
    
    time_IDS=end-start
    
    print("TIME TAKEN = ",time_IDS)
    
    node_generated_IDS=Node.number_generated
    
    print("NO OF NODE GENERATED = ",node_generated_IDS)
    
    memory_allocated_IDS=sys.getsizeof(leaf_node)
    
    print("SIZE OF A NODE = ",memory_allocated_IDS)

    total_cost_IDS=leaf_node.cost
    
    print("LEAST COST = ",total_cost_IDS)
    
    print("PATH  =")
    
    IDS_path=[]
    IDS_action=[]
    while(leaf_node!=None):
        print("CURRENT STATE = ",leaf_node.state)
        print("PARENT ACTION = ",leaf_node.parent_action)
        IDS_path.append(leaf_node.state[0])
        IDS_action.append(leaf_node.parent_action)
        leaf_node=leaf_node.parent  
    
    IDS_path.reverse()
    IDS_action.reverse()
    
    print(IDS_path)
    
    delay=10
    for i,path in enumerate(IDS_path):
        row=path%rows
        col=path//rows
        if(IDS_action[i]==4):
            gridcanvas.after(delay,drawRectangle,gridcanvas,(col+2)*50,((rows-1-row)+2)*50,(col+3)*50,((rows-1-row)+3)*50,"GREEN")
        elif(IDS_action[i]<4):
            gridcanvas.after(delay,drawRectangle,gridcanvas,(col+2)*50,((rows-1-row)+2)*50,(col+3)*50,((rows-1-row)+3)*50,"RED")
        delay+=100
        
    #print("Count of number of nodes at a particular time in IDS ",IDS_count)    
def drawRectangle(canvas,x1,y1,x2,y2,color):
    canvas.create_rectangle(x1,y1,x2,y2,fill=color)
    

    
def performBFS():
    print("")
    global BFS_count
    global rows
    global cols
    global grid_dirt
    global node_generated_BFS
    global memory_allocated_BFS
    global total_cost_BFS
    global time_BFS
    global root_node
    
    BFS_count=[]
    
    print("GOAL STATES = ",goal_states)
    
    print("ROOT NODE = ",root_node.state)
    
    start=timeit.default_timer()
    
    leaf_node=findFinalBFS(root_node)
    
    end=timeit.default_timer()
    
    time_BFS=end-start
    
    print("TIME TAKEN = ",time_BFS)
    
    memory_allocated_BFS=sys.getsizeof(leaf_node)
    
    print("MEMORY ALLOCATED PER NODE = ",memory_allocated_BFS)
    
    node_generated_BFS=Node.number_generated

    print("NUMBER OF NODES GENREATED = ",node_generated_BFS)
    
    total_cost_BFS=leaf_node.cost
    
    print("\nMAX LENGTH OF QUEUE USED = "+str(length_queue))
    print("LEAST PATH COST = ",total_cost_BFS)
    print("PATH =")
    
    BFS_path=[]
    BFS_action=[]
    while(leaf_node!=None):
        print("CURRENT NODE = ",leaf_node.state)
        print("PARENT ACTION = ",leaf_node.parent_action)
        BFS_path.append(leaf_node.state[0])
        BFS_action.append(leaf_node.parent_action)
        leaf_node=leaf_node.parent  
    
    BFS_path.reverse()
    BFS_action.reverse()
    
    delay=10
    for i,path in enumerate(BFS_path):
        row=path%rows
        col=path//rows
        if(BFS_action[i]==4):
            gridcanvas.after(delay,drawRectangle,gridcanvas,(col+2)*50,((rows-1-row)+2)*50,(col+3)*50,((rows-1-row)+3)*50,"GREEN")
        elif(BFS_action[i]<4):
            gridcanvas.after(delay,drawRectangle,gridcanvas,(col+2)*50,((rows-1-row)+2)*50,(col+3)*50,((rows-1-row)+3)*50,"RED")
        delay+=100
    #print("Count of number of nodes at a particular time in IDS ",IDS_count)    
    
def performAnalysis():
    
    top=Toplevel(root)
    top.title("Analysis of Results")
    
    
    textframe = ttk.Frame(top)
    textframe.grid(column=0, row=0, sticky=(N, W))
    
    graphframe=ttk.Frame(top)
    graphframe.grid(column=1,row=0,columnspan=2,sticky=(N,W))
    
    global rows
    global cols
    global root_node
    
    goal_states=generateGoalStates()
    
    G1canvas = Canvas(graphframe)
    G1canvas.grid(column=0, row=0, sticky=(N,W))

    for x in range(cols):
        for y in range(rows):
            G1canvas.create_rectangle((x+2)*20,((rows-1-y)+2)*20,(x+3)*20,((rows-1-y)+3)*20)

    G2canvas = Canvas(graphframe)
    G2canvas.grid(column=1, row=0, sticky=(N,W))

    for x in range(cols):
        for y in range(rows):
            G2canvas.create_rectangle((x+2)*20,((rows-1-y)+2)*20,(x+3)*20,((rows-1-y)+3)*20)
                
    
    results="T1 ANALYSIS\n"
    #generation of results of BFS
    print("GOAL STATES = ",goal_states)
    
    print("ROOT NODE = ",root_node.state)
    
    start=timeit.default_timer()
    
    leaf_node=findFinalBFS(root_node)
    
    end=timeit.default_timer()
    
    time_BFS=end-start

    node_generated_BFS=Node.number_generated
    
    results+="\nR1 : NUMBER OF NODES GENERATED = "+str(node_generated_BFS)
    
    memory_allocated_BFS=sys.getsizeof(leaf_node)
    
    results+="\nR2 : MEMORY ALLOCATED PER NODE = "+str(memory_allocated_BFS)

    results+="\nR3 : MAX LENGTH OF QUEUE USED = "+str(length_queue)
   
    total_cost_BFS=leaf_node.cost
    
    results+="\nR4 : LEAST PATH COST = "+str(total_cost_BFS)
    
    results+="\nR5 : TIME TAKEN = "+str(time_BFS)
    #generation of results for IDS

    BFS_path=[]
    BFS_action=[]
    while(leaf_node!=None):
        print("CURRENT NODE = ",leaf_node.state)
        print("PARENT ACTION = ",leaf_node.parent_action)
        BFS_path.append(leaf_node.state[0])
        BFS_action.append(leaf_node.parent_action)
        leaf_node=leaf_node.parent  
    
    BFS_path.reverse()
    BFS_action.reverse()
    
    delay=10
    for i,path in enumerate(BFS_path):
        row=path%rows
        col=path//rows
        if(BFS_action[i]==4):
            G1canvas.after(delay,drawRectangle,G1canvas,(col+2)*20,((rows-1-row)+2)*20,(col+3)*20,((rows-1-row)+3)*20,"GREEN")
        elif(BFS_action[i]<4):
            G1canvas.after(delay,drawRectangle,G1canvas,(col+2)*20,((rows-1-row)+2)*20,(col+3)*20,((rows-1-row)+3)*20,"RED")
        delay+=100  
    
    results+="\n\nT2 ANALYSIS\n"
    
    print("GOAL STATES = ",goal_states)
    
    print("ROOT NODE = ",root_node.state)
        
    start=timeit.default_timer()
    
    leaf_node=findFinalIDS(root_node)

    end=timeit.default_timer()
    
    time_IDS=end-start
    
    node_generated_IDS=Node.number_generated
    
    results+="\nR6 : NUMBER OF NODES GENERATED = "+str(node_generated_IDS)
    
    memory_allocated_IDS=sys.getsizeof(leaf_node)
    
    results+="\nR7 : SIZE OF A NODE = "+str(memory_allocated_IDS)
    
    results+="\nR8 : MAXIMUM LENGTH STACK/QUEUE = NO SUCH DATASTRUCTURE USED"

    total_cost_IDS=leaf_node.cost
    
    results+="\nR9 : LEAST COST = "+str(total_cost_IDS)
    
    results+="\nR10 : TIME TAKEN = "+str(time_IDS)
    
    
    IDS_path=[]
    IDS_action=[]
    while(leaf_node!=None):
        print("CURRENT STATE = ",leaf_node.state)
        print("PARENT ACTION = ",leaf_node.parent_action)
        IDS_path.append(leaf_node.state[0])
        IDS_action.append(leaf_node.parent_action)
        leaf_node=leaf_node.parent  
    
    IDS_path.reverse()
    IDS_action.reverse()
    
    delay=10
    for i,path in enumerate(IDS_path):
        row=path%rows
        col=path//rows
        if(IDS_action[i]==4):
            G2canvas.after(delay,drawRectangle,G2canvas,(col+2)*20,((rows-1-row)+2)*20,(col+3)*20,((rows-1-row)+3)*20,"GREEN")
        elif(IDS_action[i]<4):
            G2canvas.after(delay,drawRectangle,G2canvas,(col+2)*20,((rows-1-row)+2)*20,(col+3)*20,((rows-1-row)+3)*20,"RED")
        delay+=100
        
    total_cost_IDS=0
    total_cost_BFS=0
    
    for i in range(10):
        grid_dirt=generateDirt(int(proportion_combo.get()))
        root_node=createRoot(grid_dirt)
        leaf_node=findFinalBFS(root_node)
        total_cost_BFS+=leaf_node.cost
        leaf_node=findFinalIDS(root_node)
        total_cost_IDS+=leaf_node.cost        

    IDS_memory=[]
    
    BFS_memory=[]
    
    
    IDS_count.sort(reverse=True)
    BFS_count.sort(reverse=True)
    
    for i in range(10):
        IDS_memory.append(IDS_count[i]*memory_allocated_IDS)
    
    for i in range(10):
        BFS_memory.append(BFS_count[i]*memory_allocated_BFS)
 

    results+="\nPATH BFS = "+str(BFS_path)
    results+="\nPATH IDS = "+str(IDS_path)
       
    results+="\n\nCOMPARITIVE ANALYSIS"
    
    results+="\n\nR11 : MEMORY COMPARISION FOR BFS AND IDS( MAX 10) = "
    
    results+="\nIDS\t\tBFS"
    
    for i in range(10):
        results+="\n"+str(IDS_memory[i])+" Bytes\t"+str(BFS_memory[i])+" Bytes"
        
    avg_cost_IDS=total_cost_IDS/10
    avg_cost_BFS=total_cost_BFS/10
    
    results+="\n\nAVERAGE COST FOR 10 RANDOM DIRT GRIDS = "
    results+="\nBFS = "+str(avg_cost_BFS)
    results+="\nIDS = "+str(avg_cost_IDS)    
    
    label_text = ttk.Label(textframe, text=results)
    label_text.grid(column=0,row=0,stick=W)
       
    
     
    time_BFS=[]
    time_IDS=[]
    index=[]
    
    for i in range(3,8):
        rows=i
        cols=i
        grid_dirt=generateDirt(int(proportion_combo.get()))
        root_node=createRoot(grid_dirt)
        goal_states=generateGoalStates()
        start=timeit.default_timer();
        findFinalBFS(root_node)
        end=timeit.default_timer();
        time_BFS.append(end-start)
        start=timeit.default_timer();
        findFinalIDS(root_node)
        end=timeit.default_timer();
        time_IDS.append(end-start) 
        index.append(i)
        
    graphframelower = ttk.Frame(graphframe)
    graphframelower.grid(column=0, row=1,columnspan=2,sticky=(N, W))
    
    print("Time by IDS calls ",time_IDS)
    
    fig = Figure(figsize=(4, 3), dpi=100)
    g=fig.add_subplot(111)
    g.plot(index,time_BFS,color="RED",label="T1")
    g.plot(index,time_IDS,color="BLUE",label="T2")

    G3canvas = FigureCanvasTkAgg(fig, master=graphframelower)  # A tk.DrawingArea.
    G3canvas.draw()
    G3canvas.get_tk_widget().grid(column=0,row=0,sticky=(N,W))

    rows=int(row_combo.get())
    cols=int(col_combo.get())
    
    time_proportion=[]
    proportion=[]
        
    generateGoalStates() 
    
    for i in range(0,30,5):
        proportion.append(i)
        grid_dirt=generateDirt(i)
        generateGoalStates()
        root_node=createRoot(grid_dirt)
        start=timeit.default_timer();
        try:
            findFinalIDS(root_node)
        except KeyError:
            print("Faulty State Occured")
        end=timeit.default_timer();
        time_proportion.append(end-start)
    
    fig2 = Figure(figsize=(4, 3), dpi=100)
    fig2.add_subplot(111).plot(proportion,time_proportion)

    G4canvas = FigureCanvasTkAgg(fig2, master=graphframelower)  # A tk.DrawingArea.
    G4canvas.draw()
    G4canvas.get_tk_widget().grid(column=1,row=0,sticky=(N,W))

        

    
    
    return None
    
def createDirtGrid():
    
    global gridcanvas
    global row_combo
    global col_combo
    global rows
    global cols
    global grid_dirt
    global goal_states
    global root_node
    
    gridcanvas.delete('all')
    rows=int(row_combo.get())
    cols=int(col_combo.get())
    
    grid_dirt=generateDirt(int(proportion_combo.get()))
    
    goal_states=generateGoalStates()
    
    root_node=createRoot(grid_dirt)    
    
    for x in range(cols):
        for y in range(rows):
            if(root_node.state[0]==(x*rows+y)):
                gridcanvas.create_rectangle((x+2)*50,((rows-1-y)+2)*50,(x+3)*50,((rows-1-y)+3)*50,fill="BLACK")
            elif(grid_dirt & int(2**(x*rows+y))):
                gridcanvas.create_rectangle((x+2)*50,((rows-1-y)+2)*50,(x+3)*50,((rows-1-y)+3)*50,fill="BROWN")
            else:
                gridcanvas.create_rectangle((x+2)*50,((rows-1-y)+2)*50,(x+3)*50,((rows-1-y)+3)*50)
                
    
    
def execute():
    global choice
    #print("Ha executed")
    #print(choice)
    ch=int(choice.get())
    if(ch==1):     
        createDirtGrid()
    elif(ch==2):
        performIDS()
    elif(ch==3):
        performBFS()
    else:
        performAnalysis()

root = Tk()
root.title("Room Cleaning Intelligent Vacuum Cleaner")
root.geometry('1200x700')

mainframe = ttk.Frame(root)
mainframe.grid(column=0, row=0, sticky=(N, W, E, S))

root.columnconfigure(0, weight=1)
root.rowconfigure(0, weight=1)

gridframe = ttk.Frame(root)
gridframe.grid(column=1, row=0, sticky=(N, W))
    
gridcanvas = Canvas(gridframe,width=700,height=700)
gridcanvas.grid(column=0, row=0, sticky=(N,W))
#gridcanvas.create_line(1000, 700, 200, 50)



row_combo = ttk.Combobox(mainframe,)
row_combo.grid(column=2,row=1,sticky=W)
    
col_combo = ttk.Combobox(mainframe,)
col_combo.grid(column=2,row=2,sticky=W)
    
proportion_combo = ttk.Combobox(mainframe,)
proportion_combo.grid(column=2,row=3,sticky=W)
    
#print(row_combo)
    
row_combo['values'] = (2, 3,4,5,6,7,8,9,10,15,20)
col_combo['values'] = (2, 3,4,5,6,7,8,9,10,15,20)    
proportion_combo['values'] = (10, 20, 30,40,50,60,70,80,90,100)

label_row = ttk.Label(mainframe, text='No of Rows : ')
label_row.grid(column=1,row=1,stick=W)
    
label_col = ttk.Label(mainframe, text='No of Columns : ')
label_col.grid(column=1,row=2,stick=W)    

label_proportion = ttk.Label(mainframe, text='Proportion of Dirt : ')
label_proportion.grid(column=1,row=3,stick=W)   

button_execute=ttk.Button(mainframe, text="Execute", command=execute)
button_execute.grid(column=9, row=9, sticky=W)
    
choice = StringVar()
generate_dirt = ttk.Radiobutton(mainframe, text='Generate Dirt Layout', variable=choice, value='1')
perform_IDS = ttk.Radiobutton(mainframe, text='Calculate Least Cost using IDS', variable=choice, value='2')
perform_BFS = ttk.Radiobutton(mainframe, text='Calculate Least Cost using BFS', variable=choice, value='3')
perform_Analysis = ttk.Radiobutton(mainframe, text='Compare the two techniques', variable=choice, value='4')

generate_dirt.grid(column=2,row=5,stick=W)
perform_IDS.grid(column=2,row=6,stick=W)
perform_BFS.grid(column=2,row=7,stick=W)
perform_Analysis.grid(column=2,row=8,stick=W)

label_choice = ttk.Label(mainframe, text='Select the action to perform : ')
label_choice.grid(column=1,row=4,stick=W)

for child in mainframe.winfo_children(): child.grid_configure(padx=10, pady=10)

#for child in gridframe.winfo_children(): child.grid_configure(padx=10, pady=10)
    #feet_entry.focus()
    #root.bind('<Return>', calculate)

root.mainloop()