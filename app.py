import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import streamlit as st
import seaborn as sns
from streamlit_plotly_events import plotly_events
import plotly.graph_objects as go
from plotly.subplots import make_subplots


st.set_page_config(layout='wide')
#########Code back##########

col1, col2, col3 = st.columns(3)

with col1:
    st.image('Bunge_Logo.png')

with col2:
    st.title('')

with col3:
    st.image('logo_wild.png')


st.markdown("<h1 style='text-align: center; color: #12326d;'>DAILY VARIANCE</h1>", unsafe_allow_html=True)


uploaded_file = st.file_uploader("Upload a file")

if uploaded_file:
    xls = pd.ExcelFile(uploaded_file)
    df1 = pd.read_excel(xls, '20 06')
    df2 = pd.read_excel(xls, '21 06')
    df3 = pd.read_excel(xls, '22 06')
    #df1['FileName'] = 'df1'
    #df2['FileName'] = 'df2'
    #df3['FileName'] = 'df3'
    df = pd.concat([df1, df2, df3], keys=['df1', 'df2', 'df3'], ignore_index=True)
    df['Position Date'] = pd.to_datetime(df['Position Date'])

    df_grouped = df.groupby(['Material','MTM Doc Type']).sum()

    df_grouped_unstacked = df_grouped.unstack()
    df_grouped_unstacked = df_grouped_unstacked['MTM Quantity']
    df_grouped_unstacked.fillna(0, inplace=True)
    df_grouped_unstacked['Operation'] = df_grouped_unstacked['Purchase'] + df_grouped_unstacked['Inventory'] + df_grouped_unstacked['Sales']

    df_grouped1 = df1.groupby(['Material','MTM Doc Type']).sum()
    df_grouped_unstacked1 = df_grouped1.unstack()
    df_grouped_unstacked1 = df_grouped_unstacked1['MTM Quantity']
    df_grouped_unstacked1.fillna(0, inplace=True)
    df_grouped_unstacked1['Operation'] = df_grouped_unstacked1['Purchase'] + df_grouped_unstacked1['Inventory'] + df_grouped_unstacked1['Sales']

    df_grouped2 = df2.groupby(['Material','MTM Doc Type']).sum()
    df_grouped_unstacked2 = df_grouped2.unstack()
    df_grouped_unstacked2 = df_grouped_unstacked2['MTM Quantity']
    df_grouped_unstacked2.fillna(0, inplace=True)
    df_grouped_unstacked2['Operation'] = df_grouped_unstacked2['Purchase'] + df_grouped_unstacked2['Inventory'] + df_grouped_unstacked2['Sales']

    df_grouped3 = df3.groupby(['Material','MTM Doc Type']).sum()
    df_grouped_unstacked3 = df_grouped3.unstack()
    df_grouped_unstacked3 = df_grouped_unstacked3['MTM Quantity']
    df_grouped_unstacked3.fillna(0, inplace=True)
    df_grouped_unstacked3['Operation'] = df_grouped_unstacked3['Purchase'] + df_grouped_unstacked3['Inventory'] + df_grouped_unstacked3['Sales']

    df_grouped_unstacked1 = df_grouped_unstacked1.merge(df_grouped_unstacked2, on='Material', suffixes=('_d1', '_d2'))

    df_grouped_unstacked1 = df_grouped_unstacked1.merge(df_grouped_unstacked3, on='Material', suffixes=('aaa', 'bbb'))
    df_grouped_unstacked1['pct_change'] = df_grouped_unstacked1[['Operation_d2','Operation_d1']].pct_change(axis=1)['Operation_d1']

    df_grouped_unstacked1["Color"] = np.where(df_grouped_unstacked1["Operation_d2"]<0, 'red', 'green')

    ##############################@


    # fig = go.Figure(go.Bar(
    #              x=df_grouped_unstacked1['Operation_d2'],
    #              y=df_grouped_unstacked1.index,
    #              orientation='h',
    #              marker_color=df_grouped_unstacked1['Color']
    #              )) 


    # # fig.update_xaxes(type="log")

    # fig.update_layout(yaxis={'categoryorder':'total ascending'})
    #fig.update_layout(height=1000)

    fig = make_subplots(rows=1, cols=2, shared_yaxes=True)

    fig.add_trace(
        go.Bar(
                x=df_grouped_unstacked1['Operation_d2'],
                y=df_grouped_unstacked1.index,
                orientation='h',
                marker_color=df_grouped_unstacked1['Color']
                ),
        row=1, col=1
    )

    fig.add_trace(
        go.Scatter(
            x=df_grouped_unstacked1['pct_change'],
            y=df_grouped_unstacked1.index,
            orientation='h'
        ),
        row=1, col=2
    )

    #fig.update_layout(height=800)
    fig.update_layout(showlegend=False)

    fig.update_xaxes(title_text="Change compared to the previous day", row=1, col=2)
    fig.update_xaxes(title_text="Risk assesment", row=1, col=1)

    #st.write(selected_points[0]['y'])
    #st.plotly_chart(fig)



    selected_points = plotly_events(fig)

    #st.plotly_chart(fig)

    if selected_points : 
        st.write('Do you want to see a specific transaction type ?')
        Purchase = st.checkbox('Purchase')
        Sale = st.checkbox('Sale')
        #st.dataframe(df_grouped_unstacked1[['Inventory','Inventory_d1','Inventory_d2', 'Purchase','Purchase_d1','Purchase_d2','Sales','Sales_d1','Sales_d2','pct_change']].loc[df_grouped_unstacked1.index==selected_points[0]['y']])
        #st.multiselect('What country do you want to see ?', df_def['Incoterm Loc Country'].unique().tolist())


        if Purchase:
            st.dataframe(df_grouped_unstacked1[['Inventory','Inventory_d1','Inventory_d2', 'Purchase','Purchase_d1','Purchase_d2','pct_change']].loc[df_grouped_unstacked1.index==selected_points[0]['y']])
        elif Sale:
            st.dataframe(df_grouped_unstacked1[['Inventory','Inventory_d1','Inventory_d2','Sales','Sales_d1','Sales_d2','pct_change']].loc[df_grouped_unstacked1.index==selected_points[0]['y']])
    
        else:
            st.dataframe(df_grouped_unstacked1[['Inventory','Inventory_d1','Inventory_d2', 'Purchase','Purchase_d1','Purchase_d2','Sales','Sales_d1','Sales_d2','pct_change']].loc[df_grouped_unstacked1.index==selected_points[0]['y']])
        
    


