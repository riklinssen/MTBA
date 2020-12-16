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















####at risk of GCM by time and age_cat


def survey(results, category_names):
    """
    Parameters
    ----------
    results : dict
        A mapping from question labels to a list of answers per category.
        It is assumed all lists contain the same number of entries and that
        it matches the length of *category_names*.
    category_names : list of str
        The category labels.
    """
    labels = list(results.keys())
    data = np.array(list(results.values()))
    data_cum = data.cumsum(axis=1)
    category_colors = plt.get_cmap('plasma')(
        np.linspace(0.15, 0.85, data.shape[1]))

    fig, ax = plt.subplots(figsize=(9.2, 5))
    ax.invert_yaxis()
    ax.xaxis.set_visible(False)
    axlim=np.sum(data, axis=1).max()
    if axlim==np.nan:
        ax.set_xlim(0,1 )
    else: 
        ax.set_xlim(0)
    #spines
    ax.spines['right'].set_visible(False)
    ax.spines['top'].set_visible(False)
    ax.spines['bottom'].set_visible(False)
    ax.spines['left'].set_visible(False)

   
    for i, (colname, color) in enumerate(zip(category_names, category_colors)):
        widths = data[:, i]
        starts = data_cum[:, i] - widths
        ax.barh(labels, widths, left=starts, height=0.5,
                label=colname, color=color)
        xcenters = starts + widths / 2

        r, g, b, _ = color
        text_color = 'white' if r * g * b < 0.5 else 'darkgrey'
        for y, (x, c) in enumerate(zip(xcenters, widths)):
            ax.text(x, y,  "{:.0%}".format(
            round(c,2)), ha='center', va='center',
                    color=text_color)
       
    if len(category_names)<6: 
        ax.legend(ncol=len(category_names), bbox_to_anchor=(0, 1),
                loc='lower left', fontsize='small', frameon=False)
    if len(category_names)>5:
        ax.legend(ncol=3, bbox_to_anchor=(0, 1),
        loc='lower left', fontsize='small', frameon=False)


    fig.text(0, 0, "Source: Socio-economic impacts of COVID-19 among migrant workers in Laos,\ntotal n="+str(len(clean.loc[:,outcomes[-1]].dropna()))+".", size='x-small',  ha="left", color='gray')
    return fig, ax
































######At risk of GCM by time and age_cat

outcomes=['ind_gcm1',
'ind_gcm2',
'ind_gcm3']
total=clean.groupby(['Gage_cat', 'grouping_period'])[outcomes].mean()
total=total.rename(columns=varlabel_dict)



agecat=['1. 12-14']
sel=total.loc[idx[agecat,:],:].droplevel(0)
#sort 
sel['order']=sel.index.get_level_values('grouping_period').map({"Baseline": 1, "Midline": 2, "Endline": 3})
sel=sel.sort_values(by='order')
sel=sel.drop(columns='order')
category_names=list(sel.index)
labels = list(total.keys())

results=sel.to_dict(orient='records')

data = np.array(list(results.values()))
data_cum = data.cumsum(axis=1)
category_colors = plt.get_cmap('plasma')(np.linspace(0.15, 0.85, data.shape[1]))



fig, ax = plt.subplots(figsize=(9.2, 5))
ax.invert_yaxis()
ax.xaxis.set_visible(False)
axlim=np.sum(data, axis=1).max()
if axlim==np.nan:
    ax.set_xlim(0,1 )
else: 
    ax.set_xlim(0)
#spines
ax.spines['right'].set_visible(False)
ax.spines['top'].set_visible(False)
ax.spines['bottom'].set_visible(False)
ax.spines['left'].set_visible(False)


for i, (colname, color) in enumerate(zip(category_names, category_colors)):
    widths = data[:, i]
    starts = data_cum[:, i] - widths
    ax.barh(labels, widths, left=starts, height=0.5,
            label=colname, color=color)
    xcenters = starts + widths / 2

    r, g, b, _ = color
    text_color = 'white' if r * g * b < 0.5 else 'darkgrey'
    for y, (x, c) in enumerate(zip(xcenters, widths)):
        ax.text(x, y,  "{:.0%}".format(
        round(c,2)), ha='center', va='center',
                color=text_color)
    
if len(category_names)<6: 
    ax.legend(ncol=len(category_names), bbox_to_anchor=(0, 1),
            loc='lower left', fontsize='small', frameon=False)
if len(category_names)>5:
    ax.legend(ncol=3, bbox_to_anchor=(0, 1),
    loc='lower left', fontsize='small', frameon=False)


fig.text(0, 0, "'blabla", size='x-small',  ha="left", color='gray')
fig.show()

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
