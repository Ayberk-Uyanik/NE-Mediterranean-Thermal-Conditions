# Importing the necessary libraries #
from plotly.validators.scatter.marker import SymbolValidator
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objects as go
import plotly.express as px
from dash import dash
from dash.dependencies import Input, Output
import dash_auth
import pandas as pd
import base64
from sqlalchemy import create_engine
import psycopg2

# Postgresql Database Connection #
engine = create_engine ('postgresql+psycopg2:// import your database URL')

# App styling codes #
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
colorscales = px.colors.named_colorscales()
discretecolors = px.colors.sequential.swatches()
cyclicalcolors = px.colors.cyclical.swatches_cyclical()
colours = ["black", "red", "blue", "green", "orange", "yellow", "brown", "purple", "magenta", "goldenrod"]
marker_symbols = SymbolValidator().values
templates = ["plotly", "plotly_white", "plotly_dark", "ggplot2", "seaborn", "simple_white", "none"]
depth_values = [i for i in range (500, 5000, 500)]
map_values = ["Temperature (C)", "Geothermal Gradient (C/km)", "Heat Flow (mW/km2)"]

button_style = {
    "textAlign": "center",
    "backgroundColor": "#3283FE",
    "color": "#E2E2E2",
    "display": "inline-block"
}

# Data import section #
comparison = pd.read_sql_table ("insert your table name", con=engine)
pie1 = pd.read_sql_table ("insert your table name", con=engine)
wells1 = pd.read_sql_table ("insert your table name", con=engine)
gradients = pd.read_sql_table ("insert your table name", con=engine)
maps1 = pd.read_sql_table ("insert your table name", con=engine)

github_logo = "github.png" 
encoded_image = base64.b64encode(open(github_logo, "rb").read()).decode('ascii')

# App Layout building #
app = dash.Dash (__name__, external_stylesheets=external_stylesheets)
server = app.server
auth = dash_auth.BasicAuth(
    app,
    {'your username1': 'yourpassword1',
     'your username2': 'yourpassword2'}
)

