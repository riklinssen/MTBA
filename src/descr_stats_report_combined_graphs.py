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

#######################################################################################################


########descriptive stats report TOTALS + province. Mega graphs. 
#o	Age
#o	At risk of CM
#o	Level of education
#o	Religion --> not relevant


idx=pd.IndexSlice

province_names_col = {
    'Total': '#000000',
    'Sindh': '#E43989',
    'Punjab': '#0B9CDA'}

fig, axes = plt.subplots(nrows=3, ncols=3, sharey='row', sharex='col', figsize=(
    6.25, 6.25*1.61),  gridspec_kw={'width_ratios': [3, 3, 3,],'height_ratios': [3, 7, 3],})

filename=graphs_path/'descriptives_girls_chars.svg'   

#age
outcome='Gage_cat'
tots =clean.groupby(['grouping_total'])[outcome].value_counts(normalize=True, dropna=True).to_frame()
tots.index.set_names(['group', 'category'], inplace=True)
prov =clean.groupby(['grouping_province'])[outcome].value_counts(normalize=True, dropna=True).to_frame()
prov.index.set_names(['group', 'category'], inplace=True)
data=pd.concat([tots, prov], axis=0)
data.columns=['prop']
#make labels
data['label']=data.index.get_level_values(1)
data['label']=data['label'].apply(lambda x: x[2:])

for i,prov in enumerate(province_names_col.keys()):
    #coltitles
    axes[0,i].set_title(prov, color=province_names_col[prov])
    sel=data.loc[idx[prov,:],:]
    axes[0,i].barh(y=sel['label'], width=sel['prop'], color=province_names_col[prov])
    #labels. 
    for p in axes[0,i].patches:
        # get_width pulls left or right; get_y pushes up or down
        if p.get_width()>=0.5: 
            axes[0,i].text(p.get_width()/2, p.get_y()+0.5, "{:.0%}".format(p.get_width()), color='white', verticalalignment='top', horizontalalignment='center', size='small')
        else:
            axes[0,i].text(p.get_width()*1.1, p.get_y()+0.5, "{:.0%}".format(p.get_width()), color=p.get_facecolor(), verticalalignment='top', horizontalalignment='left', size='small')
    #xlims
    axes[0,i].set_xlim(0,1)
    axes[0,i].xaxis.set_major_formatter(PercentFormatter(xmax=1))

    #y-lebel
    axes[0,0].set_ylabel('by age', fontstyle='oblique', color='grey')

#Level of education
outcome='Geducation'
tots =clean.groupby(['grouping_total'])[outcome].value_counts(normalize=True, dropna=True).to_frame()
tots.index.set_names(['group', 'category'], inplace=True)
prov =clean.groupby(['grouping_province'])[outcome].value_counts(normalize=True, dropna=True).to_frame()
prov.index.set_names(['group', 'category'], inplace=True)
data=pd.concat([tots, prov], axis=0)
data.columns=['prop']
#make labels
data['label']=data.index.get_level_values(1)
data['label']=data['label'].apply(lambda x: x[2:])

for i,prov in enumerate(province_names_col.keys()):
    sel=data.loc[idx[prov,:],:]
    axes[1,i].barh(y=sel['label'], width=sel['prop'], color=province_names_col[prov])
    #labels. 
    for p in axes[1,i].patches:
        # get_width pulls left or right; get_y pushes up or down
        if p.get_width()>=0.5: 
            axes[1,i].text(p.get_width()/2, p.get_y()+0.5, "{:.0%}".format(p.get_width()), color='white', verticalalignment='top', horizontalalignment='center', size='small')
        else:
            axes[1,i].text(p.get_width()*1.1, p.get_y()+0.5, "{:.0%}".format(p.get_width()), color=p.get_facecolor(), verticalalignment='top', horizontalalignment='left', size='small')
    #xlims
    axes[1,i].set_xlim(0,1)
    axes[1,i].xaxis.set_major_formatter(PercentFormatter(xmax=1))

    #y-lebel
    axes[1,0].set_ylabel('by level of education', fontstyle='oblique', color='grey')

