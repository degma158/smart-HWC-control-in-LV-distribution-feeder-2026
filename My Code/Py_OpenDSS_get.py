import numpy as np
#OpenDSS_get

# Function to pull circuit information from AC and assign to the circuit data frame structure
def circuit(*args):
    #read Circuit from Active Circuit in OpenDSS    
    AC = args[0]
    Circuit = args[1]
    dss_names = args[2]
            #set the circuit name into the Main data frame
    Circuit[1]['Main'] = [AC.Name]

    #get the list of line codes
    line_codes = []
    for l in AC.LineCodes:
        line_codes.append(l.Name)

    # now add information for each LineCode
    b = Circuit[0].index('LineCodes')
    Circuit[b]['LineCodes'] = AC.LineCodes.AllNames
    for c,a in enumerate(AC.LineCodes):
        Circuit[b].loc[c,'NormAmps'] = a.NormAmps

    #read the Bus information
    b = Circuit[0].index('ActiveBus')
    Circuit[b]['ActiveBus'] = AC.AllBusNames #the field name for Bus is ActiveBus as this is used by the openDSS package
    for c,a in enumerate(AC.ActiveBus):
        Circuit[b].loc[c,'x'] = a.x
        Circuit[b].loc[c,'y'] = a.y
        Circuit[b].loc[c,'LoadList'] = a.LoadList
    
    #Voltage source information
    b = Circuit[0].index('Vsources')
    Circuit[b]['Vsources'] = AC.Vsources.AllNames
    for c,a in enumerate(AC.Vsources):
        Circuit[b].loc[c,'Frequency'] = a.Frequency
        #Circuit[b].loc[c,'BasekV'] = a.dss.BasekV

    #get the lines
    b = Circuit[0].index('Lines')
    Circuit[b]['Lines'] = AC.Lines.AllNames
    for c,a in enumerate(AC.Lines):
        Circuit[b].loc[c,'Bus1'] = a.Bus1
        Circuit[b].loc[c,'Bus2'] = a.Bus2
        Circuit[b].loc[c,'LineCode'] = a.LineCode
        Circuit[b].loc[c,'Length'] = a.Length
        
    #get loads
    b = Circuit[0].index('Loads')
    Circuit[b]['Loads'] = AC.Loads.AllNames
    for c,a in enumerate(AC.Loads):
        for e,col in enumerate(Circuit[b].columns[1:]):
            if len(dss_names[b]) > 1:
                if dss_names[b][e+1] == 'ignore':
                    _=0
                elif col == 'phase':
                    #an exception to get phase means we need to set the active element and draw out the bus terminal
                    AC.SetActiveElement('Load.' + Circuit[b]['Loads'][c])
                    Circuit[b].loc[c,'phase'] = AC.ActiveElement.BusNames[0]
                elif len(dss_names[b][e+1]) > 1:
                    exec('Circuit[b].loc[c,col] = a.' + dss_names[b][e+1])
                else:
                    exec('Circuit[b].loc[c,col] = a.' + col)      
            else:
                exec('Circuit[b].loc[c,col] = a.' + col)
            
    #get load shapes
    b = Circuit[0].index('LoadShapes')
    Circuit[b]['LoadShapes'] = AC.LoadShapes.AllNames
    for c,a in enumerate(AC.LoadShapes):
        for e,col in enumerate(Circuit[b].columns[1:]):
            if len(dss_names[b]) > 1:
                if dss_names[b][e+1] == 'ignore':
                    _=0
                elif len(dss_names[b][e+1]) > 1:
                    exec('Circuit[b].at[c,col] = a.' + dss_names[b][e+1])
                else:
                    exec('Circuit[b].at[c,col] = a.' + col)
            else:
                exec('Circuit[b].at[c,col] = a.' + col)
    #get transformer
    b = Circuit[0].index('Transformers')
    Circuit[b]['Transformers'] = AC.Transformers.AllNames
    names = AC.AllElementNames
    #to get hte buses for the transformers we need to set the activeelement
    for ai,a in enumerate(AC.Transformers):
        ib = names.index('Transformer.'+Circuit[b]['Transformers'][ai])
        AC.SetActiveElement('Transformer.' + Circuit[b]['Transformers'][ai])
        Circuit[b].loc[ai,'Bus1'] = AC.ActiveElement.BusNames[0]
        Circuit[b].loc[ai,'Bus2'] = AC.ActiveElement.BusNames[1]
    return Circuit



