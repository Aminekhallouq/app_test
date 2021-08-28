#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import requests
import dash  # (version 1.12.0) pip install dash
import dash_table
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State

import pandas as pd
import plotly
import numpy as np
# import seaborn as sns

import plotly.express as px
from plotly.subplots import make_subplots
import plotly.graph_objects as go
import matplotlib.pyplot as plt
import plotly.figure_factory as ff

import csv
from urllib.request import urlopen
import urllib.request

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from scipy.interpolate import interp1d
import plotly.graph_objects as go


bgcolors = {
    'background': '#CBC3E3',
    'text': '#FFFFFF'
}


external_scripts = [
    'https://www.google-analytics.com/analytics.js',
    {'src': 'https://cdn.polyfill.io/v2/polyfill.min.js'},
    {
        'src': 'https://cdnjs.cloudflare.com/ajax/libs/lodash.js/4.17.10/lodash.core.js',
        'integrity': 'sha256-Qqd/EfdABZUcAxjOkMi8eGEivtdTkh3b65xCZL4qAQA=',
        'crossorigin': 'anonymous'
    }
]


external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']



app = dash.Dash(__name__,
                external_scripts=external_scripts
                ,external_stylesheets=external_stylesheets)


server = app.server


import os, ssl
if (not os.environ.get('PYTHONHTTPSVERIFY', '') and
getattr(ssl, '_create_unverified_context', None)):
    ssl._create_default_https_context = ssl._create_unverified_context


    
    
    
    
    



    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    

url = "https://covidtracking.com/api/v1/us/daily.csv"
df = pd.read_csv(url)


df['year'] = df.date.astype(str).str[:4]
df['month_day'] = df.date.astype(str).str[-4:]
df['day'] = df.date.astype(str).str[-2:]
df['month'] = df.month_day.astype(str).str[:2]
df['date_new'] = df['year'] + "-" + df['month'] + "-" + df['day']

# df.head()


df['date_new'] = df['date_new'].astype('datetime64')
df.dtypes


cases = df[['date_new', 'totalTestResultsIncrease', 'negativeIncrease', 'positiveIncrease', 'deathIncrease', 'hospitalizedIncrease']]




cases['percent_positive'] = cases['positiveIncrease']/cases['totalTestResultsIncrease']
cases['percent_negative'] = cases['negativeIncrease']/cases['totalTestResultsIncrease']
cases['percent_death'] = cases['deathIncrease']/cases['totalTestResultsIncrease']
cases['percent_hospitalized'] = cases['hospitalizedIncrease']/cases['totalTestResultsIncrease']



cases['positive_pct_change'] = cases['percent_positive'].pct_change()
cases['negative_pct_change'] = cases['percent_negative'].pct_change()
cases['total_cases_pct_change'] = cases['totalTestResultsIncrease'].pct_change()
cases['death_pct_change'] = cases['percent_death'].pct_change()
cases['hospitalized_pct_change'] = cases['percent_hospitalized'].pct_change()



cases = cases[cases['date_new'] > '2020-03-20']



percent_positive = list(cases.percent_positive)
percent_negative = list(cases.percent_negative)
percent_death = list(cases.percent_death)
percent_hospitalized = list(cases.percent_hospitalized)

negativeIncrease = list(cases.negativeIncrease)
positiveIncrease = list(cases.positiveIncrease)
deathIncrease = list(cases.deathIncrease)
hospitalizedIncrease = list(cases.hospitalizedIncrease)

totalTestResultsIncrease = list(cases.totalTestResultsIncrease)
total_cases_pct_change = list(cases.total_cases_pct_change)
positive_pct_change = list(cases.positive_pct_change)
negative_pct_change = list(cases.negative_pct_change)
death_pct_change = list(cases.death_pct_change)
hospitalized_pct_change = list(cases.hospitalized_pct_change)
date = list(cases.date_new)





positive_pct_melt = pd.melt(cases, id_vars=['date_new'],value_vars=['positive_pct_change'])
negative_pct_melt = pd.melt(cases, id_vars=['date_new'],value_vars=['negative_pct_change'])
death_pct_melt = pd.melt(cases, id_vars=['date_new'],value_vars=['death_pct_change'])
hospitalized_pct_melt = pd.melt(cases, id_vars=['date_new'],value_vars=['hospitalized_pct_change'])
total_cases_pct_melt = pd.melt(cases, id_vars=['date_new'],value_vars=['total_cases_pct_change'])


cases_melted1 = positive_pct_melt.append(negative_pct_melt,ignore_index=True)
cases_melted2 = cases_melted1.append(death_pct_melt,ignore_index=True)
cases_melted3 = cases_melted2.append(hospitalized_pct_melt,ignore_index=True)
cases_melted = cases_melted3.append(total_cases_pct_melt,ignore_index=True)


fig0 = px.bar(df
             ,x="date_new"
             ,y="totalTestResults"
             ,hover_data=['totalTestResults']
             ,title="<b>Total Covid Tests (Cummulative)</b>")

fig0.update_layout(
    template='plotly_dark'
)


percent_positive = list(cases.percent_positive)
percent_negative = list(cases.percent_negative)
date = list(cases.date_new)

cases_melt = pd.melt(cases, id_vars=['date_new'], value_vars=['negativeIncrease'
                                                              ,'positiveIncrease'
                                                              ,'totalTestResultsIncrease'
                                                             ]
                    )


fig1 = make_subplots(specs=[[{"secondary_y": True}]])

fig1 = px.line(cases_melt, x='date_new', y='value', color='variable')


fig1.add_trace(
    go.Scatter(x=date, y=percent_negative, name="pourcentage_négatif"),
    secondary_y=False,
)

fig1.add_trace(
    go.Scatter(x=date, y=percent_positive, name="pourcentage_positif"),
    secondary_y=False,
)


fig1.update_layout(
    title_text="<b>Cas quotidiens de Covid avec pourcentage du  changements </b>"
    ,template='plotly_dark'
    ,showlegend=False
)



fig1.update_xaxes(title_text="<b>Date</b>")

fig1.update_yaxes(title_text="<b>Comte</b>", secondary_y=False)



fig2 = make_subplots(specs=[[{"secondary_y": True}]])

fig2.add_trace(
    go.Scatter(x=date
               ,y=percent_negative
               ,name="pourcentage_négatif"
               ,marker_color=px.colors.qualitative.Plotly[2]),
    secondary_y=True,
)
fig2.add_trace(
    go.Scatter(x=date
               ,y=percent_positive
               ,name="pourcentage_positif"
               ,marker_color=px.colors.qualitative.D3[3]),
    secondary_y=True,
)


fig2.update_layout(
    title_text="<b> Pourcentage quotidien Pos/Neg  des tests Covid</b>"
)


fig2.update_xaxes(title_text="<b>Date</b>")


fig2.update_yaxes(title_text="<b>Percentage</b>", secondary_y=True)

fig2.update_layout(barmode='stack')


fig2.update_traces(marker_line_width=.01)

fig2.update_layout(
    template='plotly_dark'
    ,legend=dict(
    orientation="h",
    yanchor="bottom",
    y=1.02,
    xanchor="right",
    x=1
))



fig3 = make_subplots(specs=[[{"secondary_y": True}]])

fig3.add_trace(
    go.Bar(x=date
           ,y=negativeIncrease
           ,name="augmentation négative"
           ,marker_color=px.colors.qualitative.Pastel1[3]),
    secondary_y=False,
)
fig3.add_trace(
    go.Bar(x=date
           ,y=positiveIncrease
           ,name="augmentation posetive"),
    secondary_y=False,
)
fig3.add_trace(
    go.Scatter(x=date
               ,y=totalTestResultsIncrease
               ,opacity=.7
               ,name="augmentation des résultats totaux des tests"
               ,mode="markers"
               ,marker_color=px.colors.qualitative.Plotly[3]),
    secondary_y=False,
)


fig3.update_layout(
    title_text="<b>Tests quotidiens Pos/Neg et  tests totaux</b>"
)


fig3.update_xaxes(title_text="<b>Date</b>")


fig3.update_yaxes(title_text="<b>Compte des cas</b>", secondary_y=False)


fig3.update_layout(barmode='stack')


fig3.update_traces(marker_line_width=.01)

fig3.update_layout(
    template='plotly_dark'
    ,legend=dict(
    orientation="h",
    yanchor="bottom",
    y=1.02,
    xanchor="right",
    x=1
))


fig4 = make_subplots(specs=[[{"secondary_y": True}]])

fig4.add_trace(
    go.Scatter(x=date
               ,y=positive_pct_change
               ,name="cahngement ponctuel positive"
               ,mode="lines+markers"
               ,marker_color=px.colors.qualitative.T10[2]),
    secondary_y=False,
)
fig4.add_trace(
    go.Scatter(x=date
               ,y=negative_pct_change
               ,name="cahngement ponctuel negative"
               ,mode="markers"
               ,marker_color=px.colors.qualitative.Plotly[5]),
    secondary_y=True,
)
fig4.add_trace(
    go.Scatter(x=date
               ,y=total_cases_pct_change
               ,name="changement ponctuel du total des cas "
               ,mode="lines+markers"
               ,marker_color=px.colors.qualitative.Plotly[3]),
    secondary_y=False,
)



fig4.update_layout(
    title_text="<b>Variations quotidiennes en pourcentage des tests positifs Covid et des tests totaux</b>"
)


fig4.update_xaxes(title_text="<b>Date</b>")

fig4.update_yaxes(title_text="<b>Changement du pourcentage</b>", secondary_y=False)

fig4.update_layout(barmode='stack')


fig4.update_traces(marker_line_width=.01)


fig4.update_layout(
    template='plotly_dark'
    ,legend=dict(
    orientation="h",
    yanchor="bottom",
    y=1.02,
    xanchor="right",
    x=1
))



fig5 = make_subplots(specs=[[{"secondary_y": True}]])

fill_colors = ['none', 'tozeroy', 'tozerox', 'tonexty', 'tonextx', 'toself', 'tonext']


fig5.add_trace(
    go.Scatter(x=date
           ,y=negativeIncrease
           ,name="augmentation négative"
           ,line=dict(width=0.5, color='rgb(111, 231, 219)')
           ,stackgroup='one'
            ),
    secondary_y=False,
)

fig5.add_trace(
    go.Scatter(x=date
           ,y=positiveIncrease
           ,fill=fill_colors[1]
           ,mode="markers+lines"
           ,name="augmentation posetive"),
    secondary_y=False,
)

fig5.add_trace(
    go.Scatter(x=date
               ,y=totalTestResultsIncrease
               ,opacity=.7
               ,name="augmentation des résultats totaux des tests"
               ,line=dict(width=0.5, color='rgb(131, 90, 241)')
               ,stackgroup='one'),
    secondary_y=False,
)


fig5.update_layout(
    title_text="<b>Tests quotidiens Pos/Neg et totaux des tests</b>"
)


