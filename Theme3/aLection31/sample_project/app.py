import pandas as pd
import dash
from dash import dcc, html
import plotly.express as px
from flask import Flask
import plotly.graph_objects as go

# Завантаження бойових звітів
df = pd.read_csv("combat_reports.csv")
df["date"] = pd.to_datetime(df["date"])  # Конвертуємо дату у відповідний формат

# Створення Flask-сервера
server = Flask(__name__)

# Ініціалізація Dash
app = dash.Dash(__name__, server=server)

# Побудова графіків
df_region_counts = df["region"].value_counts().reset_index()
df_region_counts.columns = ["region", "num_attacks"]
df_region_counts["num_attacks"] = df_region_counts["num_attacks"].astype(int)  # Ensure integer type




fig_attacks_by_region = go.Figure()

# Add a bar chart trace
fig_attacks_by_region.add_trace(go.Bar(
    x=df_region_counts["region"].tolist(),
    y=df_region_counts["num_attacks"].tolist(),
    text=df_region_counts["num_attacks"].tolist(),  # Show numbers on bars
    textposition='auto',
    marker=dict(color=["#636efa", "#EF553B", "#00cc96", "#ab63fa"])  # Assign different colors
))

# Update layout
fig_attacks_by_region.update_layout(
    title="Кількість атак за регіонами",
    xaxis_title="Регіон",
    yaxis_title="Кількість атак"
)

fig_attacks_by_type = px.pie(df, names="attack_type", title="Розподіл атак за типами")

fig_attacks_over_time = px.line(df.groupby("date")["num_casualties"].sum().reset_index(),
                                x="date", y="num_casualties",
                                title="Динаміка бойових втрат у часі")

# Структура веб-інтерфейсу
app.layout = html.Div(children=[
    html.H1(children="Аналіз бойової активності", style={"textAlign": "center"}),

    dcc.Graph(id="attacks_by_region", figure=fig_attacks_by_region),
    dcc.Graph(id="attacks_by_type", figure=fig_attacks_by_type),
    dcc.Graph(id="attacks_over_time", figure=fig_attacks_over_time),
])

# Запуск веб-сервера
if __name__ == "__main__":
    app.run_server(debug=True)
