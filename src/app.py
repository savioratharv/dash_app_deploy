from dash import Dash, dcc, html, Input, Output
import plotly.express as px
import numpy as np
import pandas as pd

df=pd.read_excel('Amazon_top100_bestselling_books_2009to2021.xlsx')
df.dropna(axis=0,inplace=True)
l1=df['title'].value_counts()
df1=l1.to_frame(name='count')
df1.index.name='title'
df1['title']=df1.index
df1.reset_index(drop=True, inplace=True)
dff=df[df['title'].isin(df1['title'])]


app = Dash(__name__, external_stylesheets=external_stylesheets)
server = app.server


external_stylesheets = [
    "https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700&display=swap"
]

app.layout = html.Div([
    # dcc.RadioItems(['Fiction', 'Non Fiction'], 'Fiction',id='genre'),
    dcc.Markdown("""[<- Go Back ](https://youtube.com/)"""),
    dcc.Dropdown(['Fiction', 'Non Fiction'],
                     ['Fiction'],
                     id='genre',
                     multi=True),
    # dcc.Markdown("""## Best Selling Books"""),
    html.Div('Best Selling Books', style={'color': '#0058CC','fontSize': 40,'marginLeft':23}),
    # html.P('Example P', className='my-class', id='my-p-element')
    # html.Link('Example P', href = 'https://www.youtube.com'),
    dcc.Graph(id='graph-with-slider',
            hoverData={'points': [{'customdata': 'StrengthsFinder 2.0'}]}),
    
    dcc.Slider(
        df['year'].min(),
        df['year'].max(),
        step=None,
        value=df['year'].max(),
        marks={str(year): str(year) for year in df['year'].unique()},
        id='year-slider'
    ),
    
    html.Div('Rank over the years', style={'color': '#0058CC','fontSize': 40,'marginLeft':23}),
    dcc.Graph(id='graph-dropdown')
],style={'fontFamily':'Inter','letterSpacing':'0.03em'})


@app.callback(
    Output('graph-with-slider', 'figure'),
    Input('year-slider', 'value'),
    Input('genre','value'))


def update_figure(selected_year,genre):
    filtered_df = df[df['year'] == selected_year]
    filtered_df = filtered_df[filtered_df['genre'].isin(genre)]

    # fig = px.scatter(filtered_df.head(20), y="ratings", x="no_of_reviews",
    #                  size="price", color="ranks", hover_name="title",
    #                  log_x=True, size_max=35)
    
    # fig = px.sunburst(filtered_df, path=['genre', 'title'], values='no_of_reviews',
    #               color='ranks', hover_data=['title'],
    #               color_continuous_scale='RdBu', 
    #               color_continuous_midpoint=np.average(100-filtered_df['ranks'], weights=filtered_df['no_of_reviews']))
    
    fig = px.treemap(filtered_df, path=[px.Constant("Books"), 'genre', 'title'], values='no_of_reviews',
                  color='ranks', hover_data=['title'],
                  color_continuous_scale='RdBu',
                  color_continuous_midpoint=np.average(100-filtered_df['ranks'], weights=filtered_df['no_of_reviews']))
    
    fig.update_layout(margin = dict(t=50, l=25, r=25, b=25))
    

    fig.update_layout(transition_duration=100)

    return fig


@app.callback(
    Output('graph-dropdown','figure'),
    Input('graph-with-slider','hoverData'))

def book_fig(hoverData):
    try:
        filtered_df=dff[dff['title'].isin(hoverData['points'][0]['customdata'])]
    except:
        filtered_df=dff[dff['title']==hoverData['points'][0]['customdata']]
    if(len(filtered_df)>3):
        fig=px.line(filtered_df, y="ranks", x='year')
    else:
        fig=px.scatter(filtered_df,x='year',y='ranks',size='no_of_reviews',color='price')
    fig.update_yaxes(autorange="reversed")
    
    return fig


if __name__ == '__main__':
    app.run_server(debug=True, use_reloader=False)