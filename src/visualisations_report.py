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

short_term = pd.read_csv(
    r"C:\Users\RikL\Box\ONL-IMK\2.0 Projects\Current\16-01 MTBA\07.2 Statistical analyses - Endline\Data analysis\4. Output\Resultsset\short_term.csv", index_col=0)
long_term = pd.read_csv(
    r"C:\Users\RikL\Box\ONL-IMK\2.0 Projects\Current\16-01 MTBA\07.2 Statistical analyses - Endline\Data analysis\4. Output\Resultsset\long_term.csv", index_col=0)
meta = pd.read_excel(
    r"C:\Users\RikL\Box\ONL-IMK\2.0 Projects\Current\16-01 MTBA\07.2 Statistical analyses - Endline\Data analysis\4. Output\Resultsset\MTBA_figs_metadata.xlsx")

#strip variables (some added spaces)
meta['variable'] = meta['variable'].str.strip()

meta = meta.set_index('variable')

graphs_path = Path(
    r"C:\Users\RikL\Box\ONL-IMK\2.0 Projects\Current\16-01 MTBA\07.2 Statistical analyses - Endline\Data analysis\4. Output\visuals_report_mtba")

    
#load in metadata for figs (labels min max prop etc)
# making full set.
# long term variable set is smallest.
# short term variable set is largest.

# for the long term set we only have baseline and endline
# for the short term set we have midline and endline.

# the total set should contain.
# - the baseline and endline measures from the long term set.
# - in case there is a baseline and endline measurement (in long_term), add the midline measurements.
# for those variables that are only in the short term set, and not in the long term set:
#     - add/use midline and endline variables and measurements from the short term set.
#     - add the variable names, set the baseline measures to nan.


# - in case there is a baseline and endline measurement (long_term), add the midline measurements.
longtermvars = long_term['variable'].unique()
shorttermvars = short_term['variable'].unique()



# assess overlap in variables.

toadd = [c for c in longtermvars if c in shorttermvars]

addmidline = short_term.loc[(short_term['variable'].isin(
    toadd)) & (short_term['period'] == 'Midline'), :]

# - the baseline and endline measures from the long term set. +the midline measurements
total_set = pd.concat([long_term, addmidline])


# for those variables that are only in the short term set, and not in the long term set:
#     - add/use midline and endline variables and measurements from the short term set.
todrop = [c for c in shorttermvars if c not in longtermvars]

add_ME = short_term.loc[(short_term['variable'].isin(todrop))]
add_ME['source'] = 'short term (M-E) no baseline'


#add the varis for which we only have midline and endline data. 


alldata = pd.concat([total_set, add_ME])


alldata = alldata.set_index(
    ['group', 'variable', 'period', 'treatment']).sort_index()

###################################################quickfix, set index for ADD_ME 
##refactor later. 
add_ME=add_ME.set_index(['group', 'variable', 'period', 'treatment']).sort_index()

# add disaggregation sets (figures that need to be combined)
alldata['disag'] = alldata.index.get_level_values(0).map({
    'Total': 'by_Total_Province',
    'Punjab': 'by_Total_Province',
    'Sindh': 'by_Total_Province',
    'affectedcm': 'by_CM',
    'atriskcm': 'by_CM',
    'neithercm': 'by_CM',
    'hhfemale': 'by_hh_head',
    'hhmale': 'by_hh_head'})

#list of vars to plot




####################################visualisations
##some helper stuff
title_anno_opts = dict(xy=(0, 0.5), size='small', xycoords='axes fraction',
                       va='top', ha='left')

title_anno_opts_centered=dict(xy=(0.5, 0.5), size='small', xycoords='axes fraction',
                                                 va='top', ha='left')
idx = pd.IndexSlice


# disag_groups_colors is sorted.
disag_groups_colors = {'Total': '#0C884A', 'Punjab': '#0B9CDA', 'Sindh': '#E43989',
                       'atriskcm': '#F16E22', 'affectedcm': '#53297D', 'neithercm': '#630235', 'hhfemale': 'blue',  'hhmale': 'red'  }

# try visualisation
# #set disagrregations

disaggregations = ['by_Total_Province','by_CM',]