#o	At risk of CM

outcome='ind_Gcm'
tots =clean.groupby(['grouping_total'])[outcome].value_counts(normalize=True, dropna=True).to_frame()
tots.index.set_names(['group', 'category'], inplace=True)
prov =clean.groupby(['grouping_province'])[outcome].value_counts(normalize=True, dropna=True).to_frame()
prov.index.set_names(['group', 'category'], inplace=True)
data=pd.concat([tots, prov], axis=0)
data.columns=['prop']
#make labels
data['label']=data.index.get_level_values(1)

for i,prov in enumerate(province_names_col.keys()):
    sel=data.loc[idx[prov,:],:]
    axes[2,i].barh(y=sel['label'], width=sel['prop'], color=province_names_col[prov])
    #labels. 
    for p in axes[2,i].patches:
        # get_width pulls left or right; get_y pushes up or down
        if p.get_width()>=0.5: 
            axes[2,i].text(p.get_width()/2, p.get_y()+0.5, "{:.0%}".format(p.get_width()), color='white', verticalalignment='top', horizontalalignment='center', size='small')
        else:
            axes[2,i].text(p.get_width()*1.1, p.get_y()+0.5, "{:.0%}".format(p.get_width()), color=p.get_facecolor(), verticalalignment='top', horizontalalignment='left', size='small')
    #xlims
    axes[2,i].set_xlim(0,1)
    axes[2,i].xaxis.set_major_formatter(PercentFormatter(xmax=1))

    #y-lebel
    axes[2,0].set_ylabel('at risk of CM', fontstyle='oblique', color='grey')
#some stuff on all axes.
for ax in fig.axes: 
    ax.xaxis.set_tick_params(rotation=90)
    sns.despine(ax=ax)

fig.align_ylabels()
fig.text(0,0, 'Source: MTBA Endline studies n total='+str(len(clean[outcome].dropna())) + ' girls (baseline+midline+endline).', fontsize='small', color='grey')
fig.savefig(filename, bbox_inches='tight')






############################################household head characteristics 1##########################.
#HHhhhead_female
#HHhhhead_marital
#HHhhhead_educ
#HHreadwrite1
#HHhhhead_occup
#HHhhhead_age_cat

#make age categories
clean['HHhhhead_age_cat']=pd.cut(clean['HHhhhead_age'], bins=[0,25, 35,45,55,65, 100],labels=['<25','25-35', '35-45', '45-55', '55-65', '65+'])


##group some marital status. 
##mashing together 
#  1. Engaged  & 3. Nikkah Shuda
#  4. Divorced &  5. Separated

clean['HHhhhead_marital_r']=clean['HHhhhead_marital'].cat.codes.map(
    { -1: np.nan, 
    0: 'Single',
    1: 'Engaged/Nikkah Shuda', 
    2: 'Married',
    3: 'Engaged/Nikkah Shuda', 
    4: 'Divorced/Separated', 
    5: 'Divorced/Separated',
    6: 'Widow(er)'
    })

print(clean['HHhhhead_marital'].cat.categories)
print(clean['HHhhhead_marital_r'].value_counts(dropna=False))
print(clean['HHhhhead_marital'].value_counts(dropna=False))





province_names_col = {
    'Total': '#000000',
    'Sindh': '#E43989',
    'Punjab': '#0B9CDA'}

fig, axes = plt.subplots(nrows=6, ncols=3, sharey='row', sharex='col', figsize=(
    6.25, 11),  gridspec_kw={'width_ratios': [3, 3, 3,],'height_ratios': [2, 6, 7, 1, 7,6],})
filename=graphs_path/'descriptives_hh_head_chars.svg'   

#HHhhhead_female
outcome='HHhhhead_female'
tots =clean.groupby(['grouping_total'])[outcome].value_counts(normalize=True, dropna=True).to_frame()
tots.index.set_names(['group', 'category'], inplace=True)
prov =clean.groupby(['grouping_province'])[outcome].value_counts(normalize=True, dropna=True).to_frame()
prov.index.set_names(['group', 'category'], inplace=True)
data=pd.concat([tots, prov], axis=0)
data.columns=['prop']
#make labels
data['label']=data.index.get_level_values(1).map({'0. No': 'Male', '1. Yes': 'Female'})