fig5.update_xaxes(title_text="<b>Date</b>")

fig5.update_yaxes(title_text="<b>Comte des cas</b>", secondary_y=False)


fig5.update_layout(barmode='stack')


fig5.update_traces(marker_line_width=.01)

fig5.update_layout(
    template='plotly_dark'
    ,legend=dict(
    orientation="h",
    yanchor="bottom",
    y=1.02,
    xanchor="right",
    x=1
))






fig6 = make_subplots(specs=[[{"secondary_y": True}]])

fig6.add_trace(
    go.Scatter(x=date
               ,y=positive_pct_change
               ,name="positive_pct_change"
               ,marker_color=px.colors.qualitative.T10[2]
               ,yaxis="y1")
#
)
fig6.add_trace(
    go.Scatter(x=date
               ,y=negative_pct_change
               ,name="negative_pct_change"
               ,marker_color=px.colors.qualitative.T10[4]
               ,yaxis="y2")

)
fig6.add_trace(
    go.Scatter(x=date
               ,y=total_cases_pct_change
               ,name="total_cases_pct_change"
               ,marker_color=px.colors.qualitative.Plotly[3]
               ,yaxis="y3")

)


fig6.update_layout(

    yaxis1=dict(
        title="positive_pct_change",
        titlefont=dict(
            color="#663399"
        ),
        tickfont=dict(
            color="#663399"
        )
    ),
    yaxis2=dict(
        title="negative_pct_change",
        titlefont=dict(
            color="#006600"
        ),
        tickfont=dict(
            color="#006600"
        ),
        anchor="free",
        overlaying="y",
        side="right",
        position=1
    ),
    yaxis3=dict(
        title="total_cases_pct_change",
        titlefont=dict(
            color="#d62728"
        ),
        tickfont=dict(
            color="#d62728"
        ),
        anchor="x",
        overlaying="y",
        side="right"
    )
)


fig6.update_layout(
    title_text="<b>Variations quotidiennes, en pourcentage, des tests Covid Pos/Neg et des tests totaux</b>"
)


fig6.update_xaxes(title_text="<b>Date</b>")


fig6.update_yaxes(title_text="<b>Percent Change</b>", secondary_y=False)


fig6.update_layout(barmode='stack')

fig6.update_traces(marker_line_width=.01)


fig6.update_layout(legend=dict(
    orientation="h",
    yanchor="bottom",
    y=1.02,
    xanchor="right",
    x=1
))

fig6.update_layout(
    # width=1200
    template='plotly_dark'
)




fig7 = make_subplots(specs=[[{"secondary_y": True}]])

fig7.add_trace(
    go.Scatter(x=date
               ,y=death_pct_change
               ,name="death_pct_change"
               ,marker_color=px.colors.qualitative.T10[0]),
    secondary_y=False,
)
fig7.add_trace(
    go.Scatter(x=date
               ,y=hospitalized_pct_change
               ,name="hospitalized_pct_change"
               ,marker_color=px.colors.qualitative.T10[6]),
    secondary_y=False,
)


fig7.update_layout(
    title_text="<b>Changements quotidiens en pourcentage de Covid Décès/Hospitalisation</b>"
)


fig7.update_xaxes(title_text="<b>Date</b>")

# Set y-axes titles
fig7.update_yaxes(title_text="<b>Percent Change</b>", secondary_y=False)

# Change the bar mode
fig7.update_layout(barmode='stack')

# Customize aspect
fig7.update_traces(
#                   marker_color='rgb(158,202,225)'
#                   , marker_line_color='rgb(8,48,107)',
                  marker_line_width=.1)
#                   ,opacity=0.6)

#update legend
fig7.update_layout(legend=dict(
    orientation="h",
    yanchor="bottom",
    y=1.02,
    xanchor="right",
    x=1,
))

fig7.update_layout(
    # width=1200
    template='plotly_dark'
)
# fig7.show()

fig8 = px.scatter(cases
                 ,x="date_new"
                 ,y="positive_pct_change"
                 ,trendline="lowess"
                 ,color_continuous_scale=px.colors.sequential.Inferno
                )
fig8.update_layout(
    height=800
    ,template='plotly_dark')

fig8.add_trace(
    go.Scatter(x=date
               ,y=negative_pct_change
               ,name="negative_pct_change"
               ,mode="lines+markers"
               ,marker_color=px.colors.qualitative.T10[1]
              )
#     secondary_y=False,
),
fig8.add_trace(
    go.Scatter(x=date
               ,y=death_pct_change
               ,name="death_pct_change"
               ,mode="lines+markers"
               ,marker_color=px.colors.qualitative.T10[2]
              )
#     secondary_y=False,
),
fig8.add_trace(
    go.Scatter(x=date
               ,y=hospitalized_pct_change
               ,name="hospitalized_pct_change"
               ,mode="lines+markers"
               ,marker_color=px.colors.qualitative.T10[3]
              )
#     secondary_y=False,
),
fig8.add_trace(
    go.Scatter(x=date
               ,y=total_cases_pct_change
               ,name="total_cases_pct_change"
               ,mode="lines+markers"
               ,marker_color=px.colors.qualitative.T10[4]
              )
#     secondary_y=False,
)
# fig8.show()


fig9 = px.scatter(cases, x="date_new", y="positive_pct_change", trendline="lowess"
                  , title="changement_pct_positif"
#                   , color_continuous_scale="icefire"
                  , color="positive_pct_change", color_continuous_scale=px.colors.sequential.Inferno
                  , marginal_y="histogram", marginal_x="violin")
fig9.update_layout(
    height=400
    ,template='plotly_dark')
# fig9.show()

fig10 = px.scatter(cases, x="date_new", y="negative_pct_change", color="negative_pct_change"
                  , trendline="lowess", title="variation_pct_négative"
                  , color_continuous_scale=px.colors.sequential.Inferno
                  , marginal_y="histogram", marginal_x="violin")
fig10.update_layout(
    height=400
    ,template='plotly_dark')
# fig10.show()

fig11 = px.scatter(cases, x="date_new", y="death_pct_change", color="death_pct_change"
                  , trendline="lowess", title="changement_pct_decces"
                  , color_continuous_scale=px.colors.sequential.Inferno
                  , marginal_y="histogram", marginal_x="violin")
fig11.update_layout(
    height=400
    ,template='plotly_dark')
# fig11.show()

fig12 = px.scatter(cases, x="date_new", y="hospitalized_pct_change", color="hospitalized_pct_change"
                  , trendline="lowess", title="hospitalisé_pct_changement"
                  , color_continuous_scale=px.colors.sequential.Inferno
                  , marginal_y="histogram", marginal_x="violin")
fig12.update_layout(
    height=400
    ,template='plotly_dark')
# fig12.show()

fig13 = px.scatter(cases, x="date_new", y="total_cases_pct_change", color="total_cases_pct_change"
                  , trendline="lowess", title="total_cases_pct_changement"
                  , color_continuous_scale=px.colors.sequential.Inferno
                  , marginal_y="histogram", marginal_x="violin")
fig13.update_layout(
    height=400
    ,template='plotly_dark')
# fig13.show()

#add traces
trace1 = fig9['data'][0]
trace2 = fig10['data'][0]
trace3 = fig11['data'][0]
trace4 = fig12['data'][0]
trace5 = fig13['data'][0]

fig14 = make_subplots(rows=3
                    ,cols=2
                    ,shared_xaxes=False
                    ,row_heights=[9., 9., 9.]
                    ,column_widths=[.1, .1]
                    ,shared_yaxes=False
                    ,vertical_spacing=0.10
                    ,subplot_titles=['<b>positive_pct_change</b>'
                                     ,'<b>negative_pct_change</b>'
                                     ,'<b>death_pct_change</b>'
                                     ,'<b>hospitalized_pct_change</b>'
                                     ,'<b>total_cases_pct_change</b>'
                                    ]
                    ,x_title="<b>date</b>"
                    ,y_title="<b>percent_change</b>"
                   )

fig14.add_trace(trace1, row=1, col=1)
fig14.add_trace(trace2, row=1, col=2)
fig14.add_trace(trace3, row=2, col=1)
fig14.add_trace(trace4, row=2, col=2)
fig14.add_trace(trace5, row=3, col=1)

fig14['layout'].update(height=800
# , width=1200
        , title='<b>Tendances des résultats du test Covid</b>'
        , template='plotly_dark')
# fig14.show()


# cases_melted.head()
cases_melted.variable.value_counts()
values_list = list(cases_melted.value)

fig15 = px.scatter(cases_melted, x="date_new", y="value"
                 , color="variable", facet_col="variable"
                 , trendline="lowess", trendline_color_override="white"
                 , color_continuous_scale=px.colors.sequential.Inferno
                 , marginal_y="bar", marginal_x="box"
                 , labels = ['test','test','test','test','test'])

fig15['layout'].update(height=800
# , width=1200
        , title='<b>Tendances des résultats du test Covid</b>'
        , template='plotly_dark')
fig15.for_each_annotation(lambda a: a.update(text=a.text.split("=")[-1]))
# fig15.show()


#make variables for subplots
percent_positive = list(cases.percent_positive)
percent_negative = list(cases.percent_negative)
negativeIncrease = list(cases.negativeIncrease)
positiveIncrease = list(cases.positiveIncrease)
totalTestResultsIncrease = list(cases.totalTestResultsIncrease)
total_cases_pct_change = list(cases.total_cases_pct_change)
positive_pct_change = list(cases.positive_pct_change)
date = list(cases.date_new)

# Create fig16ure with secondary y-axis
fig16 = make_subplots(specs=[[{"secondary_y": True}]])

# Add traces
fig16.add_trace(
    go.Bar(x=date
           ,y=negativeIncrease
           ,name="negativeIncrease"
           ,marker_color=px.colors.qualitative.Pastel1[3]),
    secondary_y=False,
)
fig16.add_trace(
    go.Bar(x=date, y=positiveIncrease, name="positiveIncrease"),
    secondary_y=False,
)
fig16.add_trace(
    go.Scatter(x=date
               ,y=totalTestResultsIncrease
               ,opacity=.7
               ,name="totalTestResultsIncrease"
               ,mode="markers"
               ,marker_color=px.colors.qualitative.Plotly[3]),
    secondary_y=False,
)
fig16.add_trace(
    go.Scatter(x=date
               ,y=percent_negative
               ,name="percent_negative"
               ,marker_color=px.colors.qualitative.Plotly[2]),
    secondary_y=True,
)
fig16.add_trace(
    go.Scatter(x=date
               ,y=percent_positive
               ,name="percent_positive"
               ,marker_color=px.colors.qualitative.D3[3]),
    secondary_y=True,
)
fig16.add_trace(
    go.Scatter(x=date
               ,y=positive_pct_change
               ,name="positive_pct_change"
               ,marker_color=px.colors.qualitative.T10[2]),
    secondary_y=True,
)
fig16.add_trace(
    go.Scatter(x=date
               ,y=negative_pct_change
               ,name="negative_pct_change"
               ,marker_color=px.colors.qualitative.Plotly[5]),
    secondary_y=True,
)
fig16.add_trace(
    go.Scatter(x=date
               ,y=total_cases_pct_change
               ,name="total_cases_pct_change"
               ,marker_color=px.colors.qualitative.Plotly[3]),
    secondary_y=True,
)


