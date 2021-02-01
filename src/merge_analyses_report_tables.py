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

all_dta=total_dta+sindh_dta+punjab_dta

##start with short term comparisons first as these have most of the outcomes and we don't need to ignore the index. 
short_term=[d for d in all_dta if d.name.endswith('_st_dta.dta')]
short_term_dfs=[]
for dta in short_term:
    group=None
    if os.path.dirname(dta).endswith('Total'): 
        group='Total'
    if os.path.dirname(dta).endswith('Sindh'): 
        group='Sindh'
    if os.path.dirname(dta).endswith('Punjab'): 
        group='Punjab'
   
    rawdf=pd.read_stata(dta)
    outcomes=[c for c in rawdf.iloc[1,]]
    outcomes=[o.replace("VARIABLES", "Parameter") for o in outcomes]
    stats=rawdf.iloc[3:5,:]
    stats.columns=outcomes
    stats.iat[1,0]="pvalue"
    stats=stats.T
    stats.columns = stats.iloc[0]
    stats=stats.drop(stats.index[0])
    #stats=stats.set_index('Parameter')
   
    stats['group']=group
    stats['comparison']='Midline-endline'

    #stats['source']=dta.name
    #keep only dif in dif rows
    short_term_dfs.append(stats)

result_short_term=pd.concat(short_term_dfs, ignore_index=False)
#made a mistake, looped over too long list (@enabling envorinment, drop duplicates. )
result_short_term=result_short_term.drop_duplicates(keep='last')




##now long term dfs 
long_term=[d for d in all_dta if d.name.endswith('_lt_dta.dta')]
long_term_dfs=[]
for dta in long_term:
    group=None
    if os.path.dirname(dta).endswith('Total'): 
        group='Total'
    if os.path.dirname(dta).endswith('Sindh'): 
        group='Sindh'
    if os.path.dirname(dta).endswith('Punjab'): 
        group='Punjab'
   
    rawdf=pd.read_stata(dta)
    outcomes=[c for c in rawdf.iloc[1,]]
    outcomes=[o.replace("VARIABLES", "Parameter") for o in outcomes]
    stats=rawdf.iloc[3:5,:]
    stats.columns=outcomes
    stats.iat[1,0]="pvalue"
    stats=stats.T
    stats.columns = stats.iloc[0]
    stats=stats.drop(stats.index[0])
   
    stats['group']=group
    stats['comparison']='Baseline-endline'

    #stats['source']=dta.name
    #keep only dif in dif rows
    long_term_dfs.append(stats)

result_long_term=pd.concat(long_term_dfs, ignore_index=False)
#made a mistake, looped over too long list (@enabling envorinment, drop duplicates. )
result_long_term=result_long_term.drop_duplicates(keep='last')


#export to excel
writer = pd.ExcelWriter(r"C:\Users\RikL\Box\ONL-IMK\2.0 Projects\Current\16-01 MTBA\07.2 Statistical analyses - Endline\Data analysis\4. Output\MTBA_endline_tables_INPUT_UPDATE.xlsx", engine='xlsxwriter')

result_short_term.to_excel(writer, sheet_name='midline_endline')
result_long_term.to_excel(writer, sheet_name='baseline_endline')
writer.save()





5