for i,prov in enumerate(province_names_col.keys()):
    #coltitles
    axes[0,i].set_title(prov, color=province_names_col[prov])
    sel=data.loc[idx[prov,:],:]
    axes[0,i].barh(y=sel['label'], width=sel['prop'], color=province_names_col[prov])
    #labels. 
    for p in axes[0,i].patches:
        # get_width pulls left or right; get_y pushes up or down
        if p.get_width()>=0.5: 
            axes[0,i].text(p.get_width()/2, p.get_y()+(p.get_height()/2), "{:.0%}".format(p.get_width()), color='white', verticalalignment='center', horizontalalignment='center', size='small')
        else:
            axes[0,i].text(p.get_width()*1.1, p.get_y()+(p.get_height()/2), "{:.0%}".format(p.get_width()), color=p.get_facecolor(), verticalalignment='center', horizontalalignment='left', size='small')
    #xlims
    axes[0,i].set_xlim(0,1)
    axes[0,i].xaxis.set_major_formatter(PercentFormatter(xmax=1))

    #y-lebel
    axes[0,0].set_ylabel('hh-head:\ngender:', fontstyle='oblique', color='grey')

#HHhhhead_marital
outcome='HHhhhead_marital_r'
tots =clean.groupby(['grouping_total'])[outcome].value_counts(normalize=True, dropna=True).to_frame()
tots.index.set_names(['group', 'category'], inplace=True)
prov =clean.groupby(['grouping_province'])[outcome].value_counts(normalize=True, dropna=True).to_frame()
prov.index.set_names(['group', 'category'], inplace=True)
data=pd.concat([tots, prov], axis=0)
data.columns=['prop']
#make labels
data['label']=data.index.get_level_values(1)

for i,prov in enumerate(province_names_col.keys()):
    sel=data.loc[idx[prov,:],:]
    axes[1,i].barh(y=sel['label'], width=sel['prop'], color=province_names_col[prov])
    #labels. 
    for p in axes[1,i].patches:
        # get_width pulls left or right; get_y pushes up or down
        if p.get_width()>=0.5: 
            axes[1,i].text(p.get_width()/2, p.get_y()+(p.get_height()/2), "{:.0%}".format(p.get_width()), color='white', verticalalignment='center', horizontalalignment='center', size='small')
        else:
            axes[1,i].text(p.get_width()*1.1, p.get_y()+(p.get_height()/2), "{:.0%}".format(p.get_width()), color=p.get_facecolor(), verticalalignment='center', horizontalalignment='left', size='small')
    #xlims
    axes[1,i].set_xlim(0,1)
    axes[1,i].xaxis.set_major_formatter(PercentFormatter(xmax=1))

    #y-lebel
    axes[1,0].set_ylabel('Marital status\nHH-head', fontstyle='oblique', color='grey')

#HHhhhead_educ
outcome='HHhhhead_educ'
tots =clean.groupby(['grouping_total'])[outcome].value_counts(normalize=True, dropna=True).to_frame()
tots.index.set_names(['group', 'category'], inplace=True)
prov =clean.groupby(['grouping_province'])[outcome].value_counts(normalize=True, dropna=True).to_frame()
prov.index.set_names(['group', 'category'], inplace=True)
data=pd.concat([tots, prov], axis=0)
data.columns=['prop']
#make labels
data['label']=data.index.get_level_values(1)
data['label']=data['label'].apply(lambda x: x[2:])


