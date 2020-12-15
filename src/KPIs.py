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

clean['grouping_target']=clean['code_group'].cat.rename_categories({"0. Comparison": "Comparison group", "1. Target": "Target group"})

sindh=clean.loc[clean['grouping_province']=='Sindh']
punjab=clean.loc[clean['grouping_province']=='Punjab']
#% of girls married before 18 ind_Gcm_18


outcomes=['ind_Gcm_18']

for c in outcomes:
    print(clean[c].cat.codes.value_counts(dropna=False))
    clean[c]=clean[c].cat.codes.map({-1:np.nan,0:0, 1:1})

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
##try first graph
title_anno_opts = dict(xy=(0, 0.5), size='medium', xycoords='axes fraction',
                       va='center', ha='center', rotation=90)
outcomes=['ind_Gcm_18']
ylab='% of girls married\n<18 yrs old'
filename=str(outcomes) +'.svg'
sns.set_style('ticks')
sns.set_context(context='notebook')
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
        axes[i,1].text(x=row['order']-1, y=row['mean']+0.05, s='{:.0%}'.format(row['mean']), ha='center', size='small', color=subset_colors[sub])
    
    
    #comparison
    comp=stats.loc[idx['Comparison group',:],:].droplevel(0).sort_values(by='order')
    axes[i,1].plot(comp.index, comp['mean'], marker='.', linestyle=':', color='grey', label='Comparison\ngroup')
    #axes[i,1].line(target.index, target['mean'], color=subset_colors[sub])
    axes[i,1].fill_between(comp.index,comp['lower'], comp['upper'], color='grey', alpha=0.2)


#some settings on all axes.
axes[0,1].legend(loc='upper center', bbox_to_anchor=(0.8, 1.15),
          ncol=1, fontsize='small',  fancybox=False, shadow=False, frameon=False)   
for ax in fig.axes: 
    ax.yaxis.set_major_formatter(PercentFormatter(xmax=1,decimals=0))
    sns.despine(ax=ax)
    ax.set_ylabel(ylab, fontstyle='oblique')
fig.text(0,0, 'Source: MTBA Endline studies n total='+str(len(clean[outcomes].dropna())) + ' girls.\nShaded areas represent 95% CI of the mean.', fontsize='small', color='grey')
fig.savefig(graphs_path/filename)



##try to wrap above in func
sns.set_style('ticks')
sns.set_context(context='notebook')
    
def make_kpi_fig(outcomes, ylab, suptit):
    """returns fig in graphs path for outcomes (dummys/%)

    Parameters
    ----------
    outcomes : list
        outcome in list
    ylab : str
        y-axis label
    suptit : str
        suptitle (for keeping track mostly KPI-title)
    """    
    #conversion to numerical
    for c in outcomes:
        for df in [clean, sindh, punjab]:
            if df[c].dtype.name=='category': 
                df[c]=df[c].cat.codes.map({-1:np.nan,0:0, 1:1})
            print(df[c].value_counts(dropna=False))

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
            axes[i,1].text(x=row['order']-1, y=row['mean']+0.05, s='{:.0%}'.format(row['mean']), ha='center', size='small', color=subset_colors[sub])
        
        
        #comparison
        comp=stats.loc[idx['Comparison group',:],:].droplevel(0).sort_values(by='order')
        axes[i,1].plot(comp.index, comp['mean'], marker='.', linestyle=':', color='grey', label='Comparison\ngroup')
        #axes[i,1].line(target.index, target['mean'], color=subset_colors[sub])
        axes[i,1].fill_between(comp.index,comp['lower'], comp['upper'], color='grey', alpha=0.2)


    #some settings on all axes.
    axes[0,1].legend(loc='upper center', bbox_to_anchor=(0.8, 1.15),
            ncol=1, fontsize='small',  fancybox=False, shadow=False, frameon=False)   
    for ax in fig.axes: 
        ax.yaxis.set_major_formatter(PercentFormatter(xmax=1,decimals=0))
        sns.despine(ax=ax)
        ax.set_ylabel(ylab, fontstyle='oblique')
    fig.suptitle(suptit, x=0, y=0.98, ha='left', size='medium', fontweight='bold', color='Black')
    fig.text(0,0, 'Source: MTBA Endline studies n total='+str(len(clean[outcomes].dropna())) + ' girls.\nShaded areas represent 95% CI of the mean.', fontsize='small', color='grey')
    fig.savefig(graphs_path/filename)
    fig.show()
        




