#scripts for setting Circuit components in OpenDSS

import pandas as pd
#helper functions for setting and getting from OpenDSS

def LoadShapes(*args):
    AC = args[0] #get the active circuit for openDSS
    Circuit = args[1]
    b = Circuit[0].index('LoadShapes')
    for ci,c in enumerate(AC.LoadShapes):
        for coli,col in enumerate(Circuit[b].columns):
            if coli == 0:
                _=0
            else:
                exec('AC.LoadShapes.' + col + '=Circuit[b].iloc[ci,coli]')
    # set the daily profile shape...
    b = Circuit[0].index('Loads')
    for li,l in enumerate(AC.Loads):
        l.daily = Circuit[b].loc[li,'daily']
        
def Loads(*args):
    AC = args[0] #get the active circuit for openDSS
    Circuit = args[1]
    if len(args) > 2:
        fields = args[2]
    else:
        fields = ['kW'] #by default only update the kW
    b = Circuit[0].index('Loads')
    for ci,c in enumerate(AC.Loads):
        for coli,col in enumerate(Circuit[b].columns):
            if coli == 0:
                _=0
            elif col in fields:
                exec('AC.Loads.' + col + '=Circuit[b].iloc[ci,coli]')
            else:
                _=0