for i,prov in enumerate(province_names_col.keys()):
    sel=data.loc[idx[prov,:],:]
    axes[2,i].barh(y=sel['label'], width=sel['prop'], color=province_names_col[prov])
    #labels. 
    for p in axes[2,i].patches:
        # get_width pulls left or right; get_y pushes up or down
        if p.get_width()>=0.5: 
            axes[2,i].text(p.get_width()/2, p.get_y()+(p.get_height()/2), "{:.0%}".format(p.get_width()), color='white', verticalalignment='center', horizontalalignment='center', size='small')
        else:
            axes[2,i].text(p.get_width()*1.1, p.get_y()+(p.get_height()/2), "{:.0%}".format(p.get_width()), color=p.get_facecolor(), verticalalignment='center', horizontalalignment='left', size='small')
    #xlims
    axes[2,i].set_xlim(0,1)
    axes[2,i].xaxis.set_major_formatter(PercentFormatter(xmax=1))

    #y-lebel
    axes[2,0].set_ylabel('Level of education\n(completed)', fontstyle='oblique', color='grey')


#HHreadwrite1
outcome='HHreadwrite1'
tots =clean.groupby(['grouping_total'])[outcome].value_counts(normalize=True, dropna=True).to_frame()
tots.index.set_names(['group', 'category'], inplace=True)
prov =clean.groupby(['grouping_province'])[outcome].value_counts(normalize=True, dropna=True).to_frame()
prov.index.set_names(['group', 'category'], inplace=True)
data=pd.concat([tots, prov], axis=0)
data.columns=['prop']
#make labels
data['label']=data.index.get_level_values(1)
data['label']=data['label'].apply(lambda x: x[2:])


for i,prov in enumerate(province_names_col.keys()):
    sel=data.loc[idx[prov,:],:]
    axes[3,i].barh(y=sel['label'], width=sel['prop'], color=province_names_col[prov])
    #labels. 
    for p in axes[3,i].patches:
        # get_width pulls left or right; get_y pushes up or down
        if p.get_width()>=0.5: 
            axes[3,i].text(p.get_width()/2, p.get_y()+(p.get_height()/2), "{:.0%}".format(p.get_width()), color='white', verticalalignment='center', horizontalalignment='center', size='small')
        else:
            axes[3,i].text(p.get_width()*1.1, p.get_y()+(p.get_height()/2), "{:.0%}".format(p.get_width()), color=p.get_facecolor(), verticalalignment='center', horizontalalignment='left', size='small')
    #xlims
    axes[3,i].set_xlim(0,1)
    axes[3,i].xaxis.set_major_formatter(PercentFormatter(xmax=1))

    #y-lebel
    axes[3,0].set_ylabel('HH-head\nis literate', fontstyle='oblique', color='grey')

#HHhhhead_occup
outcome='HHhhhead_occup'
tots =clean.groupby(['grouping_total'])[outcome].value_counts(normalize=True, dropna=True).to_frame()
tots.index.set_names(['group', 'category'], inplace=True)
prov =clean.groupby(['grouping_province'])[outcome].value_counts(normalize=True, dropna=True).to_frame()
prov.index.set_names(['group', 'category'], inplace=True)
data=pd.concat([tots, prov], axis=0)
data.columns=['prop']
#make labels
data['label']=data.index.get_level_values(1)
data['label']=data['label'].apply(lambda x: x[2:])


for i,prov in enumerate(province_names_col.keys()):
    sel=data.loc[idx[prov,:],:]
    axes[4,i].barh(y=sel['label'], width=sel['prop'], color=province_names_col[prov])
    #labels. 
    for p in axes[4,i].patches:
        # get_width pulls left or right; get_y pushes up or down
        if p.get_width()>=0.5: 
            axes[4,i].text(p.get_width()/2, p.get_y()+(p.get_height()/2), "{:.0%}".format(p.get_width()), color='white', verticalalignment='center', horizontalalignment='center', size='small')
        else:
            axes[4,i].text(p.get_width()*1.1, p.get_y()+(p.get_height()/2), "{:.0%}".format(p.get_width()), color=p.get_facecolor(), verticalalignment='center', horizontalalignment='left', size='small')
    #xlims
    axes[4,i].set_xlim(0,1)
    axes[4,i].xaxis.set_major_formatter(PercentFormatter(xmax=1))

    #y-lebel
    axes[4,0].set_ylabel('Occupation\nHH-head', fontstyle='oblique', color='grey')