##first do for all percentages. 

make_kpi_fig(['ind_Gcm_18'],'% of girls married\n<18 yrs old', 'KPI: % of girls married before 18') 
#ind_Gcm_18_ofmaried --> not in data
#make_kpi_fig(['ind_Gcm_18_ofmaried'],'% of married girls\n married before 18', 'KPI: % of girls that are married who married before 18') 
# % of girls who said best age for a girl to get married is >18
make_kpi_fig(['ind_Glegalage'],'% of girls saying\nbest age to marry >18', 'KPI: % of girls who said best age for a girl to get married is >18') 


#% of girls who discuss if they face SRHR problems
make_kpi_fig(['ind_Gdiscusssrhr'], '% of girls discus\nfacing SRHR problems', 'KPI: % of girls who discuss if they face SRHR problems')
#% of girls contributing to income
make_kpi_fig(['ind_Gincomeshare'], '% of girls\ncontributing to income', 'KPI: % of girls contributing to income')

#% of girls receiving personal allowance/cash
make_kpi_fig(['ind_allowancecash'], '% of girls\nreceiving allowance/cash', 'KPI: % of girls receiving personal allowance/cash')

#% of girls receiving personal allowance/cash
make_kpi_fig(['ind_allowancecash'], '% of girls\nreceiving allowance/cash', 'KPI: % of girls receiving personal allowance/cash')

#% of girls with increased access to economic opportunities
make_kpi_fig(['ind_Geconomic'], '% of girls\nincreased access', 'KPI: % of girls with increased access to economic opportunities')

#% of girls attending school/who attended school (formal)
make_kpi_fig(['ind_school'], '% of girls\attended school', 'KPI: % of girls attending school/who attended school (formal)')


#% married girls 
make_kpi_fig(['ind_Gm'], '% married girls\n(total) ', 'KPI: %  married girls\n(total)')
make_kpi_fig(['ind_Gcm_15'], '% married girls\n before 15 ', 'KPI: % married girls\nbefore 15')
make_kpi_fig(['ind_Gcm_18'], '% married girls\n before 18 ', 'KPI: % married girls\nbefore 18')

# When you got married to your husband, how did you feel about the marriage?
make_kpi_fig(['ind_Gmarried_noconsent'], '% girls wanted\nto marry later ', 'KPI: % Girls wanted to get married later\nWhen you got married to your husband, how did you feel about the marriage?')

#When you got pregnant, did you want to get pregnant at that time?
make_kpi_fig(['ind_children_consent'], '% girls wanted\nto get pregnant ', 'KPI: % Girls wanted to get pregnant\nWhen you got pregnant, did you want to get pregnant at that time?\n% out of ever pregnant girls')
#OC 1.1: % girls  with basic correct knowledge on SRHR
make_kpi_fig(['ind_srhrinfo'], '% girls who have\ncorrect knowldge', 'OC 1.1: % girls  with basic correct knowledge on SRHR')

#OC 1.7: % girls who started menstruating, with basic knowledge about menstruation
make_kpi_fig(['ind_menstruation'], '% girls who had\nnbasic knowledge', 'OC 1.7: % girls who started menstruating,\nwith basic knowledge about menstruation')

#Girls participating in income generating activities
make_kpi_fig(['ind_Geconomic'], '% girls with\nincreased access', 'Girls participating in income generating activities\nif having an occupation & contribute to income')


#Girls participating in unpaid care work
make_kpi_fig(['ind_Gunpaidcare'], '% girls doing\nunpaid care work', 'Girls participating in unpaid care work')




#covid stuff endline only
endline=clean.loc[clean['grouping_period']=='Endline']





