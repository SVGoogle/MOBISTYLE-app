import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# Set bins and labels
bins_TEMP, bins_RH = [-10000, 19, 20, 21, 23, 24, 25, 10000], [-10000, 20, 25, 30, 50, 60, 70, 10000]
bins_CO2, bins_VOC = [-10000, 750, 900, 1200, 10000], [-10000, 40, 80, 100, 10000]

labels_T_RH = ['Cat -IV', 'Cat -III', 'Cat -II', 'Cat I', 'Cat +II', 'Cat +III', 'Cat +IV']
labels_CO2_VOC = ['Cat I', 'Cat II', 'Cat III', 'Cat IV']

# RGB codes for Comfort category colors
cmap_T_RH = [(0, .33, .82), (0, .7, .82), (.5, .95, .75), (.3, .7, .4),
             (.6, .8, .4), (.95, .39, .4), (.8, .07, .25), 'lightgrey']
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
            ax.text(xpos - val/2, rowNum, np.where((val > 1.), f'{int(round(val))}', ''),
                    color='white', ha='center', va='center', fontsize=10)


# OUTDOOR CLIMATE
def plot_hdd(df):
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(11.7, 8.27), sharex=True)
    df.iloc[:12, :].plot(kind='barh', stacked=True, ax=ax1)
    df.iloc[12:-1, :].plot(kind='barh', stacked=True, ax=ax2, c=[color_MS, 'salmon'])
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


def plot_t_out(df, parameter='Outdoor Temperature'):
    fig, ax = plt.subplots(figsize=(11.7, 4))
    if parameter == 'Outdoor Temperature':
        unit = '[$^o$C]'
    elif parameter == 'Outdoor RH':
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


# ROOM VISUALIZATION
BL_start, BL_end = '2018-02-1', '2019-02-1'
MS_start, MS_end = '2019-02-1', '2020-02-1'


# INDOOR CLIMATE
def plot_temp(df, room_name):
    fig, ax = plt.subplots(figsize=(11.7, 4), sharex=True)
    df.loc[:, ['Temperature', 'Outdoor_Temperature']].plot(title='Office and Outdoor Air Temperature',
                                                           color=['darkblue', 'grey'],
                                                           linewidth=.4, ax=ax)
    ax.axvline(x='02-01-2019', color='orange', linestyle='--', linewidth=1)
    ax.fill_between(df.loc['02-01-2019':, :].index.values, -15, 40, facecolor=color_MS, alpha=0.1)
    ax.fill_between(df.loc[:'02-01-2019', :].index.values, -15, 40, facecolor=color_BL, alpha=0.1)
    ax.text(x='02-01-2019', y=-14, s='LED, Mobile App', color='red', size=12)
    ax.text(x='02-01-2019', y=37, s='MOBISTYLE', color=color_MS, size=12)
    ax.text(x='02-01-2018', y=37, s='BASELINE', color=color_BL, size=12)
    ax.set(ylim=(-15, 40), xticks=pd.date_range(start='2018-02-1', periods=12, freq='2MS'), xlabel='',
           ylabel='($^o$C)')
    ax.set_xticklabels(pd.date_range(start='2018-02-1', periods=12, freq='2MS').strftime('%b, %Y'), rotation=90)


def boxplot_monthly_temp(df, room_name):
    fig, ax = plt.subplots(figsize=(11.7, 4))
    data = (df.query('`Room Status` > 0').loc[:, ['Temperature']])
    data.loc[BL_start: BL_end, 'Monitoring_Period'] = 'BASELINE'
    data.loc[MS_start: MS_end, 'Monitoring_Period'] = 'MOBISTYLE'
    sns.boxplot(data=data,
                x=data.index.month, y='Temperature', hue='Monitoring_Period',
                showfliers=False, palette=[color_BL, color_MS], ax=ax)

    ax.axhline(y=25, xmax=0.35, color=(.3, .7, .4), linestyle='--', linewidth=1)
    ax.axhline(y=21, xmax=0.35, color=(.3, .7, .4), linestyle='--', linewidth=1)
    ax.text(x=-.5, y=25.1, s='Comfort cat. II+', color=(.3, .7, .4), size=12)
    ax.text(x=-.5, y=21.1, s='Comfort cat. II-', color=(.3, .7, .4), size=12)
    ax.axhline(y=27, xmin=0.35, xmax=0.75, color=(.3, .7, .4), linestyle='--', linewidth=1)
    ax.axhline(y=23, xmin=0.35, xmax=0.75, color=(.3, .7, .4), linestyle='--', linewidth=1)
    ax.axhline(y=25, xmin=0.75, color=(.3, .7, .4), linestyle='--', linewidth=1)
    ax.axhline(y=21, xmin=0.75, color=(.3, .7, .4), linestyle='--', linewidth=1)

    ax.tick_params(axis='both', which='major', labelsize=14)
    ax.legend(fontsize=14)
    ax.xaxis.grid(True)
    ax.set_title(f'Indoor air temperature (Room Occupied). {room_name}', fontsize=14)
    ax.set_ylabel('[$^o$C]', fontsize=14)
    ax.set_xlabel('', fontsize=14)
    ax.set_xticklabels(pd.date_range(start='2018-1-1', periods=12, freq='MS').strftime('%b'), rotation=0)
    fig.tight_layout()
    return fig


def boxplot_monthly_rh(df, room_name):
    fig, ax = plt.subplots(figsize=(11.7, 4))
    data = (df.query('`Room Status` > 0').loc[:, ['RH']])
    data.loc[BL_start: BL_end, 'Monitoring_Period'] = 'BASELINE'
    data.loc[MS_start: MS_end, 'Monitoring_Period'] = 'MOBISTYLE'
    sns.boxplot(data=data,
                x=data.index.month, y='RH', hue='Monitoring_Period',
                showfliers=False, palette=[color_BL, color_MS], ax=ax)

    ax.axhline(y=60, color=(.3, .7, .4), linestyle='--', linewidth=1)
    ax.axhline(y=30, color=(.3, .7, .4), linestyle='--', linewidth=1)
    ax.text(x=-.5, y=61, s='Comfort cat. II+', color=(.3, .7, .4), size=12)
    ax.text(x=-.5, y=31, s='Comfort cat. II-', color=(.3, .7, .4), size=12)
    ax.tick_params(axis='both', which='major', labelsize=14)
    ax.legend(fontsize=14)
    ax.xaxis.grid(True)
    ax.set_title(f'Indoor air Relative Humidity levels (Room Occupied). {room_name}', fontsize=14)
    ax.set_ylabel('[%]', fontsize=14)
    ax.set_xlabel('', fontsize=14)
    ax.set_xticklabels(pd.date_range(start='2018-1-1', periods=12, freq='MS').strftime('%b'), rotation=0)
    fig.tight_layout()
    return fig


def boxplot_monthly_co2(df, room_name):
    fig, ax = plt.subplots(figsize=(11.7, 4))
    data = (df.query('`Room Status` > 0').loc[:, ['CO2']])
    data.loc[BL_start: BL_end, 'Monitoring_Period'] = 'BASELINE'
    data.loc[MS_start: MS_end, 'Monitoring_Period'] = 'MOBISTYLE'
    sns.boxplot(data=data,
                x=data.index.month, y='CO2', hue='Monitoring_Period',
                showfliers=False, palette=[color_BL, color_MS], ax=ax)
    ax.axhline(y=1200, color=(.8, .07, .25), linestyle='--', linewidth=1)
    ax.text(x=-.5, y=1250, s='Comfort cat. IV+', color=(.8, .07, .25), size=12)
    ax.tick_params(axis='both', which='major', labelsize=14)
    ax.legend(fontsize=14)
    ax.xaxis.grid(True)
    ax.set_title(f'Indoor air CO2 levels (Room Occupied). {room_name}', fontsize=14)
    ax.set_ylabel('[ppm]', fontsize=14)
    ax.set_xlabel('', fontsize=14)
    ax.set_xticklabels(pd.date_range(start='2018-1-1', periods=12, freq='MS').strftime('%b'), rotation=0)
    fig.tight_layout()
    return fig