app.layout = html.Div([
  html.Div ([
    html.Div ([
      html.H1 ("Subsurface Temperature Conditions of the NE Mediterranean Region",
        style={"textAlign": "center", "font-size": "21px", "font-weight": "normal", "margin-top":"1em", 
              "color": "#fff", "height":"25px", "padding":"20px 20px", 
              "letter-spacing":"0.4px"})
    ]),

    html.Div ([
      html.A ([html.Img(src="data:image/png;base64,{}".format(encoded_image), width=40, height=40)], href="https://github.com/Ayberk-Uyanik/Temperature-Analyser", target="blank", style={"text-decoration":"none", "color":"#fff", "font-weight":"normal"})
    ], style={"margin-left":"30em", "align-items":"center"}),

    html.Div ([
      html.Label ("GitHub", style={"display":"inline-block", "font-size":"16px", "font-weight":"normal",     "text-decoration":"none", "color":"#fff", "margin-left":"0.5em", "letter-spacing":"0.1px"})
    ], style={"align-items":"center"}),         
  ], style={"margin":"none", "display":"flex", "background-color":"#004182", "justify-content":"center", 
     "height":"75px", "align-items":"center", "align-content":"center"}),

  dcc.Tabs([
    dcc.Tab(label="Overview", children=[
      html.Div ([
        html.H2 ("General Information", style={"textAlign": "left", "font-size": "20px", "font-weight": "bold",           "margin-left":"2em", "margin-top":"2em", "color":"#191970", "letter-spacing":"0.1px"}),
      ]),

      html.Div ([
        html.Div ([
          html.P (["This dashboard displays the results of temperature study conducted in 2017. For the evaluation of the present day subsurface conditions, bottom hole temperatures of 93 wells have been converted into static formation temperatures. The results are displayed as cross-plots in '2D Profiles' section based on temperature, geothermal gradient and heat flow values. 'Map View' section depicts thermal conditions for every 500m from surface to 5km depth. On the map at the right hand side, key wells are shown."])
        ], style={"font-size":"16px", "border":"0.1px solid gray", "background-color":"#fff", 
                  "padding":"10px 10px", "width":"250px", "border-radius":"1em"}),

        html.Div ([
          dcc.Graph (id="overview_map", style={"display":"inline-block", "width":"800px", 
                                              "padding":"10px 10px", "margin-left":"3em", "height":"350px"})
        ])          
      ], style={"display":"flex", "margin-top":"2em", "align-items":"center", "justify-content":"center"}),

      html.Hr (),
      html.H2 ("Statistics", style={"textAlign": "left", "font-size": "20px", "font-weight": "bold",           "margin-left":"2em", "color":"#191970", "letter-spacing":"0.1px"}),
      
      html.Div ([
        html.Div ([
          dcc.Graph (id="pie-chart", style={"display":"inline-block", "width":"500px", "margin-left":"0.5em"})
        ]),
        html.Div ([
          dcc.Graph (id="depth-chart", style={"display":"inline-block", "width":"750px", "margin-left":"1em"})
        ])          
      ], style={"display":"flex", "justify-content":"center", "margin-top":"10px", "margin-bottom":"2em"})          
    ]),

    dcc.Tab(label="2D Profiles", children=[
      html.Div ([
            html.Label ("Temperature", style={"display":"inline-block", "font-size":"20px", "font-weight":"bold",     "text-decoration":"none", "color":"#191970", "margin-left":"2em", "letter-spacing":"0.1px"})
          ], style={"text-align":"left", "margin-top":"2em"}),

      html.Div ([
        html.Div ([                                             
          dcc.Graph (id="comparison_graph", style={"display":"inline-block", "width":"800px", "margin-left":"2em"})
        ]),

        html.Div ([
          html.Div ([
            html.Label ("STYLES", style={"display":"inline-block", "margin-left":"2em", 
                                        "font-size":"18px", "font-weight":"bold"}),
          ], style={"text-align":"center"}),

          html.Div ([
            html.Label ("UNITS", style={"display":"inline-block", "margin-left":"2em", 
                                              "font-size":"16px", "font-weight":"bold"}),
            dcc.RadioItems (id="units", options=[{"label":"Celcius (C)", "value":"Celcius"}, 
                                  {"label":"Fahrenheit (F)", "value":"Fahrenheit"}], value="Celcius",
                                  labelStyle={"display":"inline-block", "margin-left":"2.5em"})
          ]),

          html.Div ([
            html.Label ("COLOURS", style={"margin-left":"2em", "font-size":"16px", "font-weight":"bold"}),              
          ], style={"margin-top":"1em"}),

          html.Div ([
            html.Div ([
              html.Label ("Horner plot", style={"display":"inline-block", "margin-left":"2em", 
                                        "font-size":"16px", "font-weight":"bold"}),
              dcc.Dropdown (id="horner_colour", options=[{"label": i, "value": i} for i in colorscales],
                                  style={"width":"100px", "margin-left":"1em", "margin-top":"0.3em"},
                                  value="plasma", 
                                  clearable=False, disabled=False, multi=False),                          
            ], style={"display":"flex", "flex-direction":"column"}),

            html.Div ([
              html.Label ("AAPG corr.", style={"display":"inline-block", "margin-left":"2em", 
                                        "font-size":"16px", "font-weight":"bold"}),
              dcc.Dropdown (id="aapg_colour", options=[{"label": i, "value": i} for i in colorscales],
                                  style={"width":"100px", "margin-left":"1em", "margin-top":"0.3em"},
                                  value="plasma", 
                                  clearable=False, disabled=False, multi=False),                          
            ], style={"display":"flex", "flex-direction":"column"}),

            html.Div ([
              html.Label ("Harrison", style={"display":"inline-block", "margin-left":"2em", 
                                        "font-size":"16px", "font-weight":"bold"}),
              dcc.Dropdown (id="harrison_colour", options=[{"label": i, "value": i} for i in colorscales],
                                  style={"width":"100px", "margin-left":"1em", "margin-top":"0.3em"},
                                  value="plasma", 
                                  clearable=False, disabled=False, multi=False),                          
            ], style={"display":"flex", "flex-direction":"column"}),
          ], style={"display":"flex", "flex-direction":"row"}),

          html.Div ([
            html.Label ("MARKER SYMBOLS", style={"display":"inline-block", "margin-left":"2em", 
                                        "font-size":"16px", "font-weight":"bold", "margin-top":"0.5em"}),
          ], style={"display":"flex", "align-items":"center", "margin-top":"1em"}),

          html.Div ([
            html.Div ([
              html.Label ("Horner plot", style={"display":"inline-block", "margin-left":"2em", 
                                        "font-size":"16px", "font-weight":"bold"}),
              dcc.Dropdown (id="hornermarkersymbols", options=[{"label": i, "value": i} for i in marker_symbols],
                                      style={"width":"100px", "margin-left":"1em"},
                                      value="circle", 
                                      clearable=False, disabled=False, multi=False)                          
            ], style={"display":"flex", "flex-direction":"column"}),

            html.Div ([
              html.Label ("AAPG corr.", style={"display":"inline-block", "margin-left":"2em", 
                                        "font-size":"16px", "font-weight":"bold"}),
              dcc.Dropdown (id="aapgmarkersymbols", options=[{"label": i, "value": i} for i in marker_symbols],
                                      style={"width":"100px", "margin-left":"1em"},
                                      value="circle", 
                                      clearable=False, disabled=False, multi=False)                          
            ], style={"display":"flex", "flex-direction":"column"}),

            html.Div ([
              html.Label ("Harrison", style={"display":"inline-block", "margin-left":"2em", 
                                        "font-size":"16px", "font-weight":"bold"}),
              dcc.Dropdown (id="harrisonmarkersymbols", options=[{"label": i, "value": i} for i in marker_symbols],
                                      style={"width":"100px", "margin-left":"1em"},
                                      value="circle", 
                                      clearable=False, disabled=False, multi=False)                          
            ], style={"display":"flex", "flex-direction":"column"}),
          ], style={"display":"flex", "flex-direction":"row"}),

          html.Div ([
            html.Label ("MARKER SIZES", style={"display":"inline-block", "margin-left":"2em", 
                                        "font-size":"16px", "font-weight":"bold", "margin-top":"0.5em"}),
          ], style={"display":"flex", "align-items":"center", "margin-top":"1em"}),

          html.Div ([
            html.Div ([
              html.Label ("Horner plot", style={"display":"inline-block", "margin-left":"2em", 
                                        "font-size":"16px", "font-weight":"bold"}),
              dcc.Dropdown (id="hornermarkersize", options=[{"label": i, "value": i} for i in range (1, 26, 1)],
                                      style={"width":"50px", "margin-left":"1em"},
                                      value=6, 
                                      clearable=False, disabled=False, multi=False)                          
            ], style={"display":"flex", "flex-direction":"column"}),

            html.Div ([
              html.Label ("AAPG corr.", style={"display":"inline-block", "margin-left":"2em", 
                                        "font-size":"16px", "font-weight":"bold"}),
              dcc.Dropdown (id="aapgmarkersize", options=[{"label": i, "value": i} for i in range (1, 26, 1)],
                                      style={"width":"50px", "margin-left":"1em"},
                                      value=6, 
                                      clearable=False, disabled=False, multi=False)                          
            ], style={"display":"flex", "flex-direction":"column"}),

            html.Div ([
              html.Label ("Harrison", style={"display":"inline-block", "margin-left":"2em", 
                                        "font-size":"16px", "font-weight":"bold"}),
              dcc.Dropdown (id="harrisonmarkersize", options=[{"label": i, "value": i} for i in range (1, 26, 1)],
                                      style={"width":"50px", "margin-left":"1em"},
                                      value=6, 
                                      clearable=False, disabled=False, multi=False)                          
            ], style={"display":"flex", "flex-direction":"column"}),
          ], style={"display":"flex", "flex-direction":"row"}),

          html.Div ([
            html.Label ("THEMES", style={"display":"inline-block", "margin-left":"2em", 
                                        "font-size":"16px", "font-weight":"bold"}),
            dcc.Dropdown (id="templates0", options=[{"label": i, "value": i} for i in templates],
                                      style={"width":"150px", "margin-left":"1em"},
                                      value="plotly", 
                                      clearable=False, disabled=False, multi=False)
          ], style={"display":"flex", "align-items":"center", "margin-top":"1em"}),
        ], style={"width":"400px", "border":"0.1px solid gray", "border-radius":"1em", "margin":"10px 10px","padding":"10px 10px"})
      ], style={"display":"flex", "align-items":"center", "margin-bottom":"4em", "margin-top":"1em"}),    
      
      html.Hr (),
      html.Div ([
            html.Label ("Geothermal Gradient & Heat Flow", style={"display":"inline-block", "font-size":"20px",       "font-weight":"bold", "text-decoration":"none", "color":"#191970", "margin-left":"2em", "letter-spacing":"0.1px"}),
          ], style={"text-align":"left"}),

      html.Div ([
        html.Div ([                          
          dcc.Graph (id="gradient_graph", style={"display":"inline-block", "width":"800px", 
                                                "margin-left":"2em", "margin-top":"2em"})
        ]),

        html.Div ([
          html.Div ([
            html.Label ("STYLES", style={"display":"inline-block", "margin-left":"2em", 
                                        "font-size":"18px", "font-weight":"bold"}),
          ], style={"text-align":"center"}),

          html.Div ([
            html.Label ("Units", style={"display":"inline-block", "margin-left":"2em", 
                                        "font-size":"16px", "font-weight":"bold"}),
            dcc.RadioItems (id="gradient_units", options=[
                            {"label":"Geothermal Gradient (C/km)", "value":"Gradient"}, 
                            {"label":"Heat Flow (mW/km2)", "value":"Flow"}], value="Gradient",
                            labelStyle={"display":"inline-block", "margin-left":"2.5em"})
          ]),

          html.Div ([
            html.Label ("Colour", style={"display":"inline-block", "margin-left":"2em", 
                                        "font-size":"16px", "font-weight":"bold"}),
            dcc.Dropdown (id="colourscale2", options=[{"label": i, "value": i} for i in colorscales],
                                      style={"width":"200px", "margin-left":"1em"},
                                      value="plasma", 
                                      clearable=False, disabled=False, multi=False)
          ], style={"display":"flex", "align-items":"center", "margin-top":"1em"}),

          html.Div ([
            html.Label ("Marker Symbol", style={"display":"inline-block", "margin-left":"2em", 
                                        "font-size":"16px", "font-weight":"bold"}),
            dcc.Dropdown (id="markersymbols", options=[{"label": i, "value": i} for i in marker_symbols],
                                      style={"width":"150px", "margin-left":"1em"},
                                      value="circle", 
                                      clearable=False, disabled=False, multi=False)
          ], style={"display":"flex", "align-items":"center", "margin-top":"1em"}),

          html.Div ([
            html.Label ("Marker Size", style={"display":"inline-block", "margin-left":"2em", 
                                        "font-size":"16px", "font-weight":"bold"}),
            dcc.Dropdown (id="markersize", options=[{"label": i, "value": i} for i in range (1, 26, 1)],
                                      style={"width":"50px", "margin-left":"1em"},
                                      value=6, 
                                      clearable=False, disabled=False, multi=False)
          ], style={"display":"flex", "align-items":"center", "margin-top":"1em"}),

          html.Div ([
            html.Label ("Themes", style={"display":"inline-block", "margin-left":"2em", 
                                        "font-size":"16px", "font-weight":"bold"}),
            dcc.Dropdown (id="templates", options=[{"label": i, "value": i} for i in templates],
                                      style={"width":"150px", "margin-left":"1em"},
                                      value="plotly", 
                                      clearable=False, disabled=False, multi=False)
          ], style={"display":"flex", "align-items":"center", "margin-top":"1em"}),
        ], style={"border":"0.1px solid gray", "border-radius":"1em", "margin":"10px 10px","padding":"10px 10px"}),
      ], style={"display":"flex", "align-items":"center", "margin-bottom":"4em"}),

      html.Hr (),
      html.Div ([
          html.Label ("Well Based Profiles", style={"display":"inline-block", "font-size":"20px", "font-weight":"bold", "text-decoration":"none", "color":"#191970", "margin-left":"2em", "letter-spacing":"0.1px"}),
      ], style={"text-align":"left"}),

      html.Div ([
        html.Div ([
          dcc.Graph (id="wells_graph", style={"display":"inline-block", "width":"800px", 
                                                  "margin-left":"2em", "margin-top":"2em"})
        ]),

        html.Div ([
          html.Div ([
            html.Label ("STYLES", style={"display":"inline-block", "margin-left":"2em", 
                                        "font-size":"18px", "font-weight":"bold"}),
          ], style={"text-align":"center"}),

          html.Div ([
            html.Label ("Units", style={"display":"inline-block", "margin-left":"2em", 
                                        "font-size":"16px", "font-weight":"bold"}),
            dcc.RadioItems (id="wells_units", options=[{"label":"Celcius (C)", "value":"Celcius"}, 
                                  {"label":"Fahrenheit (F)", "value":"Fahrenheit"}], value="Celcius",
                                  labelStyle={"display":"inline-block", "margin-left":"2.5em"})
          ]),

          html.Div ([
            html.Label ("Wellname", style={"display":"inline-block", "margin-left":"2em", 
                                        "font-size":"16px", "font-weight":"bold"}),
            dcc.Dropdown (id="wellname", options=[{"label": i, "value": i} for i in wells1["Wellname"]],
                                      style={"width":"200px", "margin-left":"1em"},
                                      value="ADA-1",  
                                      clearable=False, disabled=False, multi=False)
          ], style={"display":"flex", "align-items":"center", "margin-top":"1em"}),

          html.Div ([
            html.Label ("Colour", style={"display":"inline-block", "margin-left":"2em", 
                                        "font-size":"16px", "font-weight":"bold"}),
            dcc.Dropdown (id="wells_colourscale", options=[{"label": i, "value": i} for i in colorscales],
                                      style={"width":"200px", "margin-left":"1em"},
                                      value="thermal", 
                                      clearable=False, disabled=False, multi=False)
          ], style={"display":"flex", "align-items":"center", "margin-top":"1em"}),

          html.Div ([
            html.Label ("Marker Symbol", style={"display":"inline-block", "margin-left":"2em", 
                                        "font-size":"16px", "font-weight":"bold"}),
            dcc.Dropdown (id="wellsmarkersymbols", options=[{"label": i, "value": i} for i in marker_symbols],
                                      style={"width":"150px", "margin-left":"1em"},
                                      value="circle", 
                                      clearable=False, disabled=False, multi=False)
          ], style={"display":"flex", "align-items":"center", "margin-top":"1em"}),

          html.Div ([
            html.Label ("Marker Size", style={"display":"inline-block", "margin-left":"2em", 
                                        "font-size":"16px", "font-weight":"bold"}),
            dcc.Dropdown (id="wellsmarkersize", options=[{"label": i, "value": i} for i in range (1, 26, 1)],
                                      style={"width":"50px", "margin-left":"1em"},
                                      value=6, 
                                      clearable=False, disabled=False, multi=False)
          ], style={"display":"flex", "align-items":"center", "margin-top":"1em"}),

          html.Div ([
            html.Label ("Themes", style={"display":"inline-block", "margin-left":"2em", 
                                        "font-size":"16px", "font-weight":"bold"}),
            dcc.Dropdown (id="wellstemplates", options=[{"label": i, "value": i} for i in templates],
                                      style={"width":"150px", "margin-left":"1em"},
                                      value="plotly", 
                                      clearable=False, disabled=False, multi=False)
          ], style={"display":"flex", "align-items":"center", "margin-top":"1em"})
        ], style={"width":"400px", "border":"0.1px solid gray", "border-radius":"1em", "margin":"10px 10px","padding":"10px 10px"})
      ], style={"display":"flex", "align-items":"center", "margin-bottom":"4em"})
    ]),

    dcc.Tab(label="Map View", children=[
      html.Div ([
        html.Label ("Units", style={"display":"inline-block", "margin-left":"4em", 
                                         "font-size":"16px", "font-weight":"bold"}),
        html.Label ("Depth (m.)", style={"display":"inline-block", "margin-left":"23em", 
                                         "font-size":"16px", "font-weight":"bold"}),
        html.Label ("Colourscale", style={"display":"inline-block", "margin-left":"22em", 
                                         "font-size":"16px", "font-weight":"bold"})                                                                  
      ], style={"display":"flex", "align-items":"center", "margin-top":"2em"}),

      html.Div ([
        dcc.Dropdown (id="map_units", options=[{"label": i, "value": i} for i in map_values], value="Temperature (C)",
                            style={"width":"350px", "margin-left":"2em"}, clearable=False),
        dcc.Dropdown (id="map_depthscale", options=[{"label": i, "value": i} for i in depth_values],
                                  style={"width":"350px", "margin-left":"3em"}, clearable=False,
                                  value="500", 
                                  ),
        dcc.Dropdown (id="map_colourscale", options=[{"label": i, "value": i} for i in colorscales],
                                  style={"width":"350px", "margin-left":"3em"}, clearable=False,
                                  value="icefire", 
                                  )
      ], style={"display":"flex", "align-items":"center", "margin-top":"1em"}),

      html.Div ([                                                                           
        dcc.Graph (id="map_view", style={"display":"inline-block", "width":"90%", 
                                         "height":"700px", "margin-left":"2em", "margin-top":"2em"})                                                   
      ], style={"margin-top":"1em"})  
    ])
  ], style={"width":"50em", "margin-left":"2em", "margin-top":"2.5em", "border-radius":"20em"})  
], style={"background-color":"lightgray"})