#HHhhhead_age_cat


outcome='HHhhhead_age_cat'
tots =clean.groupby(['grouping_total'])[outcome].value_counts(normalize=True, dropna=True).to_frame()
tots.index.set_names(['group', 'category'], inplace=True)
prov =clean.groupby(['grouping_province'])[outcome].value_counts(normalize=True, dropna=True).to_frame()
prov.index.set_names(['group', 'category'], inplace=True)
data=pd.concat([tots, prov], axis=0)
data.columns=['prop']

#make labels
data['label']=data.index.get_level_values(1)


#sort according to age category. 
data['srt']=data['label'].map(dict(zip(['<25','25-35', '35-45', '45-55', '55-65', '65+'], range(6))))

for i,prov in enumerate(province_names_col.keys()):
    sel=data.loc[idx[prov,:],:]
    sel=sel.sort_values(by='srt')
    axes[5,i].barh(y=sel['label'], width=sel['prop'], color=province_names_col[prov])
    #labels. 
    for p in axes[5,i].patches:
        # get_width pulls left or right; get_y pushes up or down
        if p.get_width()>=0.5: 
            axes[5,i].text(p.get_width()/2, p.get_y()+(p.get_height()/2), "{:.0%}".format(p.get_width()), color='white', verticalalignment='center', horizontalalignment='center', size='small')
        else:
            axes[5,i].text(p.get_width()*1.1, p.get_y()+(p.get_height()/2), "{:.0%}".format(p.get_width()), color=p.get_facecolor(), verticalalignment='center', horizontalalignment='left', size='small')
    #xlims
    axes[5,i].set_xlim(0,1)
    axes[5,i].xaxis.set_major_formatter(PercentFormatter(xmax=1))

    #y-lebel
    axes[5,0].set_ylabel('Age of\nHH-head', fontstyle='oblique', color='grey')
#some stuff on all axes.
for ax in fig.axes: 
    ax.xaxis.set_tick_params(rotation=90)
    sns.despine(ax=ax)

fig.align_ylabels()
fig.text(0,0, 'Source: MTBA Endline studies n total='+str(len(clean[outcome].dropna())) + ' households (baseline+midline+endline).', fontsize='small', color='grey')
fig.savefig(filename, bbox_inches='tight')


##now for socio-economics (and continuous vars)

############################################household characteristics 1##########################.


##HHliteracyrate
#HHnrhhmembers
#HHdependency
#PPI_likelihood_inter_200

title_anno_opts = dict(xy=(0.5, 0.8), size='medium', xycoords='axes fraction',
                       va='top', ha='center')

sns.set_style('ticks')
filename=graphs_path/'descriptives_household_chars1.svg'   
fig, axes=plt.subplots(nrows=4, ncols=2, sharex='col', figsize= (6.25, 6.25/1.61))




#HHnrhhmembers
### literacy rate
outcome,outcol='HHnrhhmembers', 0
total_df=clean.loc[:,[outcome, 'grouping_total']].dropna()
sindh_df=clean.loc[clean['grouping_province']=='Sindh', ['grouping_province', outcome]].dropna()
punjab_df=clean.loc[clean['grouping_province']=='Punjab', ['grouping_province', outcome]].dropna()

for plotrow, df, prov in zip([1,2,3],[total_df, sindh_df, punjab_df], province_names_col.keys()):
    sns.kdeplot(x=outcome,  cut=0, fill=True, alpha=0.3, data=df, color=province_names_col[prov], ax=axes[plotrow,outcol])
    #plot average line. 
    avgline=axes[plotrow,outcol].axvline(x=df[outcome].mean(), ymin=0, ymax=0.8, color=province_names_col[prov], ls='--')
    #inv = avgline.transData.inverted()

    #label for avg
    x,y=avgline.get_xdata()[1],avgline.get_ydata()[1]
    lab="{:.2f}".format(x)
    
    axes[plotrow,outcol].text(x, .17, 'avg:\n'+lab , color=province_names_col[prov], verticalalignment='bottom', horizontalalignment='center', size='small')
    #y-label
    axes[plotrow,outcol].set_ylabel(prov, color=province_names_col[prov], fontstyle='oblique')
    #x-axis formatter
    #axes[plotrow,outcol].xaxis.set_major_formatter(PercentFormatter(xmax=1))
    # x-axis label
    axes[plotrow,outcol].set_xlabel('no of of household-members', fontstyle='oblique', color='grey')
    axes[plotrow,outcol].set_xlim(0,15)