def boxplot_monthly_voc(df, room_name):
    fig, ax = plt.subplots(figsize=(11.7, 4))
    data = (df.query('`Room Status` > 0').loc[:, ['VOC']])
    data.loc[BL_start: BL_end, 'Monitoring_Period'] = 'BASELINE'
    data.loc[MS_start: MS_end, 'Monitoring_Period'] = 'MOBISTYLE'
    sns.boxplot(data=data,
                x=data.index.month, y='VOC', hue='Monitoring_Period',
                showfliers=False, palette=[color_BL, color_MS], ax=ax)
    ax.axhline(y=100, color=(.8, .07, .25), linestyle='--', linewidth=1)
    ax.text(x=-.5, y=105, s='Comfort cat. IV+', color=(.8, .07, .25), size=12)
    ax.tick_params(axis='both', which='major', labelsize=14)
    ax.legend(fontsize=14)
    ax.xaxis.grid(True)
    ax.set_title(f'Indoor air VOC levels (Room Occupied). {room_name}', fontsize=14)
    ax.set_ylabel('[ppb]', fontsize=14)
    ax.set_xlabel('', fontsize=14)
    ax.set_xticklabels(pd.date_range(start='2018-1-1', periods=12, freq='MS').strftime('%b'), rotation=0)
    fig.tight_layout()
    return fig


# THERMAL COMFORT
def stats_category(df, cat_name):
    """
    This f-n calculates time distribution of indoor air parameters in comfort categories
    and percentage of missing data.
    """
    if cat_name in ('Category_TEMP', 'Category_RH'):
        df_cat = pd.DataFrame(0, index=[cat_name], columns=labels_T_RH + ['Missing data'])
        for cat in labels_T_RH:
            df_cat.loc[cat_name, cat] = df[cat_name].isin([cat]).sum() * 100 / len(df[cat_name])
    else:
        df_cat = pd.DataFrame(0, index=[cat_name], columns=labels_CO2_VOC + ['Missing data'])
        for cat in labels_CO2_VOC:
            df_cat.loc[cat_name, cat] = df[cat_name].isin([cat]).sum() * 100 / len(df[cat_name])
    df_cat.loc[cat_name, 'Missing data'] = df[cat_name].isna().sum() * 100 / len(df[cat_name])

    return df_cat.fillna(0)


def plot_comfort_cat_temp_rh(df, room_name, parameter):
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(11.7, 4), sharey=True)
    if parameter == 'Temperature':
        category_name = 'Category_TEMP'
    else:
        category_name = 'Category_RH'
    df_cat = (df.query('`Room Status` > 0')
                .groupby(['Monitoring_Period', 'Season']).apply(stats_category, category_name)
                .reset_index().set_index('Season'))
    BL_T = df_cat.query('Monitoring_Period == "BASELINE"').loc[:, labels_T_RH + ['Missing data']]
    MS_T = df_cat.query('Monitoring_Period == "MOBISTYLE"').loc[:, labels_T_RH + ['Missing data']]
    BL_T.plot(kind='barh', stacked=True, color=cmap_T_RH, legend='', ax=ax1)
    MS_T.plot(kind='barh', stacked=True, color=cmap_T_RH, legend='', ax=ax2)
    set_barh_text(BL_T, ax1)
    set_barh_text(MS_T, ax2)
    for ax in (ax1, ax2):
        ax.set(xlim=(0, 100), xticks=[0, 20, 40, 60, 80, 100], xticklabels=[0, 20, 40, 60, 80, '100%'], ylabel='')
        ax.tick_params(axis='both', which='major', labelsize=14)
        ax.legend('')
    ax1.set_title('BASELINE')
    ax2.set_title('MOBISTYLE')
    plt.suptitle(f'Time Distribution (%) in Comfort Categories. {parameter} for {room_name}', fontsize=14)
    fig.legend(labels_T_RH + ['Missing data'], loc='lower center', bbox_to_anchor=(0.5, 0.0), ncol=8, fontsize=12)
    fig.tight_layout()
    fig.subplots_adjust(top=0.85, bottom=0.2)
    return fig


def plot_comfort_cat_co2_voc(df, room_name, parameter):
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(11.7, 4), sharey=True)
    if parameter == 'CO2':
        category_name = 'Category_CO2'
    else:
        category_name = 'Category_VOC'
    df_cat = (df.query('`Room Status` > 0')
                .groupby(['Monitoring_Period', 'Season']).apply(stats_category, category_name)
                .reset_index().set_index('Season')
              )
    BL_T = df_cat.query('Monitoring_Period == "BASELINE"').loc[:, labels_CO2_VOC + ['Missing data']]
    MS_T = df_cat.query('Monitoring_Period == "MOBISTYLE"').loc[:, labels_CO2_VOC + ['Missing data']]
    BL_T.plot(kind='barh', stacked=True, color=cmap_CO2_VOC, legend='', ax=ax1)
    MS_T.plot(kind='barh', stacked=True, color=cmap_CO2_VOC, legend='', ax=ax2)
    set_barh_text(BL_T, ax1)
    set_barh_text(MS_T, ax2)

    for ax in (ax1, ax2):
        ax.set(xlim=(0, 100), xticks=[0, 20, 40, 60, 80, 100], xticklabels=[0, 20, 40, 60, 80, '100%'], ylabel='')
        ax.tick_params(axis='both', which='major', labelsize=14)
        ax.legend('')
    ax1.set_title('BASELINE')
    ax2.set_title('MOBISTYLE')
    plt.suptitle(f'Time Distribution (%) in Comfort Categories. {parameter} in {room_name}', fontsize=14)
    fig.legend(labels_CO2_VOC + ['Missing data'], loc='lower center', bbox_to_anchor=(0.5, 0.0), ncol=8, fontsize=12)
    fig.tight_layout()
    fig.subplots_adjust(top=0.85, bottom=0.2)
    return fig


