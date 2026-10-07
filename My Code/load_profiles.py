# Code to import and preprocess the household electrical load profiles including scaling
# Edited by Max de Groot based on code by Dougal McQueen

# Load dependencies
import os
import pandas as pd
import numpy as np
from numpy.random import default_rng
import pickle
import bottleneck
import matplotlib.pyplot as plt

# Fuction to load REFIT data and bootstrap profiles
def bootstrap_REFIT(*args):
    #https://pureportal.strath.ac.uk/en/datasets/refit-electrical-load-measurements-cleaned   
    # data from Strathclyde
    N = args[0]
    pth = r"C:\Users\Max de Groot\OneDrive - University of Otago\Documents\Honours\Data\CLEAN_REFIT_081116"
    read_Hdat = False
    if read_Hdat:
        for h in range(20):
            try:
                fl = 'CLEAN_House' + str(h+1) + '.csv'
                Dat = pd.read_csv(pth + '/' + fl)
                #get columns with grid_import
                
                Dat['Datetime'] = pd.to_datetime(Dat['Time'])
                Dat = Dat[['Datetime','Aggregate']]
                Dat.index = Dat['Datetime']
                Dat = Dat.resample('1min').mean()
                Dat = Dat[['Aggregate']]
                
                Dat = Dat[np.where(Dat.index[0:1440].hour==0)[0][0]:]
                
                days = int(len(Dat)/1440)
                Datr = np.transpose(np.reshape(Dat[0:1440*days],(days*len(Dat.columns),1440)))
                Datf = bottleneck.push(Datr,axis=0)
                #exclude profiles with NaNs...
                Datf = Datf[:,np.sum(Datf,0)>0]
                if h == 0:
                    profiles = Datf
                else:
                    profiles = np.append(profiles,Datf,axis=1)
                    
            except:
                print('Skip '+str(h))
        #12 kWh/day
        profiles = (12/24)/np.mean(profiles) * profiles # Scale to have mean of 12 kWh/day
        fh = open(pth + '/refit_household_profiles.dat', "wb")
        pickle.dump(profiles,fh)
        fh.close()
    else:
        fh = open(pth + '/refit_household_profiles.dat', "rb")
        profiles = pickle.load(fh)
        fh.close()
        rng = default_rng()
        idx = rng.choice(np.shape(profiles)[1], size=N, replace=False)
        return profiles[:,idx]
#############


# ----------
# Analysing the Load Profiles
# ----------

plt.rcParams['font.family'] = 'Times New Roman'

profiles = bootstrap_REFIT(1000)
mean_profiles = np.mean(profiles, axis=1) # Mean load profile shape
print(f'Mean household load of {np.mean(profiles)*24} kWh/day') 
t = np.arange(0, len(mean_profiles))
t = t/60

out_pth = r"C:\Users\Max de Groot\OneDrive - University of Otago\Documents\Honours\figures\methodology"

# mean load profile
plt.figure(figsize=(6, 4))
plt.plot(t, mean_profiles, color='black')
plt.ylabel('Electrical Load (kW)', fontsize=19)
plt.xlabel('Hour of day', fontsize=19)
plt.grid(axis='y', alpha=0.5)#, linewidth=0.6)
plt.xticks(fontsize=16)
plt.yticks(fontsize=16)
plt.tight_layout()
plt.savefig(
    out_pth + '/average other household load profile.pdf'
)
plt.show()

print(f'Mean household load of {np.mean(profiles)*24} kWh/day') 

# # individual load profiles
# plt.figure(figsize=(9,6))
# for n in [1, 2, 3]:
#     plt.plot(t, profiles[:, n], label=f'Profile {n}')
# plt.ylabel('Household Load (kW)', fontsize=19)
# plt.xlabel('Hour of day', fontsize=19)
# plt.grid(True)
# plt.xticks(fontsize=16)
# plt.yticks(fontsize=16)
# plt.legend(fontsize=16)
# plt.savefig(
#     out_pth + '/individual houehold load profiles.png',
#     dpi=600
# )
# plt.show()