# App Callback Functions #
# Overview Tab #
@app.callback (
  Output("pie-chart", "figure"),
  Input ("horner_colour", "value")   
)

def pie_chart_update (colors):
  fig0 = go.Figure (data=[go.Pie(labels=pie1["Method"], values=pie1["Number"], hole=0.2)])
  fig0.update_layout (title="Methods Used")
  fig0.update_traces (marker=dict(colors=px.colors.sequential.RdBu))

  return fig0

@app.callback (
  Output("depth-chart", "figure"),
  Input ("horner_colour", "value")   
)

def depth_figure_update (colour):
  fig2 = go.Figure ()
  fig2.add_trace(go.Scatter(x=wells1["Wellname"], y=wells1["Depth"], fill='tozeroy', fillcolor = "navy",
                    mode="lines", line=dict(width=0.3, color='black')))
  # fillcolor = "rgb(111, 231, 219)"                  
  fig2.update_layout(title = "Wells vs. TD(m.)")
  fig2.update_yaxes (title="MD (m.)", autorange="reversed")
  fig2.update_xaxes ()

  return fig2                  

@app.callback (
  Output("overview_map", "figure"),
  Input ("horner_colour", "value")   
)

def overview_map_update (value):
  fig4 = px.scatter_mapbox(maps1, lat="Lat", lon="Long", hover_name="Wellname",
                        color_discrete_sequence=["yellow"], zoom=5.5, height=200)
  fig4.update_layout(
    mapbox_style="white-bg",
    mapbox_layers=[
        {
            "below": 'traces',
            "sourcetype": "raster",
            "sourceattribution": "United States Geological Survey",
            "source": [
                "https://basemap.nationalmap.gov/arcgis/rest/services/USGSImageryOnly/MapServer/tile/{z}/{y}/{x}"
            ]
        }
      ]
  )
  fig4.update_layout(margin={"r":0,"t":0,"l":0,"b":0})

  return fig4


