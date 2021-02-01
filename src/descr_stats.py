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
graphs_path = Path(r"C:\Users\RikL\Box\ONL-IMK\2.0 Projects\Current\16-01 MTBA\07.2 Statistical analyses - Endline\Data analysis\4. Output\visuals_report_mtba")


clean=pd.read_stata(cleandata_path/"5. MTBA Endline Cleaning 5 - Incl outcome indicators.dta")


#make some groupings
clean['grouping_period']=clean['period'].cat.rename_categories({"0. Baseline": "Baseline", "1. Midline": "Midline",  "2. Endline": "Endline"})
clean['grouping_period']=clean['grouping_period'].astype(str)
#remove nrs periods and sstrip string for province
clean['grouping_province']=clean['code_province'].astype(str).str.replace('\d+', '').str.replace('.', '').str.strip()
clean['grouping_total']='Total'


##varlabel dict
varlabel_df = pd.read_excel(labels_path/"mtba_endline_VariableLabels_viz.xlsx", usecols=['varname','label'], index_col='varname')

varlabel_dict=varlabel_df['label'].to_dict()          

##descriptive stats. 

###number of respondents. GIRLS
period_names_col = {
    'Baseline': '#0B9CDA',
    'Midline': '#53297D',
    'Endline': '#630235'}

#anno options for headings
title_anno_opts = dict(xy=(0.5, 0.5), size='small', xycoords='axes fraction',
                       va='center', ha='center')

idx=pd.IndexSlice


filename=graphs_path/'nrofobs_by_time_province.svg'
sns.set_style('ticks')

fig, axes = plt.subplots(nrows=4, ncols=len(period_names_col.keys()), sharex='col', sharey='row', figsize=(
    4, 4), gridspec_kw={'height_ratios': [1, 3, 3, 3 ]})

#totals
data =clean.groupby(['grouping_period', 'grouping_total']).size().to_frame()
data.columns=['nrobs']

data['label']='no. of girls'
# title row.
for i,period in enumerate(period_names_col.keys()):
    axes[0,i].annotate(period, **title_anno_opts, color=period_names_col[period])
    # remove spines
    axes[0,i].axis('off')

#total
for i,period in enumerate(period_names_col.keys()):
    #axes[1,i].set_xlim(0, 1)
    sel=data.loc[idx[period,:,:],:]
    axes[1,i].barh(y=sel['label'], width=sel['nrobs'], color=period_names_col[period])
    # remove spines)
    # labels
    for p in axes[1,i].patches:
        # get_width pulls left or right; get_y pushes up or down
        axes[1,i].text(p.get_width()/2, (p.get_y()+p.get_height()/2), "{:,}".format(
            p.get_width()), color='white', verticalalignment='center', horizontalalignment='center', size='small')
    if i == 0:
        axes[1,i].set_ylabel('Total', fontstyle='oblique')
    
    sns.despine(ax=axes[1,i])


#sindh
data =clean.loc[clean['grouping_province']=='Sindh'].groupby(['grouping_period', 'grouping_total']).size().to_frame()
data.columns=['nrobs']
data['label']='no. of girls'
for i,period in enumerate(period_names_col.keys()):
    sel=data.loc[idx[period,:,:],:]
    axes[2,i].barh(y=sel['label'], width=sel['nrobs'], color=period_names_col[period])
    # remove spines)
    # labels
    for p in axes[2,i].patches:
        # get_width pulls left or right; get_y pushes up or down
        axes[2,i].text(p.get_width()+0.05,  (p.get_y()+p.get_height()/2), "{:,}".format(
            p.get_width()), color=p.get_facecolor(), verticalalignment='center', size='small')
    if i == 0:
        axes[2,i].set_ylabel('Sindh', fontstyle='oblique')
    
    sns.despine(ax=axes[2,i])


#punjab
data =clean.loc[clean['grouping_province']=='Punjab'].groupby(['grouping_period', 'grouping_total']).size().to_frame()
data.columns=['nrobs']
data['label']='no. of girls'
for i,period in enumerate(period_names_col.keys()):
    sel=data.loc[idx[period,:,:],:]
    axes[3,i].barh(y=sel['label'], width=sel['nrobs'], color=period_names_col[period])
    # remove spines)
    # labels
    for p in axes[3,i].patches:
        # get_width pulls left or right; get_y pushes up or down
        axes[3,i].text(p.get_width()+0.05,  (p.get_y()+p.get_height()/2), "{:,}".format(
            p.get_width()), color=p.get_facecolor(), verticalalignment='center', size='small')
    if i == 0:
        axes[3,i].set_ylabel('Punjab', fontstyle='oblique')
    
    sns.despine(ax=axes[3,i])

