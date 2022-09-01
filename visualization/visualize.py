import datetime

from matplotlib import pyplot as plt
import numpy as np
import pandas as pd

DEST_DIR = '/home/mh/Outputs/'

month_names_full = ['January', 'February', 'March', 'April',
                    'May', 'June', 'July', 'August',
                    'September', 'October', 'November', 'December']

month_names_short = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun',
                     'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']

days_of_week = ['Monday', 'Tuesday', 'Wednesday', 'Thursday',
                'Friday', 'Saturday', 'Sunday']

aqi = pd.read_csv('../data/uniq.csv', parse_dates=[['Date', 'Time']])


def generate_plot(x_axis,
                  y_axis,
                  name,
                  x_lab='',
                  y_lab='Air Quality Index (AQI)',
                  color='green',
                  title='',
                  legend=None):
    """
Generates plot and saves it in $DEST_DIR
    """
    if legend is None:
        legend = []
    if type(x_axis[0]) == int or type(x_axis[0]) == float:
        plt.xticks(np.arange(min(x_axis), max(x_axis) + 1, 3.0))
    plt.rcParams["font.family"] = 'Segoe UI Variable'
    plt.title(title, color='red')
    plt.plot(x_axis, y_axis, '.-', color=color, linewidth=1)
    plt.xlabel(x_lab, color='blue')
    plt.ylabel(y_lab, color='blue')
    plt.grid(axis='y')
    plt.legend(legend, frameon=False)
    plt.gcf().savefig(DEST_DIR + name, dpi=300)
    plt.clf()


# Split the data
months_aqi = []
for mi in range(1, 13):
    months_aqi.append(aqi[aqi.Date_Time.dt.month == mi])

#########################################################
"""
year_wm = {
    "January": {1: avg, 2: avg, 3: avg, ...},
    "February": [{1: avg, 2, avg, ...},
    ...
}
"""

"""
year_wma = {
    "January": avg,
    "February": avg,
    ...
}
"""

# full data
year_wm = {}

# avg per months
year_wm_avg = {}

for mo in range(12):
    # month
    days = list(set(months_aqi[mo].Date_Time.dt.day))
    days_len = len(days)

    tmp_days = {}
    for i in range(days_len):
        # day
        daily_sum = 0
        today = months_aqi[mo][months_aqi[mo].Date_Time.dt.day == days[i]]
        for j in range(len(today)):
            # hour
            daily_sum += today.AQI.iloc[j]

        tmp_days[list(set(today.Date_Time.dt.day))[0]] = daily_sum / len(today)

    year_wm[month_names_full[mo]] = tmp_days

    monthly_sum = 0
    for it in year_wm[month_names_full[mo]].values():
        monthly_sum += it

    year_wm_avg[month_names_full[mo]] = monthly_sum / days_len

######################################################
# YEARLY
generate_plot(x_axis=month_names_short,
              y_axis=list(year_wm_avg.values()),
              x_lab='Months',
              title='AQI of Dhaka (Feb 2020 - Jan 2021)',
              name='yearly')

######################################################
# MONTHLY
k = 0
for i in year_wm.values():
    generate_plot(x_axis=list(i.keys()),
                  y_axis=list(i.values()),
                  x_lab='Days',
                  title=month_names_full[k],
                  name=month_names_full[k])
    k += 1


######################################################
# WEEKLY
def generate_weekly(season='dry'):
    """
Generate weekly plot (Rainy and Dry season)
    """
    wd_sum = {'Monday': 0, 'Tuesday': 0, 'Wednesday': 0, 'Thursday': 0,
              'Friday': 0, 'Saturday': 0, 'Sunday': 0}

    wd_avg = wd_sum.copy()
    num = wd_sum.copy()

    k, m = 0, 1
    year = 2020
    for i in year_wm.values():
        if season == 'dry' and 6 <= m <= 9:
            m += 1
            continue
        elif season == 'rainy' and m < 5 or m > 8:
            m += 1
            continue

        if k == 0:
            year = 2021
        else:
            year = 2020

        for j in i:
            wd_sum[days_of_week[datetime.datetime(year, m, j).weekday()]] += i[j]
            num[days_of_week[datetime.datetime(year, m, j).weekday()]] += 1

        k += 1
        m += 1

    for i in wd_sum:
        wd_avg[i] = wd_sum[i] / num[i]

    title = 'Daily Average (' + 'Dry' if season == 'dry' else 'Rainy'
    generate_plot(x_axis=days_of_week,
                  y_axis=list(wd_avg.values()),
                  name='Weekly_' + 'dry' if season == 'dry' else 'rainy',
                  title=title + ' Season)',
                  x_lab='Days')


generate_weekly()
generate_weekly('rainy')


###################################################
# HOURLY
def generate_hourly(season='dry'):
    """
Generate hourly plot (Rainy and Dry season)
    """
    hours = {'00': 0, '01': 0, '02': 0, '03': 0, '04': 0, '05': 0, '06': 0,
             '07': 0, '08': 0, '09': 0, '10': 0, '11': 0, '12': 0, '13': 0,
             '14': 0, '15': 0, '16': 0, '17': 0, '18': 0, '19': 0, '20': 0,
             '21': 0, '22': 0, '23': 0}

    hours_cnt = hours.copy()

    for mo in range(12):
        if season == 'dry' and 6 <= mo <= 9:
            mo += 1
            continue
        elif season == 'rainy' and mo < 5 or mo > 8:
            mo += 1
            continue

        days = list(set(months_aqi[mo].Date_Time.dt.day))
        days_len = len(days)
        for i in range(days_len):
            today = months_aqi[mo][months_aqi[mo].Date_Time.dt.day == days[i]]

            for j in range(len(today)):
                hour = str(today.Date_Time.dt.hour.iloc[j])
                hour = '0' + hour if len(hour) < 2 else hour
                hours[hour] += today.AQI.iloc[j]
                hours_cnt[hour] += 1

    for key, val in hours.items():
        hours[key] = hours[key] / hours_cnt[key]

    title = 'Dry' if season == 'dry' else 'Rainy' + ' Season)' + ' Season)'
    generate_plot(list(hours.keys()),
                  list(hours.values()),
                  name='Hourly_' + 'dry' if season == 'dry' else 'rainy',
                  title='Hourly Analysis (' + title,
                  x_lab='Hours')


generate_hourly()
generate_hourly('rainy')