# Temperature Comparison Tab #
@app.callback (
     Output("comparison_graph", "figure"),
     [Input ("units", "value"),
     Input ("horner_colour", "value"),
     Input ("aapg_colour", "value"),
     Input ("harrison_colour", "value"),
     Input ("hornermarkersymbols", "value"),
     Input ("aapgmarkersymbols", "value"),
     Input ("harrisonmarkersymbols", "value"),
     Input ("hornermarkersize", "value"),
     Input ("aapgmarkersize", "value"),
     Input ("harrisonmarkersize", "value"),
     Input ("templates0", "value")]   
)

def comparison_update (unit, horner_colour, aapg_colour, harrison_colour, horner_symbol, aapg_symbol, 
                       harrison_symbol, horner_size, aapg_size, harrison_size, template):
  fig1 = go.Figure ()
  if unit == "Celcius":
    fig1.add_trace(go.Scatter (x=comparison["HornerC"], y=comparison["TVDgl"], mode="markers", name="Horner plot method (C)", marker=dict(size=horner_size, color=comparison["HornerC"], colorscale=horner_colour, showscale=True, symbol=horner_symbol, colorbar=dict(title="Horner plot", x=1.05, thickness=20)), text=comparison["Wellname"]))
    fig1.add_trace(go.Scatter (x=comparison["AAPGC"], y=comparison["TVDgl"], mode="markers", name="AAPG correction (C)",    marker=dict(size=aapg_size, color=comparison["AAPGC"], colorscale=aapg_colour, showscale=True, symbol=aapg_symbol, colorbar=dict(title="AAPG corr.", x=1.25, thickness=20)), text=comparison["Wellname"]))
    fig1.add_trace(go.Scatter (x=comparison["HarrC"], y=comparison["TVDgl"], mode="markers", name="Harrison et al.(1983) (C)", marker=dict(size=harrison_size, color=comparison["HarrC"], colorscale=harrison_colour, showscale=True, symbol=harrison_symbol, colorbar=dict(title="Harrison", x=1.45, thickness=20)), text=comparison["Wellname"]))
    fig1.update_xaxes (title="Temperature (C)")   
  elif unit == "Fahrenheit":
    fig1.add_trace(go.Scatter (x=comparison["HornerF"], y=comparison["TVDgl"], mode="markers", name="Horner plot method (F)", marker=dict(size=horner_size, color=comparison["HornerF"], colorscale=horner_colour, showscale=True, symbol=horner_symbol, colorbar=dict(title="Horner plot", x=1.05, thickness=20)), text=comparison["Wellname"]))
    fig1.add_trace(go.Scatter (x=comparison["AAPGF"], y=comparison["TVDgl"], mode="markers", name="AAPG correction (F)",    marker=dict(size=aapg_size, color=comparison["AAPGF"], colorscale=aapg_colour, showscale=True, symbol=aapg_symbol, colorbar=dict(title="AAPG corr.", x=1.25, thickness=20)), text=comparison["Wellname"]))
    fig1.add_trace(go.Scatter (x=comparison["HarrF"], y=comparison["TVDgl"], mode="markers", name="Harrison et al.(1983) (F)", marker=dict(size=harrison_size, color=comparison["HarrF"], colorscale=harrison_colour, showscale=True, symbol=harrison_symbol, colorbar=dict(title="Harrison", x=1.45, thickness=20)), text=comparison["Wellname"]))
    fig1.update_xaxes (title="Temperature (F)")
    
  fig1.update_yaxes (title="TVDgl (m.)", autorange="reversed")
  fig1.update_layout (title="Static Temperature Comparison Graph", font_family="Arial", template=template, 
                      legend=dict (orientation="h",
                                   yanchor="bottom",
                                   y=-0.45,
                                   x=0.5,
                                   xanchor="center"
                                   ))

  return fig1

