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

##########################FIlEPATHS##########
currentwd_path = Path.cwd()
data_path = currentwd_path / "data"
cleandata_path = Path(r"C:\Users\RikL\Box\ONL-IMK\2.0 Projects\Current\16-01 MTBA\07.2 Statistical analyses - Endline\Data analysis\2. Clean")
labels_path = currentwd_path.parent/"docs"
graphs_path = Path(r"C:\Users\RikL\Box\ONL-IMK\2.0 Projects\Current\16-01 MTBA\07.2 Statistical analyses - Endline\visuals")


clean=pd.read_stata(cleandata_path/"4. MTBA Endline Cleaning 5 - Incl outcome indicators.dta")


#make some groupings
clean['grouping_period']=clean['period'].cat.rename_categories({"0. Baseline": "Baseline", "1. Midline": "Midline",  "2. Endline": "Endline"})
clean['grouping_period']=clean['grouping_period'].astype(str)
#remove nrs periods and sstrip string for province
clean['grouping_province']=clean['code_province'].astype(str).str.replace('\d+', '').str.replace('.', '').str.strip()
clean['grouping_total']='Total'




##descriptive stats. 
#Girls
##baseline, midline, endline in cols, indicators in rows. 
period_names_col = {
    'Baseline': '#0B9CDA',
    'Midline': '#53297D',
    'Endline': '#630235'}

varlabel_df = pd.read_excel(labels_path/"mtba_endline_VariableLabels_viz.xlsx", usecols=['varname','label'], index_col='varname')

varlabel_dict=varlabel_df['label'].to_dict()                            

#anno options for headings
title_anno_opts = dict(xy=(0.5, 0.5), size='small', xycoords='axes fraction',
                       va='center', ha='center')

idx=pd.IndexSlice

#agecat
age = [c for c in clean.columns if c.startswith('ind_gagecat_')]


filename=graphs_path/'agecats_by_time_province.svg'
sns.set_style('white')

fig, axes = plt.subplots(nrows=4, ncols=len(period_names_col.keys()), sharex='col', sharey='row', figsize=(
    6.25, 6), gridspec_kw={'height_ratios': [1, 3, 3, 3 ]})

#totals
data =clean.groupby(['grouping_period', 'grouping_total'])[age].mean().stack().to_frame()
data.index.names=['period', 'group', 'ind']
data.columns=['prop']
data['label']=data.index.get_level_values(2)
data['label']=data['label'].map(varlabel_dict)


# title row.
for i,period in enumerate(period_names_col.keys()):
    axes[0,i].annotate(period, **title_anno_opts, color=period_names_col[period])
    # remove spines
    axes[0,i].axis('off')
#total
for i,period in enumerate(period_names_col.keys()):
    axes[1,i].set_xlim(0, 1)
    sel=data.loc[idx[period,:,:],:]
    axes[1,i].barh(y=sel['label'], width=sel['prop'], color=period_names_col[period])
    # remove spines)
    # labels
    for p in axes[1,i].patches:
        # get_width pulls left or right; get_y pushes up or down
        axes[1,i].text(p.get_width()+0.05, p.get_y()+0.5, "{:.0%}".format(
            p.get_width()), color=p.get_facecolor(), verticalalignment='top', size='xx-small')
    if i == 0:
        axes[1,i].set_ylabel('Total', fontstyle='oblique')
    
    sns.despine(ax=axes[1,i])
#sindh
data =clean.loc[clean['grouping_province']=='Sindh'].groupby(['grouping_period', 'grouping_total'])[age].mean().stack().to_frame()
data.index.names=['period', 'group', 'ind']
data.columns=['prop']
data['label']=data.index.get_level_values(2)
data['label']=data['label'].map(varlabel_dict)
for i,period in enumerate(period_names_col.keys()):
    axes[2,i].set_xlim(0, 1)
    sel=data.loc[idx[period,:,:],:]
    axes[2,i].barh(y=sel['label'], width=sel['prop'], color=period_names_col[period])
    # remove spines)
    # labels
    for p in axes[2,i].patches:
        # get_width pulls left or right; get_y pushes up or down
        axes[2,i].text(p.get_width()+0.05, p.get_y()+0.5, "{:.0%}".format(
            p.get_width()), color=p.get_facecolor(), verticalalignment='top', size='xx-small')
    if i == 0:
        axes[2,i].set_ylabel('Sindh', fontstyle='oblique')
    
    sns.despine(ax=axes[2,i])