#some stuff on all axes.
for ax in fig.axes: 
    ax.set_xlim(0,1200)
fig.savefig(filename, bbox_inches='tight')




#Girls
##baseline, midline, endline in cols, indicators in rows. 
period_names_col = {
    'Baseline': '#0B9CDA',
    'Midline': '#53297D',
    'Endline': '#630235'}

                  

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







##level of education




#educ GIRLS


educ = ['Geducation']


#generate data for educ

tots =clean.groupby(['grouping_total', 'grouping_period'])['Geducation'].value_counts(normalize=True, dropna=True).to_frame()
prov =clean.groupby(['grouping_province', 'grouping_period'])['Geducation'].value_counts(normalize=True, dropna=True).to_frame()

data=pd.concat([tots,prov], axis=0)
data.index.names=['period', 'group', 'ind']
data.columns=['prop']
data['label']=data.index.get_level_values(2)


filename=graphs_path/'Geducation_time_province.svg'
sns.set_style('ticks')

fig, axes = plt.subplots(nrows=4, ncols=4, sharex='col', figsize=(
    6.25, 6), gridspec_kw={'width_ratios': [1, 3, 3, 3], 'height_ratios': [1, 3, 3, 3],})

# title row.
for i,period in enumerate(period_names_col.keys(),1):
    axes[0,i].annotate(period, **title_anno_opts, color=period_names_col[period])
    # remove spines
    axes[0,i].axis('off')


#province names
for i, provname in enumerate(['Total', 'Punjab', 'Sindh'],1):
    axes[i,0].annotate(provname, xy=(0.5,0.5), size='medium', xycoords='axes fraction',
                       va='center', ha='center', rotation=90)
    axes[i,0].axis('off') 
#baseline no data. 
for i in range(1,4):
    axes[i,1].axis('off')

axes[0,1].annotate('no data', xy=(0.5,0.2), size='small', xycoords='axes fraction',
                       va='center', ha='center')

#total
for i,period in enumerate(['Midline', 'Endline'],2):
    axes[1,i].set_xlim(0, 1)
    sel=data.loc[idx['Total',period,:],:]
    axes[1,i].barh(y=sel['label'], width=sel['prop'], color=period_names_col[period])
    # remove spines)
    # labels
    for p in axes[1,i].patches:
        # get_width pulls left or right; get_y pushes up or down
        axes[1,i].text(p.get_width()+0.05, p.get_y()+0.5, "{:.0%}".format(
            p.get_width()), color=p.get_facecolor(), verticalalignment='top', size='xx-small')
    #yaxis invisible on last ax.
    if i == 3:
        axes[1,i].yaxis.set_visible(False)
    sns.despine(ax=axes[1,i])

#Punjab
for i,period in enumerate(['Midline', 'Endline'],2):
    axes[2,i].set_xlim(0, 1)
    sel=data.loc[idx['Punjab',period,:],:]
    axes[2,i].barh(y=sel['label'], width=sel['prop'], color=period_names_col[period])
    # remove spines)
    # labels
    for p in axes[2,i].patches:
        # get_width pulls left or right; get_y pushes up or down
        axes[2,i].text(p.get_width()+0.05, p.get_y()+0.5, "{:.0%}".format(
            p.get_width()), color=p.get_facecolor(), verticalalignment='top', size='xx-small')
    #yaxis invisible on last ax.
    if i == 3:
        axes[2,i].yaxis.set_visible(False)
    sns.despine(ax=axes[2,i])
#sindh
for i,period in enumerate(['Midline', 'Endline'],2):
    axes[3,i].set_xlim(0, 1)
    sel=data.loc[idx['Sindh',period,:],:]
    axes[3,i].barh(y=sel['label'], width=sel['prop'], color=period_names_col[period])
    # remove spines)
    # labels
    for p in axes[3,i].patches:
        # get_width pulls left or right; get_y pushes up or down
        axes[3,i].text(p.get_width()+0.05, p.get_y()+0.5, "{:.0%}".format(
            p.get_width()), color=p.get_facecolor(), verticalalignment='top', size='xx-small')
    #yaxis invisible on last ax.
    if i == 3:
        axes[3,i].yaxis.set_visible(False)
    sns.despine(ax=axes[3,i])
