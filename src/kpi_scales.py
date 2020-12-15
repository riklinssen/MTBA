##############IMPORTS########################
import numpy as np
import pandas as pd
import pathlib
import datetime
import seaborn as sns
import matplotlib.cm
import matplotlib.dates as mdates
import matplotlib.gridspec as gridspec
import matplotlib.patches as mpatches
import matplotlib.pyplot as plt
from matplotlib.ticker import PercentFormatter

from pathlib import Path


import scipy.stats as st
##########################BOILERPLATE##########
# Oxfam colors
hex_values = ['#E70052',  # rood
              '#F16E22',  # oranje
              '#E43989',  # roze
              '#630235',  # Bordeax
              '#53297D',  # paars
              '#0B9CDA',  # blauw
              '#61A534',  # oxgroen
              '#0C884A'  # donkergroen
              ]

#####some utils
#make set with avgs and bounds

def get_mean_ci_in_df(df, groupings, outcomes):
    groupings= [c for c in groupings]
    outcomes=[c for c in outcomes]
    outcomedfs=[]
    for c in outcomes: 
        colnames=[str(c)+'_mean', str(c)+'_sem']
        mean_outcome=df.groupby(groupings)[outcomes].agg(['mean', 'sem']).droplevel(0, axis=1)
        mean_outcome.columns=colnames
        meancolname=str(c)+'_mean'
        semcolname=str(c)+'_sem'
        mean_outcome[str(c)+'_lower']=mean_outcome[meancolname]-1.96*mean_outcome[semcolname]
        mean_outcome[str(c)+'_upper']=mean_outcome[meancolname]+1.96*mean_outcome[semcolname]
        ##add order
        outcomedfs.append(mean_outcome)
    data=pd.concat(outcomedfs)
    data['order']=data.index.get_level_values('grouping_period').map({"Baseline": 1, "Midline": 2, "Endline": 3})
    return data
    
subset_colors={'Total': '#0C884A' ,'Sindh': '#630235','Punjab': '#0B9CDA'}


idx=pd.IndexSlice
##########################FIlEPATHS##########
currentwd_path = Path.cwd()
data_path = currentwd_path / "data"
cleandata_path = Path(r"C:\Users\RikL\Box\ONL-IMK\2.0 Projects\Current\16-01 MTBA\07.2 Statistical analyses - Endline\Data analysis\2. Clean")
labels_path = currentwd_path.parent/"docs"
graphs_path = Path(r"C:\Users\RikL\Box\ONL-IMK\2.0 Projects\Current\16-01 MTBA\07.2 Statistical analyses - Endline\visuals")


clean=pd.read_csv(r"C:\Users\RikL\Projects\MTBA\src\data\interim\clean.csv")


#make some groupings
clean['grouping_period']=clean['period'].map({0:"Baseline", 1: "Midline", 2: "Endline"})
#remove nrs periods and sstrip string for province
clean['grouping_province']=clean['code_province'].map({1: 'Sindh', 2: 'Punjab'})
clean['grouping_total']='Total'

clean['grouping_target']=clean['code_group'].map({0: "Comparison group", 1: "Target group"})

sindh=clean.loc[clean['grouping_province']=='Sindh']
punjab=clean.loc[clean['grouping_province']=='Punjab']


########################combined scales do not convert categoricals###################

#make some groupings


##ind_gstat advocacy combined scale
##but we need these indicators without categorical encoding. 

#conversion to numerical
clean['ind_mobility_sc']=clean['ind_mobility']
sindh['ind_mobility_sc']=sindh['ind_mobility']
punjab['ind_mobility_sc']=punjab['ind_mobility']

outcomes=['ind_mobility_sc']
print(clean['ind_mobility_sc'].max())
filename='KPI_'+str(outcomes[0]) +'.svg'
print(filename)

title_anno_opts = dict(xy=(-0.5, 0.5), size='medium', xycoords='axes fraction',
                       va='center', ha='center', rotation=90)
fig, axes=plt.subplots(nrows=3, ncols=2, sharex='col', sharey='col',   gridspec_kw={'width_ratios': [1, 3,]}, figsize=(6,(6*1.61)))
#titlecol
for i, sub in enumerate(subset_colors.keys()): 
    axes[i,0].annotate(sub, **title_anno_opts, color=subset_colors[sub])
# remove spines
    axes[i,0].axis('off')
for i, (sub) in enumerate(subset_colors.keys()):
    print(sub)
    if sub=='Total':
        stats=get_mean_ci_in_df(clean, ['grouping_target', 'grouping_period'],outcomes)
    if sub=='Sindh':
        stats=get_mean_ci_in_df(sindh, ['grouping_target', 'grouping_period'],outcomes)
    if sub=='Punjab':
        stats=get_mean_ci_in_df(punjab, ['grouping_target', 'grouping_period'],outcomes)
    stats.columns=['mean', 'sem', 'lower', 'upper', 'order']
    #target group
    target=stats.loc[idx['Target group',:],:].droplevel(0).sort_values(by='order')
    axes[i,1].plot(target.index, target['mean'], marker='o', color=subset_colors[sub])
    #axes[i,1].line(target.index, target['mean'], color=subset_colors[sub])
    axes[i,1].fill_between(target.index,target['lower'], target['upper'], color=subset_colors[sub], alpha=0.2)
    #labels
    for key, row in target.iterrows():
        axes[i,1].text(x=row['order']-1, y=row['mean']+0.15, s='{:.2f}'.format(row['mean']), ha='center', size='small', color=subset_colors[sub])
    
    
    #comparison
    comp=stats.loc[idx['Comparison group',:],:].droplevel(0).sort_values(by='order')
    axes[i,1].plot(comp.index, comp['mean'], marker='.', linestyle=':', color='grey', label='Comparison\ngroup')
    #axes[i,1].line(target.index, target['mean'], color=subset_colors[sub])
    axes[i,1].fill_between(comp.index,comp['lower'], comp['upper'], color='grey', alpha=0.2)


