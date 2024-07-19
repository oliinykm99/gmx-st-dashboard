import plotly.graph_objects as go
import plotly.express as px
import streamlit as st
import textwrap

def display_metrics(metrics):
        cols = st.columns(len(metrics))
        for col, metric in zip(cols, metrics):
            col.metric(label=f"**{metric['label']}**", value=metric['value'], delta=metric['delta'], help=metric['help'])

def plot_general(df, time_col, value_col, xlabel, ylabel, title, annotate=None):
    fig = px.line(df, x=time_col, y=value_col, title=title)
    fig.update_xaxes(title=xlabel, tickangle=-45,
                     showgrid=True, gridwidth=1,
                     gridcolor='lightgray', tickformat='%Y-%m-%d')
    fig.update_yaxes(title=ylabel, showgrid=True, gridwidth=1, gridcolor='lightgray')
    fig.update_layout(title_font=dict(size=20), width=1600, height=550)

    if annotate:
        wrapped_text = "<br>".join(textwrap.wrap(annotate, width=80))
        annotation = go.layout.Annotation(
            x=df[time_col].iloc[0],
            y=1,  
            xref='x',
            yref='paper',  
            text='Additional Information',
            showarrow=False,
            align='left',
            xanchor='left',  
            yanchor='bottom',  
            hovertext=wrapped_text,
            hoverlabel=dict(bgcolor="white", font_size=12)
        )
        fig.update_layout(annotations=[annotation])

    st.plotly_chart(fig)

def plot_general_bar(df, time_col, value_col, bar_col, xtitle, ytitle, ylabel1, ylabel2, title):
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=df[time_col], 
        y=df[value_col],
        mode='lines', 
        name=xtitle,
        line=dict(color='darkblue'),
        yaxis='y1'
    ))
    fig.add_trace(go.Bar(
        x=df[time_col], 
        y=df[bar_col],
        name=ytitle, 
        marker_color='red', 
        opacity=0.5,
        yaxis='y2'
    ))
    fig.update_layout(
        title=title,
        xaxis=dict(tickangle=-45, tickformat='%Y-%m-%d'),
        yaxis=dict(title=ylabel1),
        yaxis2=dict(
            title=ylabel2,
            overlaying='y',
            side='right'
        ),
        title_font=dict(size=20),
        legend=dict(x=0, y=1.0),
        xaxis_showgrid=True, 
        yaxis_showgrid=False,  
        xaxis_gridcolor='lightgrey', 
        yaxis_gridcolor='lightgrey',
        width=1600, 
        height=550
    )

    st.plotly_chart(fig)

def plot_bar_chart(df, time_col, column_name, xaxis_title, yaxis_title, title, annotate=None, legend=False):
    fig = px.bar(df, x='date', y=column_name, color='symbol', title=title, labels={column_name: yaxis_title, 'date': xaxis_title})
    fig.update_layout(
        hovermode='closest',
        plot_bgcolor='rgba(0,0,0,0)',
        xaxis=dict(
            showgrid=True,  
            gridcolor='rgba(0,0,0,0.1)',  
            gridwidth=1,
            tickangle=-45, tickformat='%Y-%m-%d'),
        yaxis=dict(
            showgrid=True, 
            gridcolor='rgba(0,0,0,0.1)', 
            gridwidth=1
        ),
        title_font=dict(size=20),
        width=1600, 
        height=550,
        showlegend=legend
    )
    if annotate:
        wrapped_text = "<br>".join(textwrap.wrap(annotate, width=80))
        annotation = go.layout.Annotation(
            x=df['timestamp'].iloc[0],
            y=1,  
            xref='x',
            yref='paper',  
            text='Additional Information',
            showarrow=False,
            align='left',
            xanchor='left',  
            yanchor='bottom',  
            hovertext=wrapped_text,
            hoverlabel=dict(bgcolor="white", font_size=12)
        )
        fig.update_layout(annotations=[annotation])
    st.plotly_chart(fig)

def plot_percentage_bar_chart(df, time_col, long_col, short_col, xaxis_title, yaxis_title, title, annotate=None, legend=False):
    df_melted = df.melt(id_vars=[time_col], value_vars=[long_col, short_col], var_name='PositionType', value_name='Percentage')
    fig = px.bar(df_melted, x=time_col, y='Percentage', color='PositionType', title=title, labels={'Percentage': yaxis_title, time_col: xaxis_title})
    fig.update_layout(
        hovermode='closest',
        plot_bgcolor='rgba(0,0,0,0)',
        xaxis=dict(
            showgrid=True,  
            gridcolor='rgba(0,0,0,0.1)',  
            gridwidth=1,
            tickangle=-45, tickformat='%Y-%m-%d'
        ),
        yaxis=dict(
            showgrid=True, 
            gridcolor='rgba(0,0,0,0.1)', 
            gridwidth=1
        ),
        title_font=dict(size=20),
        width=1600, 
        height=550,
        showlegend=legend
    )
    if annotate:
        wrapped_text = "<br>".join(textwrap.wrap(annotate, width=80))
        annotation = go.layout.Annotation(
            x=df[time_col].iloc[0],
            y=1,  
            xref='x',
            yref='paper',  
            text='Additional Information',
            showarrow=False,
            align='left',
            xanchor='left',  
            yanchor='bottom',  
            hovertext=wrapped_text,
            hoverlabel=dict(bgcolor="white", font_size=12)
        )
        fig.update_layout(annotations=[annotation])
    st.plotly_chart(fig)