#some stuff on all axes.
for ax in fig.axes: 
    ax.xaxis.set_major_formatter(PercentFormatter(xmax=1))
    ax.xaxis.set_tick_params(rotation=90)

#remove top left ax
axes[0,0].axis('off')
fig.text(0,0, 'Source: MTBA Endline studies n total='+str(len(clean['Geducation'].dropna())) + ' girls.', fontsize='small', color='grey')
fig.savefig(filename, bbox_inches='tight')











#educ HOUSEHOLD


educ = ['HHeduc1']


#generate data for educ

tots =clean.groupby(['grouping_total', 'grouping_period'])['HHeduc1'].value_counts(normalize=True, dropna=True).to_frame()
prov =clean.groupby(['grouping_province', 'grouping_period'])['HHeduc1'].value_counts(normalize=True, dropna=True).to_frame()

data=pd.concat([tots,prov], axis=0)
data.index.names=['period', 'group', 'ind']
data.columns=['prop']
data['label']=data.index.get_level_values(2)


filename=graphs_path/'HHeduc1_time_province.svg'
sns.set_style('ticks')

fig, axes = plt.subplots(nrows=4, ncols=4, sharex='col', figsize=(
    6.25, 6), gridspec_kw={'width_ratios': [2, 4, 4, 4], 'height_ratios': [2, 4, 4, 4],})

# title row.
for i,period in enumerate(period_names_col.keys(),1):
    axes[0,i].annotate(period, **title_anno_opts, color=period_names_col[period])
    # remove spines
    axes[0,i].axis('off')


#province names
for i, provname in enumerate(['Total', 'Punjab', 'Sindh'],1):
    axes[i,0].annotate(provname, xy=(-0.5,0.5), size='medium', xycoords='axes fraction',
                       va='center', ha='center', rotation=90)
    axes[i,0].axis('off') 

#total
for i,period in enumerate(['Baseline', 'Midline', 'Endline'],1):
    axes[1,i].set_xlim(0, 1)
    sel=data.loc[idx['Total',period,:],:]
    axes[1,i].barh(y=sel['label'], width=sel['prop'], color=period_names_col[period])
    # remove spines)
    # labels
    for p in axes[1,i].patches:
        # get_width pulls left or right; get_y pushes up or down
        axes[1,i].text(p.get_width()+0.05, p.get_y()+0.5, "{:.0%}".format(
            p.get_width()), color=p.get_facecolor(), verticalalignment='top', size='xx-small')
    #yaxis invisible on last ax.
    if i > 1:
        axes[1,i].yaxis.set_visible(False)
    sns.despine(ax=axes[1,i])

#Punjab
for i,period in enumerate(['Baseline', 'Midline', 'Endline'],1):
    axes[2,i].set_xlim(0, 1)
    sel=data.loc[idx['Punjab',period,:],:]
    axes[2,i].barh(y=sel['label'], width=sel['prop'], color=period_names_col[period])
    # remove spines)
    # labels
    for p in axes[2,i].patches:
        # get_width pulls left or right; get_y pushes up or down
        axes[2,i].text(p.get_width()+0.05, p.get_y()+0.5, "{:.0%}".format(
            p.get_width()), color=p.get_facecolor(), verticalalignment='top', size='xx-small')
    #yaxis invisible on last ax.
    if i> 1:
        axes[2,i].yaxis.set_visible(False)
    sns.despine(ax=axes[2,i])
#sindh
for i,period in enumerate(['Baseline', 'Midline', 'Endline'],1):
    axes[3,i].set_xlim(0, 1)
    sel=data.loc[idx['Sindh',period,:],:]
    axes[3,i].barh(y=sel['label'], width=sel['prop'], color=period_names_col[period])
    # remove spines)
    # labels
    for p in axes[3,i].patches:
        # get_width pulls left or right; get_y pushes up or down
        axes[3,i].text(p.get_width()+0.05, p.get_y()+0.5, "{:.0%}".format(
            p.get_width()), color=p.get_facecolor(), verticalalignment='top', size='xx-small')
    #yaxis invisible on last ax.
    if i > 1:
        axes[3,i].yaxis.set_visible(False)
    sns.despine(ax=axes[3,i])
#some stuff on all axes.
for ax in fig.axes: 
    ax.xaxis.set_major_formatter(PercentFormatter(xmax=1))
    ax.xaxis.set_tick_params(rotation=90)

