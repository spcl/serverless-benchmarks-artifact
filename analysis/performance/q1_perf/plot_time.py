#!/usr/bin/env python3

import math
import matplotlib
import matplotlib.pyplot as plt
import seaborn as sns
import os
import pandas as pd
import numpy as np
from itertools import groupby
import scipy.stats as st
from scipy.stats import norm
from matplotlib import gridspec

sns.set(rc={'figure.figsize':(24, 8)})
sns.set(style="ticks")
sns.set_style("white")
matplotlib.rcParams['pdf.fonttype'] = 42
plt.rcParams["axes.grid"] = True
plt.rcParams['axes.xmargin'] = 0
plt.clf()

SCRIPTPATH = os.path.dirname(os.path.abspath(__file__))

axs = []
f = plt.figure()
gs0 = gridspec.GridSpec(2, 3, figure=f,hspace=0.35, wspace=0.1)

dirs = ['120', '210_python','210_node', '311', '411', '503']
names = ['uploader\nUpload downloaded zip package to storage',
         'thumbnailer Python\nimage thumbnailer',
         'thumbnailer Node.js\nimage thumbnailer',
         'compression\nzip-compression of LaTex project',
         'image-recognition\npytorch ResNet-50 inference',
         'graph-bfs\nBreadth-first search'
]

def basic_stats(times: float) :
    mean = np.mean(times)
    median = np.median(times)
    std = np.std(times)
    cv = std / mean * 100
    return (mean, median, std, cv)

def ci_tstudents(alpha: float, times: float):
    mean = np.mean(times)
    return st.t.interval(
        alpha, len(times) - 1, loc=mean, scale=st.sem(times)
    )


def ci_le_boudec(alpha: float, times: float):

    sorted_times = sorted(times)
    n = len(times)
    if n < 150:
        print(f"Not enough samples! {n}")
        return (0, 0)

    # z(alfa/2)
    z_value = {
        0.95: 1.96,
        0.99: 2.576
    }.get(alpha)

    low_pos = math.floor( (n - z_value * math.sqrt(n)) / 2)
    high_pos = math.ceil( 1 + (n + z_value * math.sqrt(n)) / 2)

    return (sorted_times[low_pos], sorted_times[high_pos])

def add_line(ax, xpos, ypos):
    line = plt.Line2D([xpos, xpos], [ypos + .1, ypos],
                      transform=ax.transAxes, color='gray')
    line.set_clip_on(False)
    ax.add_line(line)

def label_len(my_index,level):
    labels = my_index.get_level_values(level)
    return [(k, sum(1 for i in g)) for k,g in groupby(labels)]

def label_group_bar_table(ax, df, rpositions):
    ypos = -.1
    scale = 1./df.index.get_level_values(0).nunique()#df.index.size
    for level in range(df.index.nlevels)[::-1]:
        pos = 0
        for label, rpos in label_len(df.index,level):
            #rpos = 1600
            rpos=1
            lxpos = (pos + .5 * rpos)*scale
            y_offset = 0
            if len(label) > 6:
                y_offset = -.08
            elif len(label) >= 4:
                y_offset = -.02
            ax.text(lxpos, ypos - .03 + y_offset, label, ha='center', transform=ax.transAxes, rotation=45, fontsize=13)
            add_line(ax, pos*scale, ypos)
            pos += rpos
        add_line(ax, pos*scale , ypos)
        ypos -= .1

for i in range(len(dirs)):

    dir = dirs[i]
    name = names[i]
    
    dataframes = []
    datapoints_per_plot = []
    for data_type in [["aws", "AWS"], ["gcp", "GCP"], ["azure", "Azure"]]:
    
        df = pd.read_csv(os.path.join(
            SCRIPTPATH, os.path.pardir, os.path.pardir, os.path.pardir, "data", "performance",
            f"{data_type[0]}_perf_cost", dir, "perf-cost", "result.csv"
        ))
        df = df.drop(df[(df.type == 'warm') & (df.is_cold == True)].index)
        df = df.drop(df[(df.type == 'cold') & (df.is_cold == False)].index)
        df['client_time'] = df['client_time'] - df['connection_time'] * 1000*1000
        if data_type[0] == 'gcp':
            df['provider_time'] = df['provider_time'].multiply(1000)
        df = df.drop(df[df.provider_time == 0].index)
        # incorrect data for GCP NodeJS)
        df = df.drop(df[df.exec_time == 0].index)
        df['provider_time'] /= 10**6
        df['exec_time'] /= 10**6
        df['client_time'] /= 10**6

        # Azure processing 
        df = df.drop(df[(df['type'] == 'burst') & (df.is_cold == True)].index)

        groups = []
        if df['memory'].iloc[0] == 0:
            df['memory'] = 'Dynamic'
        datapoints_per_plot.append(df['memory'].nunique())
        df_grouped = df.groupby(['memory', 'type'])
        # we generate larger number of samples because of cloud failures
        for group_name, df_group in df_grouped:
            groups.append(df_group.head(200))

        df = pd.concat(groups)
        df = pd.melt(df,id_vars=['memory', 'type', 'is_cold'], var_name='exec_time', value_name='val')
        df['run2'] = df['memory'].map(str)
        df['run'] = data_type[1]
        df['run3'] = data_type[1] + df['memory'].map(str)
        df = df.sort_values(['memory','exec_time'])
        dataframes.append(df)

    df = pd.concat(dataframes)
    df.set_index(['run2'], inplace=True)
    df.to_csv('data.txt') 
    
    
    # add subplots with size according to proportion of # of boxplots
    # Azure adds one more since it was a bit cramped and Azure in the title didn't fit
    datapoints_per_plot[-1] += 1
    gs00 = gridspec.GridSpecFromSubplotSpec(1, sum(datapoints_per_plot), subplot_spec=gs0[i],wspace=0)
    prefix_sum = [0]
    for val in datapoints_per_plot:
        prefix_sum.append(prefix_sum[-1] + val)
    ax1 = f.add_subplot(gs00[0:1,:prefix_sum[1]])
    ax2 = f.add_subplot(gs00[0:1,prefix_sum[1]:prefix_sum[2]], sharey=ax1)
    ax3 = f.add_subplot(gs00[0:1,prefix_sum[2]:], sharey=ax1)
    axs.append((ax1, ax2, ax3))
    
    min_ylim = 10000000
    max_ylim = -1
    
    for idx, run in zip([0,1,2], ["AWS", "GCP", "Azure"]):

        local_data_slice = df.loc[
            (
                (df['type'] == 'warm')
            ) &
            (
                (df['exec_time']=='exec_time') |
                (df['exec_time']=='client_time') |
                (df['exec_time']=='provider_time')
            ) & (df['run'] == run)
        ]
        min_ylim = min(min_ylim, local_data_slice['val'].min())
        max_ylim = max(max_ylim, local_data_slice['val'].max())
        
        ax = sns.boxplot(
            x="run3",
            y="val",
            ax=axs[i][idx],
            hue='exec_time',
            data=local_data_slice,
            palette="Set3",
            hue_order=["exec_time", "provider_time", "client_time"],
            whis=[2, 98]
        )
        j = 0
        ax.legend().set_visible(False)
        ax.set_xticklabels('')
        ax.set_xlabel('')
        ax.set_ylabel('')
        ax.set_yscale('log')
        if idx > 0:
            ax.tick_params(axis='y',length=0, which='both', bottom=False, top=False, labelbottom=False)
            #ax.set_yticklabels('')
            # Disabling ticks on axis affect the first axis as well and we don't want that.
            for tk in ax.get_yticklabels():
                tk.set_visible(False)
        
        label_group_bar_table(ax, local_data_slice, [])
        
        
        from matplotlib.offsetbox import AnchoredText
        from mpl_toolkits.axes_grid1 import make_axes_locatable
        divider = make_axes_locatable(ax)
        cax = divider.append_axes("top", size="13%", pad=0)
        cax.get_xaxis().set_visible(False)
        cax.get_yaxis().set_visible(False)
        cax.set_facecolor('lightgray')

        at = AnchoredText(run, loc=10, frameon=False,
                          prop=dict(size=20, color='black'))
        cax.add_artist(at)

    if min_ylim == 0:
        min_ylim = 0.001
    axs[i][0].tick_params(axis='y', which='major', labelsize=15)
    axs[i][0].tick_params(axis='y', which='minor', labelsize=8)
    
    # title above
    up, bottom = name.split('\n')
    axs[i][0].text(1.1, 1.23, up, ha='center',
        transform=axs[i][0].transAxes,
        fontsize=20)
    axs[i][0].text(1.1, 1.15, bottom, ha='center',
        transform=axs[i][0].transAxes, fontstyle='italic',
        fontsize=18)
    
    # xlabel below
    # length of GCP + AWS, try to center 
    axs[i][0].text(1, -0.21, 'Memory [MB]', ha='center', transform=axs[i][0].transAxes, fontsize=18)
    # Azure, try to center 
    # add boundaries left AWS, right GCP
    add_line(axs[i][0],  0, -0.2)
    # add boundaries right Azure
    add_line(axs[i][2],  1, -0.2)
    
axs[0][0].set_ylabel('Execution Time [s]',fontsize=22)
axs[3][0].set_ylabel('Execution Time [s]',fontsize=22)
handles, labels = ax.get_legend_handles_labels()
new_labels = {
    'exec_time': 'Benchmark Time',
    'provider_time':'Provider Time',
    'client_time':'Client Time',
}


plt.subplots_adjust(left=0, bottom=0, right=1, top=1, wspace=0.01, hspace=0)
plt.tight_layout()
# add legend
axs[4][0].legend(handles, [new_labels[l] for l in labels],bbox_to_anchor=(-0.5, -0.5),fancybox=False,prop={'size': 20}, loc='lower left', ncol=6)

plt.savefig('time.pdf', bbox_inches='tight')

