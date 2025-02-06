import dash
import calendar
from dash import dcc
from dash import html
import plotly.express as px
import pandas as pd
from dash.dependencies import Input, Output

def show_plot(gauge_id, name="placeholder"):
  data = pd.read_csv(f"geopandas/ai360_climateviz/lvl_obs/{gauge_id}.csv")
  data_pred = pd.read_csv(f"geopandas/ai360_climateviz/lvl_pred_csv/{gauge_id}.csv")
  data_pred['date'] = pd.to_datetime(data_pred['date'])
  data_pred['day_of_year'] = data_pred['date'].dt.dayofyear
  data_pred_1=data_pred.groupby(["day_of_year"])["lvl_sm_sim"].describe()["mean"]
  data_pred_2=data_pred_1.reset_index()

  data['date'] = pd.to_datetime(data['date'])
  data['day_of_year'] = data['date'].dt.dayofyear
  data_1=data.groupby(["day_of_year"])["lvl_sm"].describe()[["mean","25%","75%"]]
  data_2=data_1.reset_index()
  data=data_2
  data["Уровень воды по предсказаниям ИИ"]=data_pred_2["mean"]
  data["День года"]=data_pred["date"]

  fig = px.line(data, x="День года", y=["mean", "25%", "75%", "Уровень воды по предсказаниям ИИ"], title=f"{name}")
  fig.update_yaxes(title_text='Уровень воды, см')
  return fig