for dis in disaggregations:
    disag = dis
    # select relevant data and groups
    dissagregation_df = alldata.loc[alldata['disag'] == disag]
    groups_l = None
    groups_l = [
        gr for gr in disag_groups_colors.keys() if gr in dissagregation_df.index.get_level_values('group')]
    periods_srt = {'Baseline': 0, 'Midline': 1, 'Endline': 2}

    #get list of outcomes
    outcomes = None
    outcomes = [o for o in dissagregation_df.index.get_level_values(
        'variable').unique()]

    #plot loop
    for outcome in outcomes:
        filename = outcome+disag+".svg"
        outfile = graphs_path/disag/filename

        fig, axes = plt.subplots(nrows=4, ncols=1, sharex='col', sharey='col', gridspec_kw={
            'height_ratios': [3, 3, 3, 3]}, figsize=(4, 6))

        proportion = meta.at[outcome, 'prop']
        title = str(meta.at[outcome, 'label']).replace(r'\n', '\n')

        print("visualising:", str(outcome), " by ", disag)
        # title box
        axes[0].annotate(title, **title_anno_opts, color='black')
        axes[0].axis('off')
        #select treatment and control data.
        for i, gr in enumerate(groups_l, start=1):
            treatment = dissagregation_df.loc[idx[gr, outcome, :, 'treated']].droplevel(
                ['group', 'variable']).reset_index()
            treatment['srt'] = treatment['period'].map(periods_srt)
            treatment = treatment.sort_values(by='srt')
            #sometimes proportions are 0-100, mistake in data.
            if (proportion == True) and (treatment['Mean'].max() > 1):
                for col in ['Mean', 'sem', 'upper', 'lower']:
                    treatment[col] = treatment[col]/100

            control = dissagregation_df.loc[idx[gr, outcome, :, 'control']].droplevel(
                ['group', 'variable']).reset_index()
            if (proportion == True) and (control['Mean'].max() > 1):
                for col in ['Mean', 'sem', 'upper', 'lower']:
                    control[col] = treatment[col]/100

            control['srt'] = control['period'].map(periods_srt)
            control = control.sort_values(by='srt')
            #plot treatment

            if treatment.empty:  # sometimes there is only missing data
                axes[i].annotate('no data', **title_anno_opts_centered, color=disag_groups_colors[gr])
                axes[i].axis('off')

            else:
                axes[i].plot(treatment['period'], treatment['Mean'],
                             marker='o', color=disag_groups_colors[gr], clip_on=False)
                axes[i].fill_between(treatment['period'], treatment['lower'], treatment['upper'],
                                     color=disag_groups_colors[gr], alpha=0.2, clip_on=False)
                #labels
                if proportion == False:
                    for key, row in treatment.iterrows():
                        axes[i].text(x=row['period'], y=row['Mean']+0.07, s="{:.1f}".format(round(
                            row['Mean'], 1)), va='bottom', ha='center', size='x-small', color=disag_groups_colors[gr])
                if proportion == True:
                    for key, row in treatment.iterrows():
                        axes[i].text(x=row['period'], y=row['Mean']+0.07, s='{:.0%}'.format(
                            row['Mean']), va='bottom', ha='center', size='x-small', color=disag_groups_colors[gr])
            #plot control
            if control.empty:
                axes[i].annotate('no data', **title_anno_opts,
                                 color=disag_groups_colors[gr])
                axes[i].axis('off')
            else:
                axes[i].plot(control['period'], control['Mean'],
                             marker='o', color='grey', clip_on=False)
                axes[i].fill_between(control['period'], control['lower'],
                                     control['upper'], color='grey', alpha=0.2, clip_on=False)
            #ylabel
            #make nicer ylabels
            if gr == 'atriskcm':
                ylabeltje = 'At risk of CM'
            if gr == 'affectedcm':
                ylabeltje = 'Affected by CM'
            if gr == 'neithercm':
                ylabeltje = 'Neither at risk\nnor affected CM'
            if gr == 'hhfemale':
                ylabeltje = 'Female headed households'
            if gr == 'hhmale':
                ylabeltje = 'Male headed households'
            if gr in ['Total', 'Punjab', 'Sindh']:
                ylabeltje = gr
            
            axes[i].set_ylabel(ylabeltje, color=disag_groups_colors[gr], fontstyle='oblique')

            # y-axis format
            if proportion == True:
                ylow, yhigh = (0, 1)
                axes[i].yaxis.set_major_formatter(
                    PercentFormatter(xmax=1, decimals=0))
            if proportion == False:
                ylow, yhigh = meta.at[outcome, 'min'], meta.at[outcome, 'max']
            axes[i].set_ylim(ylow, yhigh)
            
            fig.align_ylabels()
            #despine + footnotes
            sns.despine(ax=axes[i], offset=5)
            fig.text(0, 0, 'Source: MTBA Endline studies\nMatched-estimates (repeated cross-sections)\nShaded areas represent 95% CI of the mean.',
                     fontsize='small', color='grey')
            fig.savefig(outfile, bbox_inches='tight')
            fig.show()
            print(outcome, 'by:', disag, 'saved in: ', outfile)








##############################by hh head (only 2 grapjhs)



disaggregations = ['by_hh_head']