#some settings on all axes.
axes[0,1].legend(loc='upper center', bbox_to_anchor=(0.8, 1.15),
        ncol=1, fontsize='small',  fancybox=False, shadow=False, frameon=False)   
for ax in fig.axes: 
    ax.set_ylim(1,5)
    ax.set_yticks(np.arange(1,6), minor=False)
    yticklabs=[str(i) for i in np.arange(1,6)]
    yticklabs[0]='1-others would disapprove'
    yticklabs[-1]='5-others would approve'
    ax.set_yticklabels(yticklabs)

    sns.despine(ax=ax)
    ax.spines['left'].set_position(('outward',5))
    ax.spines['bottom'].set_position(('outward',5))
    ax.set_ylabel('', fontstyle='oblique')
    
fig.suptitle('Norms re. Freedom of movement scale: Mobility of women', x=0, y=0.98, ha='left', size='medium', fontweight='bold', color='Black')
fig.text(0,0, 'Source: MTBA Endline studies n total='+str(len(clean[outcomes].dropna())) + ' girls.\nShaded areas represent 95% CI of the mean.', fontsize='small', color='grey')
fig.savefig(graphs_path/filename)
fig.show()
    


##ind_gstat advocacy combined scale

#conversion to numerical
clean['ind_Gstat_advocacy_sc']=clean['ind_Gstat_advocacy']
sindh['ind_Gstat_advocacy_sc']=sindh['ind_Gstat_advocacy']
punjab['ind_Gstat_advocacy_sc']=punjab['ind_Gstat_advocacy']

outcomes=['ind_Gstat_advocacy_sc']

filename='KPI_'+str(outcomes[0]) +'.svg'
print(filename)
fig, axes=plt.subplots(nrows=3, ncols=2, sharex='col', sharey='col',   gridspec_kw={'width_ratios': [1, 3,]}, figsize=(6,(6*1.61)))
#titlecol
for i, sub in enumerate(subset_colors.keys()): 
    axes[i,0].annotate(sub, **title_anno_opts, color=subset_colors[sub])
# remove spines
    axes[i,0].axis('off')
for i, (sub) in enumerate(subset_colors.keys()):
    print(sub)
    if sub=='Total':
        stats=get_mean_ci_in_df(clean, ['grouping_target', 'grouping_period'],outcomes)
    if sub=='Sindh':
        stats=get_mean_ci_in_df(sindh, ['grouping_target', 'grouping_period'],outcomes)
    if sub=='Punjab':
        stats=get_mean_ci_in_df(punjab, ['grouping_target', 'grouping_period'],outcomes)
    stats.columns=['mean', 'sem', 'lower', 'upper', 'order']
    #target group
    target=stats.loc[idx['Target group',:],:].droplevel(0).sort_values(by='order')
    axes[i,1].plot(target.index, target['mean'], marker='o', color=subset_colors[sub])
    #axes[i,1].line(target.index, target['mean'], color=subset_colors[sub])
    axes[i,1].fill_between(target.index,target['lower'], target['upper'], color=subset_colors[sub], alpha=0.2)
    #labels
    for key, row in target.iterrows():
        axes[i,1].text(x=row['order']-1, y=row['mean']+0.15, s='{:.2f}'.format(row['mean']), ha='center', size='small', color=subset_colors[sub])
    
    
    #comparison
    comp=stats.loc[idx['Comparison group',:],:].droplevel(0).sort_values(by='order')
    axes[i,1].plot(comp.index, comp['mean'], marker='.', linestyle=':', color='grey', label='Comparison\ngroup')
    #axes[i,1].line(target.index, target['mean'], color=subset_colors[sub])
    axes[i,1].fill_between(comp.index,comp['lower'], comp['upper'], color='grey', alpha=0.2)


#some settings on all axes.
axes[0,1].legend(loc='upper center', bbox_to_anchor=(0.8, 1.15),
        ncol=1, fontsize='small',  fancybox=False, shadow=False, frameon=False)   
for ax in fig.axes: 
    ax.set_ylim(1,5)
    ax.set_yticks(np.arange(1,6), minor=False)
    yticklabs=[str(i) for i in np.arange(1,6)]
    yticklabs[0]='1-low'
    yticklabs[-1]='5-high'
    ax.set_yticklabels(yticklabs)

    sns.despine(ax=ax)
    ax.spines['left'].set_position(('outward',5))
    ax.spines['bottom'].set_position(('outward',5))
    ax.set_ylabel('mean on scale', fontstyle='oblique')
    
fig.suptitle('Advocating for rights scale (child bearing, educ, work, marriage)', x=0, y=0.98, ha='left', size='medium', fontweight='bold', color='Black')
fig.text(0,0, 'Source: MTBA Endline studies n total='+str(len(clean[outcomes].dropna())) + ' girls.\nShaded areas represent 95% CI of the mean.', fontsize='small', color='grey')
fig.savefig(graphs_path/filename)
fig.show()
    