# Add fig16ure title
fig16.update_layout(
    title_text="<b>Les cas quotidiens de Covid</b>"
    ,height=800
    # ,width=1200
)

# Set x-axis title
fig16.update_xaxes(title_text="<b>Date</b>")

# Set y-axes titles
fig16.update_yaxes(title_text="<b>Count Cases</b>", secondary_y=False)
fig16.update_yaxes(title_text="<b>% Change</b>", secondary_y=True)

# Change the bar mode
fig16.update_layout(barmode='stack')

# Customize aspect
fig16.update_traces(marker_line_width=.01)

#update legend
fig16.update_layout(
    template='plotly_dark'
    ,legend=dict(
    orientation="h",
    yanchor="bottom",
    y=1.02,
    xanchor="right",
    x=1
))
# fig16.show()


#create a day of week column
s = pd.date_range(min(df.date_new),max(df.date_new), freq='D').to_series()
s = s.dt.dayofweek.tolist()
df['day_of_week'] = s

def day_of_week(df):
    if df['day_of_week'] == 0:
        return "Tuesday"
    elif df['day_of_week'] == 1:
        return "Monday"
    elif df['day_of_week'] == 2:
        return "Sunday"
    elif df['day_of_week'] == 3:
        return "Saturday"
    elif df['day_of_week'] == 4:
        return "Friday"
    elif df['day_of_week'] == 5:
        return "Thursday"
    elif df['day_of_week'] == 6:
        return "Wednesday"
    else:
        return ""

df['dayofweek'] = df.apply(day_of_week, axis=1)
# df.head(30)


#create min and max variables
y_min = min(df.totalTestResultsIncrease)
y_max = max(df.totalTestResultsIncrease)
# x_min = min(df.index)
# x_max = max(df.index)
x_min = min(df.month)
x_max = max(df.month)
x_range = [x_min,x_max]
y_range = [y_min,y_max]

# print('y_min:',y_min)
# print('y_max:',y_max)
# print('x_min:',x_min)
# print('x_max:',x_max)
# print('x_range:',x_range)
# print('y_range:',y_range)


#create total pos/neg/total variables by day
total_pos_increase_grp_day = df.groupby(['dayofweek'])['positiveIncrease'].sum()
avg_total_pos_increase_grp_day = df.groupby(['dayofweek'])['positiveIncrease'].mean()

total_neg_increase_grp_day = df.groupby(['dayofweek'])['negativeIncrease'].sum()
avg_total_neg_increase_grp_day = df.groupby(['dayofweek'])['negativeIncrease'].mean()

total_increase_grp_day = df.groupby(['dayofweek'])['totalTestResultsIncrease'].sum()
avg_total_increase_grp_day = df.groupby(['dayofweek'])['totalTestResultsIncrease'].mean()

avg_total_per_week = avg_total_increase_grp_day/7
avg_pos_per_week = avg_total_pos_increase_grp_day/7
avg_neg_per_week = avg_total_neg_increase_grp_day/7


# print('total_pos_increase_grp_day:',total_pos_increase_grp_day)
# print("")
# print('total_neg_increase_grp_day:',total_neg_increase_grp_day)
# print("")
# print('total_increase_grp_day:',total_increase_grp_day)
# print("")
# print("")
# print('avg_total_pos_increase_grp_day:',avg_total_pos_increase_grp_day)
# print("")
# print('avg_total_neg_increase_grp_day:',avg_total_neg_increase_grp_day)
# print("")
# print('avg_total_increase_grp_day:',avg_total_increase_grp_day)
# print("")
# print("")
# print('avg_pos_per_week:',avg_pos_per_week)
# print("")
# print('avg_neg_per_week:',avg_neg_per_week)
# print("")
# print('avg_total_per_week:',avg_total_per_week)

#put totals in a list for labeling later on
total_totals = list(total_increase_grp_day)
pos_totals = list(total_pos_increase_grp_day)
neg_totals = list(total_neg_increase_grp_day)

# print('total_totals:', total_totals)
# print('pos_totals:', pos_totals)
# print('neg_totals:', neg_totals)

#make day list
x_labels = ['Monday','Tuesday','Wednesday','Thursday', 'Friday', 'Saturday', 'Sunday']
# print('x_labels:', x_labels)


#plots by day
fig17 = px.bar(df
             ,x='dayofweek'
             ,y='positiveIncrease'
             ,text='positiveIncrease'
             ,color='dayofweek'
             ,height=500
             ,hover_data=['negativeIncrease', 'positiveIncrease', 'totalTestResultsIncrease']
             ,hover_name="positiveIncrease")
fig17.update_traces(texttemplate='%{text:.2s}'
                  ,textposition='outside')
fig17.update_layout(uniformtext_minsize=8
                 ,uniformtext_mode='hide'
                 ,title_text="<b>Covid Tests Outcome</b>"
                 ,template='plotly_dark'
                 # ,xaxis={'categoryorder':'array', 'categoryarray':['Monday','Tuesday','Wednesday','Thursday', 'Friday', 'Saturday', 'Sunday']}
                 )

# Set x-axis title
fig17.update_xaxes(title_text="<b>Date</b>")

fig17.add_shape( # add a horizontal "target" line
    type="line", line_color="salmon", line_width=3, opacity=1, line_dash="dot",
    x0=0, x1=1, xref="paper", y0=avg_total_increase_grp_day, y1=avg_total_increase_grp_day, yref="y"
)

fig17.add_annotation( # add a text callout with arrow
    text="Lowest", x="Friday", y=500000, arrowhead=1, showarrow=True
)

total_labels = [{"x": x, "y": pos_totals*1.3, "text": str(pos_totals), "showarrow": False} for x, pos_totals in zip(x_labels, pos_totals)]

fig17.update_layout(uniformtext_minsize=8
                 ,uniformtext_mode='hide'
                 # ,width=1200
                 ,title_text="<b>Total des tests Covid regroupés par jour</b>"
                 ,template='plotly_dark'
                 ,xaxis={'categoryorder':'array', 'categoryarray':['Monday','Tuesday','Wednesday','Thursday', 'Friday', 'Saturday', 'Sunday']}
                 # ,annotations=total_labels
                 )
# fig17.show()



fig18 = px.bar(df
             ,x='dayofweek'
             ,y='negativeIncrease'
             ,text='negativeIncrease'
             ,color='dayofweek'
             ,height=500
             ,hover_data=['negativeIncrease', 'positiveIncrease', 'totalTestResultsIncrease']
             ,hover_name="negativeIncrease")
fig18.update_traces(texttemplate='%{text:.2s}'
                  ,textposition='outside')
fig18.update_layout(uniformtext_minsize=8
                 ,uniformtext_mode='hide'
                 ,template='plotly_dark'
                 ,title_text="<b>Tests de Neagtive Covid groupés par jour</b>"
                 ,xaxis={'categoryorder':'array', 'categoryarray':['Monday','Tuesday','Wednesday','Thursday', 'Friday', 'Saturday', 'Sunday']})

# Set x-axis title
fig18.update_xaxes(title_text="<b>Date</b>")

fig18.add_shape( # add a horizontal "target" line
    type="line", line_color="salmon", line_width=3, opacity=1, line_dash="dot",
    x0=0, x1=1, xref="paper", y0=avg_total_increase_grp_day, y1=avg_total_increase_grp_day, yref="y"
)

fig18.add_annotation( # add a text callout with arrow
    text="Highest", x="Tuesday", y=6700000, arrowhead=1, showarrow=True
)

fig18.add_annotation( # add a text callout with arrow
    text="Lowest", x="Friday", y=6000000, arrowhead=1, showarrow=True
)

total_labels = [{"x": x, "y": neg_totals*1.25, "text": str(neg_totals), "showarrow": False} for x, neg_totals in zip(x_labels, neg_totals)]

fig18.update_layout(uniformtext_minsize=8
                 ,uniformtext_mode='hide'
                 # ,width=1200
                 ,title_text="<b>Total des tests Covid regroupés par jour</b>"
                 ,template='plotly_dark'
                 ,xaxis={'categoryorder':'array', 'categoryarray':['Monday','Tuesday','Wednesday','Thursday', 'Friday', 'Saturday', 'Sunday']}
                 # ,annotations=total_labels
                 )
# fig18.show()


fig19 = px.bar(df
             ,x='dayofweek'
             ,y='totalTestResultsIncrease'
             ,text='totalTestResultsIncrease'
             ,color='dayofweek'
             ,height=500
             ,hover_data=['negativeIncrease', 'positiveIncrease', 'totalTestResultsIncrease']
             ,hover_name="totalTestResultsIncrease")
fig19.update_traces(texttemplate='%{text:.2s}'
                  ,textposition='outside')

# Set x-axis title
fig19.update_xaxes(title_text="<b>Date</b>")

fig19.add_shape( # add a horizontal "target" line
    type="line", line_color="salmon", line_width=3, opacity=1, line_dash="dot",
    x0=0, x1=1, xref="paper", y0=avg_total_increase_grp_day, y1=avg_total_increase_grp_day, yref="y"
)

fig19.add_annotation( # add a text callout with arrow
    text="Highest", x="Tuesday", y=7400000, arrowhead=1, showarrow=True
)

fig19.add_annotation( # add a text callout with arrow
    text="Lowest", x="Friday", y=6600000, arrowhead=1, showarrow=True
)

total_labels = [{"x": x, "y": total_totals*.95, "text": str(total_totals), "showarrow": True} for x, total_totals in zip(x_labels, total_totals)]

fig19.update_layout(uniformtext_minsize=8
                 ,uniformtext_mode='hide'
                 ,title_text="<b>Total des tests Covid regroupés par jour</b>"
                 ,template='plotly_dark'
                 # ,width=1200
                 ,xaxis={'categoryorder':'array', 'categoryarray':['Monday','Tuesday','Wednesday','Thursday', 'Friday', 'Saturday', 'Sunday']}
                 # ,annotations=total_labels
                 )
# fig19.show()


#deaths
fig20 = px.bar(df
             ,x='dayofweek'
             ,y='deathIncrease'
             ,text='deathIncrease'
             ,color='dayofweek'
             ,height=500
             ,hover_data=['negativeIncrease', 'positiveIncrease', 'totalTestResultsIncrease','deathIncrease']
             ,hover_name="deathIncrease")
fig20.update_traces(texttemplate='%{text:.2s}'
                  ,textposition='outside')
fig20.update_layout(uniformtext_minsize=8
                 ,uniformtext_mode='hide'
                 # ,width=1200
                 ,title_text="<b>Tests Covid de décès regroupés par jour</b>"
                 ,template='plotly_dark'
                 ,xaxis={'categoryorder':'array', 'categoryarray':['Monday','Tuesday','Wednesday','Thursday', 'Friday', 'Saturday', 'Sunday']})

# Set x-axis title
fig20.update_xaxes(title_text="<b>Date</b>")

fig20.add_shape( # add a horizontal "target" line
    type="line", line_color="salmon", line_width=3, opacity=1, line_dash="dot",
    x0=0, x1=1, xref="paper", y0=avg_total_increase_grp_day, y1=avg_total_increase_grp_day, yref="y"
)

fig20.add_annotation( # add a text callout with arrow
    text="Highest", x="Monday", y=24000, arrowhead=1, showarrow=True
)

fig20.add_annotation( # add a text callout with arrow
    text="Lowest", x="Friday", y=12000, arrowhead=1, showarrow=True
)

fig20.update_layout(uniformtext_minsize=8
                 ,uniformtext_mode='hide'
                 # ,width=1200
                 ,title_text="<b>Total des décès Covid regroupés par jour</b>"
                 ,template='plotly_dark'
                 ,xaxis={'categoryorder':'array', 'categoryarray':['Monday','Tuesday','Wednesday','Thursday', 'Friday', 'Saturday', 'Sunday']})
#                  ,annotations=total_labels)
# fig20.show()



fig21 = px.bar(df
             ,x='dayofweek'
             ,y='hospitalizedIncrease'
             ,text='hospitalizedIncrease'
             ,color='dayofweek'
             ,height=500
             ,hover_data=['negativeIncrease', 'positiveIncrease', 'totalTestResultsIncrease','deathIncrease','hospitalizedIncrease']
             ,hover_name="hospitalizedIncrease")
fig21.update_traces(texttemplate='%{text:.2s}'
                  ,textposition='outside')
fig21.update_layout(uniformtext_minsize=8
                 ,uniformtext_mode='hide'
                 ,title_text="<b>Tests Covid hospitalisés regroupés par jour</b>"
                 ,template='plotly_dark'
                 # ,width=1200
                 ,xaxis={'categoryorder':'array', 'categoryarray':['Monday','Tuesday','Wednesday','Thursday', 'Friday', 'Saturday', 'Sunday']})

# Set x-axis title
fig21.update_xaxes(title_text="<b>Date</b>")

fig21.add_shape( # add a horizontal "target" line
    type="line", line_color="salmon", line_width=3, opacity=1, line_dash="dot",
    x0=0, x1=1, xref="paper", y0=avg_total_increase_grp_day, y1=avg_total_increase_grp_day, yref="y"
)

fig21.add_annotation( # add a text callout with arrow
    text="Highest", x="Tuesday", y=55000, arrowhead=1, showarrow=True
)

fig21.add_annotation( # add a text callout with arrow
    text="Lowest", x="Thursday", y=25000, arrowhead=1, showarrow=True
)

fig21.update_layout(uniformtext_minsize=8
                 ,uniformtext_mode='hide'
                 ,title_text="<b>Décès totaux de Covid hospitalisés regroupés par jour</b>"
                 ,template='plotly_dark'
                 ,xaxis={'categoryorder':'array', 'categoryarray':['Monday','Tuesday','Wednesday','Thursday', 'Friday', 'Saturday', 'Sunday']})
# fig21.show()


#map day of week column to cases_melted dataframe
mapping = df[['date_new', 'dayofweek']]
# mapping
cases_melted = pd.merge(cases_melted, mapping, how='left', on=['date_new', 'date_new'])
# print(cases_melted)
# print(df.dayofweek)


fig22 = px.scatter(cases_melted, x="date_new", y="value"
                 , color="variable", facet_row="variable", facet_col="dayofweek"
                 , trendline="lowess", trendline_color_override="white"
                 , color_continuous_scale=px.colors.sequential.Inferno
                 , marginal_y="bar", marginal_x="box")

fig22['layout'].update(height=1000
                # , width=1200
                , title='<b>Tendances des résultats du test Covid</b>'
                , template='plotly_dark')
fig22.for_each_annotation(lambda a: a.update(text=a.text.split("=")[-1]))
# fig22.show()

fig23 = px.bar(cases_melted, x="date_new", y="value"
                 , color="variable", facet_row="variable", facet_col="dayofweek"
                 , color_continuous_scale=px.colors.sequential.Inferno)

fig23['layout'].update(height=1000
                # , width=1200
                , title='<b>Tendances des résultats du test Covid</b>'
                , template='plotly_dark')
fig23.for_each_annotation(lambda a: a.update(text=a.text.split("=")[-1]))
# fig23.show()


# cases_melted = cases_melted.drop(['dayofweek_x', 'dayofweek_y'], axis=1)
# cases_melted.style.background_gradient(cmap='Blues')


cases_melted['rank_value'] = cases_melted['value'].rank(method="max")
# print(cases_melted.head(30).sort_values(by='rank_value'))
# print(cases_melted.tail(30).sort_values(by='rank_value'))


#sum percent changes by day
#sundays have the highest positive percent changes
#tuesdays have the highest negative percent changes
cases_day = cases_melted[['dayofweek','value']]
cases_day = cases_day.groupby('dayofweek').sum().reset_index()
# cases_day.head(10).style.background_gradient(cmap='inferno')

fig24 = px.bar(cases_day, x="dayofweek", y="value"
                 , color="dayofweek"
                 , text="value"
                 , color_continuous_scale=px.colors.sequential.Inferno
                 , template="plotly_dark")

fig24['layout'].update(height=800
                     # , width=1200
                     , title='<b>Somme des changements de pourcentage quotidiens du test Covid par jour de la semaine</b>'
                     , template='plotly_dark'
                     , yaxis_title="Sum of % Change"
                     , xaxis_title="Day of Week"
                     , legend_title="Day of Week"
                     , xaxis={'categoryorder':'array', 'categoryarray':['Monday','Tuesday','Wednesday','Thursday', 'Friday', 'Saturday', 'Sunday']}
                    )
# fig24.show()


fig40 = px.bar(cases_melted
                 , x="dayofweek", y="value"
                 , color="variable"
                 , hover_name="value"
                 , range_y=[-2,2]
                 , animation_group="dayofweek"
                 , animation_frame=cases_melted.index)


fig40['layout'].update(height=500
                # , width=1200
                , title='<b>Tendances des résultats du test Covid</b>'
                , template='plotly_dark')
fig40.for_each_annotation(lambda a: a.update(text=a.text.split("=")[-1]))
# fig40.show()


fig25 = px.bar(cases_melted, x="date_new", y="value"
                 , color="variable"
                 , color_continuous_scale=px.colors.sequential.Inferno)

fig25['layout'].update(height=500
                     # , width=1200
                     , title='<b>Somme des variations quotidiennes en pourcentage du test Covid par résultat</b>'
                     , yaxis_title="Sum of Daily % Changes"
                     , xaxis_title="Date"
                     , legend_title="Sum of Daily % Changes"
                     , template='plotly_dark')
fig25.for_each_annotation(lambda a: a.update(text=a.text.split("=")[-1]))
# fig25.show()

fig26 = px.bar(cases_melted, x="date_new", y="value"
                 , color="dayofweek"
                 , color_continuous_scale=px.colors.sequential.Inferno)


fig26['layout'].update(height=500
                     # , width=1200
                     , title='<b>Somme des variations quotidiennes en pourcentage du test Covid par résultat</b>'
                     , yaxis_title="Sum of Daily % Changes"
                     , xaxis_title="Date"
                     , legend_title="Day of Week"
                     , template='plotly_dark')
fig26.for_each_annotation(lambda a: a.update(text=a.text.split("=")[-1]))
# fig26.show()

fig27 = px.bar(cases_melted, x="date_new", y="value"
                 , color="dayofweek", facet_col="dayofweek"
                 , color_continuous_scale=px.colors.sequential.Inferno)
#                  , facet_col_wrap=3)
#                  , size=cases_melted.index)

fig27['layout'].update(height=500
                     # , width=1200
                     , title='<b>Tendances des résultats des tests Covid regroupés par jour de la semaine</b>'
                     , template='plotly_dark'
                     , yaxis_title="Sum of Daily % Changes"
                     , xaxis_title="Day of Week"
                     , legend_title="Sum of Daily % Changes")
fig27.for_each_annotation(lambda a: a.update(text=a.text.split("=")[-1]))
# fig27.show()

fig28 = px.bar(cases_melted, x="dayofweek", y="value"
                 , color="value"
                 , color_continuous_scale=px.colors.sequential.Inferno)
#                  , facet_col_wrap=3)
#                  , size=cases_melted.index)

fig28['layout'].update(height=500
                     # , width=1200
                     , title='<b>Tendances des résultats des tests Covid regroupés par jour de la semaine</b>'
                     , template='plotly_dark'
                     , yaxis_title="Sum of Daily % Changes"
                     , xaxis_title="Day of Week"
                     , legend_title="Sum of Daily % Changes")
fig28.for_each_annotation(lambda a: a.update(text=a.text.split("=")[-1]))
# fig28.show()

fig29 = px.bar(cases_melted, x="variable", y="value"
                 , color="dayofweek"
                 , color_continuous_scale=px.colors.sequential.Inferno)
#                  , facet_col_wrap=3)
#                  , size=cases_melted.index)

fig29['layout'].update(height=500
                     # , width=1200
                     , title='<b>Tendances des résultats des tests Covid regroupés par jour de la semaine</b>'
                     , template='plotly_dark'
                     , yaxis_title="Sum of Daily % Changes"
                     , xaxis_title="Outcome"
                     , legend_title="Sum of Daily % Changes")
fig29.for_each_annotation(lambda a: a.update(text=a.text.split("=")[-1]))
# fig29.show()

#create rounded columns and df
cases['total_rounded'] = cases.totalTestResultsIncrease.round(-4)
cases['percent_positive_rounded'] = cases.percent_positive.round(2)
cases['percent_negative_rounded'] = cases.percent_negative.round(2)
cases['percent_death_rounded'] = cases.percent_death.round(2)
cases['percent_hospitalized_rounded'] = cases.percent_hospitalized.round(2)

cases_rounded = cases[['date_new','total_rounded','percent_positive_rounded'
                      ,'percent_negative_rounded','percent_death_rounded'
                      ,'percent_hospitalized_rounded']]

#add 5 day moving average columns
cases_rounded['percent_pos_5d_avg'] = cases_rounded.rolling(window=5)['percent_positive_rounded'].mean()
cases_rounded['total_rounded_5d_avg'] = cases_rounded.rolling(window=5)['total_rounded'].mean()
cases_rounded['percent_neg_5d_avg'] = cases_rounded.rolling(window=5)['percent_negative_rounded'].mean()
cases_rounded['percent_death_5d_avg'] = cases_rounded.rolling(window=5)['percent_death_rounded'].mean()
cases_rounded['percent_hospitalized_5d_avg'] = cases_rounded.rolling(window=5)['percent_hospitalized_rounded'].mean()

#create slope cols
cases_rounded['percent_pos_5d_avg_slope'] = cases_rounded.percent_pos_5d_avg.diff().fillna(0)
cases_rounded['total_rounded_5d_avg_slope'] = cases_rounded.total_rounded_5d_avg.diff().fillna(0)
cases_rounded['percent_neg_5d_avg_slope'] = cases_rounded.percent_neg_5d_avg.diff().fillna(0)
cases_rounded['percent_death_5d_avg_slope'] = cases_rounded.percent_death_5d_avg.diff().fillna(0)
cases_rounded['percent_hospitalized_5d_avg_slope'] = cases_rounded.percent_hospitalized_5d_avg.diff().fillna(0)

#convert lists
#rounded lists
total_rounded = list(cases_rounded.total_rounded)
percent_positive_rounded = list(cases_rounded.percent_positive_rounded)
percent_negative_rounded = list(cases_rounded.percent_negative_rounded)
percent_death_rounded = list(cases_rounded.percent_death_rounded)
percent_hospitalized_rounded = list(cases_rounded.percent_hospitalized_rounded)

#5d avg lists
percent_pos_5d_avg = list(cases_rounded.percent_pos_5d_avg)
total_rounded_5d_avg = list(cases_rounded.total_rounded_5d_avg)
percent_neg_5d_avg = list(cases_rounded.percent_neg_5d_avg)
percent_death_5d_avg = list(cases_rounded.percent_death_5d_avg)
percent_hospitalized_5d_avg = list(cases_rounded.percent_hospitalized_5d_avg)

#slope lists
percent_pos_5d_avg_slope = list(cases_rounded.percent_pos_5d_avg_slope)
total_rounded_5d_avg_slope = list(cases_rounded.total_rounded_5d_avg_slope)
percent_neg_5d_avg_slope = list(cases_rounded.percent_neg_5d_avg_slope)
percent_death_5d_avg_slope = list(cases_rounded.percent_death_5d_avg_slope)
percent_hospitalized_5d_avg_slope = list(cases_rounded.percent_hospitalized_5d_avg_slope)


# Create fig30ure with secondary y-axis
fig30 = make_subplots(specs=[[{"secondary_y": True}]])

# Add traces
fig30.add_trace(
    go.Scatter(x=date
           ,y=total_rounded
           ,name="total_rounded"
           ,mode="lines+markers"
#            ,opacity=.5
           ,marker_color=px.colors.qualitative.Plotly[3]),
    secondary_y=False,
)
fig30.add_trace(
    go.Scatter(x=date
           , y=percent_positive_rounded
#            , opacity=.5
           , mode="lines+markers"
           , marker_color=px.colors.qualitative.Plotly[5]
           , name="percent_positive_rounded"),
    secondary_y=True,
)

#moving averages
fig30.add_trace(
    go.Scatter(x=date
           , y=total_rounded_5d_avg
           , opacity=.6
           , mode="lines"
           , marker_color=px.colors.qualitative.Plotly[1]
           , name="total_rounded_5d_avg"),
    secondary_y=False,
)
fig30.add_trace(
    go.Scatter(x=date
           , y=percent_pos_5d_avg
           , opacity=.6
           , mode="lines"
           , marker_color=px.colors.qualitative.Plotly[1]
           , name="percent_pos_5d_avg"),
    secondary_y=True,
)

#slopes
fig30.add_trace(
    go.Scatter(x=date
           , y=total_rounded_5d_avg_slope
           , opacity=.7
           , mode="lines"
           , marker_color=px.colors.qualitative.Plotly[3]
           , name="total_rounded_5d_avg_slope"),
    secondary_y=False,
)
fig30.add_trace(
    go.Scatter(x=date
           , y=percent_pos_5d_avg_slope
           , opacity=.7
           , mode="lines"
           , marker_color=px.colors.qualitative.Plotly[5]
           , name="percent_pos_5d_avg_slope"),
    secondary_y=True,
)


fig30.update_layout(
    title_text="<b>Total des cas quotidiens par rapport au pourcentage quotidien de cas positifs (arrondis) avec moyenne mobile sur 5 jours et pente</b>"
    ,height=800
)


fig30.update_xaxes(title_text="<b>Date</b>")


fig30.update_yaxes(title_text="<b>Count Cases</b>", secondary_y=False)
fig30.update_yaxes(title_text="<b>% Positive Cases</b>", secondary_y=True)


fig30.update_layout(barmode='stack')


fig30.update_traces(
#                   marker_color='rgb(158,202,225)'
#                   , marker_line_color='rgb(8,48,107)',
                  marker_line_width=.01)
#                   ,opacity=0.6)


fig30.update_layout(
    template='plotly_dark'
    ,legend=dict(
    orientation="h",
    yanchor="bottom",
    y=1.01,
    xanchor="right",
    x=1
))



fig31 = make_subplots(specs=[[{"secondary_y": True}]])


fig31.add_trace(
    go.Scatter(x=date
           ,y=total_rounded
           ,name="total_rounded"
           ,mode="lines+markers"
#            ,opacity=.5
           ,marker_color=px.colors.qualitative.Plotly[3]),
    secondary_y=False,
)
fig31.add_trace(
    go.Scatter(x=date
           , y=percent_negative_rounded
#            , opacity=.5
           , mode="lines+markers"
           , marker_color=px.colors.qualitative.Plotly[2]
           , name="percent_negative_rounded"),
    secondary_y=True,
)


fig31.add_trace(
    go.Scatter(x=date
           , y=total_rounded_5d_avg
           , opacity=.6
           , mode="lines"
           , marker_color=px.colors.qualitative.Plotly[1]
           , name="total_rounded_5d_avg"),
    secondary_y=False,
)
fig31.add_trace(
    go.Scatter(x=date
           , y=percent_neg_5d_avg
           , opacity=.6
           , mode="lines"
           , marker_color=px.colors.qualitative.Plotly[1]
           , name="percent_neg_5d_avg"),
    secondary_y=True,
)


fig31.add_trace(
    go.Scatter(x=date
           , y=total_rounded_5d_avg_slope
           , opacity=.7
           , mode="lines"
           , marker_color=px.colors.qualitative.Plotly[3]
           , name="total_rounded_5d_avg_slope"),
    secondary_y=False,
)
fig31.add_trace(
    go.Scatter(x=date
           , y=percent_neg_5d_avg_slope
           , opacity=.7
           , mode="lines"
           , marker_color=px.colors.qualitative.Plotly[2]
           , name="percent_neg_5d_avg_slope"),
    secondary_y=True,
)


fig31.update_layout(
    title_text="<b>Total des cas quotidiens par rapport au pourcentage quotidien de négatifs (arrondis) avec moyenne mobile sur 5 jours et pente</b>"
    ,height=800
)


fig31.update_xaxes(title_text="<b>Date</b>")


fig31.update_yaxes(title_text="<b>Nombre de cas</b>", secondary_y=False)
fig31.update_yaxes(title_text="<b>Pourcentage des cas négatifs</b>", secondary_y=True)


fig31.update_layout(barmode='stack')


fig31.update_traces(
#                   marker_color='rgb(158,202,225)'
#                   , marker_line_color='rgb(8,48,107)',
                  marker_line_width=.01)
#                   ,opacity=0.6)


fig31.update_layout(
    template='plotly_dark'
    ,legend=dict(
    orientation="h",
    yanchor="bottom",
    y=1.01,
    xanchor="right",
    x=1
))

fig32 = make_subplots(specs=[[{"secondary_y": True}]])


fig32.add_trace(
    go.Scatter(x=date
           ,y=total_rounded
           ,name="total_rounded"
           ,mode="lines+markers"
#            ,opacity=.5
           ,marker_color=px.colors.qualitative.Plotly[3]),
    secondary_y=False,
)
fig32.add_trace(
    go.Scatter(x=date
           , y=percent_death_rounded
#            , opacity=.5
           , mode="lines+markers"
           , marker_color=px.colors.qualitative.Plotly[6]
           , name="percent_death_rounded"),
    secondary_y=True,
)


fig32.add_trace(
    go.Scatter(x=date
           , y=total_rounded_5d_avg
           , opacity=.6
           , mode="lines"
           , marker_color=px.colors.qualitative.Plotly[1]
           , name="total_rounded_5d_avg"),
    secondary_y=False,
)
fig32.add_trace(
    go.Scatter(x=date
           , y=percent_death_5d_avg
           , opacity=.6
           , mode="lines"
           , marker_color=px.colors.qualitative.Plotly[1]
           , name="percent_death_5d_avg"),
    secondary_y=True,
)


fig32.add_trace(
    go.Scatter(x=date
           , y=total_rounded_5d_avg_slope
           , opacity=.7
           , mode="lines"
           , marker_color=px.colors.qualitative.Plotly[3]
           , name="total_rounded_5d_avg_slope"),
    secondary_y=False,
)
fig32.add_trace(
    go.Scatter(x=date
           , y=percent_death_5d_avg_slope
           , opacity=.7
           , mode="lines"
           , marker_color=px.colors.qualitative.Plotly[6]
           , name="percent_death_5d_avg_slope"),
    secondary_y=True,
)


fig32.update_layout(
    title_text="<b>Total des cas quotidiens par rapport au pourcentage quotidien de décès (arrondi) avec moyenne mobile sur 5 jours et pente</b>"
    ,height=800
)


fig32.update_xaxes(title_text="<b>Date</b>")


fig32.update_yaxes(title_text="<b>Nombre de cas</b>", secondary_y=False)
fig32.update_yaxes(title_text="<b>% de cas de décès</b>", secondary_y=True)


fig32.update_layout(barmode='stack')


fig32.update_traces(
#                   marker_color='rgb(158,202,225)'
#                   , marker_line_color='rgb(8,48,107)',
                  marker_line_width=.01)
#                   ,opacity=0.6)


fig32.update_layout(
    template='plotly_dark'
    ,legend=dict(
    orientation="h",
    yanchor="bottom",
    y=1.01,
    xanchor="right",
    x=1
))

fig33 = make_subplots(specs=[[{"secondary_y": True}]])


fig33.add_trace(
    go.Scatter(x=date
           ,y=total_rounded
           ,name="total_rounded"
           ,mode="lines+markers"
#            ,opacity=.5
           ,marker_color=px.colors.qualitative.Plotly[3]),
    secondary_y=False,
)
fig33.add_trace(
    go.Scatter(x=date
           , y=percent_hospitalized_rounded
#            , opacity=.5
           , mode="lines+markers"
           , marker_color=px.colors.qualitative.Plotly[4]
           , name="percent_hospitalized_rounded"),
    secondary_y=True,
)


