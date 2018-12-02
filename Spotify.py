#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Sat Dec  1 13:47:09 2018

@author: yewanxin
"""

import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
#pip install dash-dangerously-set-inner-html
import plotly.graph_objs as go
import plotly
import pandas as pd
import numpy as np
#pip install dash-table-experiments
import dash_table_experiments as dt
import urllib, json
import ast
import logging
from sklearn.metrics import roc_auc_score
import helperFunctions
import seaborn as sns
import matplotlib
from sklearn import metrics
from sklearn.metrics import accuracy_score
from sklearn.model_selection import cross_val_score, GridSearchCV
import matplotlib.pyplot as plt
import xgboost as xgb
from xgboost.sklearn import XGBRegressor
from xgboost.sklearn import XGBClassifier
from sklearn.model_selection import KFold
from sklearn.ensemble import RandomForestClassifier
import copy
from sklearn.model_selection import train_test_split
from sklearn.model_selection import cross_val_score
from sklearn import svm
from sklearn import preprocessing
from sklearn.ensemble import RandomForestClassifier
from demo import get_info


data= pd.read_csv('SimpleDataSetWithNewTarget.csv')
# resultdata= pd.read_csv('50Songs.csv')



app = dash.Dash(__name__)

app.layout = html.Div(style = {'backgroundColor': '#F5F5F5', 'height': 1000},children = [
        
        
                html.Div([
                        
                        html.Img(id = 'logo', src = 'https://developer.spotify.com/assets/branding-guidelines/logo@2x.png', height='80',  width= '100'),
                        dcc.Input(
                                id='song_input',
                                value='thank u,next',type='text',
#                                children=html.Div([
#                                    'Input a song name'
#                               ]),
                                style={
                                    'width': '80%',
                                    'height': '100px',
                                    'lineHeight': '100px',
                                    'borderWidth': '2px',
                                    'borderStyle': 'dashed',
                                    'borderRadius': '8px',
                                    'textAlign': 'center',
                                    'margin': '12px'
                                },
                                # Allow multiple files to be uploaded
                              ),
                         dcc.Input(
                                 id='artist_input',
                                 value='ariana grande',type='text',
#                                 children=html.Div([
#                                         'Input the artist name',
#                                ]),
                                style={
                                    'width': '80%',
                                    'height': '100px',
                                    'lineHeight': '100px',
                                    'borderWidth': '2px',
                                    'borderStyle': 'dashed',
                                    'borderRadius': '8px',
                                    'textAlign': 'center',
                                    'margin': '12px'
                                },
                                 ),
                         
                          ]),
                html.Button(id='button',n_clicks=0,children='Submit'),
                html.Div(id='output-container-button',
                         children='Enter the song name, artist name and press submit'),
                html.Div([
                         html.Br(),
                         html.Br(),
                         html.Br(),
                         html.P(children = 'Probability Result', style = {'font-weight':'bold'}),
                         html.Div(id='output',
                                  children=[html.Div(dt.DataTable(rows=[{}]), style={'display': 'visible'})]),   
                                  html.Br(),
                              ], className='seven columns')
                                                        

                ], className = 'row') 


def popularity(song_name,artist_name):
    le = preprocessing.LabelEncoder()
    data['artist_id'] = le.fit_transform(data['artist_id'].astype('str'))
    drop_list = ['artist_location', 'artist_latitude', 'artist_longitude','artist_name', 'release', 'title' ,'song_hotttnesss', 'artist_id', 'artist_familiarity']
    train = data.drop(drop_list, axis=1)
    Y = copy.deepcopy(train.bbhot)
    train1 = train.drop("bbhot", axis=1)
    xgb1 = helperFunctions.loadModel("model.dat")
    print(song_name, artist_name)
    ser_3, popularity = helperFunctions.getSpotifyTrackInfo(song_name, artist_name)

    song3 = pd.DataFrame(ser_3).transpose()

    song3 = helperFunctions.matchOrder(correctShape= train1,incorrectShape=song3)

    prediction = xgb1.predict_proba(song3)

    C=(prediction[0][1]*100,popularity)
    print(C)
    return C
    # return (popularity)
    #print("Predicted Hit Probability(according to our model): {:.2f}%\nActual Popularity (according to Spotify): {}".format(prediction[0][1]*100, popularity))


#@app.callback(Output('output-container-button', 'children'),
#              [Input('button', 'n_clicks')],
#              [State('song_input', 'value'),
#               State('artist_input', 'value')
#               ])

@app.callback(Output('output','children'),
              [Input('button', 'n_clicks')],
              [State('song_input', 'value'),
               State('artist_input', 'value')]
               )
def output(n_clicks, song_name,artist_name):
    result= list(popularity(song_name,artist_name)) 
    print (result)
    dff=pd.DataFrame(result).transpose()
    dff.columns = ['Predicted Probability', 'Spotify Popularity']
    children = [
                    dt.DataTable(rows=dff.to_dict('records')),
    ]
    print(children)

    return children
            
if __name__ == '__main__':
	app.run_server(debug=True)
