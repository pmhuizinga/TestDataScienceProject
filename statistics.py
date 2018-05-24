import pandas as pd

notapplicables = "N/A|NA|Not applicable|#NA"

def BasicStatistics(dataframe):
    statframe = []
    statlist = []
    cols = dataframe.columns.tolist()
    for i in range(len(dataframe.columns)):
        if dataframe.iloc[:,i].dtypes == 'float' or dataframe.iloc[:,i].dtypes == 'int' or dataframe.iloc[:,i].dtypes == 'int64' or dataframe.iloc[:,i].dtypes == 'float64':
            statlist.append([cols[i], 'numeric', \
                             format(dataframe.iloc[:,i].min(), '4f'), \
                             format(dataframe.iloc[:,i].max(), '4f'), \
                             format(dataframe.iloc[:,i].max() - dataframe.iloc[:,i].min(), '4f'), \
                             format(dataframe.iloc[:,i].mean(), '4f'), \
                             format(dataframe.iloc[:,i].std(), '4f'), \
                             int(dataframe.iloc[:,i].count()), \
                             format(dataframe.iloc[:,i].sum(), '4f'), \
                             int(dataframe.iloc[:,i].nunique()), \
                             '', \
                             int(dataframe.iloc[:,i].isnull().sum()), \
                             ''])
        elif dataframe.iloc[:,i].dtypes == 'object':
            statlist.append([cols[i],'string', \
                             '' ,'' ,'' ,'' ,'' , \
                             int(dataframe.iloc[:,i].count()), \
                             '', \
                             int(dataframe.iloc[:,i].nunique()), \
                             set(dataframe.iloc[:,i]), \
                             int(dataframe.iloc[:,i].isnull().sum()), \
                             dataframe.iloc[:,i].str.contains(notapplicables, na=True).sum()])
        elif dataframe.iloc[:,i].dtypes == 'bool':
            statlist.append([cols[i],'boolean', \
                             '' ,'' ,'' ,'' ,'' , \
                             int(dataframe.iloc[:,i].count()), \
                             '' , \
                             int(dataframe.iloc[:,i].nunique()), \
                             '', \
                             int(dataframe.iloc[:,i].isnull().sum()), \
                             ''])
    columns = (['column', \
                'type', \
                'min', \
                'max', \
                'range', \
                'mean', \
                'stdev', \
                'populated', \
                'sum', \
                'unique', \
                'uniquelist', \
                'nulls', \
                'not applicable'])

    # Make dataframe
    statframe = pd.DataFrame(statlist, columns=columns)
    return statframe