def voltage(*args):
    #get all the voltages from the current array and assign to Circuit
    AC = args[0] #dss.ActiveCircuit
    Circuit = args[1]
    if len(args) > 2:
        fields = args[2]
    else:
        fields = ['Loads']
        
    buses = AC.AllBusNames
    #volts = AC.AllBusVolts
    vmag = AC.AllBusVmag
    #unpack volts into circuit
    
    if 'ActiveBus' in fields:
        a = Circuit[0].index('ActiveBus')
        Circuit[a]['Volts'] = Circuit[a]['Volts'].apply(lambda x: []) # we must put an array in each position to be filled
        for li in range(len(Circuit[a])):
            bus = Circuit[a]['ActiveBus'][li]
            bi = buses.index(bus)
            #ci = list(Circuit[b].columns).index('Volts')
            Circuit[a].at[li,'Volts'] = vmag[3*bi:3*bi+3]
    if 'Loads' in fields:
        b = Circuit[0].index('Loads')
        Circuit[b]['Volts'] = Circuit[b]['Volts'].apply(lambda x: []) # we must put an array in each position to be filled
        for li in range(len(Circuit[b])):
            bus = Circuit[b]['Bus1'][li]
            bi = buses.index(bus)
            #ci = list(Circuit[b].columns).index('Volts')
            Circuit[b].at[li,'Volts'] = vmag[3*bi:3*bi+3]
    if 'Transformers' in fields:
        b = Circuit[0].index('Transformers')
        #'Voltage1','Voltage2','Current2','Current2'
        Circuit[b]['Voltage1'] = Circuit[b]['Voltage1'].apply(lambda x: []) # we must put an array in each position to be filled
        Circuit[b]['Voltage2'] = Circuit[b]['Voltage2'].apply(lambda x: []) # we must put an array in each position to be filled
        for li in range(len(Circuit[b])):
            bus = Circuit[b]['Bus1'][li]
            bi = buses.index(bus)
            #ci = list(Circuit[b].columns).index('Volts')
            Circuit[b].at[li,'Voltage1'] = vmag[3*bi:3*bi+3]
            bus = Circuit[b]['Bus2'][li]
            bi = buses.index(bus)
            #ci = list(Circuit[b].columns).index('Volts')
            Circuit[b].at[li,'Voltage2'] = vmag[3*bi:3*bi+3]
         
    return Circuit

def current(*args):
    #get the current at each field
    AC = args[0] #dss.ActiveCircuit
    Circuit = args[1]
    if len(args) > 2:
        fields = args[2]
    else:
        fields = ['Loads']
    
    if 'VSources' in fields:
        b = Circuit[0].index('Vsources')
        AC.SetActiveElement('Load.'+Circuit[b]['Loads'][li])
        
        
    if 'Loads' in fields:
        b = Circuit[0].index('Loads')
        Circuit[b]['Current'].apply(lambda x: [])
        for li in range(len(Circuit[b])):
            AC.SetActiveElement('Load.'+Circuit[b]['Loads'][li])
            #ci = list(Circuit[b].columns).index('Current')
            Circuit[b].at[li,'Current'] = AC.ActiveElement.Currents
    if 'Transformers' in fields:
        b = Circuit[0].index('Transformers')
        Circuit[b]['Current1'].apply(lambda x: [])
        Circuit[b]['Current2'].apply(lambda x: [])
        for li in range(len(Circuit[b])):
            AC.SetActiveElement('Transformer.'+Circuit[b]['Transformers'][li])
            #ci = list(Circuit[b].columns).index('Current')
            current = AC.ActiveElement.Currents
            Circuit[b].at[li,'Current1'] = current[0:7]
            Circuit[b].at[li,'Current2'] = current[8:16]
            
    return Circuit
            
def distance(*args):
    #get the distance for each bus..
    AC = args[0] #dss.ActiveCircuit
    Circuit = args[1]
    if len(args) > 2:
        fields = args[2]
    else:
        fields = ['Loads']
    buses = AC.AllBusNames
    dist = AC.AllBusDistances
    if 'Loads' in fields:
        b = Circuit[0].index('Loads')
        Circuit[b]['Distance'] = Circuit[b]['Distance'].apply(lambda x: []) # we must put an array in each position to be filled
        for li in range(len(Circuit[b])):
            bus = Circuit[b]['Bus1'][li]
            bi = buses.index(bus)
            #ci = list(Circuit[b].columns).index('Volts')
            Circuit[b].at[li,'Distance'] = dist[bi]
    return Circuit