fig33.add_trace(
    go.Scatter(x=date
           , y=total_rounded_5d_avg
           , opacity=.6
           , mode="lines"
           , marker_color=px.colors.qualitative.Plotly[1]
           , name="total_rounded_5d_avg"),
    secondary_y=False,
)
fig33.add_trace(
    go.Scatter(x=date
           , y=percent_hospitalized_5d_avg
           , opacity=.6
           , mode="lines"
           , marker_color=px.colors.qualitative.Plotly[1]
           , name="percent_hospitalized_5d_avg"),
    secondary_y=True,
)


fig33.add_trace(
    go.Scatter(x=date
           , y=total_rounded_5d_avg_slope
           , opacity=.7
           , mode="lines"
           , marker_color=px.colors.qualitative.Plotly[3]
           , name="total_rounded_5d_avg_slope"),
    secondary_y=False,
)
fig33.add_trace(
    go.Scatter(x=date
           , y=percent_hospitalized_5d_avg_slope
           , opacity=.7
           , mode="lines"
           , marker_color=px.colors.qualitative.Plotly[4]
           , name="percent_hospitalized_5d_avg_slope"),
    secondary_y=True,
)


fig33.update_layout(
    title_text="<b>Total des cas quotidiens par rapport au pourcentage quotidien d'hospitalisés (arrondi) avec moyenne mobile sur 5 jours et pente</b>"
    ,height=800
)


fig33.update_xaxes(title_text="<b>Date</b>")


fig33.update_yaxes(title_text="<b>Nombre de cas</b>", secondary_y=False)
fig33.update_yaxes(title_text="<b>% de cas hospitalisés</b>", secondary_y=True)


fig33.update_layout(barmode='stack')


fig33.update_traces(
#                   marker_color='rgb(158,202,225)'
#                   , marker_line_color='rgb(8,48,107)',
                  marker_line_width=.01)
#                   ,opacity=0.6)


fig33.update_layout(
    template='plotly_dark'
    ,legend=dict(
    orientation="h",
    yanchor="bottom",
    y=1.0,
    xanchor="right",
    x=1
))

fig34 = make_subplots(specs=[[{"secondary_y": True}]])


fig34.add_trace(
    go.Scatter(x=date
           ,y=percent_death_rounded
           ,name="percent_death_rounded"
           ,mode="lines+markers"
#            ,opacity=.5
           ,marker_color=px.colors.qualitative.Plotly[6]),
    secondary_y=False,
)
fig34.add_trace(
    go.Scatter(x=date
           , y=percent_positive_rounded
#            , opacity=.5
           , mode="lines+markers"
           , marker_color=px.colors.qualitative.Plotly[5]
           , name="percent_positive_rounded"),
    secondary_y=True,
)


fig34.add_trace(
    go.Scatter(x=date
           , y=percent_death_5d_avg
           , opacity=.6
           , mode="lines"
           , marker_color=px.colors.qualitative.Plotly[1]
           , name="percent_death_5d_avg"),
    secondary_y=False,
)
fig34.add_trace(
    go.Scatter(x=date
           , y=percent_pos_5d_avg
           , opacity=.6
           , mode="lines"
           , marker_color=px.colors.qualitative.Plotly[1]
           , name="percent_pos_5d_avg"),
    secondary_y=True,
)


fig34.add_trace(
    go.Scatter(x=date
           , y=percent_death_5d_avg_slope
           , opacity=.7
           , mode="lines"
           , marker_color=px.colors.qualitative.Plotly[6]
           , name="percent_death_5d_avg_slope"),
    secondary_y=False,
)
fig34.add_trace(
    go.Scatter(x=date
           , y=percent_pos_5d_avg_slope
           , opacity=.7
           , mode="lines"
           , marker_color=px.colors.qualitative.Plotly[5]
           , name="percent_pos_5d_avg_slope"),
    secondary_y=True,
)

fig34.update_layout(
    title_text="<b>Pourcentage quotidien de décès contre pourcentage quotidien positif (arrondi) avec moyenne mobile sur 5 jours et pente</b>"
    ,height=800
)


fig34.update_xaxes(title_text="<b>Date</b>")


fig34.update_yaxes(title_text="<b>% Death Cases</b>", secondary_y=False)
fig34.update_yaxes(title_text="<b>% Positive Cases</b>", secondary_y=True)


fig34.update_layout(barmode='stack')


fig34.update_traces(
#                   marker_color='rgb(158,202,225)'
#                   , marker_line_color='rgb(8,48,107)',
                  marker_line_width=.01)
#                   ,opacity=0.6)


fig34.update_layout(
    template='plotly_dark'
    ,legend=dict(
    orientation="h",
    yanchor="bottom",
    y=1.01,
    xanchor="right",
    x=1
))

fig35 = make_subplots(specs=[[{"secondary_y": True}]])


fig35.add_trace(
    go.Bar(x=date
           ,y=deathIncrease
           ,name="deathIncrease"
           ,marker_color=px.colors.qualitative.Plotly[5]),
    secondary_y=False,
)
fig35.add_trace(
    go.Bar(x=date
           , y=positiveIncrease
           , name="positiveIncrease"
           , marker_color=px.colors.qualitative.D3[7]),
    secondary_y=False,
)

fig35.add_trace(
    go.Scatter(x=date
               ,y=percent_death
               ,name="percent_death"
               ,marker_color=px.colors.qualitative.Plotly[2]),
    secondary_y=True,
)
fig35.add_trace(
    go.Scatter(x=date
               ,y=percent_positive
               ,name="percent_positive"
               ,marker_color=px.colors.qualitative.Plotly[3]),
    secondary_y=True,
)

fig35.add_trace(
    go.Scatter(x=date
               ,y=positive_pct_change
               ,name="positive_pct_change"
               ,mode="lines+markers"
               ,marker_color=px.colors.qualitative.T10[2]),
    secondary_y=True,
)
fig35.add_trace(
    go.Scatter(x=date
               ,y=death_pct_change
               ,name="death_pct_change"
               ,mode="lines+markers"
               ,marker_color=px.colors.qualitative.Plotly[5]),
    secondary_y=True,
)

fig35.update_layout(
    title_text="<b>Cas Covid positif vs. mort</b>"
    ,height=800
)

fig35.update_xaxes(title_text="<b>Date</b>")


fig35.update_yaxes(title_text="<b>Count Cases</b>", secondary_y=False)
fig35.update_yaxes(title_text="<b>% Change</b>", secondary_y=True)


fig35.update_layout(barmode='stack')


fig35.update_traces(
                  marker_line_width=.01)


fig35.update_layout(
    template='plotly_dark'
    ,legend=dict(
    orientation="h",
    yanchor="bottom",
    y=1.02,
    xanchor="right",
    x=1
))
df_confirmed = pd.read_csv("https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_confirmed_global.csv")
df_death = pd.read_csv('https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_deaths_global.csv')
df_confirmed.drop(['Province/State','Lat','Long'],axis=1,inplace=True)#dropping useless columns
df_death.drop(['Province/State','Lat','Long'],axis=1,inplace=True)
df_confirmed=df_confirmed.groupby(['Country/Region'],as_index=False).sum()
df_evol=df_confirmed.apply(np.sum)[1:]
death_evol=df_death.apply(np.sum)[1:]
df_pop = pd.read_csv('C://Users//youssef//Desktop//Nouveau dossier (3)//population.csv.csv')
df_pop.replace(('United States','Russian Federation'),('US','Russia'),inplace=True)
df_pop=df_pop[pd.to_numeric(df_pop['2019 [YR2019]'],errors='coerce').notnull()]
df_pop=df_pop.astype({'2019 [YR2019]':'int64'})
#cahngement au nom 'country dans tous les datat sets'
df_pop.rename(columns={'Country Name':'Country','2019 [YR2019]':'population'},inplace=True)
df_confirmed.rename(columns={'Country/Region':'Country'},inplace=True)
df_death.rename(columns={'Country/Region':'Country'},inplace=True)

# nom des pays en miniscule
df_confirmed.Country=df_confirmed.Country.str.lower()
df_death['Country']=df_death.Country.str.lower()
df_pop.Country=df_pop.Country.str.lower()

#fusion des data sets

population=df_pop.loc[:,['Country','population']]
confirmed_full=pd.merge(df_confirmed,population,'inner',on='Country')
deaths_full=pd.merge(df_death,population,'inner',on='Country')

# pays extreme 
df_confirmed_sum=confirmed_full.sort_values(by=df_confirmed.columns[-1],ascending=False)[0:10] #10 countries with most cases
last_countries=confirmed_full.sort_values(by=df_confirmed.columns[-1])[0:10] # 10 couontries with least cases
df_confirmed_sum.set_index('Country',inplace=True)
last_countries.set_index('Country',inplace=True)
countries=df_confirmed_sum.index
cumulative = df_confirmed_sum.iloc[:,-2]
population=df_confirmed_sum.population
fig101 = go.Figure(data=[
    go.Bar(name='Total Cases', x=countries, y=cumulative),
    go.Bar(name='population', x=countries, y=population )
])

fig101.update_layout(barmode='group')
fig101.update_yaxes(type='log')

fig101.update_layout(title="pays ayant le plus de cas de Covid<br>Total des cas confirmés et<br>population par pays",
                title_x=0.5,
                  yaxis_title="Cases - population"
                    ,template='plotly_dark')

countries=df_confirmed_sum.index
cumulative = df_confirmed_sum.iloc[:,-2]
population=df_confirmed_sum.population
fig102 = go.Figure(data=[
    go.Bar(name='Total Cases', x=countries, y=cumulative),
    go.Bar(name='Normalized', x=countries, y=cumulative/population)
])

fig102.update_layout(barmode='group')
fig102.update_yaxes(type='log')

fig102.update_layout(title="pays ayant le plus de cas Covid<br>Total des cas confirmés et<br>Total des cas confirmés normalisés par million d'habitants",
                title_x=0.5,
                  yaxis_title="Cases - Cases Normalized"
                    ,template='plotly_dark')
countries=df_confirmed_sum.index
cumulative = df_confirmed_sum.iloc[:,-2]
population=df_confirmed_sum.population
fig103 = go.Figure(data=[
    go.Bar(name='Normalized', x=countries, y=cumulative/population)
])

fig103.update_layout(barmode='group')
fig103.update_yaxes(type='log')

fig103.update_layout(title="Total des cas confirmés normalisé par la population",
                title_x=0.5,
                  yaxis_title="Cases - Cases Normalized",
                    template='plotly_dark')

#countries with least nbre of cases
countries=last_countries.index
cumulative = last_countries.iloc[:,-2]
population=last_countries.population
fig104 = go.Figure(data=[
    go.Bar(name='Total Cases', x=countries, y=cumulative),
    go.Bar(name='population', x=countries, y=population)
])
# Change the bar mode
fig104.update_layout(barmode='group')
fig104.update_yaxes(type='log')

