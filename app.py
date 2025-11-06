#Github
#hj

#Dashboard: Evolución de la Edad Media por Departamento
# Versión para GitHub

#Importar librerías
from dash import Dash, dcc, html, Input, Output, dash_table
import dash_bootstrap_components as dbc
import pandas as pd
import plotly.express as px
import dash

#Paso 1: Cargar datos
df = pd.read_excel("edadmedia.xlsx")

#Asegurar que 'Year' sea un número entero
df["Year"] = df["Year"].astype(int)

#Pasar a formato largo (de ancho → largo)
df_long = df.melt(id_vars="Year", var_name="Departamento", value_name="Edad")

#Paso 2: Inicializar app
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
server = app.server  #Necesario para GitHub
app.title = "Evolución de la Edad Media por Departamento"

#Paso 3: Layout
app.layout = html.Div([
    html.H2("Evolución de la Edad Media en Guatemala", 
            style={"textAlign": "center", "marginTop": 20}),

    #Dropdown de departamentos
    html.Div([
        html.Label("Selecciona los departamentos:", style={"fontWeight": "bold"}),
        dcc.Dropdown(
            id="deptos-dropdown",
            options=[{"label": d, "value": d} for d in sorted(df_long["Departamento"].unique())],
            value=["Guatemala", "Quetzaltenango"],  # valores iniciales
            multi=True,
            style={"width": "70%", "margin": "auto"}
        )
    ], style={"textAlign": "center", "marginBottom": 30}),

    #Gráfica principal
    dcc.Graph(id="grafica-lineas", figure={}),

    #Tabla de datos
    html.Div(id="tabla-container", style={"width": "80%", "margin": "auto", "marginTop": 20})
])

#Paso 4: Callback
@app.callback(
    [Output("grafica-lineas", "figure"),
     Output("tabla-container", "children")],
    Input("deptos-dropdown", "value")
)
def actualizar_vista(deptos_seleccionados):
    df_filtrado = df_long[df_long["Departamento"].isin(deptos_seleccionados)]

    #Gráfica de líneas
    fig = px.line(
        df_filtrado,
        x="Year",
        y="Edad",
        color="Departamento",
        markers=True,
        title="Evolución de la Edad Media por Departamento"
    )

    fig.update_traces(mode="lines+markers", line=dict(width=2))
    fig.update_layout(
        xaxis=dict(
            tickmode="linear",
            tick0=df_long["Year"].min(),
            dtick=1
        ),
        xaxis_title="Año",
        yaxis_title="Edad media",
        template="plotly_white",
        legend_title="Departamento",
        hovermode="x unified",
        margin=dict(l=60, r=40, t=80, b=60)
    )

    #Tabla interactiva
    tabla = dash_table.DataTable(
        columns=[{"name": i, "id": i} for i in df_filtrado.columns],
        data=df_filtrado.to_dict("records"),
        page_size=10,
        style_table={"overflowX": "auto"},
        style_header={"backgroundColor": "#007BFF", "color": "white", "fontWeight": "bold"},
        style_cell={"textAlign": "center"}
    )

    return fig, tabla

#Paso 5: Ejecutar app
if __name__ == "__main__":
    app.run(debug=False, host="0.0.0.0", port=10000)
