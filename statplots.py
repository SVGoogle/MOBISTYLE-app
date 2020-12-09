import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st

# Set bins and labels
bins_TEMP, bins_RH = [-10000, 19, 20, 21, 23, 24, 25, 10000], [-10000, 20, 25, 30, 50, 60, 70, 10000]
bins_CO2, bins_VOC = [-10000, 750, 900, 1200, 10000], [-10000, 40, 80, 100, 10000]

labels_T_RH = ['Cat -IV', 'Cat -III', 'Cat -II', 'Cat I', 'Cat +II', 'Cat +III', 'Cat +IV']
labels_CO2_VOC = ['Cat I', 'Cat II', 'Cat III', 'Cat IV']

# RGB codes for Comfort category colors
cmap_T_RH = [(0, .33, .82), (0, .7, .82), (.5, .95, .75), (.3, .7, .4), (.6, .8, .4), (.95, .39, .4), (.8, .07, .25), 'lightgrey']
cmap_CO2_VOC = [(.3, .7, .4), (.6, .8, .4), (.95, .39, .4), (.8, .07, .25), 'lightgrey']

# Colors for plots
current_pallete = sns.color_palette()
pallete = sns.color_palette().as_hex()

# Hex codes for Mobistyle and Baseline colors
color_BL = '#1f77b4'
color_MS = '#ff7f0e'
color_other = '#2ca02c'
color_out = '#7f7f7f'
color_missing = 'lightgrey'


def set_barh_text(df, ax):
    """Function to plot text in the middle of horizontal bar charts.
    """
    for rowNum, row in enumerate(df.fillna(0.).values):
        xpos = 0
        for val in row:
            xpos += val
            ax.text(xpos - val/2, rowNum, np.where((val >1.), f'{int(round(val))}', ''), color='white', ha='center', va='center', fontsize=10)


def plot_hdd(df):
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(11.7, 8.27), sharex=True)
    df.iloc[:12, :].plot(kind='barh', stacked=True, ax=ax1)
    df.iloc[12:-1, :].plot(kind='barh', stacked=True, ax=ax2)
    set_barh_text(df.iloc[:12, :], ax1)
    set_barh_text(df.iloc[12:-1, :], ax2)

    for ax in (ax1, ax2):
        ax.set(xticklabels=[0, 100, 200, 300, 400, 500, 600], ylabel='')
        ax.set_xlabel('[count]', size=14)
        ax.tick_params(axis='both', which='major', labelsize=14)
        ax.legend('')

    ax1.set_title('BASELINE')
    ax2.set_title('MOBISTYLE')
    ax1.set(yticklabels=df.iloc[:12, :].index.strftime('%b, %Y'))
    ax2.set(yticklabels=df.iloc[12:-1, :].index.strftime('%b, %Y'))
    ax2.yaxis.set_label_position('right')
    ax2.yaxis.tick_right()

    plt.suptitle('Heating degree-days (HDD) and cooling degree-days (CDD). Slovenia, Ljubljana', fontsize=14)

    fig.legend(['HDD', 'CDD'], loc='lower center', bbox_to_anchor=(0.5, 0.0), ncol=2, fontsize=12)
    fig.tight_layout()
    fig.subplots_adjust(top=0.9, bottom=0.1)
    return fig


def plot_t_out(df, parameter='Temperature'):
    fig, ax = plt.subplots(figsize=(11.7, 4))

    if parameter == 'Temperature':
        unit = '[$^o$C]'
    elif parameter == 'RH':
        unit = '[%]'
    elif parameter == 'Global radiation' or 'Diffuse radiation':
        unit = '[W/m2]'

    sns.boxplot(data=df, x=df.index.month, y=parameter, hue='Monitoring_Period',
                showfliers=False, palette=[color_BL, color_MS], ax=ax)
    ax.tick_params(axis='both', which='major', labelsize=14)
    ax.legend(fontsize=14)
    ax.xaxis.grid(True)
    ax.set_title(f'Outdoor Air {parameter}. Slovenia, Ljubljana (Bežigrad)', fontsize=14)
    ax.set_ylabel(unit, fontsize=14)
    ax.set_xlabel('', fontsize=14)
    ax.set_xticklabels(pd.date_range(start='2018-1-1', periods=12, freq='MS').strftime('%b'), rotation=0)
    if parameter == 'Temperature':
        ax.set(yticks=[-10, 0, 10, 20, 30], ylim=(-15, 40))
    fig.tight_layout()
    return fig