fig104.update_layout(title="Total des cas confirmés pour les pays moins infl<br>Population",
                title_x=0.5,
                  yaxis_title="Cases - population",
                    template='plotly_dark')
df=df_confirmed_sum.drop('population',axis=1)
df=df.transpose()
df=df_confirmed_sum.drop('population',axis=1)
data =df.reset_index().melt(id_vars='Country', var_name='date')
data.loc[(data.value < 1),'value']=None
df = data.pivot(index='date', columns='Country', values='value')

datetime_index = pd.DatetimeIndex(df.index)
df.set_index(datetime_index,inplace=True)

period = 7
xv = []
yv = []
for j  in range(7):
    y = df_confirmed_sum.iloc[j,:]
    yd = pd.Series(y).diff(periods=period)  
    xv.append(y[period:len(y)])
    yv.append(yd[period:len(y)])
    

fig55 = go.Figure()
for j in range(7):
    fig55.add_trace((go.Scatter(x=xv[j],
                                y=yv[j],
                                marker=dict(size=4),
                                mode='lines+markers',
                                name=df_confirmed_sum.index[j],
                                text=df_confirmed_sum.index[j]))) #
    
fig55.update_xaxes(range=[2, 6.5])
fig55.update_yaxes(range=[2, 6])
fig55.update_layout(title='Pays avec le plus grand nombre de cas de Covid',
                                    title_x=0.5,
                  xaxis_type="log",
                  yaxis_type="log",
                  xaxis_title="Total Cumulatuve Cases",
                  yaxis_title="Weekly Increase in Cases",
                    template='plotly_dark'
                  )
#-------------------------------------------------------------
#run app layout things

# app = dash.Dash()