@app.callback (
     Output("gradient_graph", "figure"),
     [Input ("gradient_units", "value"),
     Input ("colourscale2", "value"), 
     Input ("markersymbols", "value"),
     Input ("markersize", "value"),
     Input ("templates", "value")]   
)

def gradient_comparison (unit, colour, symbol, size, template):
  fig3 = go.Figure ()
  if unit == "Gradient":
    fig3.add_trace(go.Scatter (x=gradients["GG"], y=gradients["TVD"], mode="markers", name="Geothermal Gradients (C/km)", marker=dict(size=size, color=gradients["GG"], colorscale=colour, showscale=True, symbol=symbol), text=gradients["Wellname"]))
    fig3.update_xaxes (title="Geothermal Gradient (C/km)")
    fig3.update_layout (title="Geothermal Gradients Comparison Graph")  
  elif unit == "Flow":
    fig3.add_trace(go.Scatter (x=gradients["HF"], y=gradients["TVD"], mode="markers", name="Heat Flows (mW/km2)", marker=dict(size=size, color=gradients["HF"], colorscale=colour, showscale=True, symbol=symbol), text=gradients["Wellname"]))
    fig3.update_xaxes (title="Heat Flow (mW/km2)")
    fig3.update_layout (title="Heat Flows Comparison Graph")


  fig3.update_yaxes (title="TVDgl (m.)", autorange="reversed")
  fig3.update_layout (font_family="Arial", template=template)

  return fig3

