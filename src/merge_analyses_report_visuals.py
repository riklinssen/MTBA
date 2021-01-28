##############IMPORTS########################
import numpy as np
import pandas as pd
import datetime
import seaborn as sns
import matplotlib.cm
import matplotlib.dates as mdates
import matplotlib.gridspec as gridspec
import matplotlib.patches as mpatches
import matplotlib.pyplot as plt
from matplotlib.ticker import PercentFormatter
from os import listdir

from pathlib import Path
import pathlib
import os

def find_filenames( path_to_dir, suffix=".dta"):
    pathname=Path(path_to_dir)
    filenames = [f for f in listdir(path_to_dir) if f.endswith(suffix)]
    fullnames=[Path(pathname/f) for f in filenames]
    return fullnames



total_dta=find_filenames(r"C:\Users\RikL\Box\ONL-IMK\2.0 Projects\Current\16-01 MTBA\07.2 Statistical analyses - Endline\Data analysis\4. Output\Resultsset\Total")
sindh_dta=find_filenames(r"C:\Users\RikL\Box\ONL-IMK\2.0 Projects\Current\16-01 MTBA\07.2 Statistical analyses - Endline\Data analysis\4. Output\Resultsset\Sindh")
punjab_dta=find_filenames(r"C:\Users\RikL\Box\ONL-IMK\2.0 Projects\Current\16-01 MTBA\07.2 Statistical analyses - Endline\Data analysis\4. Output\Resultsset\Punjab")

atriskcm=find_filenames(r"C:\Users\RikL\Box\ONL-IMK\2.0 Projects\Current\16-01 MTBA\07.2 Statistical analyses - Endline\Data analysis\4. Output\Resultsset\AtriskCM")
affectedcm=find_filenames(r"C:\Users\RikL\Box\ONL-IMK\2.0 Projects\Current\16-01 MTBA\07.2 Statistical analyses - Endline\Data analysis\4. Output\Resultsset\AffectedCM")
neithercm=find_filenames(r"C:\Users\RikL\Box\ONL-IMK\2.0 Projects\Current\16-01 MTBA\07.2 Statistical analyses - Endline\Data analysis\4. Output\Resultsset\NeitheratriskaffectedCM")

femalehhhead=find_filenames(r"C:\Users\RikL\Box\ONL-IMK\2.0 Projects\Current\16-01 MTBA\07.2 Statistical analyses - Endline\Data analysis\4. Output\Resultsset\HHfemale")
malehhhead=find_filenames(r"C:\Users\RikL\Box\ONL-IMK\2.0 Projects\Current\16-01 MTBA\07.2 Statistical analyses - Endline\Data analysis\4. Output\Resultsset\HHmale")

all_dta=total_dta+sindh_dta+punjab_dta+atriskcm+affectedcm+neithercm+femalehhhead+malehhhead

#short term comparisons (midline-endline)
short=[d for d in all_dta if d.name.endswith('_st_dta.dta')]
shortt_dfs=[]
for dta in short:
    #group indicator from filename
    group=None
    if os.path.dirname(dta).endswith('Total'): 
        group='Total'
    if os.path.dirname(dta).endswith('Sindh'): 
        group='Sindh'
    if os.path.dirname(dta).endswith('Punjab'): 
        group='Punjab'
    if os.path.dirname(dta).endswith('AtriskCM'): 
        group='atriskcm'
    if os.path.dirname(dta).endswith('AffectedCM'): 
        group='affectedcm'
    if os.path.dirname(dta).endswith('NeitheratriskaffectedCM'): 
        group='neithercm'
    if os.path.dirname(dta).endswith('HHfemale'): 
        group='hhfemale' 
    if os.path.dirname(dta).endswith('HHmale'): 
        group='hhmale' 
    #source indicator
    source='Short term set (midline-endline)'
    rawdf=pd.read_stata(dta)
#process raw df get out relevant nrs. 
    stats=pd.DataFrame()
    stats=rawdf.iloc[8:16,:]
    #colindex (outcomevars)
    outcomes=None
    outcomes=[c for c in rawdf.iloc[1,]]
    outcomes=[o.replace("VARIABLES", "param") for o in outcomes]
    #transpose and check for duplicates
    stats.columns=outcomes
    #remove some weird labels (t0)
    #strip
    stats['param']=stats['param'].str.strip()
    stats['param']=stats['param'].replace({'Endline mean control t(1)':'Endline mean control', 'Endline Mean treated t(1)': 'Endline mean treated'})
    stats=stats.set_index('param').T

    ##check for duplicates in outcomes. 
    if stats.duplicated(keep=False).sum()>0: 
        print("Duplicates in vars (same estimate run multiple times in single loop):", group, os.path.basename(dta))
        print(stats.duplicated(keep=False))
    #remove duplicates
    stats=stats.drop_duplicates(keep='last')
    #transpose back. 
    stats=stats.T.reset_index()
    stats[['period', 'parameter', 'treatment']]=stats['param'].str.split(expand=True)
    #lowercase
    stats['parameter']=stats['parameter'].str.lower()

    #adding other ids
    stats['group']=group

    stats=stats.drop(['param'], axis=1)

    #select avgs
    avgs=stats.loc[stats['parameter']=='mean'].melt(id_vars=['group', 'period', 'treatment'], value_name='Mean')
    sems=stats.loc[stats['parameter']=='sem'].melt(id_vars=['group', 'period', 'treatment'], value_name='sem')
    
    #drop redundant rows from melt (allow for missings in means or sems)
    avgs=avgs.loc[avgs['variable']!='parameter']
    sems=sems.loc[sems['variable']!='parameter']

    #convert to numeric
    avgs['Mean']=pd.to_numeric(avgs['Mean'], errors = 'coerce')
    sems['sem']=pd.to_numeric(sems['sem'], errors = 'coerce')

    groupdata=pd.merge(avgs, sems, on=['group', 'period', 'treatment', 'variable']) 

    ##add bounds
    groupdata['upper']=groupdata['Mean']+(1.96*groupdata['sem'])
    groupdata['lower']=groupdata['Mean']-(1.96*groupdata['sem'])
    #replace with 0 if lower than 0 (looks better in graphs)
    groupdata['lower']=np.where(groupdata['lower']<0,0,groupdata['lower'])

    #add source set indicator
    groupdata['source']='short term (M-E)'
    shortt_dfs.append(groupdata)

