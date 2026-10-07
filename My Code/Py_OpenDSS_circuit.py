import pandas as pd
from dss import dss
import numpy as np
#OpenDSS helper functions for defining, reading, and writing Circuits

# Function defining the circuit data frame structure
def new():
    # define a list of data frames for each circuit component type
    # the field names in the dss package can be differnet to those used in OpenDSS.. i.e. for the Loads
    Main = pd.DataFrame(columns = ['Main'])
    dss_Main = []
    
    Info = pd.DataFrame(columns = ['Info','Name'])
    dss_Info = []
    
    LineCodes = pd.DataFrame(columns = ['LineCodes','NormAmps'])
    dss_LineCodes = []
    
    Vsources = pd.DataFrame(columns = ['Vsources','Frequency','BasekV','pu'])
    dss_Vsources = ['','ignore','','','','']
    
    ActiveBus = pd.DataFrame(columns = ['ActiveBus','x','y','LoadList','Depth','Volts'])
    dss_ActiveBus = []
    
    Lines = pd.DataFrame(columns = ['Lines','Bus1','Bus2','LineCode','Length','x1','y1','x2','y2'])
    dss_Lines = ['','','','','','ignore','ignore','ignore','ignore']
    
    Transformers = pd.DataFrame(columns = ['Transformers','Bus1','Bus2','Voltage1','Voltage2','Current1','Current2'])
    dss_Transformers = [];
    
    Loads = pd.DataFrame(columns = ['Loads','phases','Bus1','kV','Model','conn','kW','pf','yearly','daily','Volts','Current','Distance','x','y','phase'])
    dss_Loads = ['','Phases','ignore','','','ignore','','PF','Yearly','ignore','ignore','ignore','ignore','ignore','ignore','']
    
    LoadShapes = pd.DataFrame(columns = ['LoadShapes','Npts','Pmult','Qmult','HrInterval'])
    dss_LoadShapes = [];
    
    #add the data frames into a list with the first item in the list being the names of the dataframes
    order = ['Main','Info','LineCodes','Vsources','ActiveBus','Lines','Transformers','Loads','LoadShapes']
    dss_order = ['dss_Main','dss_Info','dss_LineCodes','dss_Vsources','dss_ActiveBus','dss_Lines','dss_Transformers','dss_Loads','dss_LoadShapes']
    
    Circuit = [order]
    dss_names = [dss_order]
    for o in order[1:]:
        exec('Circuit.append(' +  o + ')')
    for o in dss_order[1:]:
        exec('dss_names.append(' +  o + ')')
        
    return [Circuit,dss_names]


def OpenDSS_circuit_compact(*args):
    #very compact script for looping through each dataframe in list using words...
    #### has potential for use.. but debugging field codes is tiresome.
    Circuit = args[0]
    dss_names = args[1]
    AC = dss.ActiveCircuit
    AC_ = pd.DataFrame(columns = Circuit[0])
    for bi,b in enumerate(Circuit[0]):
        if bi <= 1:
            _=0
        else:
            if b == 'Buses':
                Circuit[bi][b] = AC.AllBusNames    
            else:
                exec('Circuit[bi][b] = AC.' + b + '.AllNames')
            
            exec('AC_.loc[0,b] = AC.' + b)
            for c,a in enumerate(AC_[b][0]):
                for e,col in enumerate(Circuit[bi].columns[1:]):
                    if len(dss_names[bi]) > 1:
                        if dss_names[bi][e+1] == 'ignore':
                            _=0
                        elif len(dss_names[bi][e+1]) > 1:
                            exec('Circuit[bi].at[c,col] = a.' + dss_names[bi][e+1])
                        else:
                            exec('Circuit[bi].at[c,col] = a.' + col)
                    else:
                        exec('Circuit[bi].at[c,col] = a.' + col)
                        
    return Circuit

# Function to assign which bus each load is connected to
def bus_loadlist_2_load_buses(*args):
    # function to get buses for loads from buses['loadlist']
    Circuit = args[0]
    b = Circuit[0].index('ActiveBus')
    c = Circuit[0].index('Loads')
    for l in range(len(Circuit[b])):
        bus = Circuit[b]['ActiveBus'][l]
        loadlist = Circuit[b]['LoadList'][l]
        for m in loadlist:
            if len(m) > 0:
                Circuit[c].loc[list(Circuit[c]['Loads']).index(m[5:]),'Bus1'] = bus
    return Circuit
    