# WINDOW OPENINGS
def plot_monthly_window(df, room_name):
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(11.7, 8), sharex=True)
    df_OP = df[['Window State Change']].resample('MS').apply(lambda x: x.isin([1]).sum())
    df_OP['Window_State'] = df[['Window State']].resample('MS').mean() * 100
    df_OP.loc[:'2019-02-1', 'Monitoring_Period'] = 'BASELINE'
    df_OP.loc['2019-02-1':, 'Monitoring_Period'] = 'MOBISTYLE'

    sns.barplot(data=df_OP, x=df_OP.index.month, y='Window State Change', hue='Monitoring_Period',
                palette=pallete, ax=ax1)
    sns.barplot(data=df_OP, x=df_OP.index.month, y='Window_State', hue='Monitoring_Period',
                palette=pallete, ax=ax2)
    ax1.set(ylabel='Opening (count)', xlabel='')
    ax2.set(ylabel='Time open (pct)', xlabel='')
    ax2.set_xticklabels(pd.date_range(start='2018-1-1', periods=12, freq='MS').strftime('%b'), rotation=0)
    [ax.legend(loc='upper right', fontsize=14) for ax in (ax1, ax2)]
    plt.suptitle(f'Window opening data. {room_name}', fontsize=14)
    plt.tight_layout()
    return fig


def plot_window_temp_out(df, room_name):
    df = df.query('`Room Status` > 0')
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(11.7, 4), sharey=True, sharex=True)
    for period, ax in zip(['BASELINE', 'MOBISTYLE'], (ax1, ax2)):
        mask = (df['Monitoring_Period'] == period)
        x, y = df.loc[mask, 'Temperature'], df.loc[mask, 'Outdoor Temperature']
        z = df.loc[mask, 'Window State'] * 100
        sct = ax.scatter(x, y, c=z, cmap='GnBu')
        ax.set_title(period, size=14)
        ax.set(xlabel='Office Temperature ($^o$C)')

    ax1.set_ylabel('Outdoor Temperature ($^o$C)')
    cbar = plt.colorbar(sct)
    cbar.ax.set_ylabel('Window open (pct)', size=12, rotation=90, va='top')
    cbar.ax.yaxis.set_ticks_position('right')
    plt.suptitle(f'Window open state, Indoor and Outdoor Temperature. {room_name}', size=14)
    plt.tight_layout()
    fig.subplots_adjust(top=0.8)
    return fig


# CORRELATION MATRIX
def plot_corr_matrix(df, room_name, period):
    mask_period = (df['Monitoring_Period'] == period)
    df = df.query('`Room Status` > 0').loc[mask_period, ]
    df = df.drop(columns=['Room Status', 'Season', 'Monitoring_Period', 'Diffuse radiation', 'Window State Change'])
    fig, ax = plt.subplots(figsize=(11.7, 8.27))

    mask = np.zeros_like(df.corr(method='spearman'))
    mask[np.triu_indices_from(mask)] = True
    labels = [col.replace('_', ' ') for col in df.columns]
    hm = sns.heatmap(df.corr(method='spearman'), square=True,
                     cmap='RdBu_r', linewidths=.5, annot=True, fmt='.2f',
                     xticklabels=labels, yticklabels=labels,
                     mask=mask, vmax=1., vmin=-1., ax=ax)
    hm.figure.axes[-1].set_ylabel('Correlation coeficient', size=16)
    hm.tick_params(labelsize=14)
    hm.set_title(f"Correlation matrix for {room_name}. {period}", fontsize=16)
    plt.tight_layout()
    return fig





