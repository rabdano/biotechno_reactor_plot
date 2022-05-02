import matplotlib as mpl
mpl.use('Agg')
import matplotlib.pyplot as plt
from glob import glob
import numpy as np
import pandas as pd
import os


files = sorted(glob('./data/*/*.csv'))

for file in files:
    print(file)
    filename = file.split('\\')[-2] + '_' + file.split('\\')[-1][:-4]
    print(filename)
    if not os.path.exists('./figures/' + filename):
        os.mkdir('./figures/' + filename)

    data = pd.read_csv(file,
                       sep=';',
                       skiprows=5,
                       low_memory=False,
                       parse_dates=['Date'],
                       dayfirst=True,
                       dtype=np.float64,
                       decimal=',')

    time_0_idx = 0
    for i in range(len(data['Date'])):
        if data['3DO001 - Раств. кислород 1 F3'][i] >= 100:
            time_0_idx = i
    print(time_0_idx)

    time_h = (data['Date'].to_numpy(dtype=np.float64)-data['Date'].to_numpy(dtype=np.float64)[time_0_idx])/1e9/3600

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

        plt.figure(figsize=(16./2.54, 12./2.54))
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
        plt.savefig('./figures/' + filename + '/' + l + '.png', bbox_inches='tight', dpi=300)
        plt.close()
