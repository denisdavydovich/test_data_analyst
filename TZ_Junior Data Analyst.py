#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt


# загрузка данных из файла
data = pd.read_csv('tz_data.csv')

# удаление лишних колонок
columns = ['area', 'cluster', 'cluster_name', 'keyword', 'x', 'y', 'count']
data = data[columns].sort_values(['area', 'cluster', 'cluster_name', 'count'], ascending=[True, True, True, False])

# добавление заголовков
header = 'area, cluster, cluster_name, keyword, x, y, count, color\n'
with open('output_data.csv', 'w') as f:
    f.write(header)
    data.to_csv(f, index=False, header=False)

# добавление фильтра
filter_row = 'Filter: ,,,\n'
with open('output_data.csv', 'r') as f:
    content = f.read()
with open('output_data.csv', 'w') as f:
    f.write(filter_row)
    f.write(content)

# генерация цветов для каждого кластера внутри области
cluster_colors = {}
for area in data['area'].unique():
    clusters = data[data['area'] == area]['cluster'].unique()
    palette = sns.color_palette('hls', len(clusters)).as_hex()
    for i, cluster in enumerate(clusters):
        if pd.isna(area) or pd.isna(cluster):
            continue
        else:
            cluster_colors[(area, cluster)] = palette[i].upper()

# Добавление колонки c цветом в Data
default_color = sns.color_palette('hls', 1)
data['color'] = data.apply(lambda row: cluster_colors.get((row['area'], row['cluster']), default_color[0]), axis=1)


# удаление дубликатов слов в одной области
data.drop_duplicates(subset=['area', 'keyword'], keep='first', inplace=True)

# сортировка данных
data = data.sort_values(by=['area', 'cluster', 'cluster_name', 'count'], ascending=[True, True, True, False])

# сохранение данных в файл
data.to_csv('/home/denis/Рабочий стол/output_data.csv', index=False)


# In[2]:


# загрузка данных из файла
data = pd.read_csv('output_data.csv')

# определение цветов для кластеров
colors = {
    'green': '#1f77b4',
    'red': '#d62728',
    'blue': '#9467bd',
    'orange': '#ff7f0e',
    'purple': '#8c564b',
    'brown': '#e377c2',
    'pink': '#ff99ff',
    'gray': '#bcbd22',
    'olive':'#7f7f7f',
    'cyan': '#17becf'
}

# построение диаграмм рассеяния для каждой области
for area in data['area'].unique():
    area_data = data[data['area'] == area]
    clusters = area_data['cluster'].unique()

    # определение цветов для кластеров
    color_map = {}
    for i, cluster in enumerate(clusters):
        color_map[cluster] = colors[list(colors.keys())[i]]

    # построение диаграммы рассеяния
    fig, ax = plt.subplots(figsize=(8, 8))
    for cluster, cluster_data in area_data.groupby('cluster'):
        ax.scatter(cluster_data['x'], cluster_data['y'], c=color_map[cluster], edgecolors='black', label=f'Cluster {cluster}')
        handles, labels = ax.get_legend_handles_labels()

    # настройка легенды и подписей
    ax.legend(labels=[f'Cluster {cluster}' for cluster in clusters], loc='best', bbox_to_anchor=(1, 0.5))
    ax.set_title(area)
    ax.set_xlabel('x')
    ax.set_ylabel('y')
    ax.set_xlim(left=0)  # добавляем отступ для оси x
    ax.set_aspect('equal')
    plt.tight_layout()

    # сохранение диаграммы рассеяния в файл и смена размера изображений
    fig.set_size_inches(1500/100, 1500/100)
    plt.savefig(f'/home/denis/Рабочий стол/{area}.png', dpi=100)
    plt.close()

