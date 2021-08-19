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

#larger
#sns.set(rc={'figure.figsize':(24, 5)})
sns.set(rc={'figure.figsize':(24, 4)})
sns.set(style="ticks")
sns.set_style("white")
matplotlib.rcParams['pdf.fonttype'] = 42
plt.rcParams["axes.grid"] = True
plt.rcParams['axes.xmargin'] = 0
plt.rcParams['axes.autolimit_mode'] = 'round_numbers'
plt.clf()

SCRIPTPATH = os.path.dirname(os.path.abspath(__file__))

axs = []
axs.append(plt.subplot2grid(shape=(1,6), loc=(0,0)))
axs.append(plt.subplot2grid(shape=(1,6), loc=(0,1)))
axs.append(plt.subplot2grid(shape=(1,6), loc=(0,2)))
axs.append(plt.subplot2grid(shape=(1,6), loc=(0,3)))
axs.append(plt.subplot2grid(shape=(1,6), loc=(0,4)))
axs.append(plt.subplot2grid(shape=(1,6), loc=(0,5)))

dirs = ['120', '210_python','210_node', '311', '411', '503']
names_short = ['uploader',
         'thumbnailer Python',
         'thumbnailer Node.js',
         'compression',
         'image-recognition',
         'graph-bfs'
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
    scale = 1./df.index.size
    #print(df.index.size)
    rotations = [45, 45, 0]
    for level, rotation in zip(range(df.index.nlevels)[::-1], rotations):
        pos = 0
        for label, rpos in label_len(df.index,level):
            #rpos = 1600
            lxpos = (pos + .5 * rpos)*scale
            #print((pos*scale, lxpos, ypos, rpos, label))
            ax.text(lxpos, ypos, label, ha='center',
                    transform=ax.transAxes,
                    rotation=rotation,
                    fontsize=18)
            #print((pos*scale, ypos))
            add_line(ax, pos*scale, ypos)
            pos += rpos
        add_line(ax, pos*scale , ypos)
        ypos -= .1

all_frames = []

memories = [
    [128, 2048],
    [128, 2048],
    [128, 2048],
    [256, 2048],
    [512, 2048],
    [128, 2048]
]

from matplotlib.patches import PathPatch

def adjust_box_widths(g, fac):
    """
    Adjust the widths of a seaborn-generated boxplot.
    """

    # iterating through Axes instances
    for ax in g.axes:

        # iterating through axes artists:
        for c in ax.get_children():

            # searching for PathPatches
            if isinstance(c, PathPatch):
                # getting current width of box:
                p = c.get_path()
                verts = p.vertices
                verts_sub = verts[:-1]
                xmin = np.min(verts_sub[:, 0])
                xmax = np.max(verts_sub[:, 0])
                xmid = 0.5*(xmin+xmax)
                xhalf = 0.5*(xmax - xmin)

                # setting new width of box
                xmin_new = xmid-fac*xhalf
                xmax_new = xmid+fac*xhalf
                verts_sub[verts_sub[:, 0] == xmin, 0] = xmin_new
                verts_sub[verts_sub[:, 0] == xmax, 0] = xmax_new

                # setting new width of median line
                for l in ax.lines:
                    if np.all(l.get_xdata() == [xmin, xmax]):
                        l.set_xdata([xmin_new, xmax_new])

for i in range(len(dirs)):

    dir = dirs[i]
    
    dataframes = []
    memory = memories[i]
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

        groups = []
        #memories.append(df['memory'].nunique())
        df_grouped = df.groupby(['memory', 'type'])
        for group_name, df_group in df_grouped: 
            groups.append(df_group.head(200))


        df = pd.concat(groups)

        if data_type[0] == 'azure':
            df['memory'] = 'Dynamic'
        # select datapoints for aws, gcp
        else:
            df = df.drop(df[(df['memory'] != memory[0]) & (df['memory'] != memory[1])].index)
        df = df[['memory', 'type', 'client_time']]
      
        # On Azure we use burst and warm data
        if data_type[0] == 'azure':
            merge = df.loc[df['type'] == 'warm'].merge(df.loc[df['type'] == 'burst'], left_on="memory", right_on="memory")
            merge['ratio'] = merge['client_time_y'] / merge['client_time_x']
        # on AWS and GCP we use warm and cold data
        else:
            merge = df.loc[df['type'] == 'warm'].merge(df.loc[df['type'] == 'cold'], left_on="memory", right_on="memory")
            merge['ratio'] = merge['client_time_y'] / merge['client_time_x']
        merge['provider'] = data_type[1]
        dataframes.append(merge)

    df = pd.concat(dataframes)
    df['benchmark'] = names_short[i]
    all_frames.append(df)
    df['index'] = df['provider'].map(str) + df['memory'].map(str)
    df['index2'] = 0
    df.set_index(['provider', 'memory'], inplace=True)
    ax = sns.boxplot(
        x="index2",
        y="ratio",
        hue="index",
        data=df,
        ax=axs[i],
    )

    ax.legend().set_visible(False)
    ax.set_ylabel('')
    ax.tick_params(axis='y', which='major', labelsize=25)
    ax.tick_params(axis='y', which='minor', labelsize=8)
    ax.set_xticklabels('')
    ax.set_xlabel('')
    ax.set_yscale('log')
    ax.set_ylim((0.1, 130))
    # necessary to remove margins
    ax.set_xlim((-0.42, 0.42))

    from matplotlib.offsetbox import AnchoredText
    from mpl_toolkits.axes_grid1 import make_axes_locatable
    divider = make_axes_locatable(ax)
    cax = divider.append_axes("top", size="12%", pad=0)
    cax.get_xaxis().set_visible(False)
    cax.get_yaxis().set_visible(False)
    cax.set_facecolor('lightgray')

    at = AnchoredText(names_short[i], loc=10, frameon=False,
                      prop=dict(size=20, color='black'))
    cax.add_artist(at)
    
adjust_box_widths(plt.gcf(), 0.9)
#def resize(event):
#    # use the figure width as width of the text box 
#    bb.set_boxstyle(pad=0.4, width=plt.gcf().get_size_inches()[0]*plt.gcf().dpi )

#resize(None)
# Optionally: use eventhandler to resize the title box, in case the window is resized
#cid = plt.gcf().canvas.mpl_connect('resize_event', resize)
#axs[0].set_ylabel('Cold Startup Overhead',fontsize=25)
axs[0].set_ylabel('$\dfrac{T_{cold}}{T_{warm}}$',fontsize=25)
for i in range(1, 6):
    axs[i].set_yticklabels('')
handles, labels = ax.get_legend_handles_labels()
new_labels = {
    'AWS128': 'AWS, 128 MB',
    'AWS2048':'AWS, 2048 MB',
    'GCP128':'GCP, 128 MB',
    'GCP2048': 'GCP, 2048 MB',
    'AzureDynamic': 'Azure',
}

plt.subplots_adjust(left=0, bottom=0, right=1, top=1, wspace=0.01, hspace=0)
plt.tight_layout()
plt.subplots_adjust(left=0, bottom=0, right=1, top=1, wspace=0.01, hspace=0)
axs[1].legend(handles, [new_labels[l] for l in labels],bbox_to_anchor=(0, -0.2),fancybox=False,prop={'size': 22}, loc='lower left', ncol=6)
plt.savefig('cold_startup.pdf', bbox_inches='tight')