def get_mean_ci_in_endline(df,outcomes):
    groupings= ['grouping_target']
    outcomes=[c for c in outcomes]
    #recode cats
    for c in outcomes:
        if df[c].dtype.name=='category': 
            df[c]=df[c].cat.codes.map({-1:np.nan,0:0, 1:1})
            print(df[c].value_counts(dropna=False))
    print(outcomes)
    outcomedfs=[]
    for c in outcomes: 
        colnames=[str(c)+'_mean', str(c)+'_sem',str(c)+'_size']
        mean_outcome=df.groupby(groupings)[outcomes].agg(['mean', 'sem', 'count'])
        mean_outcome.columns=colnames
        meancolname=str(c)+'_mean'
        semcolname=str(c)+'_sem'
        mean_outcome[str(c)+'_lower']=mean_outcome[meancolname]-1.96*mean_outcome[semcolname]
        mean_outcome[str(c)+'_upper']=mean_outcome[meancolname]+1.96*mean_outcome[semcolname]
        ##add order
        outcomedfs.append(mean_outcome)
    data=pd.concat(outcomedfs)
    return data


sindh_endline=endline.loc[clean['grouping_province']=='Sindh']
punjab_endline=endline.loc[clean['grouping_province']=='Punjab']

sns.set_style('white')


def make_cov_dum_fig(outcomes, ylab, suptit):
    """returns fig for single dummy, by target group for total, punjab, sindh, endline onl. Saved in graphs path

    Parameters
    ----------
    outcomes : [list]
        outcomes (single dummy)
    ylab : str
        label for yaxis
    suptit : str
        suptitle
    """    
    filename='COV'+str(outcomes[0]) +'.svg'
    fig, axes=plt.subplots(nrows=1, ncols=3, sharey='row')
    for i, (sub) in enumerate(subset_colors.keys()):
        if sub=='Total':
            stats=get_mean_ci_in_endline(endline,outcomes)
            stats['color']=stats.index.map({'Target group': '#0C884A', 'Comparison group': 'grey'})
        if sub=='Sindh':
            stats=get_mean_ci_in_endline(sindh_endline,outcomes)
            stats['color']=stats.index.map({'Target group': '#630235', 'Comparison group': 'grey'})
        if sub=='Punjab':
            stats=get_mean_ci_in_endline(punjab_endline,outcomes)
            stats['color']=stats.index.map({'Target group': '#0B9CDA', 'Comparison group': 'grey'})
        print(sub)
        print(stats.head())
        axes[i].set_title(sub+'\nn='+ str(stats[str(outcomes[0])+'_size'].sum(axis=0)), color=subset_colors[sub])
        axes[i].bar(stats.index, stats[str(outcomes[0])+'_mean'], color=stats['color'], yerr=stats[str(outcomes[0])+'_sem'])
        
    #labels
        for p in axes[i].patches:
        # get_width pulls left or right; get_y pushes up or down
            axes[i].text(p.get_x()+(p.get_width()/2), p.get_height()/2, '{:.0%}'.format(
                p.get_height()), color='white', horizontalalignment='center', verticalalignment='top', size='small')

        axes[0].set_ylabel(ylab, fontstyle='oblique')
        if i==0:
            axes[i].spines['left'].set_visible(True)
            axes[i].spines['right'].set_visible(False)
            axes[i].spines['top'].set_visible(False)
        if i>0:
            axes[i].spines['left'].set_visible(False)
            axes[i].spines['right'].set_visible(False)
            axes[i].spines['top'].set_visible(False)

        for ax in fig.axes: 
            ax.xaxis.set_tick_params(rotation=90)
            ax.yaxis.set_major_formatter(PercentFormatter(xmax=1,decimals=0))
        fig.suptitle(suptit, x=0, y=1.05, ha='left', size='medium', fontweight='bold', color='Black')
        fig.text(0,-0.3, 'Source: MTBA Endline studies\nError bars represent 95% CI of the mean.', fontsize='small', color='grey')
        fig.show()
        fig.savefig(graphs_path/filename)
        

make_cov_dum_fig(['ind_Goccupation_covid'], '%', '% girls with negative change in occupation because of covid')

make_cov_dum_fig(['ind_Gincomeshare_covid'], '%', '% girls with decreased share in income contribution because of covid')

#NOT ENOUGH VALUES
#make_cov_dum_fig(['ind_Geconomic_covid'], '%', '% girls with decreased access to econ. opportunitoes because of covid') 
make_cov_dum_fig(['ind_Gunpaidcare_covid'], '%', '% girls with increased hours unpaid care work because of covid')

print(clean.groupby(['grouping_province','grouping_target', 'grouping_period'] )['ind_Gstat_safeatschool'].value_counts(dropna=False))