#Punjab
data =clean.loc[clean['grouping_province']=='Punjab'].groupby(['grouping_period', 'grouping_total'])[age].mean().stack().to_frame()
data.index.names=['period', 'group', 'ind']
data.columns=['prop']
data['label']=data.index.get_level_values(2)
data['label']=data['label'].map(varlabel_dict)
for i,period in enumerate(period_names_col.keys()):
    axes[3,i].set_xlim(0, 1)
    sel=data.loc[idx[period,:,:],:]
    axes[3,i].barh(y=sel['label'], width=sel['prop'], color=period_names_col[period])
    # remove spines)
    # labels
    for p in axes[3,i].patches:
        # get_width pulls left or right; get_y pushes up or down
        axes[3,i].text(p.get_width()+0.05, p.get_y()+0.5, "{:.0%}".format(
            p.get_width()), color=p.get_facecolor(), verticalalignment='top', size='xx-small')
    if i == 0:
        axes[3,i].set_ylabel('Punjab', fontstyle='oblique')
    
    sns.despine(ax=axes[3,i])
#some stuff on all axes.
for ax in fig.axes: 
    ax.xaxis.set_major_formatter(PercentFormatter(xmax=1))
fig.savefig(filename, bbox_inches='tight')








######At risk of GCM by time and age_cat

outcomes=['ind_gcm1',
'ind_gcm2',
'ind_gcm3']

outcome_colors=dict(zip(outcomes, ['#E70052',  # rood
              '#F16E22',  # oranje
              '#E43989']))  # roze))
total=clean.groupby(['Gage_cat', 'grouping_period'])[outcomes].mean()
total=total.rename(columns=varlabel_dict)




sns.set_context('notebook')
fig, axes = plt.subplots(nrows=3, ncols=2, sharex='row', figsize=(
    6.25, 3), gridspec_kw={'width_ratios': [1, 3,]})

#titles in cols
for i, agegroup in enumerate(['Girls aged:\n12-14', 'Girls aged:\n 15-17', 'Girls aged:\n18+']):
    axes[i,0].annotate(agegroup, **title_anno_opts, color='black', fontsize='large')
    # remove spines
    axes[i,0].axis('off')

for i, agecat in enumerate(['1. 12-14', '2. 15-17', '3. 18+']): 
    sel=total.loc[idx[agecat,:],:].droplevel(0)
    sel['cumsum']=sel.sum(axis=1)
        #ordering baseline-endline
    sel['order']=[1,3,2]
    sel=sel.sort_values(by='order')
    axes[i,1].barh(y=sel['order'], width=sel['At risk of CM'], color='#E70052', label='At risk of CM')
    #axes[i,1].barh(y=sel['order'], width=sel['Affected by CM'], color='#53297D', left=sel['At risk of CM'], label='Affected by CM')
    #axes[i,1].barh(y=sel['order'], width=sel['Neither at risk nor affected'], color='#0C884A' , left=(sel['cumsum']-sel['Neither at risk nor affected']), label='Neither at risk nor affected')
    #text labels


    #At risk of CM
    
    sel['xpos']=sel['At risk of CM']/2
    sel['perc']=sel['At risk of CM'].apply(lambda x:'{:.0f}%'.format(x*100))

    axes[i,1].text(sel['xpos'],sel['order'], t=sel['perc'], color='white')


    #text labels
    for p in axes[1,i].patches:
       # get_width pulls left or right; get_y pushes up or down
        axes[i,1].text(p.get_width(), p.get_y(), "{:.0%}".format(
            p.get_width()), color='white', verticalalignment='top', size='xx-small')
   


print(sel['At risk of CM'].str)
