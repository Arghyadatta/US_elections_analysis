import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

data = pd.read_csv('data/elections.csv', sep=';')


#------------------------------------------------Vote Calculations-----------------------------------

df = data.groupby('State')['Democrats 08 (Votes)'].sum().to_frame().rename(columns = {'Democrats 08 (Votes)':'Votes'})
print 'In 2008, Democrats won Max votes in: '+ str(df.Votes.idxmax())+' and the value is: '+str(df.Votes.max())
df = data.groupby('State')['Democrats 12 (Votes)'].sum().to_frame().rename(columns = {'Democrats 12 (Votes)':'Votes'})
print 'In 2012, Democrats won Max votes in: '+ str(df.Votes.idxmax())+' and the value is: '+str(df.Votes.max())
df = data.groupby('State')['Republicans 08 (Votes)'].sum().to_frame().rename(columns = {'Republicans 08 (Votes)':'Votes'})
print 'In 2008, Republicans won Max votes in: '+ str(df.Votes.idxmax())+' and the value is: '+str(df.Votes.max())
df = data.groupby('State')['Republicans 12 (Votes)'].sum().to_frame().rename(columns = {'Republicans 12 (Votes)':'Votes'})
print 'In 2012, Republicans won Max votes in: '+ str(df.Votes.idxmax())+' and the value is: '+str(df.Votes.max())



def variations_bar(data, group_by, xlbl, col, ylbl,titl):
    df = data.groupby(group_by)[col].sum().to_frame().copy()
    y_pos = np.arange(len(df.index))
    plt.bar(y_pos, df[col], align='center')
    plt.xticks(y_pos, df.index, rotation = 'vertical')
    plt.ylabel(ylbl)
    plt.title(titl)
    plt.show()

def state_county(state,data,col,titl):
    df = data[data.State == state]
    df.County = df.County.apply(lambda x: x[0:x.rfind(' County')])
    df = df.groupby(['State', 'County'])[col].sum().to_frame().copy()
    if len(df) > 50:
        df = df.nlargest(30,col)
    y_pos = np.arange(len(df.index))
    plt.bar(y_pos, df[col], align='center')
    df.reset_index(inplace = True)
    plt.xticks(y_pos, df.County, rotation = 'vertical')
    plt.xlabel('County')
    plt.ylabel(col)
    plt.title(titl)
    plt.tight_layout()
    plt.show()

def change_votes_year(data,state,party1,year1,year2,compare = True, party2=None):
    data = df[df.State == state].copy()
    data.County = data.County.apply(lambda x: x[0:x.rfind(' County')])
    if compare:data = data.groupby('County')[party1 +' '+ year1 + ' (Votes)',  party1 +' '+ year2 + ' (Votes)', party2 +' '+ year1 + ' (Votes)', party2 +' '+ year2 + ' (Votes)' ].sum()
    else: data = data.groupby('County')[party1 +' '+ year1 + ' (Votes)',  party1 +' '+ year2 + ' (Votes)'].sum()
    data['Change_'+party1] = data[party1+' '+ year2 + ' (Votes)'] - data[party1+' '+ year2 + ' (Votes)']
    if compare: data['Change_'+party2] = data[party2 +' '+ year2 + ' (Votes)'] - data[party2+' '+ year2 + ' (Votes)']
    data = data.dropna()
    data['ChangePercentage'] = (data.Change / data[party+' '+ year1 + ' (Votes)']) * 100
    increase = data[data.Change < 0].copy()
    increase.Change = increase.Change * (-1)
    increase.ChangePercentage = increase.ChangePercentage *(-1)
    increase.sort_values('ChangePercentage', ascending = False)
    

def education(data, edu1, edu2):
    data[edu1+str('population')] = data['Total Population'] * data[edu] * 0.01
    data[edu2+str('population')] = data['Total Population'] * data[edu] * 0.01
    data1 = data.groupby(['State', 'County'])[edu1+str('population')].sum().sort_index().copy()
    data2 = data.groupby(['State', 'County'])[edu2+str('population')].sum().sort_index().copy()
    df = pd.concat([data1, data2], axis = 1)
    return df

def salary(data,state):
    data = data[data.State == state]
    data = data.groupby(['State', 'County'])['Median Earnings 2010'].median()
    return data

def by_columns(data,col):
    if col != 'Violent.crime':
        data[col + '_nos'] = data['Total Population']*0.01*data[col]
        data = data.groupby(['State','County'])[col + '_nos'].sum().to_frame().copy()
     else:
        data['Violent.crime.nos'] = (data['Total Population']/100000) * data.['Violent.crime']
    return data


def by_state_county(df,state):
    data1 = df[df.State == state].copy()
    data1.County = data1.County.apply(lambda x: x[0:x.rfind(' County')])
    data1 = data1.groupby('County')['Democrats 08 (Votes)', 'Republicans 08 (Votes)'].sum()
    # There are a total of over 3000 rows here so please add max row view in pandas to get the full list
    trace1 = go.Bar(
            x= data1.index.tolist(),
            y= data1['Democrats 08 (Votes)'].tolist(),
            name = 'Democratic Party'
            )

    trace2 = go.Bar(
            x= data1.index.tolist(),
            y= data1['Republicans 08 (Votes)'].tolist(),
            name = 'Republican Party'
            )


    data = [trace1, trace2]
    layout = go.Layout(
    barmode='stack'
            )

    fig = go.Figure(data=data, layout=layout)
    py.iplot(fig, filename='stacked-bar') 