make_cov_dum_fig(['ind_Gschool_covid'], '%', '% Girls reporting negative effect school att. because of covid')

make_cov_dum_fig(['ind_HHschool_covid'], '%', '% Households reporting negative effect school att. because of covid')

make_cov_dum_fig(['ind_HHschool_girlsreturn_covid'], '%', '% Households reporting that girls will return to school after covid')


make_cov_dum_fig(['ind_HHschool_boysreturn_covid'], '%', '% Households reporting that boys will return to school after covid')

##################################reload clean dataset for likert5 func
clean=pd.read_stata(cleandata_path/"4. MTBA Endline Cleaning 5 - Incl outcome indicators.dta")


#make some groupings
clean['grouping_period']=clean['period'].cat.rename_categories({"0. Baseline": "Baseline", "1. Midline": "Midline",  "2. Endline": "Endline"})
clean['grouping_period']=clean['grouping_period'].astype(str)
#remove nrs periods and sstrip string for province
clean['grouping_province']=clean['code_province'].astype(str).str.replace('\d+', '').str.replace('.', '').str.strip()
clean['grouping_total']='Total'

clean['grouping_target']=clean['code_group'].cat.rename_categories({"0. Comparison": "Comparison group", "1. Target": "Target group"})

sindh=clean.loc[clean['grouping_province']=='Sindh']
punjab=clean.loc[clean['grouping_province']=='Punjab']

sns.set_style('ticks')
#change anno opts
title_anno_opts = dict(xy=(-0.5, 0.5), size='medium', xycoords='axes fraction',
                    va='center', ha='center', rotation=90)

def make_kpi_fig_likert(outcomes, ylab, suptit, ylowlab, yhighlab):
    """returns fig in graphs path for outcomes (dummys/%)

    Parameters
    ----------
    outcomes : list
        outcome in list
    ylab : str
        y-axis label
    suptit : str
        suptitle (for keeping track mostly KPI-title)
    ylowlab : str
        label for lowest value of y
    yhighlab : str
        label for highest value of y
    """    
    #conversion to numerical
    for c in outcomes:
        for df in [clean, sindh, punjab]:
            if df[c].dtype.name=='category': 
                df[c]=df[c].cat.codes
                #add one & nan
                df[c]=df[c].replace({-1:np.nan, 0:1, 1:2, 2:3, 3:4, 4:5})

            print(df[c].value_counts(dropna=False))

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
        yticklabs=[ylowlab,2,3,4,yhighlab]
        ax.set_yticklabels(yticklabs)
        #ax.set_yticks(1,5)
        sns.despine(ax=ax)
        ax.spines['left'].set_position(('outward',5))
        ax.spines['bottom'].set_position(('outward',5))
        ax.set_ylabel(ylab, fontstyle='oblique')
        
    fig.suptitle(suptit, x=0, y=0.98, ha='left', size='medium', fontweight='bold', color='Black')
    fig.text(0,0, 'Source: MTBA Endline studies n total='+str(len(clean[outcomes].dropna())) + ' girls.\nShaded areas represent 95% CI of the mean.', fontsize='small', color='grey')
    fig.savefig(graphs_path/filename)
    fig.show()
        



make_kpi_fig_likert(['ind_Gstat_safeatschool'], 'mean', 'Statement:I feel safe at school/college', 'Strongly disagree-1', 'Strongly agree-5')
make_kpi_fig_likert(['ind_Gstat_saferoad'], 'mean', 'Statement:I feel safe at the road to school/college', 'Strongly disagree-1', 'Strongly agree-5')

make_kpi_fig_likert(['ind_Gstat_advocchild'], 'mean', 'Statement:I feel that I can advocate for myself when it comes to decision about child bearing', 'Strongly disagree-1', 'Strongly agree-5')

make_kpi_fig_likert(['ind_Gstat_selfesteem'], 'mean', 'Statement:I see myself as someone who has high self-esteem', 'Strongly disagree-1', 'Strongly agree-5')

make_kpi_fig_likert(['ind_Gpeoplechangecomm'], 'mean', 'Statement:Do you feel that people like yourself can generally change things\nin your community if they want to?', 'No, not at all -1', ' Yes, very easily-5')

make_kpi_fig_likert(['ind_comrejectcm'], 'mean', 'Community members who reject child marriage', 'Strongly disagree-1', 'Strongly agree-5')