#remove top left ax
axes[0,0].axis('off')
fig.text(0,0, 'Source: MTBA Endline studies n total='+str(len(clean['HHeduc1'].dropna())) + ' household-heads.', fontsize='small', color='grey')
fig.savefig(filename, bbox_inches='tight')





#Occupation HOUSEHOLD


print(clean['HHoccupation1'].value_counts(dropna=False))

#generate data for educ

tots =clean.groupby(['grouping_total', 'grouping_period'])['HHoccupation1'].value_counts(normalize=True, dropna=True).to_frame()
prov =clean.groupby(['grouping_province', 'grouping_period'])['HHoccupation1'].value_counts(normalize=True, dropna=True).to_frame()

data=pd.concat([tots,prov], axis=0)
data.index.names=['period', 'group', 'ind']
data.columns=['prop']
data['label']=data.index.get_level_values(2)
#remove nrs from label
data['label']=data.index.get_level_values(2)
data['label']=data['label'].apply(lambda x: x[3:])
filename=graphs_path/'HHoccupation1_time_province.svg'
sns.set_style('ticks')

fig, axes = plt.subplots(nrows=4, ncols=4, sharex='col', figsize=(
    6.25, 6), gridspec_kw={'width_ratios': [2, 4, 4, 4], 'height_ratios': [2, 4, 4, 4],})

# title row.
for i,period in enumerate(period_names_col.keys(),1):
    axes[0,i].annotate(period, **title_anno_opts, color=period_names_col[period])
    # remove spines
    axes[0,i].axis('off')


#province names
for i, provname in enumerate(['Total', 'Punjab', 'Sindh'],1):
    axes[i,0].annotate(provname, xy=(-1.5,0.5), size='medium', xycoords='axes fraction',
                       va='center', ha='center', rotation=90)
    axes[i,0].axis('off') 

#total
for i,period in enumerate(['Baseline', 'Midline', 'Endline'],1):
    axes[1,i].set_xlim(0, 1)
    sel=data.loc[idx['Total',period,:],:]
    axes[1,i].barh(y=sel['label'], width=sel['prop'], color=period_names_col[period])
    # remove spines)
    # labels
    for p in axes[1,i].patches:
        # get_width pulls left or right; get_y pushes up or down
        axes[1,i].text(p.get_width()+0.05, p.get_y()+0.5, "{:.0%}".format(
            p.get_width()), color=p.get_facecolor(), verticalalignment='top', size='xx-small')
    #yaxis invisible on last ax.
    if i > 1:
        axes[1,i].yaxis.set_visible(False)
    sns.despine(ax=axes[1,i])

#Punjab
for i,period in enumerate(['Baseline', 'Midline', 'Endline'],1):
    axes[2,i].set_xlim(0, 1)
    sel=data.loc[idx['Punjab',period,:],:]
    axes[2,i].barh(y=sel['label'], width=sel['prop'], color=period_names_col[period])
    # remove spines)
    # labels
    for p in axes[2,i].patches:
        # get_width pulls left or right; get_y pushes up or down
        axes[2,i].text(p.get_width()+0.05, p.get_y()+0.5, "{:.0%}".format(
            p.get_width()), color=p.get_facecolor(), verticalalignment='top', size='xx-small')
    #yaxis invisible on last ax.
    if i> 1:
        axes[2,i].yaxis.set_visible(False)
    sns.despine(ax=axes[2,i])
#sindh
for i,period in enumerate(['Baseline', 'Midline', 'Endline'],1):
    axes[3,i].set_xlim(0, 1)
    sel=data.loc[idx['Sindh',period,:],:]
    axes[3,i].barh(y=sel['label'], width=sel['prop'], color=period_names_col[period])
    # remove spines)
    # labels
    for p in axes[3,i].patches:
        # get_width pulls left or right; get_y pushes up or down
        axes[3,i].text(p.get_width()+0.05, p.get_y()+0.5, "{:.0%}".format(
            p.get_width()), color=p.get_facecolor(), verticalalignment='top', size='xx-small')
    #yaxis invisible on last ax.
    if i > 1:
        axes[3,i].yaxis.set_visible(False)
    sns.despine(ax=axes[3,i])
#some stuff on all axes.
for ax in fig.axes: 
    ax.xaxis.set_major_formatter(PercentFormatter(xmax=1))
    ax.xaxis.set_tick_params(rotation=90)
    ax.invert_yaxis()

