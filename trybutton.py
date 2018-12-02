#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Sun Dec  2 00:12:30 2018

@author: yewanxin
"""

import dash
from dash.dependencies import Input, State, Output, Event
import dash_core_components as dcc
import dash_html_components as html

app = dash.Dash()
app.layout = html.Div([
    html.Div(id='target'),
    dcc.Input(id='input', type='text', value=''),
    html.Button(id='submit', type='submit', children='ok'),
    html.Button(id='other-action', children='other action'),
])

@app.callback(Output('target', 'children'), [], [State('input', 'value')], [Event('submit', 'click'),Event('other-action', 'click')])
def callback(state, click_submit, click_other_action):
    if click_other_action: print('other action has been clicked')
    return "callback received value: {}".format(state)

if __name__ == '__main__':
    app.run_server(debug=True)