for dis in disaggregations:
    disag = dis
    # select relevant data and groups
    dissagregation_df = alldata.loc[alldata['disag'] == disag]
    groups_l = None
    groups_l = [
        gr for gr in disag_groups_colors.keys() if gr in dissagregation_df.index.get_level_values('group')]
    periods_srt = {'Baseline': 0, 'Midline': 1, 'Endline': 2}

    #get list of outcomes
    outcomes = None
    outcomes = [o for o in dissagregation_df.index.get_level_values(
        'variable').unique()]

    #plot loop
    for outcome in outcomes:
        filename = outcome+disag+".svg"
        outfile = graphs_path/disag/filename

        fig, axes = plt.subplots(nrows=3, ncols=1, sharex='col', sharey='col', gridspec_kw={
            'height_ratios': [3, 3, 3]}, figsize=(4, 6))

        proportion = meta.at[outcome, 'prop']
        title = str(meta.at[outcome, 'label']).replace(r'\n', '\n')

        print("visualising:", str(outcome), " by ", disag)
        # title box
        axes[0].annotate(title, **title_anno_opts, color='black')
        axes[0].axis('off')
        #select treatment and control data.
        for i, gr in enumerate(groups_l, start=1):
            treatment = dissagregation_df.loc[idx[gr, outcome, :, 'treated']].droplevel(
                ['group', 'variable']).reset_index()
            treatment['srt'] = treatment['period'].map(periods_srt)
            treatment = treatment.sort_values(by='srt')
            #sometimes proportions are 0-100, mistake in data.
            if (proportion == True) and (treatment['Mean'].max() > 1):
                for col in ['Mean', 'sem', 'upper', 'lower']:
                    treatment[col] = treatment[col]/100

            control = dissagregation_df.loc[idx[gr, outcome, :, 'control']].droplevel(
                ['group', 'variable']).reset_index()
            if (proportion == True) and (control['Mean'].max() > 1):
                for col in ['Mean', 'sem', 'upper', 'lower']:
                    control[col] = treatment[col]/100

            control['srt'] = control['period'].map(periods_srt)
            control = control.sort_values(by='srt')
            #plot treatment

            if treatment.empty:  # sometimes there is only missing data
                axes[i].annotate('no data', **title_anno_opts_centered, color=disag_groups_colors[gr])
                axes[i].axis('off')

            else:
                axes[i].plot(treatment['period'], treatment['Mean'],
                             marker='o', color=disag_groups_colors[gr], clip_on=False)
                axes[i].fill_between(treatment['period'], treatment['lower'], treatment['upper'],
                                     color=disag_groups_colors[gr], alpha=0.2, clip_on=False)
                #labels
                if proportion == False:
                    for key, row in treatment.iterrows():
                        axes[i].text(x=row['period'], y=row['Mean']+0.07, s="{:.1f}".format(round(
                            row['Mean'], 1)), va='bottom', ha='center', size='x-small', color=disag_groups_colors[gr])
                if proportion == True:
                    for key, row in treatment.iterrows():
                        axes[i].text(x=row['period'], y=row['Mean']+0.07, s='{:.0%}'.format(
                            row['Mean']), va='bottom', ha='center', size='x-small', color=disag_groups_colors[gr])
            #plot control
            if control.empty:
                axes[i].annotate('no data', **title_anno_opts,
                                 color=disag_groups_colors[gr])
                axes[i].axis('off')
            else:
                axes[i].plot(control['period'], control['Mean'],
                             marker='o', color='grey', clip_on=False)
                axes[i].fill_between(control['period'], control['lower'],
                                     control['upper'], color='grey', alpha=0.2, clip_on=False)
            #ylabel
            #make nicer ylabels
            if gr == 'atriskcm':
                ylabeltje = 'At risk of CM'
            if gr == 'affectedcm':
                ylabeltje = 'Affected by CM'
            if gr == 'neithercm':
                ylabeltje = 'Neither at risk\nnor affected CM'
            if gr == 'hhfemale':
                ylabeltje = 'Female\nheaded households'
            if gr == 'hhmale':
                ylabeltje = 'Male\nheaded households'
            if gr in ['Total', 'Punjab', 'Sindh']:
                ylabeltje = gr
            
            axes[i].set_ylabel(ylabeltje, color=disag_groups_colors[gr], fontstyle='oblique')

            # y-axis format
            if proportion == True:
                ylow, yhigh = (0, 1)
                axes[i].yaxis.set_major_formatter(
                    PercentFormatter(xmax=1, decimals=0))
            if proportion == False:
                ylow, yhigh = meta.at[outcome, 'min'], meta.at[outcome, 'max']
            axes[i].set_ylim(ylow, yhigh)
            
            fig.align_ylabels()
            #despine + footnotes
            sns.despine(ax=axes[i], offset=5)
            fig.text(0, 0, 'Source: MTBA Endline studies\nMatched-estimates (repeated cross-sections)\nShaded areas represent 95% CI of the mean.',
                     fontsize='small', color='grey')
            fig.savefig(outfile, bbox_inches='tight')
            fig.show()
            print(outcome, 'by:', disag, 'saved in: ', outfile)




# ####################################
# ##short term (Midline endline no baseline)



# # add disaggregation sets (figures that need to be combined)
# add_ME['disag'] = add_ME.index.get_level_values(0).map({
#     'Total': 'by_Total_Province',
#     'Punjab': 'by_Total_Province',
#     'Sindh': 'by_Total_Province',
#     'affectedcm': 'by_CM',
#     'atriskcm': 'by_CM',
#     'neithercm': 'by_CM',
#     'hhfemale': 'by_hh_head',
#     'hhmale': 'by_hh_head'})