#titlerow. 
axes[0,0].annotate('Household size:\n(no of of household-members)', **title_anno_opts, color='black')
axes[0,0].axis('off')


### literacy rate
outcome,outcol='HHliteracyrate', 1
total_df=clean.loc[:,[outcome, 'grouping_total']].dropna()
sindh_df=clean.loc[clean['grouping_province']=='Sindh', ['grouping_province', outcome]].dropna()
punjab_df=clean.loc[clean['grouping_province']=='Punjab', ['grouping_province', outcome]].dropna()

for plotrow, df, prov in zip([1,2,3],[total_df, sindh_df, punjab_df], province_names_col.keys()):
    sns.kdeplot(x=outcome,  cut=0, fill=True, alpha=0.3, data=df, color=province_names_col[prov], ax=axes[plotrow,outcol])
    #plot average line. 
    avgline=axes[plotrow,outcol].axvline(x=df[outcome].mean(), ymin=0, ymax=0.8, color=province_names_col[prov], ls='--')
    #label for avg
    x,y=avgline.get_xdata()[1],avgline.get_ydata()[1]
    lab="{:.0%}".format(x)
    # "{:.2f}".format(x)
    axes[plotrow,outcol].text(x, y+0.25, 'avg:\n'+lab , color=province_names_col[prov], verticalalignment='bottom', horizontalalignment='center', size='small')
    #y-label
    axes[plotrow,outcol].set_ylabel(prov, color=province_names_col[prov], fontstyle='oblique')
    #x-axis formatter
    axes[plotrow,outcol].xaxis.set_major_formatter(PercentFormatter(xmax=1))
    # x-axis label
    axes[plotrow,outcol].set_xlabel('Literacy-rate', fontstyle='oblique', color='grey')


#titlerow. 
axes[0,1].annotate('Household literacy rate:\n(% of household-members aged>15\nable to read and write)', **title_anno_opts, color='black')
    # remove axis
axes[0,1].axis('off')


for ax in fig.axes: 
    ax.xaxis.set_tick_params(rotation=90)
    ax.spines['right'].set_visible(False)
    ax.spines['top'].set_visible(False)
    ax.spines['left'].set_visible(False)
    ax.spines['bottom'].set_visible(True)
    ax.axes.yaxis.set_ticks([])
    

fig.tight_layout()
fig.align_xlabels()
fig.text(0,0, 'Source: MTBA Endline studies n total='+str(len(clean[outcome].dropna())) + ' households (baseline+midline+endline).', fontsize='small', color='grey')
fig.savefig(filename, bbox_inches='tight')






############################################household characteristics 2##########################.

#HHdependency
#PPI_likelihood_inter_200

title_anno_opts = dict(xy=(0.5, 0.8), size='medium', xycoords='axes fraction',
                       va='top', ha='center')

sns.set_style('ticks')
filename=graphs_path/'descriptives_household_chars2.svg'   
fig, axes=plt.subplots(nrows=4, ncols=2, sharex='col', figsize= (6.25, 6.25/1.61))




#HHdependency
### literacy rate
outcome,outcol='HHdependency', 0
total_df=clean.loc[:,[outcome, 'grouping_total']].dropna()
sindh_df=clean.loc[clean['grouping_province']=='Sindh', ['grouping_province', outcome]].dropna()
punjab_df=clean.loc[clean['grouping_province']=='Punjab', ['grouping_province', outcome]].dropna()

