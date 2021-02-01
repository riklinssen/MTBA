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

alldata = pd.concat([total_set, add_ME])


alldata = total_set.set_index(
    ['group', 'variable', 'period', 'treatment']).sort_index()


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


####################################visualisations
##some helper stuff
title_anno_opts = dict(xy=(0, 0.5), size='small', xycoords='axes fraction',
                       va='top', ha='left')

title_anno_opts_centered=dict(xy=(0.5, 0.5), size='small', xycoords='axes fraction',
                                                 va='top', ha='left')
idx = pd.IndexSlice


# disag_groups_colors is sorted.
disag_groups_colors = {'Total': '#0C884A', 'Punjab': '#0B9CDA', 'Sindh': '#E43989',
                       'atriskcm': '#F16E22', 'affectedcm': '#53297D', 'neithercm': '#630235'}

# try visualisation
# #set disagrregations
disaggregations = ['by_Total_Province', 'by_CM', 'by_hh_head']

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
            'height_ratios': [2, 3, 3, 3]}, figsize=(4, 6))

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
            ylabeltje = None
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
            else:
                ylabeltje = gr

            axes[i].set_ylabel(
                ylabeltje, color=disag_groups_colors[gr], fontstyle='oblique')
            # y-axis format
            if proportion == True:
                ylow, yhigh = (0, 1)
                axes[i].yaxis.set_major_formatter(
                    PercentFormatter(xmax=1, decimals=0))
            if proportion == False:
                ylow, yhigh = meta.at[outcome, 'min'], meta.at[outcome, 'max']
            axes[i].set_ylim(ylow, yhigh)
            
            #despine + footnotes
            sns.despine(ax=axes[i], offset=5)
            fig.text(0, 0, 'Source: MTBA Endline studies\nMatched-estimates (repeated cross-sections)\nShaded areas represent 95% CI of the mean.',
                     fontsize='small', color='grey')
            fig.savefig(outfile, bbox_inches='tight')
            fig.show()
            print(outcome, 'by:', disag, 'saved in: ', outfile)