# disaggregations = ['by_Total_Province', 'by_CM', 'by_hh_head']


# for dis in disaggregations:
#     disag = dis
#     # select relevant data and groups
#     #only add_ME set for short term
#     dissagregation_df = add_ME.loc[add_ME['disag'] == disag]
#     groups_l = None
#     groups_l = [
#         gr for gr in disag_groups_colors.keys() if gr in dissagregation_df.index.get_level_values('group')]
    
#     periods_srt = {'Midline': 1, 'Endline': 2}

#     #get list of outcomes
#     outcomes = None
#     outcomes = [o for o in dissagregation_df.index.get_level_values(
#         'variable').unique()]

#     #plot loop
#     for outcome in outcomes:
#         filename = outcome+disag+'M_E.svg'
#         outfile = graphs_path/disag/filename

#         fig, axes = plt.subplots(nrows=3, ncols=1, sharex='col', sharey='col', gridspec_kw={
#             'height_ratios': [3, 3, 3]}, figsize=(4, 6))

#         proportion = meta.at[outcome, 'prop']
#         title = str(meta.at[outcome, 'label']).replace(r'\n', '\n')

#         print("visualising:", str(outcome), " by ", disag)
#         # title box
#         axes[0].annotate(title, **title_anno_opts, color='black')
#         axes[0].axis('off')
#         #select treatment and control data.
#         for i, gr in enumerate(groups_l, start=1):
#             treatment = dissagregation_df.loc[idx[gr, outcome, :, 'treated']].droplevel(
#                 ['group', 'variable']).reset_index()
#             treatment['srt'] = treatment['period'].map(periods_srt)
#             treatment = treatment.sort_values(by='srt')
#             #sometimes proportions are 0-100, mistake in data.
#             if (proportion == True) and (treatment['Mean'].max() > 1):
#                 for col in ['Mean', 'sem', 'upper', 'lower']:
#                     treatment[col] = treatment[col]/100

#             control = dissagregation_df.loc[idx[gr, outcome, :, 'control']].droplevel(
#                 ['group', 'variable']).reset_index()
#             if (proportion == True) and (control['Mean'].max() > 1):
#                 for col in ['Mean', 'sem', 'upper', 'lower']:
#                     control[col] = treatment[col]/100

#             control['srt'] = control['period'].map(periods_srt)
#             control = control.sort_values(by='srt')
#             #plot treatment

#             if treatment.empty:  # sometimes there is only missing data
#                 axes[i].annotate('no data', **title_anno_opts_centered, color=disag_groups_colors[gr])
#                 axes[i].axis('off')

#             else:
#                 axes[i].plot(treatment['period'], treatment['Mean'],
#                              marker='o', color=disag_groups_colors[gr], clip_on=False)
#                 axes[i].fill_between(treatment['period'], treatment['lower'], treatment['upper'],
#                                      color=disag_groups_colors[gr], alpha=0.2, clip_on=False)
#                 #labels
#                 if proportion == False:
#                     for key, row in treatment.iterrows():
#                         axes[i].text(x=row['period'], y=row['Mean']+0.07, s="{:.1f}".format(round(
#                             row['Mean'], 1)), va='bottom', ha='center', size='x-small', color=disag_groups_colors[gr])
#                 if proportion == True:
#                     for key, row in treatment.iterrows():
#                         axes[i].text(x=row['period'], y=row['Mean']+0.07, s='{:.0%}'.format(
#                             row['Mean']), va='bottom', ha='center', size='x-small', color=disag_groups_colors[gr])
#             #plot control
#             if control.empty:
#                 axes[i].annotate('no data', **title_anno_opts,
#                                  color=disag_groups_colors[gr])
#                 axes[i].axis('off')
#             else:
#                 axes[i].plot(control['period'], control['Mean'],
#                              marker='o', color='grey', clip_on=False)
#                 axes[i].fill_between(control['period'], control['lower'],
#                                      control['upper'], color='grey', alpha=0.2, clip_on=False)
#             #ylabel
#             #make nicer ylabels
#             if gr == 'atriskcm':
#                 ylabeltje = 'At risk of CM'
#             if gr == 'affectedcm':
#                 ylabeltje = 'Affected by CM'
#             if gr == 'neithercm':
#                 ylabeltje = 'Neither at risk\nnor affected CM'
#             if gr == 'hhfemale':
#                 ylabeltje = 'Female\nheaded households'
#             if gr == 'hhmale':
#                 ylabeltje = 'Male\nheaded households'
#             if gr in ['Total', 'Punjab', 'Sindh']:
#                 ylabeltje = gr
            
#             axes[i].set_ylabel(ylabeltje, color=disag_groups_colors[gr], fontstyle='oblique')