@app.callback (
     Output("wells_graph", "figure"),
     [Input ("wells_units", "value"),
     Input ("wells_colourscale", "value"),
     Input ("wellsmarkersymbols", "value"),
     Input ("wellsmarkersize", "value"),
     Input ("wellstemplates", "value"),
     Input ("wellname", "value")]   
)

def comparison_update (unit, colour, symbol, size, template, wellname):
  fig6 = go.Figure ()
  if unit == "Celcius":
    fig6.add_trace(go.Scatter (x=comparison["HornerC"].loc[comparison["Wellname"]==wellname], y=comparison["TVDgl"].loc[comparison["Wellname"]==wellname], name="Horner plot method (C)", mode="lines+markers", marker=dict(size=size, color=comparison["HornerC"].loc[comparison["Wellname"]==wellname], colorscale=colour, showscale=False, symbol=symbol), text=comparison["Wellname"].loc[comparison["Wellname"]==wellname]))
    fig6.add_trace(go.Scatter (x=comparison["AAPGC"].loc[comparison["Wellname"]==wellname], y=comparison["TVDgl"].loc[comparison["Wellname"]==wellname], name="AAPG correction (C)", mode="lines+markers", marker=dict(size=size, color=comparison["AAPGC"].loc[comparison["Wellname"]==wellname], colorscale=colour, showscale=False, symbol=symbol), text=comparison["Wellname"].loc[comparison["Wellname"]==wellname]))
    fig6.add_trace(go.Scatter (x=comparison["HarrC"].loc[comparison["Wellname"]==wellname], y=comparison["TVDgl"].loc[comparison["Wellname"]==wellname], name="Harrison et al.(1983) (C)", mode="lines+markers", marker=dict(size=size, color=comparison["HarrC"].loc[comparison["Wellname"]==wellname], colorscale=colour, showscale=False, symbol=symbol), text=comparison["Wellname"].loc[comparison["Wellname"]==wellname]))
    fig6.update_xaxes (title="Temperature (C)")   
  elif unit == "Fahrenheit":
    fig6.add_trace(go.Scatter (x=comparison["HornerF"].loc[comparison["Wellname"]==wellname], y=comparison["TVDgl"].loc[comparison["Wellname"]==wellname], name="Horner plot method (F)", mode="lines+markers", marker=dict(size=size, color=comparison["HornerF"].loc[comparison["Wellname"]==wellname], colorscale=colour, showscale=False, symbol=symbol), text=comparison["Wellname"].loc[comparison["Wellname"]==wellname]))
    fig6.add_trace(go.Scatter (x=comparison["AAPGF"].loc[comparison["Wellname"]==wellname], y=comparison["TVDgl"].loc[comparison["Wellname"]==wellname], name="AAPG correction (F)", mode="lines+markers", marker=dict(size=size, color=comparison["AAPGF"].loc[comparison["Wellname"]==wellname], colorscale=colour, showscale=False, symbol=symbol), text=comparison["Wellname"].loc[comparison["Wellname"]==wellname]))
    fig6.add_trace(go.Scatter (x=comparison["HarrF"].loc[comparison["Wellname"]==wellname], y=comparison["TVDgl"].loc[comparison["Wellname"]==wellname], name="Harrison et al.(1983) (F)", mode="lines+markers", marker=dict(size=size, color=comparison["HarrF"].loc[comparison["Wellname"]==wellname], colorscale=colour, showscale=False, symbol=symbol), text=comparison["Wellname"].loc[comparison["Wellname"]==wellname]))
    fig6.update_xaxes (title="Temperature (F)")
    
  fig6.update_yaxes (title="TVDgl (m.)", autorange="reversed")
  fig6.update_layout (title="Temperature Profile of {}".format (wellname), font_family="Arial", template=template,
                      legend=dict (orientation="h",
                                   yanchor="bottom",
                                   y=-0.45,
                                   x=0.45,
                                   xanchor="center"
                                   ))

  return fig6

