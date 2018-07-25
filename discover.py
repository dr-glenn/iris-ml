# Visualizing Fisher's Iris data set.
# See article: https://en.wikipedia.org/wiki/Iris_flower_data_set
# This small dataset contains measurements from 3 species of Iris flower.
# There are 50 observations of each species: Iris setosa, Iris virginica and Iris versicolor.

# Here's how you do it in R, including classifier:
# http://www.lac.inpe.br/~rafael.santos/Docs/R/CAP394/WholeStory-Iris.html
# colormaps: winter is nice.

# The jupyter notebook is more recent.

import matplotlib.pyplot as plt
import pandas as pd

def gen_colormap(df,column,palette):
    if isinstance(column, basestring):
        factor_name = column #save off the name
        factor = df[column] #extract column
        classes = factor.unique()
        #df = df.drop(factor_name,axis=1) # remove from df, so it 
        # doesn't get a row and col in the plot.
    else:
        classes = column.unique()
        
    if palette is None:
        palette = ['#e41a1c', '#377eb8', '#4eae4b', 
                   '#994fa1', '#ff8101', '#fdfc33', 
                   '#a8572c', '#f482be', '#999999']

    color_map = dict(zip(classes,palette))

    if len(classes) > len(palette):
        raise ValueError('''Too many groups for the number of colors provided.
We only have {} colors in the palette, but you have {}
groups.'''.format(len(palette), len(classes)))
    # Apply color_map to the 'factor' column to generate list of colors for each data row
    colors = factor.apply(lambda group: color_map[group])
    return color_map,colors

data = pd.read_csv('bezdekIris_copy.data')
my_cmap = ('red','blue','green')
my_colors,scatter_color = gen_colormap(data,'class',my_cmap)  
print 'species coloring: '+str(my_colors) # it is a dict with species as key
print scatter_color # it is a list with one color for each data row
# Some of the pandas plots cannot use 'scatter_color' list, they just need
# a palette constructed as a list. But the palette must contain colors in the
# order that they are encounterd in the 'scatter_color' list, we cannot get them
# by iterating over the dict object.
my_color_list = []
for col in scatter_color:
    if not col in my_color_list:
        my_color_list.append(col)
print 'my_color_list: '+str(my_color_list)

from pandas.plotting import parallel_coordinates
fig = plt.figure(figsize=(8,8))
# Draw lines for each row (each flower observation)
# X-axis is paramater of column header: sepal and petal length and width
# Each distinct 'class' (last column of data) is assigned a unique color
# With this plot you can see which categories are useful discriminants of the 'class'
#parallel_coordinates(data,'class', colormap='rainbow')
parallel_coordinates(data,'class', color=my_color_list)
plt.show()
fig.clf()

from pandas.plotting import radviz
# Plot a point for each observation.
# The parameters categories are plotted on a unit circle.
# There are 4 params in the iris dataset, so each "anchor" value is plotted at 90 degree angles.
# That is, SepalLength=0, SepalWidth=90, PetalLength=180, PetalWidth=270.
# Then a given flower observation will be plotted within this unit circle.
# Each flower is plotted using a "spring tension minimization" algorithm.
# Essentially each point is plotted so that distance from anchors is inversely proportional
# to length or width value.
#radviz(data,'class',colormap='rainbow') 
radviz(data,'class',color=my_color_list) 
plt.show()
fig.clf()

# scatter plot matrix: each parameter is compared with the others.
# There are 4 parameters, so this forms a 4x4 grid, but the grid is symmetrical (sort of)
# along the diagonal. I.E., X vs Y in one cell, but also
# Y vs X on the other side of the diagonal.

from pandas.plotting import scatter_matrix
# diagonal: either kde or hist
# color-code by 'class' does not work with my pandas.
# Here is one solution: https://stackoverflow.com/questions/22943894/class-labels-in-pandas-scattermatrix
# That solution also plots color-coded curves along the diagonal - nice.

#scatter_matrix(data,diagonal='kde') # OK, but all one color
#scatter_matrix(data,diagonal='hist',c='class',colormap='viridis')
# FIX: construct a list of colors corresponding to 'class'. Call gen_colormap
from scipy.stats import gaussian_kde
import numpy as np
axarr = scatter_matrix(data,marker='o',c=scatter_color,diagonal=None)
for rc in xrange(len(data.columns)-1):
    for group in data['class'].unique():
        print 'processing rc=%d, group=%s, color=%s' %(rc,group,my_colors[group])
        y = data[data['class'] == group].iloc[:,rc]
        gkde = gaussian_kde(y)
        ind = np.linspace(y.min(), y.max(), 1000)
        axarr[rc][rc].plot(ind, gkde.evaluate(ind),c=my_colors[group])

plt.show()