#             # y-axis format
#             if proportion == True:
#                 ylow, yhigh = (0, 1)
#                 axes[i].yaxis.set_major_formatter(
#                     PercentFormatter(xmax=1, decimals=0))
#             if proportion == False:
#                 ylow, yhigh = meta.at[outcome, 'min'], meta.at[outcome, 'max']
#             axes[i].set_ylim(ylow, yhigh)
            
#             fig.align_ylabels()
#             #despine + footnotes
#             sns.despine(ax=axes[i], offset=5)
#             fig.text(0, 0, 'Source: MTBA Endline studies\nMatched-estimates (repeated cross-sections)\nShaded areas represent 95% CI of the mean.',
#                      fontsize='small', color='grey')
#             fig.savefig(outfile, bbox_inches='tight')
#             fig.show()
#             print(outcome, 'by:', disag, 'saved in: ', outfile)







# ########################################################some indicators wrongplots
# wrongindi=['ind_Gstat_advocacy',
# 'ind_Gstat_saferoad',
# 'ind_finanliteracy',
# 'ind_knowledmarry',
# 'ind_knowledbearing',
# 'ind_EE_norm1']



# shorttermwrong=['ind_Gstat_advocacy', 'ind_Gstat_saferoad',  ]

# longermwrong=[w for w in wrongindi if w not in shorttermwrong]


# checkmeta=[w for w in wrongindi if w in meta.index]

# check_alldata=[w for w in wrongindi if w in alldata.index.get_level_values('variable')]

# longermwrongvarstoplot=alldata.loc[idx[:,longermwrong, :, :]]


# longermwrongvarstoplot.to_excel(r"C:\Users\RikL\Box\ONL-IMK\2.0 Projects\Current\16-01 MTBA\07.2 Statistical analyses - Endline\Data analysis\4. Output\Resultsset\longermwrongvarstoplot.xlsx")

# #replacing alldata
# alldata=longermwrongvarstoplot


# ####################################visualisations
# ##some helper stuff
# title_anno_opts = dict(xy=(0, 0.5), size='small', xycoords='axes fraction',
#                        va='top', ha='left')

# title_anno_opts_centered=dict(xy=(0.5, 0.5), size='small', xycoords='axes fraction',
#                                                  va='top', ha='left')
# idx = pd.IndexSlice


# # disag_groups_colors is sorted.
# disag_groups_colors = {'Total': '#0C884A', 'Punjab': '#0B9CDA', 'Sindh': '#E43989',
#                        'atriskcm': '#F16E22', 'affectedcm': '#53297D', 'neithercm': '#630235', 'hhfemale': 'blue',  'hhmale': 'red'  }

# # try visualisation
# # #set disagrregations

# disaggregations = ['by_Total_Province','by_CM',]

# for dis in disaggregations:
#     disag = dis
#     # select relevant data and groups
#     dissagregation_df = alldata.loc[alldata['disag'] == disag]
#     groups_l = None
#     groups_l = [
#         gr for gr in disag_groups_colors.keys() if gr in dissagregation_df.index.get_level_values('group')]
#     periods_srt = {'Baseline': 0, 'Midline': 1, 'Endline': 2}

#     #get list of outcomes
#     outcomes = None
#     outcomes = [o for o in dissagregation_df.index.get_level_values(
#         'variable').unique()]

#     #plot loop
#     for outcome in outcomes:
#         filename = outcome+disag+".svg"
#         outfile = graphs_path/disag/filename

#         fig, axes = plt.subplots(nrows=4, ncols=1, sharex='col', sharey='col', gridspec_kw={
#             'height_ratios': [3, 3, 3, 3]}, figsize=(4, 6))

#         proportion = meta.at[outcome, 'prop']
#         title = str(meta.at[outcome, 'label']).replace(r'\n', '\n')

#         print("visualising:", str(outcome), " by ", disag)
#         # title box
#         axes[0].annotate(title, **title_anno_opts, color='black')
#         axes[0].axis('off')
#         #select treatment and control data.
#         for i, gr in enumerate(groups_l, start=1):
#             treatment = dissagregation_df.loc[idx[gr, outcome, :, 'treated']].droplevel(
#                 ['group', 'variable']).reset_index()
#             treatment['srt'] = treatment['period'].map(periods_srt)
#             treatment = treatment.sort_values(by='srt')
#             #sometimes proportions are 0-100, mistake in data.
#             if (proportion == True) and (treatment['Mean'].max() > 1):
#                 for col in ['Mean', 'sem', 'upper', 'lower']:
#                     treatment[col] = treatment[col]/100

#             control = dissagregation_df.loc[idx[gr, outcome, :, 'control']].droplevel(
#                 ['group', 'variable']).reset_index()
#             if (proportion == True) and (control['Mean'].max() > 1):
#                 for col in ['Mean', 'sem', 'upper', 'lower']:
#                     control[col] = treatment[col]/100

#             control['srt'] = control['period'].map(periods_srt)
#             control = control.sort_values(by='srt')
#             #plot treatment

#             if treatment.empty:  # sometimes there is only missing data
#                 axes[i].annotate('no data', **title_anno_opts_centered, color=disag_groups_colors[gr])
#                 axes[i].axis('off')

#             else:
#                 axes[i].plot(treatment['period'], treatment['Mean'],
#                              marker='o', color=disag_groups_colors[gr], clip_on=False)
#                 axes[i].fill_between(treatment['period'], treatment['lower'], treatment['upper'],
#                                      color=disag_groups_colors[gr], alpha=0.2, clip_on=False)
#                 #labels
#                 if proportion == False:
#                     for key, row in treatment.iterrows():
#                         axes[i].text(x=row['period'], y=row['Mean']+0.07, s="{:.1f}".format(round(
#                             row['Mean'], 1)), va='bottom', ha='center', size='x-small', color=disag_groups_colors[gr])
#                 if proportion == True:
#                     for key, row in treatment.iterrows():
#                         axes[i].text(x=row['period'], y=row['Mean']+0.07, s='{:.0%}'.format(
#                             row['Mean']), va='bottom', ha='center', size='x-small', color=disag_groups_colors[gr])
#             #plot control
#             if control.empty:
#                 axes[i].annotate('no data', **title_anno_opts,
#                                  color=disag_groups_colors[gr])
#                 axes[i].axis('off')
#             else:
#                 axes[i].plot(control['period'], control['Mean'],
#                              marker='o', color='grey', clip_on=False)
#                 axes[i].fill_between(control['period'], control['lower'],
#                                      control['upper'], color='grey', alpha=0.2, clip_on=False)
#             #ylabel
#             #make nicer ylabels
#             if gr == 'atriskcm':
#                 ylabeltje = 'At risk of CM'
#             if gr == 'affectedcm':
#                 ylabeltje = 'Affected by CM'
#             if gr == 'neithercm':
#                 ylabeltje = 'Neither at risk\nnor affected CM'
#             if gr == 'hhfemale':
#                 ylabeltje = 'Female headed households'
#             if gr == 'hhmale':
#                 ylabeltje = 'Male headed households'
#             if gr in ['Total', 'Punjab', 'Sindh']:
#                 ylabeltje = gr
            
#             axes[i].set_ylabel(ylabeltje, color=disag_groups_colors[gr], fontstyle='oblique')

#             # y-axis format
#             if proportion == True:
#                 ylow, yhigh = (0, 1)
#                 axes[i].yaxis.set_major_formatter(
#                     PercentFormatter(xmax=1, decimals=0))
#             if proportion == False:
#                 ylow, yhigh = meta.at[outcome, 'min'], meta.at[outcome, 'max']
#             axes[i].set_ylim(ylow, yhigh)
            
#             fig.align_ylabels()
#             #despine + footnotes
#             sns.despine(ax=axes[i], offset=5)
#             fig.text(0, 0, 'Source: MTBA Endline studies\nMatched-estimates (repeated cross-sections)\nShaded areas represent 95% CI of the mean.',
#                      fontsize='small', color='grey')
#             fig.savefig(outfile, bbox_inches='tight')
#             fig.show()
#             print(outcome, 'by:', disag, 'saved in: ', outfile)



# ##now short term fixes.





# #################note alldata is only a selection now. 


# #replacing add_ME. 
# ######################################################replacing add_ME set for quick fix of wrong indicators. 
# add_ME=add_ME.loc[idx[:,shorttermwrong, :, :]]
# ##short term (Midline endline no baseline)



# # add disaggregation sets (figures that need to be combined)
# add_ME['disag'] = add_ME.index.get_level_values(0).map({
#     'Total': 'by_Total_Province',
#     'Punjab': 'by_Total_Province',
#     'Sindh': 'by_Total_Province',
#     'affectedcm': 'by_CM',
#     'atriskcm': 'by_CM',
#     'neithercm': 'by_CM',
#     'hhfemale': 'by_hh_head',
#     'hhmale': 'by_hh_head'})

# disaggregations = ['by_Total_Province', 'by_CM', 'by_hh_head']



# disaggregations = ['by_Total_Province', 'by_CM', 'by_hh_head']


# for dis in disaggregations:
#     disag = dis
#     # select relevant data and groups
#     #only add_ME set for short term
#     dissagregation_df = add_ME.loc[add_ME['disag'] == disag]
#     groups_l = None
#     groups_l = [
#         gr for gr in disag_groups_colors.keys() if gr in dissagregation_df.index.get_level_values('group')]
    
#     periods_srt = {'Midline': 1, 'Endline': 2}

#     #get list of outcomes
#     outcomes = None
#     outcomes = [o for o in dissagregation_df.index.get_level_values(
#         'variable').unique()]

#     #plot loop
#     for outcome in outcomes:
#         filename = outcome+disag+'M_E.svg'
#         outfile = graphs_path/disag/filename

#         fig, axes = plt.subplots(nrows=3, ncols=1, sharex='col', sharey='col', gridspec_kw={
#             'height_ratios': [3, 3, 3]}, figsize=(4, 6))

#         proportion = meta.at[outcome, 'prop']
#         title = str(meta.at[outcome, 'label']).replace(r'\n', '\n')

#         print("visualising:", str(outcome), " by ", disag)
#         # title box
#         axes[0].annotate(title, **title_anno_opts, color='black')
#         axes[0].axis('off')
#         #select treatment and control data.
#         for i, gr in enumerate(groups_l, start=1):
#             treatment = dissagregation_df.loc[idx[gr, outcome, :, 'treated']].droplevel(
#                 ['group', 'variable']).reset_index()
#             treatment['srt'] = treatment['period'].map(periods_srt)
#             treatment = treatment.sort_values(by='srt')
#             #sometimes proportions are 0-100, mistake in data.
#             if (proportion == True) and (treatment['Mean'].max() > 1):
#                 for col in ['Mean', 'sem', 'upper', 'lower']:
#                     treatment[col] = treatment[col]/100

#             control = dissagregation_df.loc[idx[gr, outcome, :, 'control']].droplevel(
#                 ['group', 'variable']).reset_index()
#             if (proportion == True) and (control['Mean'].max() > 1):
#                 for col in ['Mean', 'sem', 'upper', 'lower']:
#                     control[col] = treatment[col]/100

#             control['srt'] = control['period'].map(periods_srt)
#             control = control.sort_values(by='srt')
#             #plot treatment

#             if treatment.empty:  # sometimes there is only missing data
#                 axes[i].annotate('no data', **title_anno_opts_centered, color=disag_groups_colors[gr])
#                 axes[i].axis('off')

#             else:
#                 axes[i].plot(treatment['period'], treatment['Mean'],
#                              marker='o', color=disag_groups_colors[gr], clip_on=False)
#                 axes[i].fill_between(treatment['period'], treatment['lower'], treatment['upper'],
#                                      color=disag_groups_colors[gr], alpha=0.2, clip_on=False)
#                 #labels
#                 if proportion == False:
#                     for key, row in treatment.iterrows():
#                         axes[i].text(x=row['period'], y=row['Mean']+0.07, s="{:.1f}".format(round(
#                             row['Mean'], 1)), va='bottom', ha='center', size='x-small', color=disag_groups_colors[gr])
#                 if proportion == True:
#                     for key, row in treatment.iterrows():
#                         axes[i].text(x=row['period'], y=row['Mean']+0.07, s='{:.0%}'.format(
#                             row['Mean']), va='bottom', ha='center', size='x-small', color=disag_groups_colors[gr])
#             #plot control
#             if control.empty:
#                 axes[i].annotate('no data', **title_anno_opts,
#                                  color=disag_groups_colors[gr])
#                 axes[i].axis('off')
#             else:
#                 axes[i].plot(control['period'], control['Mean'],
#                              marker='o', color='grey', clip_on=False)
#                 axes[i].fill_between(control['period'], control['lower'],
#                                      control['upper'], color='grey', alpha=0.2, clip_on=False)
#             #ylabel
#             #make nicer ylabels
#             if gr == 'atriskcm':
#                 ylabeltje = 'At risk of CM'
#             if gr == 'affectedcm':
#                 ylabeltje = 'Affected by CM'
#             if gr == 'neithercm':
#                 ylabeltje = 'Neither at risk\nnor affected CM'
#             if gr == 'hhfemale':
#                 ylabeltje = 'Female\nheaded households'
#             if gr == 'hhmale':
#                 ylabeltje = 'Male\nheaded households'
#             if gr in ['Total', 'Punjab', 'Sindh']:
#                 ylabeltje = gr
            
#             axes[i].set_ylabel(ylabeltje, color=disag_groups_colors[gr], fontstyle='oblique')

#             # y-axis format
#             if proportion == True:
#                 ylow, yhigh = (0, 1)
#                 axes[i].yaxis.set_major_formatter(
#                     PercentFormatter(xmax=1, decimals=0))
#             if proportion == False:
#                 ylow, yhigh = meta.at[outcome, 'min'], meta.at[outcome, 'max']
#             axes[i].set_ylim(ylow, yhigh)
            
#             fig.align_ylabels()
#             #despine + footnotes
#             sns.despine(ax=axes[i], offset=5)
#             fig.text(0, 0, 'Source: MTBA Endline studies\nMatched-estimates (repeated cross-sections)\nShaded areas represent 95% CI of the mean.',
#                      fontsize='small', color='grey')
#             fig.savefig(outfile, bbox_inches='tight')
#             fig.show()
#             print(outcome, 'by:', disag, 'saved in: ', outfile)









#############relationships.
#Marrgins chld marriage by level of educ (Girls)
#load in margins from stata. 
margins=pd.read_stata(r"C:\Users\RikL\Box\ONL-IMK\2.0 Projects\Current\16-01 MTBA\07.2 Statistical analyses - Endline\Data analysis\4. Output\Resultsset\relationships\atmeans_geduc.dta")
sns.set_style('ticks')
#filename=visuals_path/"Margins_age_Action_incl_discussion.svg"