# Map View Tab #
@app.callback (
     Output("map_view", "figure"),
     [Input ("map_units", "value"),
     Input ("map_depthscale", "value"),
     Input ("map_colourscale", "value"),]      
)

def update_map_view (unit, depth, colour):
  hoverdata = maps1["Wellname"]
  fig5 = go.Figure()
  if unit == "Temperature (C)":
    fig5.add_trace (go.Densitymapbox (lat=maps1["Lat"], lon=maps1["Long"], z=maps1["{}T".format (depth)], colorscale=colour, radius=90, opacity=0.65, name="Temperatures (C)", customdata=hoverdata, hovertemplate="Well: %{customdata}"))
    fig5.update_layout (title="Temperature Map at {}m.".format(depth))
    
  elif unit == "Geothermal Gradient (C/km)":
    fig5.add_trace (go.Densitymapbox (lat=maps1["Lat"], lon=maps1["Long"], z=maps1["{}GR".format (depth)], colorscale=colour, radius=90, opacity=0.65, name="Geothermal Gradients (C/km2)", customdata=hoverdata, hovertemplate="Well: %{customdata}"))
    fig5.update_layout (title="Geothermal Gradient Map at {}m.".format(depth))
    
  elif unit == "Heat Flow (mW/km2)":
    fig5.add_trace (go.Densitymapbox (lat=maps1["Lat"], lon=maps1["Long"], z=maps1["{}HF".format (depth)], colorscale=colour, radius=90, opacity=0.65, name="Heat Flows (mW/km2)", customdata=hoverdata, hovertemplate="Well: %{customdata}"))
    fig5.update_layout (title="Heat Flow Map at {}m.".format(depth))

  fig5.add_trace (go.Scattermapbox(mode = "lines", name="Cyprus Arc",
      lon = [33.52, 33.73, 33.96,	34.09, 34.23, 34.33, 34.5, 34.63, 34.82, 35, 35.13, 35.33, 35.48, 35.73, 36.18, 36.36, 36.57, 36.65, 36.78],
      lat = [34.24,	34.34, 34.38, 34.39, 34.38,	34.4,	34.37, 34.44, 34.48, 34.57,	34.6,	34.76, 34.89,	35.39, 36.18,	36.51,	36.87, 37.08, 37.22],
      line = dict(color="red", width=2)))

  fig5.add_trace (go.Scattermapbox(mode = "lines", name="Misis-Kyrenia Fault Zone",
      lon = [32.91,	33.11, 33.36,	33.49, 33.79,	34.01, 34.37,	34.65, 34.98,	35.35, 35.74,	36.07, 36.37,	36.57],
      lat = [35.38,	35.3,	35.27, 35.26,	35.33, 35.41,	35.55, 35.69,	35.94, 36.41,	36.8,	37, 37.16, 37.19],
      line = dict(color="red", width=2)))

  fig5.add_trace (go.Scattermapbox(mode = "lines", name="Kozan Fault Zone", 
      lon = [33.91,	34.05, 34.2, 34.37,	34.63, 34.86,	35.24, 35.6, 35.81,	36.01],
      lat = [36.04, 36.09, 36.18,	36.23, 36.57,	36.75, 37.12,	37.33, 37.4, 37.41],
      line = dict(color="red", width=2)))
  
  fig5.update_layout (mapbox_style="stamen-terrain", mapbox=dict(center=dict(lat=36.8, lon=36), zoom=6.5),
                      legend=dict (x=0,
                                   y=1,
                                   traceorder="reversed",
                                   title_font_family="Arial",
                                   font=dict(
                                      family="Arial",
                                      size=14,
                                      color="black"
                                   ),
                                   bgcolor="LightSteelBlue",
                                   bordercolor="Black",
                                   borderwidth=1))
  fig5.update_traces (showlegend=True)

  return fig5


# App Launching Codes #
if __name__ == "__main__":
  app.run_server(debug=False)