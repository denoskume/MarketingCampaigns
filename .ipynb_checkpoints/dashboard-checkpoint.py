import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import plotly.express as px
import pandas as pd
import dash_bootstrap_components as dbc
from dash import dash_table

# Load the engineered features
file_path = 'data/processed/engineered_features.csv'
df = pd.read_csv(file_path)

# Initialize the Dash app with Bootstrap theme
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

# Define the layout of the dashboard
app.layout = dbc.Container([
    # Navigation Bar
    dbc.NavbarSimple(
        brand="Marketing Campaign Dashboard",
        brand_href="#",
        color="primary",
        dark=True,
        className="mb-4"
    ),
    
    # KPIs
    html.Div([
        html.Div([
            html.H3("Total Customers"),
            html.P(f"{df['CustomerID'].nunique()}")
        ], className="kpi-box"),
        html.Div([
            html.H3("Total Campaigns"),
            html.P(f"{df['Campaign_Acceptance'].sum()}")
        ], className="kpi-box"),
        html.Div([
            html.H3("Acceptance Rate"),
            html.P(f"{df['Campaign_Acceptance'].mean() * 100:.2f}%")
        ], className="kpi-box")
    ], className="kpi-container"),
    
    # Summary Table
    dbc.Row([
        dbc.Col(html.H2("Summary Table"), className="mb-4")
    ]),
    dbc.Row([
        dbc.Col(dash_table.DataTable(
            id='summary-table',
            columns=[{"name": i, "id": i} for i in df.columns],
            data=df.to_dict('records'),
            page_size=10,
            style_table={'overflowX': 'auto'},
            style_cell={'textAlign': 'left'},
            style_header={'backgroundColor': 'rgb(230, 230, 230)', 'fontWeight': 'bold'}
        ))
    ]),
    
    # Interactive Graphs
    dbc.Row([
        dbc.Col(html.H2("Interactive Graphs"), className="mb-4")
    ]),
    dbc.Row([
        dbc.Col(dcc.Dropdown(
            id='feature-dropdown',
            options=[{'label': col, 'value': col} for col in df.columns if col not in ['CustomerID', 'Campaign_Acceptance', 'Last_Purchase_Date']],
            value='Age',
            className="mb-4"
        ))
    ]),
    dbc.Row([
        dbc.Col(dcc.Graph(id='bar-chart')),
        dbc.Col(dcc.Graph(id='pie-chart'))
    ]),
    dbc.Row([
        dbc.Col(dcc.Graph(id='line-chart')),
        dbc.Col(dcc.Graph(id='scatter-plot'))
    ])
], fluid=True)

# Define the callback to update the summary table
@app.callback(
    Output('summary-table', 'data'),
    Input('feature-dropdown', 'value')
)
def update_summary_table(selected_feature):
    summary_df = df.groupby(selected_feature)['Campaign_Acceptance'].agg(['count', 'sum', 'mean']).reset_index()
    summary_df.columns = [selected_feature, 'Total', 'Accepted', 'Acceptance Rate']
    summary_df['Acceptance Rate'] = summary_df['Acceptance Rate'] * 100
    return summary_df.to_dict('records')

# Define the callback to update the bar chart
@app.callback(
    Output('bar-chart', 'figure'),
    Input('feature-dropdown', 'value')
)
def update_bar_chart(selected_feature):
    fig = px.bar(df, x=selected_feature, y='Campaign_Acceptance', color='Campaign_Acceptance', title=f"Bar Chart of {selected_feature}")
    return fig

# Define the callback to update the pie chart
@app.callback(
    Output('pie-chart', 'figure'),
    Input('feature-dropdown', 'value')
)
def update_pie_chart(selected_feature):
    pie_df = df[selected_feature].value_counts().reset_index()
    pie_df.columns = [selected_feature, 'count']
    fig = px.pie(pie_df, values='count', names=selected_feature, title=f"Pie Chart of {selected_feature}")
    return fig

# Define the callback to update the line chart
@app.callback(
    Output('line-chart', 'figure'),
    Input('feature-dropdown', 'value')
)
def update_line_chart(selected_feature):
    fig = px.line(df, x=selected_feature, y='Campaign_Acceptance', title=f"Line Chart of {selected_feature}")
    return fig

# Define the callback to update the scatter plot
@app.callback(
    Output('scatter-plot', 'figure'),
    Input('feature-dropdown', 'value')
)
def update_scatter_plot(selected_feature):
    fig = px.scatter(df, x=selected_feature, y='Campaign_Acceptance', color='Campaign_Acceptance', title=f"Scatter Plot of {selected_feature}")
    return fig

# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)