#margins=pd.read_stata(r"C:\Users\RikL\Box\ONL-IMK\2.0 Projects\Current\16-01 SP\1. Global\Endline surveys\Comparative analysis\Data\Results\FE_margins\FE_age_cont.dta", convert_categoricals=True)


fig, ax = plt.subplots(nrows= 1, ncols=1)   #, sharex='col' , sharey='row', gridspec_kw={'height_ratios': [1, 6,8], 'wspace':0.3,}, figsize=(7.8,6))
filename=(r"C:\Users\RikL\Box\ONL-IMK\2.0 Projects\Current\16-01 MTBA\07.2 Statistical analyses - Endline\Data analysis\4. Output\visuals_report_mtba\Relationships\CMbyeduc.svg")
#remove numbers in educ labels
#margins['_m1']=margins['_m1'].apply(lambda x: x[2:])
ax.plot(margins['_m1'], margins['_margin'], color= '#0C884A')
ax.fill_between(margins['_m1'],  margins['_ci_lb'], margins['_ci_ub'], color ='lightgrey', alpha=0.4)
ax.scatter(margins['_m1'], margins['_margin'], color= '#0C884A')
#add labels
for key, row in margins.iterrows():
    ax.text(x=row['_m1'], y=row['_margin']+0.01, s='{:.2f}'.format(row['_margin'])[1:], ha='center', size='x-small', color= '#0C884A')
ax.set_xlabel('Highest level of education completed', fontstyle='oblique')
ax.grid(axis='y', which='major', linestyle=':', linewidth='0.5', color='darkgrey')


for tick in ax.get_xticklabels():
    tick.set_rotation(90)

sns.despine(ax=ax)

ax.set_ylabel("Predicted probability\nof marriage before 18 years old", fontstyle='oblique')
ax.set_ylim(0,0.25)

fig.suptitle('Probability of child marriage (<18 years), by level of education', x=0, y=0.98, ha='left', size='x-large', fontweight='bold', color='Black')
fig.text(0, -.5, "Source: MTBA endline studies, total n=2478 girls.\nShaded areas represents 95% confidence interval of the estimate.\nEstimates are marginal effects, controlled for household socio-economic characteristics and girls 'year of birth (at means)", size='small',  ha="left", color='gray')
fig.savefig(filename, bbox_inches='tight')
fig.clf()

## knowledge about harmful effects. 
margins=pd.read_stata(r"C:\Users\RikL\Box\ONL-IMK\2.0 Projects\Current\16-01 MTBA\07.2 Statistical analyses - Endline\Data analysis\4. Output\Resultsset\relationships\atmeans_ind_knowledmarry .dta")

sns.set_style('ticks')
fig, ax = plt.subplots(nrows= 1, ncols=1)   #, sharex='col' , sharey='row', gridspec_kw={'height_ratios': [1, 6,8], 'wspace':0.3,}, figsize=(7.8,6))

filename=(r"C:\Users\RikL\Box\ONL-IMK\2.0 Projects\Current\16-01 MTBA\07.2 Statistical analyses - Endline\Data analysis\4. Output\visuals_report_mtba\Relationships\CMbyknowledge.svg")
#remove numbers in educ labels
#margins['_m1']=margins['_m1'].apply(lambda x: x[2:])
ax.plot(margins['_m1'], margins['_margin'], color= '#0C884A')
ax.fill_between(margins['_m1'],  margins['_ci_lb'], margins['_ci_ub'], color ='lightgrey', alpha=0.4)
ax.scatter(margins['_m1'], margins['_margin'], color= '#0C884A')
#add labels
for key, row in margins.iterrows():
    ax.text(x=row['_m1'], y=row['_margin']+0.01, s='{:.2f}'.format(row['_margin'])[1:], ha='center', size='x-small', color= '#0C884A')
ax.set_xlabel('Knowledge of harmful effects\n(0-low-, 9-high-)', fontstyle='oblique')
ax.grid(axis='y', which='major', linestyle=':', linewidth='0.5', color='darkgrey')


for tick in ax.get_xticklabels():
    tick.set_rotation(90)

sns.despine(ax=ax)

ax.set_ylabel("Predicted probability\nof marriage before 18 years old", fontstyle='oblique')
ax.set_ylim(0,0.5)

fig.suptitle('Probability of child marriage (<18 years),\n by knowledge of harmful effects', x=0, y=1, ha='left', size='x-large', fontweight='bold', color='Black')
fig.text(0, -.1, "Source: MTBA endline studies, total n=1334 parents.\nShaded areas represents 95% confidence interval of the estimate.\nEstimates are marginal effects, controlled for household socio-economic characteristics and girls 'year of birth (at means)", size='small',  ha="left", color='gray')
fig.savefig(filename, bbox_inches='tight')


#margins=pd.read_stata(r"C:\Users\RikL\Box\ONL-IMK\2.0 Projects\Current\16-01 SP\1. Global\Endline surveys\Comparative analysis\Data\Results\FE_margins\FE_age_cont.dta", convert_categoricals=True)