for plotrow, df, prov in zip([1,2,3],[total_df, sindh_df, punjab_df], province_names_col.keys()):
    sns.kdeplot(x=outcome,  cut=0, fill=True, alpha=0.3, data=df, color=province_names_col[prov], ax=axes[plotrow,outcol])
    #plot average line. 
    avgline=axes[plotrow,outcol].axvline(x=df[outcome].mean(), ymin=0, ymax=0.8, color=province_names_col[prov], ls='--')
    #inv = avgline.transData.inverted()

    #label for avg
    x,y=avgline.get_xdata()[1],avgline.get_ydata()[1]
    lab="{:.2f}".format(x)
    
    axes[plotrow,outcol].text(x, .6, 'avg:\n'+lab , color=province_names_col[prov], verticalalignment='bottom', horizontalalignment='center', size='small')
    #y-label
    axes[plotrow,outcol].set_ylabel(prov, color=province_names_col[prov], fontstyle='oblique')
    #x-axis formatter
    #axes[plotrow,outcol].xaxis.set_major_formatter(PercentFormatter(xmax=1))
    # x-axis label
    axes[plotrow,outcol].set_xlabel('dependency-ratio', fontstyle='oblique', color='grey')
    axes[plotrow,outcol].set_xlim(0,3)


#titlerow. 
axes[0,0].annotate('Household-dependency ratio:\n' + r'$\frac{no.\ of\ people\ below\ 15\ and\ over\ 65\ in\ HH}{no.\ of\ people\ aged\ 15\ to\ 65\ in\ HH}$' +'\n(higher values mean more dependants)', **title_anno_opts, color='black')
axes[0,0].axis('off')

#Household dependency ratio:\nr of people below 15 and over 65/
### literacy rate
outcome,outcol='PPI_likelihood_inter_200', 1
total_df=clean.loc[:,[outcome, 'grouping_total']].dropna()
sindh_df=clean.loc[clean['grouping_province']=='Sindh', ['grouping_province', outcome]].dropna()
punjab_df=clean.loc[clean['grouping_province']=='Punjab', ['grouping_province', outcome]].dropna()

for plotrow, df, prov in zip([1,2,3],[total_df, sindh_df, punjab_df], province_names_col.keys()):
    sns.kdeplot(x=outcome,  cut=0, fill=True, alpha=0.3, data=df, color=province_names_col[prov], ax=axes[plotrow,outcol])
    #plot average line. 
    avgline=axes[plotrow,outcol].axvline(x=df[outcome].mean(), ymin=0, ymax=0.8, color=province_names_col[prov], ls='--')
    #label for avg
    x,y=avgline.get_xdata()[1],avgline.get_ydata()[1]
    lab="{:.2f}".format(x)
    # "{:.2f}".format(x)
    axes[plotrow,outcol].text(x, 0.016, 'avg:\n'+lab , color=province_names_col[prov], verticalalignment='bottom', horizontalalignment='center', size='small')
    #y-label
    axes[plotrow,outcol].set_ylabel(prov, color=province_names_col[prov], fontstyle='oblique')
    #x-axis formatter
    #axes[plotrow,outcol].xaxis.set_major_formatter(PercentFormatter(xmax=1))
    # x-axis label
    axes[plotrow,outcol].set_xlabel('PPI-score', fontstyle='oblique', color='grey')


#titlerow. 
axes[0,1].annotate('Likelihood of\nliving below povertly line: PPI-score (0-100)\n(higher values are poorer households)', **title_anno_opts, color='black')
    # remove axis
axes[0,1].axis('off')


for ax in fig.axes: 
    ax.xaxis.set_tick_params(rotation=90)
    ax.spines['right'].set_visible(False)
    ax.spines['top'].set_visible(False)
    ax.spines['left'].set_visible(False)
    ax.spines['bottom'].set_visible(True)
    ax.axes.yaxis.set_ticks([])
    

fig.tight_layout()
fig.align_xlabels()
fig.text(0,-0.1, 'Source: MTBA Endline studies n total='+str(len(clean[outcome].dropna())) + ' households (baseline+midline+endline).\nBelow poverty line is incomes of <$2 a day', fontsize='small', color='grey')
fig.savefig(filename, bbox_inches='tight')

