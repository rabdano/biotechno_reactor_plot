import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages
import numpy as np
import pandas as pd
import os
import matplotlib as mpl


mpl.use('Agg')

path_to_file = 'data\Выгрузка - Серия 1\Серия 1.csv'
start_date_time = (2022, 2, 8, 16, 11, 39)  # 08/02/2022 16:11:39


print(path_to_file)
filename = path_to_file.split('\\')[-2] + '_' + path_to_file.split('\\')[-1][:-4]
print(filename)
if not os.path.exists('./figures/' + filename):
    os.mkdir('./figures/' + filename)
plot_out_name = './figures/' + filename + '/' + filename + '.pdf'
pp = PdfPages(plot_out_name)
plt.figure(figsize=(16./2.54, 12./2.54))

data = pd.read_csv(path_to_file,
                   sep=';',
                   skiprows=5,
                   low_memory=False,
                   parse_dates=['Date'],
                   dayfirst=True,
                   dtype=np.float64,
                   decimal=',')

time_0_idx = 0
timeline = data['Date'].to_numpy(dtype=np.float64)
timeline_0 = pd.Timestamp(*start_date_time).to_numpy().astype(np.float64)
time_h = (timeline-timeline_0)/1e9/3600

legends = data.columns
ylims = {'Мешалка': [0, 700],
         'Раств. кислород': [0, 100],
         'pH': [6, 8],
         'Оптическая пл-ть': [0, 3],
         'Давление': [0, 0.6],
         'Масса': [0, 33],
         'Tемпература': [0, 135],
         'Воздух': [0, 22],
         'O2': [0, 11],
         'N2': [0, 11],
         'Датчик пены': [0, 120]}

y_captions = {'Мешалка': 'Мешалка, об/мин',
              'Раств. кислород': 'Раств. кислород, %',
              'pH': 'pH',
              'Оптическая пл-ть': 'Мутность, AU',
              'Давление': 'Давление, бар',
              'Масса': 'Масса, кг',
              'Tемпература': r'Температура, $\degree$С',
              'Воздух': 'Воздух, л/мин',
              'O2': 'Кислород, л/мин',
              'N2': 'Азот, л/мин',
              'Датчик пены': 'Датчик пены'}

for l in legends:
    # print(l)

    plt.clf()
    plt.xlim([0, 16])
    for yl in ylims:
        if yl in l:
            plt.ylim(ylims[yl])
    plt.locator_params(axis='y', nbins=10)
    plt.locator_params(axis='x', nbins=17)
    plt.plot(time_h, data[l].to_numpy(), 'k-', lw=0.75)
    plt.xlabel('Время, ч')
    for yc in y_captions:
        if yc in l:
            plt.ylabel(y_captions[yc])
    plt.title(l)
    plt.grid(True, lw=0.3)
    pp.savefig()

plt.close()
pp.close()