#remove top left ax
axes[0,0].axis('off')
fig.text(0,0, 'Source: MTBA Endline studies n total='+str(len(clean['HHoccupation1'].dropna())) + ' household-heads.', fontsize='small', color='grey')
fig.savefig(filename, bbox_inches='tight')




###number of respondents. Households

#check in which indicator we have the smallest nr of households (as these will be in the matching this will be listwise missing in all subsequent analyses)


period_names_col = {
    'Baseline': '#0B9CDA',
    'Midline': '#53297D',
    'Endline': '#630235'}

#anno options for headings
title_anno_opts = dict(xy=(0.5, 0.5), size='small', xycoords='axes fraction',
                       va='center', ha='center')

idx=pd.IndexSlice


filename=graphs_path/'nrofobs_households_by_time_province.svg'
sns.set_style('ticks')

fig, axes = plt.subplots(nrows=4, ncols=len(period_names_col.keys()), sharex='col', sharey='row', figsize=(
    4, 4), gridspec_kw={'height_ratios': [1, 3, 3, 3 ]})

#totals
#take in hh-set if hhgender= not missing. 
for col in ['HHhhhead_female',  'HHliteracyrate',  'HHnrhhmembers',  'HHdependency',  'PPI_likelihood_inter_200']:
    print("indicator:", col) 
    print("nrmissing:", clean[col].isnull().sum())
#most missings in hh head female
data =clean.dropna(subset=['HHhhhead_female']).groupby(['grouping_period', 'grouping_total']).size().to_frame()
data.columns=['nrobs']

data['label']='no. of households'
# title row.
for i,period in enumerate(period_names_col.keys()):
    axes[0,i].annotate(period, **title_anno_opts, color=period_names_col[period])
    # remove spines
    axes[0,i].axis('off')

#total
for i,period in enumerate(period_names_col.keys()):
    #axes[1,i].set_xlim(0, 1)
    sel=data.loc[idx[period,:,:],:]
    axes[1,i].barh(y=sel['label'], width=sel['nrobs'], color=period_names_col[period])
    # remove spines)
    # labels
    for p in axes[1,i].patches:
        # get_width pulls left or right; get_y pushes up or down
        axes[1,i].text(p.get_width()/2, (p.get_y()+p.get_height()/2), "{:,}".format(
            p.get_width()), color='white', verticalalignment='center', horizontalalignment='center', size='small')
    if i == 0:
        axes[1,i].set_ylabel('Total', fontstyle='oblique')
    
    sns.despine(ax=axes[1,i])


#sindh
data =clean.loc[clean['grouping_province']=='Sindh'].groupby(['grouping_period', 'grouping_total']).size().to_frame()
data.columns=['nrobs']
data['label']='no. of households'
for i,period in enumerate(period_names_col.keys()):
    sel=data.loc[idx[period,:,:],:]
    axes[2,i].barh(y=sel['label'], width=sel['nrobs'], color=period_names_col[period])
    # remove spines)
    # labels
    for p in axes[2,i].patches:
        # get_width pulls left or right; get_y pushes up or down
        axes[2,i].text(p.get_width()+0.05,  (p.get_y()+p.get_height()/2), "{:,}".format(
            p.get_width()), color=p.get_facecolor(), verticalalignment='center', size='small')
    if i == 0:
        axes[2,i].set_ylabel('Sindh', fontstyle='oblique')
    
    sns.despine(ax=axes[2,i])


#punjab
data =clean.loc[clean['grouping_province']=='Punjab'].groupby(['grouping_period', 'grouping_total']).size().to_frame()
data.columns=['nrobs']
data['label']='no. of households'
for i,period in enumerate(period_names_col.keys()):
    sel=data.loc[idx[period,:,:],:]
    axes[3,i].barh(y=sel['label'], width=sel['nrobs'], color=period_names_col[period])
    # remove spines)
    # labels
    for p in axes[3,i].patches:
        # get_width pulls left or right; get_y pushes up or down
        axes[3,i].text(p.get_width()+0.05,  (p.get_y()+p.get_height()/2), "{:,}".format(
            p.get_width()), color=p.get_facecolor(), verticalalignment='center', size='small')
    if i == 0:
        axes[3,i].set_ylabel('Punjab', fontstyle='oblique')
    
    sns.despine(ax=axes[3,i])

#some stuff on all axes.
for ax in fig.axes: 
    ax.set_xlim(0,1200)
fig.align_ylabels()
fig.savefig(filename, bbox_inches='tight')