def xy_buses2linesloads(*args):
    #function to copy x,y co-ordinates from buses into lines and loads etc.
    Circuit = args[0]
    b = Circuit[0].index('ActiveBus')
    
    c = Circuit[0].index('Lines')
    for l in range(len(Circuit[b])):
        idb = Circuit[b]['ActiveBus'].isin([Circuit[c]['Bus1'][l]])
        Circuit[c].loc[l,'x1'] = Circuit[b]['x'][idb]
        Circuit[c].loc[l,'y1'] = Circuit[b]['y'][idb]
        idb = Circuit[b]['ActiveBus'].isin([Circuit[c]['Bus2'][l]])
        Circuit[c].loc[l,'x2'] = Circuit[b]['x'][idb]
        Circuit[c].loc[l,'y2'] = Circuit[b]['y'][idb]
        
    c = Circuit[0].index('Loads')
    for l in range(len(Circuit[b])):
        idb = Circuit[b]['Bus'].isin([Circuit[c]['Bus1'][l]])
        Circuit[c].loc[l,'x'] = Circuit[b]['x'][idb]
        Circuit[c].loc[l,'y'] = Circuit[b]['y'][idb]

def length2depth(*args):
    #function to convert X,Y to physical displacement from source using xy
    #start at the sourcebus
    #we may have a transformer or line for the sourcebus.. code will need ammending if reactors, fuses etc are in the circuit
    Circuit = args[0]
    a = Circuit[0].index('ActiveBus')
    b = Circuit[0].index('Transformers')
    c = Circuit[0].index('Lines')
    #initiate a data struture
    
    #form an array of buses so they always go from Bus1 to Bus2
    B1 = list(Circuit[b]['Bus1']) + list(Circuit[c]['Bus1'])
    B2 = list(Circuit[b]['Bus2']) + list(Circuit[c]['Bus2'])
    Elements = list(Circuit[b].columns[0] + '.'+ Circuit[b][Circuit[b].columns[0]]) + list(Circuit[c].columns[0] + '.' + Circuit[c][Circuit[c].columns[0]])
    Length = list(np.zeros(len(Circuit[b])) ) + list(Circuit[c]['Length'])
        
    Buses = [['sourcebus']]
    Indices = [[B1.index('sourcebus')]]
    Tree = [['sourcebus']]
    Depth = [[0]]
    
    i = 0
    while len(B1) > 0 and i < 300:
        #print(len(B1))
        I = []
        B = []
        D = []
        E = []
        for n in range(len(Buses[i])):
            index1 = [k for k, x in enumerate(B1) if x == Buses[i][n]]
            index2 = [k for k, x in enumerate(B2) if x == Buses[i][n]]
            #add to depth of tree
            [I.append(index1[x]) for x in range(len(index1))]
            [I.append(index2[x]) for x in range(len(index2))]
            [B.append(B2[index1[x]]) for x in range(len(index1))]
            [B.append(B1[index2[x]]) for x in range(len(index2))]
            [D.append(Depth[i][n]+Length[index1[x]]) for x in range(len(index1))]
            [D.append(Depth[i][n]+Length[index2[x]]) for x in range(len(index2))]
            [E.append(Elements[index1[x]]) for x in range(len(index1))]
            [E.append(Elements[index2[x]]) for x in range(len(index2))]
        Indices.append(index1 + index2)
        Buses.append(B)
        Depth.append(D)
        Tree.append(E)
        #now remove the lines
        for x in sorted(I, reverse = True):
            del B1[x]
            del B2[x]
            del Elements[x]
            del Length[x]
        i = i + 1
    BS = np.concatenate(Buses)
    DP = np.concatenate(Depth)
    for idb,x in enumerate(BS):
        idx = np.where(Circuit[a]['ActiveBus']==x)[0][0]
        Circuit[a].loc[idx,'Depth'] = DP[idb]
    return Circuit