short_term=pd.concat(shortt_dfs, axis=0)



#short term comparisons (midline-endline)
longt=[d for d in all_dta if d.name.endswith('_lt_dta.dta')]
longt_dfs=[]
for dta in longt:
    #group indicator from filename
    group=None
    if os.path.dirname(dta).endswith('Total'): 
        group='Total'
    if os.path.dirname(dta).endswith('Sindh'): 
        group='Sindh'
    if os.path.dirname(dta).endswith('Punjab'): 
        group='Punjab'
    if os.path.dirname(dta).endswith('AtriskCM'): 
        group='atriskcm'
    if os.path.dirname(dta).endswith('AffectedCM'): 
        group='affectedcm'
    if os.path.dirname(dta).endswith('NeitheratriskaffectedCM'): 
        group='neithercm'
    if os.path.dirname(dta).endswith('HHfemale'): 
        group='hhfemale' 
    if os.path.dirname(dta).endswith('HHmale'): 
        group='hhmale' 
    #source indicator
    source='Long term set (midline-endline)'
    rawdf=pd.read_stata(dta)
#process raw df get out relevant nrs. 
    stats=pd.DataFrame()
    stats=rawdf.iloc[8:16,:]
    #colindex (outcomevars)
    outcomes=None
    outcomes=[c for c in rawdf.iloc[1,]]
    outcomes=[o.replace("VARIABLES", "param") for o in outcomes]
    #transpose and check for duplicates
    stats.columns=outcomes
    #remove some weird labels (t0)
    #strip
    stats['param']=stats['param'].str.strip()
    stats['param']=stats['param'].replace({'Endline mean control t(1)':'Endline mean control', 'Endline Mean treated t(1)': 'Endline mean treated'})
    stats=stats.set_index('param').T

    ##check for duplicates in outcomes. 
    if stats.duplicated(keep=False).sum()>0: 
        print("Duplicates in vars (same estimate run multiple times in single loop):", group, os.path.basename(dta))
        print(stats.duplicated(keep=False))
    #remove duplicates
    stats=stats.drop_duplicates(keep='last')
    #transpose back. 
    stats=stats.T.reset_index()
    stats[['period', 'parameter', 'treatment']]=stats['param'].str.split(expand=True)
    #lowercase
    stats['parameter']=stats['parameter'].str.lower()

    #adding other ids
    stats['group']=group

    stats=stats.drop(['param'], axis=1)

    #select avgs
    avgs=stats.loc[stats['parameter']=='mean'].melt(id_vars=['group', 'period', 'treatment'], value_name='Mean')
    sems=stats.loc[stats['parameter']=='sem'].melt(id_vars=['group', 'period', 'treatment'], value_name='sem')
    
    #drop redundant rows from melt (allow for missings in means or sems)
    avgs=avgs.loc[avgs['variable']!='parameter']
    sems=sems.loc[sems['variable']!='parameter']

    #convert to numeric
    avgs['Mean']=pd.to_numeric(avgs['Mean'], errors = 'coerce')
    sems['sem']=pd.to_numeric(sems['sem'], errors = 'coerce')

    groupdata=pd.merge(avgs, sems, on=['group', 'period', 'treatment', 'variable']) 

    ##add bounds
    groupdata['upper']=groupdata['Mean']+(1.96*groupdata['sem'])
    groupdata['lower']=groupdata['Mean']-(1.96*groupdata['sem'])
    #replace with 0 if lower than 0 (looks better in graphs)
    groupdata['lower']=np.where(groupdata['lower']<0,0,groupdata['lower'])

    #add source set indicator
    groupdata['source']='long term (B-E)'
    longt_dfs.append(groupdata)

long_term=pd.concat(longt_dfs, axis=0)



#export datasets
short_term.to_csv(r"C:\Users\RikL\Box\ONL-IMK\2.0 Projects\Current\16-01 MTBA\07.2 Statistical analyses - Endline\Data analysis\4. Output\Resultsset\short_term.csv")
long_term.to_csv(r"C:\Users\RikL\Box\ONL-IMK\2.0 Projects\Current\16-01 MTBA\07.2 Statistical analyses - Endline\Data analysis\4. Output\Resultsset\long_term.csv")


