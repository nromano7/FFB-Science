
# coding: utf-8

# <p style="font-family: Arial; 
# font-size:2em;
# color:#2462C0; 
# font-style:bold"
# >NFLdb Example - Carson Wentz Stats</p>
# 
# #### Comparing Carson Wentz's QB Rating

# In[1]:

import nfldb
import pandas as pd
import numpy as np


# Connect to NFLdb.

# In[2]:

db = nfldb.connect()


# Define function that calculates NFL Passer Rating.

# In[3]:

def nfl_pass_rating(pass_att,pass_cmp,pass_yds,pass_tds,pass_int):
    cmp_per_att = (pass_cmp/pass_att-0.3)*5
    yds_per_att = (pass_yds/pass_att-3.0)*.25
    td_per_att = (pass_tds/pass_att)*20
    int_per_att = 2.375 - (25*pass_int/pass_att)
    pass_rating = ((cmp_per_att+yds_per_att+td_per_att+int_per_att)/6)*100
    return pass_rating


# Using nfldb 'Query' class, query db for QB stats needed for *nfl_pass_rating*. These stats include:
# * Passing Attempts
# * Passing Completions
# * Passng Interceptions
# * Total Passing Yards
# * Total Passing Touchdowns

# In[4]:

q = nfldb.Query(db)
q.game(season_year=2016, season_type='Regular',week=1)
q.player(position='QB')
q.play_player(passing_att__gt=0)
player_data = [(1, x.player.full_name, x.passing_att, x.passing_cmp, x.passing_yds, 
                x.passing_tds, x.passing_int) for x in q.as_aggregate()]


# Pipe player stats ( of Python type *list* ) into a Pandas DataFrame. Get QB passer rating, add *pass_pct,* *pass_rtg,* and *week* features to dataframe, and sort by pass_rtg.

# In[5]:

labels = ['week','full_name','pass_att','pass_cmp','pass_yds','pass_tds', 'pass_int']
df = pd.DataFrame.from_records(player_data,columns=labels)
df['pass_pct'] = 100*df.pass_cmp/df.pass_att
df['pass_rtg'] = nfl_pass_rating(df.pass_att,df.pass_cmp,df.pass_yds,df.pass_tds,df.pass_int) # calc rating
df.sort_values('pass_rtg',ascending=False).reset_index(drop=True).head(12) # show top 12 qb ratings for week 1


# 
# Up to this point we've been able to extract QB passing stats for a single week. The dataframe above gives the top 12 QBs (by passer rating) for Week 1. Carson Wentz got Philly fans very excited after a Top 12 performance in the first game of his rookie year. Let's see how he stands against other QBs through the rest of the season. 
# 
# We'll have to modify the code slightly to aquire statistics for each week of the 2016 Regular Season.

# In[6]:

weeks = np.arange(1,18)
season = {}
for wk in weeks:
    q = nfldb.Query(db)
    q.game(season_year=2016, season_type='Regular',week=wk)
    q.player(position='QB')
    q.play_player(passing_att__gt=0)
    season[wk] = [(wk, x.player.full_name,x.passing_att,x.passing_cmp,x.passing_yds, 
                    x.passing_tds,x.passing_int) for x in q.as_aggregate()]


# Store dataframes for each week in dictionary called *season_df*. For each week, get QB passer rating, add pass_pct, pass_rtg, and week features to dataframe, and sort by pass_rtg.

# In[7]:

# pipe dataframes for each week into a dictionary for later use
season_dfs = {'Week '+str(wk): pd.DataFrame.from_records(season[wk],columns=labels) for wk in weeks}
for wk in weeks:
    df_tmp = season_dfs['Week '+str(wk)]
    df_tmp['pass_pct'] = 100*df_tmp.pass_cmp/df_tmp.pass_att
    df_tmp['pass_rtg'] = nfl_pass_rating(df_tmp.pass_att, df_tmp.pass_cmp,
                                            df_tmp.pass_yds, df_tmp.pass_tds, df_tmp.pass_int) # calc rating
    season_dfs['Week '+str(wk)] = df_tmp

# manually check for same output
season_dfs['Week 1'].head(5) == df.head(5)


# Now that we have all QB data for each week, we can start to explore the data and compare Carson Wentz to the rest of the NFL. We'll use the interactive plotting capabilities of Plotly to show Wentz's performance throughout the season.

# In[60]:

import plotly.offline as py
import plotly.graph_objs as go
py.init_notebook_mode()


# In[63]:
bye=4
wks = [wk for wk in weeks[weeks!=bye]]
wk_labels = ['Week '+str(wk) for wk in wks]

trace1 = go.Scatter(name='Carson Wentz',
                    x=wks,
                    y=new_df['Carson Wentz'].values,
                    fill='tonexty',
                    fillcolor='#004953',
                    text=wk_labels,
                    line = dict(color='Grey')
                   )
trace2 = go.Scatter(name='NFL Best',
                    x=wks,
                    y=new_df['NFL Best'].values,
                    fill='tonexty',
                    fillcolor='White',
                    text=wk_labels,
                    line = dict(color='Red')
                   )
data = [trace1,trace2]
layout = dict(title = 'NFL Passer Rating for 2016 Regular Season',
              xaxis = dict(title = 'Week'),
              yaxis = dict(title = 'Rating'),
              )

fig = dict(data=data, layout=layout)
py.iplot(fig)


# In[ ]:



