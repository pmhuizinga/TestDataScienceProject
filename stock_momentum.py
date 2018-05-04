# Libraries
import pandas as pd
import numpy as np

# Variables
nr_of_stocks = 2 # Number of best performing stocks
nr_of_cumulative_periods = 4 # Number of periods to calculate cumulative returns
rebalance_frequency = 2 # Number of periods to rebalancing
transaction_costs = 0.01 # 1%

file = 'AEX-data.xlsx'
sheet = 'total returns aandelen'
df = pd.read_excel(file, sheet, header=0)

# Verwijder eerste record (met datastream security code)
df = df[1:]

# even tijdelijk het bereik verkleinen tbv test
df = df.iloc[0:10,0:4]

# Sortering op datum
df.sort_values(by=['Name'])

# Maak arrays aan voor cumulatieve rendementen en voor gewichten
df_cum = df.copy(deep=True) # array voor cumulatieve 
df_contribution = df.copy(deep=True)
rows, cols = df.shape # grootte van het bereik

# replace market values in df with monthly returns and append cumulative returns to df_cum dataframe.
for x in df.columns.tolist()[1:]:
    #df_weight[x] = df[x].cumsum(df).fillna(0)
    df[x] = df[x].pct_change().fillna(0) # monthly returns
    df_cum[x] = df_cum[x].pct_change(periods=nr_of_cumulative_periods).fillna(0) # cumulative returns

# sort descending on cumulative returns replace top 'nr_of_stocks' with avg weight and the remainder with zeros.
# het minteken bepaald de sorteringsvolgorde
weights = np.where(np.argsort(-df_cum.iloc[:,1:]) >= nr_of_stocks, 0, 1/nr_of_stocks)
#weights_rebal = np.where(np.mod(weights[:]-nr_of_cumulative_periods, rebalance_frequency),'a','b') # kan het in 1 keer?
weights_rebal =  np.empty(shape=[weights.shape[0],weights.shape[1]])

# bepaal gewicht rekening houdend met de rebalance frequency
for x in range(weights.shape[0]): # rows
    for y in range(weights.shape[1]): # columns
        weights_rebal[x][y] = weights[x-np.mod(x-nr_of_cumulative_periods,rebalance_frequency)][y]

# bepaal de contributie (weights_rebal * maand rendement)
for x in range(df.shape[0]):
    for y in range(df.shape[1])[1:]:
        df_contribution.iloc[x,y] = df.iloc[x,y] * weights_rebal[x][y-1]

# Bepaal cu ulatief rendement van de basket
result = (np.cumprod((1+(df_contribution.iloc[:,1:].sum(axis=1))))-1).iloc[-1]

