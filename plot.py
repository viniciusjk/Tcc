
# coding: utf-8

# In[81]:

import pandas as pd
get_ipython().magic('matplotlib inline')
from scipy.stats.mstats import gmean


# In[48]:

f = pd.read_csv('Results_condensado.csv', delimiter=';')


# In[153]:

medias = f.groupby(['Heuristica', 'Tamanho amostra']).Tempo.apply(gmean).reset_index()


# In[181]:


for i in medias.Heuristica.unique():
    medias[medias.Heuristica == i].plot.line(x='Tamanho amostra', y='Tempo', grid=True, legend= i)


# In[ ]:

#medias.to_excel('Medias.xlsx', index=False)
#mee.to_excel('mm.xlsx')
#f.to_csv('mm.csv', index=False)

input()
# In[109]:

#f.rename(columns={'Heuristica': 'Heu'})