app.layout = html.Div(children=[
        html.Br()
        ,html.Br()
        ,html.Br()

        ,html.H1(children='PROJET ENCADRER : analyze de la pandémie de covid')

        ,html.Div([
        html.H6(children='realiser par : youssef amine khallouq et Amine el omairi ')
          
        ], style={"color": "#B2B7B7"})
        ,html.Div([
        html.H6(children='encadrante : Mme  Kaoutar ELHARI')
           
        ], style={"color": "#B2B7B7"})

        ,html.Br()
        ,html.Br()

        ,html.Div(children='''
        Le but de cette page est de fournir une analyse plus approfondie de\
        l'épidémie de Covid-19. Les graphiques de cette page offrent une gamme  \
        d'analyses.
        
        ''')

        ,html.Br()

        ,html.Div(children='''
        les données utiliser durant cette etude sont issue du '''),dcc.Markdown('''\
        [github]("https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series")''')
        ,html.Div(children='''
        la base de données concernant USA '''),dcc.Markdown('''\
        [Our World in Data]("https://covidtracking.com/api/v1/us/daily.csv")''')
   

        ,html.Br()

        ,html.Br()

    
        ,html.Br()
        ,html.Br()
        ,html.Br(),


  
    
    
    
    html.H1(children='statistiques générales')

        ,html.Div(children='''
        les graphiques ci-dessous représentent une vision générale des décès et des cas confirmés de covid-19 dans le monde, ainsi qu'une carte décrivant la propagation du covid-19. 
        ''')

        ,html.Br()

        ,html.H5(children='points à retenir:')

        ,html.Div(children='''
        on voit que le nombre des cas augmente légèrement avec la population , mais on trouve des pays qui font l'exception , les Etats-Unis par exemple a une population inférieure
        à celle de l'Inde pourtant elle a le plus grand nombre de cas. Pour avoir une vision plus clair, on compare le rapport : nombre de cas/population.
        ''')
        ,html.Br()

        ,html.Div(children='''
        on trouve ainsi que l'Inde a le quotient le plus petit alors qu'elle est la 2ème en terme de nombre de cas, cela vient du fait qu'elle a une grande population(la 2eme au monde)
        alors que le nombre de cas est relativement petit; de l'autre coté, les Etats-Unis, la France et l'Espagne sont les premiers dans de ce rapport puisque leurs nombre de cas est 
        relativement supérieur en comparaison avec leurs population.
        ''')
        ,html.Br()

        ,html.Div(children='''
        contrairement aux 10 premiers pays , les chiffres des pays les moins influencés ne montrent pas une corrélation entre le nombre de cas et la population, 
        cela peut être du aux manques des tests ou parce que les populations sont trop faibles et donc non-représentatives
        ''')

        ,html.Br()
    
         ,html.Div(children='''
        on remarque que les états-unis ont connut des hauts et bas dans leur journée covid , mais globalement leur nbre de cas augmente , pour l'Inde , 
        on trouve un point d'inflexion(dans le mois avril) suivi par une augmentation intense des cas , le Brazil avance toujours avec une pente élevée ,
        pour les autres pays ils avancent presque du méme comportement: une pente constante et relativement faible.
        ''')
        
        ,html.Br()

        ,html.Div(children='''
        on trouve l'evolution hebdomadaire a diminué dans les mémes periodes pour la plupart des pays , 2 période principalement : dès que le nombre des cas dépasse les 100 milles ,
        le nombbre de nouveaux cas par semaine diminue jusqu'à 500 cas , et l'orsque le nombre de cas dépasse 1.5 million le nbre de nouveaux cas par semaine se stabilse à 50k cas.
        Pourtant pour les états-unis,l'Inde et le Brazil : l'évolution hebdomadaire était toujours en augmentation. On remarque aussi que la France a connu une situation spéciale 
        pour nombre de cas envers 50k l'evolution hebdomadaire dans cette période était presque nulle.
        ''')
        

        ,html.Br()

        ,html.Div([
        dcc.Graph(figure=fig101)
        ])

        ,html.Br(),

        html.Div([
        dcc.Graph(figure=fig102)
        ])

        ,html.Br(),

        html.Div([
        dcc.Graph(figure=fig103)
        ])

        ,html.Br(),

        html.Div([
        dcc.Graph(figure=fig104)
        ])

        ,html.Br()

        ,html.Div([
        dcc.Graph(figure=fig55)
        ])
        
    
      

        ,html.Br()
        ,html.Br()
        ,html.Br()
        ,html.Br(),
        
        html.Iframe(srcDoc = open('C:\\Users\\youssef\\Desktop\\carteinitial.html', 'r').read(),style={"height": "1067px", "width": "100%"})
    
        ,html.Br()
        ,html.Br()
        ,html.Br()
        ,html.Br(),
    
      html.H1(children=' données des tests des états unis')

        ,html.Div(children='''
       d'après la partie précédente, les états-unis semblent avoir les taux de mortalité les plus élevés,
       et c'est l'un des rares pays qui ont une base de données complète et 
       détaillée des tests covid
       , donc nous avons décidé d'exploiter ces données qui concernent les états-unis.
        ''')
        ,html.Br()
        ,html.Br()
        ,html.Br(),
    
       html.Div([
        html.Div([
        html.H4("Cumule des  Tests"),
        dcc.Graph(figure=fig0)
        # ])
        ], className="six columns"
        ,style={'padding-left': '2%', 'padding-right': '2%',
                'vertical-align': 'middle'})

        ,html.Br(),

        html.Div([
        html.H4(" Tests "),
        dcc.Graph(figure=fig1)
        # ])
        ], className="six columns"
        ,style={'padding-left': '2%', 'padding-right': '2%',
                'margin-top': -24})

    ], className="row")
    
    
        ,html.Br()
        ,html.Br()
        ,html.Br()

        ,html.H2("Tests Covid quotidiens en fonction du Pourcentage Pos/Neg et  Pourcentage de changement quotidien")

        
        ,html.Br()

        ,html.Div([
        dcc.Graph(figure=fig16)
        ])

        ,html.Br()
        ,html.Br()
        ,html.Br()
        ,html.Br()

        ,html.H1(children='Analyse du graphique ci-dessus')

        ,html.Div(children='''
        Les graphiques ci-dessous offrent une décomposition du graphique ci-dessus. Compte tenu de la complexité, on a décidé de proposer une vue pour chacune des pièces du graphique.
        ''')

        ,html.Br()

        ,html.H5(children=' points à retenir:')

        ,html.Div(children='''
        Plus il y a de tests quotidiens de covid, plus il y a de tests positifs.
        C'est simplement dans les chiffres. Ci-dessous, nous allons examiner les taux de mortalité
        pour répondre à la question : "Plus de tests covid égalent plus de décès dus au covid ?""
        ''')

        ,html.Br()

        ,html.Div(children='''
        En juillet, nous avons une moyenne d'environ 700 000 tests quotidiens de covid.
        ''')

        ,html.Br()

        
        ,html.Br()

        ,html.Div([
        dcc.Graph(figure=fig2)
        ])
        # ], className="six columns"),

        ,html.Br(),

        html.Div([
        dcc.Graph(figure=fig3)
        ])

        ,html.Br(),

        html.Div([
        dcc.Graph(figure=fig4)
        ])

        ,html.Br(),

        html.Div([
        dcc.Graph(figure=fig5)
        ])

        ,html.Br(),

        html.Div([
        dcc.Graph(figure=fig6)
        ])

        ,html.Br(),

        html.Div([
        dcc.Graph(figure=fig7)
        ])

        ,html.Br()
        ,html.Br()
        ,html.Br()
        ,html.Br(),

        html.H1(children='Tendances de distribution des résultats quotidiens')

        ,html.Div(children='''
        Les graphiques ci-dessous offrent une ventilation de chaque métrique du test covid (positif, 
        négatif, décès, hospitalisation). Il existe plusieurs façons de visualiser les éléments suivants 
        les graphiques - je propose quelques vues dans et autour des cartes thermiques, des diagrammes de dispersion avec des sous-points, 
        et des histogrammes.
        ''')

        ,html.Br()

        ,html.Div(children='''
        Les hauts et les bas de chaque marque sur les diagrammes de dispersion ci-dessous représentent les variations quotidiennes en pourcentage. 
        les variations quotidiennes en pourcentage ; ainsi, plus la marque est haute et plus elle est claire, plus le pourcentage de variation/augmentation par rapport au jour précédent est important. 
        de variation/augmentation en pourcentage par rapport à la journée précédente.
        ''')

        ,html.Br()

        ,html.H5(children=' points à retenir:')

        ,html.Div(children='''
        La majorité des pics ont eu lieu au début de l'épidémie de covid. 
         mois de mars et avril. Les variations quotidiennes en pourcentage 
        se sont aplatis pour la plupart dans chaque variable
        ''')

        ,html.Br()

       

        ,html.Br()

        
        ,html.Br()

        ,html.Br(),

        html.Div([
        dcc.Graph(figure=fig8)
        ])

        ,html.Br(),

        html.Div([
        dcc.Graph(figure=fig9)
        ])

        ,html.Br(),

        html.Div([
        dcc.Graph(figure=fig10)
        ])

        ,html.Br(),

        html.Div([
        dcc.Graph(figure=fig11)
        ])

        ,html.Br(),

        html.Div([
        dcc.Graph(figure=fig12)
        ])

        ,html.Br(),

        html.Div([
        dcc.Graph(figure=fig13)
        ])

        ,html.Br(),

        html.Div([
        dcc.Graph(figure=fig14)
        ])

        ,html.Br(),

        html.Div([
        dcc.Graph(figure=fig15)
        ])

        ,html.Br()
        ,html.Br()
        ,html.Br()
        ,html.Br(),

        html.H1(children='Les mesures quotidiennes en fonction des  jours  de la semaine ')

        ,html.Div(children='''
        Les graphiques ci-dessous analysent les tendances au sein de jours spécifiques de la semaine 
        combinées à chaque métrique. Ainsi, nous pouvons répondre à des questions telles que 
        "quel jour de la semaine a vu le plus grand nombre de tests covid positifs" ou 
        "quel jour les gens sont plus susceptibles d'être hospitalisés à cause du covid-19"
        ''')

        ,html.Br()

        ,html.Div(children='''
       
        pour vous aider à mieux comprendre les tendances quotidiennes 

        ''')

        ,html.Br()

        ,html.H5(children=' points à retenir:')

        ,html.Div(children='''
        Le jour de la semaine où les tests sont les plus positifs est le mardi, suivi de près par le dimanche. 
        et le jour le moins positif est le vendredi.
        ''')

        ,html.Br()

        ,html.Div(children='''
        Les jours les plus négatifs sont aussi les mardis, tandis que les plus bas sont les vendredis.
        ''')

        ,html.Br()

        ,html.Div(children='''
        Cette conclusion est logique étant donné que les mardis et les vendredis sont respectivement les jours 
        les jours où les tests sont les plus élevés et les plus bas, respectivement.
        ''')

        ,html.Br()

        ,html.Div(children='''
        Les décès surviennent plus régulièrement les lundis et les dimanches, et sont moins susceptibles de se produire les jeudis et les vendredis. 
        de se produire les jeudis et les vendredis.
        ''')

        ,html.Br()

        ,html.Div(children='''
        Les hospitalisations ont lieu principalement les mardis et les samedis, et sont moins susceptibles 
        de tomber le jeudi.
        ''')

        ,html.Br()
        ,html.Br()

        
        ,html.Br()

        ,html.Br()

        ,html.Div([
        dcc.Graph(figure=fig17)
        ])

        ,html.Br()

        ,html.Div([
        dcc.Graph(figure=fig18)
        ])

        ,html.Br()

        ,html.Div([
        dcc.Graph(figure=fig19)
        ])

        ,html.Br()

        ,html.Div([
        dcc.Graph(figure=fig20)
        ])

        ,html.Br()

        ,html.Div([
        dcc.Graph(figure=fig21)
        ])

        ,html.Br()

        ,html.Div([
        dcc.Graph(figure=fig22)
        ])

        ,html.Br()

        ,html.Div([
        dcc.Graph(figure=fig23)
        ])

        ,html.Br()

        ,html.Div([
        dcc.Graph(figure=fig24)
        ])

        ,html.Br()
        ,html.Br()
        ,html.Br()
        ,html.Br()

        ,html.H1(children='Mesures historiques en fonction des Jours de la semaine et Totaux cumulatifs ')

        ,html.Div(children='''
        Les graphiques ci-dessous diffèrent des précédents en ce sens qu'ils analysent les métriques 
        au niveau quotidien - alors que la plupart des graphiques ci-dessus étaient regroupés par jour. 
        Les graphiques ci-dessous offrent une vue d'ensemble des pics de mesures par jour, ce qui permet de mieux comprendre les tendances hebdomadaires et mensuelles ainsi que les pics aberrants. 
        de mieux comprendre les tendances hebdomadaires et mensuelles ainsi que les pics aberrants.
        ''')

        ,html.Br()

        ,html.Div(children='''
        Les questions que l'on peut se poser sont les suivantes : 
        "Y a-t-il des jours précédents dans la semaine qui ont augmenté avec le temps ?", 
        "quels jours de la semaine sont plus/moins volatils ?",
        "Quelles sont les mesures qui ont les pics les plus élevés/les plus bas ?",
        "dans l'ensemble, quels sont les jours où la variation quotidienne en pourcentage est la plus faible/la plus forte ?" 
        ''')

        ,html.Br()

        ,html.H5(children=' points à retenir:')

        ,html.Div(children='''
        il apparaît que le nombre de pics a augmenté le mercredi, tandis que 
        Les mardis ont commencé avec un peu plus de pics, mais ont diminué.
        ''')
        ,html.Br()

        ,html.Div(children='''
        Le samedi a vu le pic le plus élevé dans les pourcentages de changement quotidiens, mais... 
        on peut se demander pourquoi. Le lundi a connu le pic le plus bas dans les variations quotidiennes en pourcentage.
        ''')
        ,html.Br()

        ,html.Div(children='''
        Les dimanches, vendredis et jeudis semblent avoir la même volatilité 
        lorsqu'il s'agit des variations quotidiennes cumulées en pourcentage.
        ''')
        ,html.Br()

        ,html.Div(children='''
        Les hospitalisations présentent le plus grand nombre de pics ainsi que les pics les plus élevé et le plus bas 
         globalement dans les variations quotidiennes cumulées en pourcentage.
        ''')
        ,html.Br()

        ,html.Div(children='''
        Les vendredis ont tendance à avoir les pics les plus bas dans les variations quotidiennes cumulées en pourcentage. 
        Plus de 50% des vendredis ont un pic négatif.
        ''')

        ,html.Br()
        ,html.Br()

        
        # ,html.Br()
        #
        # ,html.Div([
        # dcc.Graph(figure=fig40)
        # ])

        ,html.Br()

        ,html.Div([
        dcc.Graph(figure=fig25)
        ])

        ,html.Br(),

        html.Div([
        dcc.Graph(figure=fig26)
        ])

        ,html.Br(),

        html.Div([
        dcc.Graph(figure=fig27)
        ])

        ,html.Br(),

        html.Div([
        dcc.Graph(figure=fig28)
        ])

        ,html.Br(),

        html.Div([
        dcc.Graph(figure=fig29)
        ])

        ,html.Br()
        ,html.Br()
        ,html.Br()
        ,html.Br(),

        html.H1(children='Moyenne mobile sur 5 jours des résultats obtenus en % des résultats quotidiens (arrondis)')

        ,html.Div(children='''
        Les graphiques ci-dessous offrent une vue plus analytique en comparant les pourcentages cumulés quotidiens arrondis de chaque mesure au total des tests quotidiens. 
        arrondis de chaque paramètre par rapport au total des tests quotidiens. on a également ajouté la pente 
        de chaque mesure par rapport au total des tests quotidiens, qui apparaît au bas de chaque graphique. 
        bas de chaque graphique. Les moyennes mobiles sur 5 jours sont arrondies pour lisser davantage les lignes (ce qui aide à montrer la pente). 
        les lignes (ce qui permet de mieux faire ressortir la pente). L'objectif de ces graphiques est de 
        de fournir une corrélation entre la métrique et le total des tests quotidiens.  et répondre a L'hypothèse 
        suivante : "plus il y a de tests, plus il y a de chaque métrique 

        ''')

        ,html.Br()

        ,html.Div(children='''
        Les questions que l'on peut se poser sont les suivantes : 
        "à quoi ressemblent les pentes de chaque mesure par rapport au total des tests quotidiens ?" 
        "Les pentes sont-elles corrélées au nombre total de tests quotidiens ? 
        ''')

        ,html.Br()

        ,html.H5(children=' points à retenir:')

        ,html.Div(children='''
        Les tests positifs et le total des tests quotidiens semblent très bien corrélés 
        à partir du mois de juin. L'augmentation des tests quotidiens s'avère être en corrélation directe avec le nombre de tests positifs. 
        corrélation directe avec le nombre de tests positifs ; 450 000 tests quotidiens équivalent à 
        environ 5 % de tests positifs par jour ; et donc 800 000 tests quotidiens équivalent à 
        environ 10 % de tests positifs.

        ''')
        ,html.Br()

        ,html.Div(children='''
        Les autres mesures ne semblent pas avoir de corrélation car les chiffres 
        sont tout simplement trop bas. Peut-être une analyse logarithmique pourrait aider
        ''')
        ,html.Br()

        ,html.Div(children='''
        Les vendredis ont tendance à avoir les pics les plus bas dans les variations quotidiennes cumulées en pourcentage. 
        Plus de 50% des vendredis ont un pic négatif.
        ''')

        ,html.Br()

        

        ,html.Br()

        ,html.Div([
        dcc.Graph(figure=fig30)
        ])

        ,html.Br(),

        html.Div([
        dcc.Graph(figure=fig31)
        ])

        ,html.Br(),

        html.Div([
        dcc.Graph(figure=fig32)
        ])

        ,html.Br(),

        html.Div([
        dcc.Graph(figure=fig33)
        ])

        ,html.Br()

        ,html.Div([
        dcc.Graph(figure=fig34)
        ])

        ,html.Br()
        ,html.Br()
        ,html.Br()
        ,html.Br()

        ,html.H1(children='Graphiques supplémentaires')

        ,html.Div(children='''
        Le graphique offrira des analyses supplémentaires, moins thématiques. 
        .
        ''')

        ,html.Br()

        ,html.Div(children='''
        Le  graph montre la corrélation entre les tests positifs quotidiens et les taux de mortalité quotidiens. 
        ainsi que les variations quotidiennes en pourcentage de chacune de ces mesures, 
        et le pourcentage de tests positifs pour la journée.
        ''')

        ,html.Br()

        ,html.H5(children=' points à retenir:')

        ,html.Div(children='''
        Les taux de mortalité diminuent aux États-Unis, malgré l'augmentation exponentielle 
        des tests quotidiens ainsi que du nombre de tests positifs. Il y a eu un petit 
        pic au début (pendant les mois d'avril et mai), mais ces chiffres ont diminué 
        de façon spectaculaire en juin et juillet. Il semble que nous ayons une légère 
        remontée vers la fin du mois de juillet.
        ''')

        ,html.Br()

        ,html.Div(children='''
        Les décès semblent atteindre un pic le dimanche et le lundi et diminuer au fil de la semaine. 
        Cela explique les pics de la ligne bleue (variation quotidienne du pourcentage de décès)..
        ''')

        ,html.Br()

        ,html.Div([
        dcc.Graph(figure=fig35)
        ])

        ,html.Br()
        ,html.Br()
        ,html.Br()

       
        

        ,html.Br()

],style={'padding-left': '20%'
        , 'padding-right': '20%'
        , 'backgroundColor':'white'}
        )



app.run_server(debug=True, use_reloader=False)  # Turn off reloader if inside Jupyter

if __name__ == '__main__':
    app.run_server(debug=True)


# In[ ]:




