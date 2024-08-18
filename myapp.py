import pandas as pd
import plotly.express as px
import streamlit as st

st.set_page_config(
    page_title="Consoleflare Analytics Portal",
    page_icon="📊")

st.title(':rainbow[DATA ANALYTICS PORTAL]')
st.subheader(':grey[Explore Data with ease.]', divider="rainbow")

file = st.file_uploader('Drop csv or excel file', type=['csv','xlsx'])
if(file!=None):
    if(file.name.endswith('csv')):
        data=pd.read_csv(file)
    else:
        data = pd.read_excel(file)
    st.dataframe(data)
    st.info('File is successfully uploaded', icon="🏁")

    st.subheader(':rainbow[Basic information of the dataset]', divider="rainbow")
    tab1,tab2,tab3,tab4=st.tabs(['Summary','Top And Bottom Rows','Data Types','Columns'])

    with tab1:
        st.write(f'There are {data.shape[0]} rows in dataset and {data.shape[1]} columns in dataset')
        st.subheader(':blue[statistical summary of the dataset]')
        st.dataframe(data.describe())
    with tab2:
        st.subheader(':blue[Top Rows]')
        toprows=st.slider(':green[Number of rows you want]',1,data.shape[0],key='topslider')
        st.dataframe(data.head(toprows))
        st.subheader(':blue[Bottom Rows]')
        bottomrows = st.slider(':green[Number of rows you want]', 1, data.shape[0],key='bottomslider')
        st.dataframe(data.tail(bottomrows))
    with tab3:
        st.subheader(':blue[Data types of columns]')
        st.dataframe(data.dtypes)
    with tab4:
        st.subheader(':blue[columns Name in Dataset]')
        st.write(list(data.columns))
    st.subheader(':rainbow[Column Value To Count]',divider='rainbow')
    with st.expander('Value Count'):
        col1,col2=st.columns(2)
        with col1:
            column=st.selectbox('Choose Column Name',options=list(data.columns))
        with col2:
            toprows=st.number_input('Top Rows',min_value=1, step=1)
        count=st.button('Count')
        if(count==True):
            result=data[column].value_counts().reset_index().head(toprows)
            st.dataframe(result)
            st.subheader('Visualization',divider='green')
            tab1, tab2, tab3= st.tabs(['Bar Chart', 'Line Chart','Pie Chart'])
            with tab1:
                fig = px.bar(data_frame=result, x=column, y='count', text='count', template='plotly_white')
                st.plotly_chart(fig)
            with tab2:
                fig = px.line(data_frame=result, x=column, y='count', text='count', template='plotly_white')
                st.plotly_chart(fig)
            with tab3:
                fig = px.pie(data_frame=result, names=column, values='count')
                st.plotly_chart(fig)
    st.subheader(':rainbow[Groupby: Simplify Your Data Analysis]', divider='rainbow')
    st.write('The groupby lets you summarize data by specific categories and groups')
    with st.expander('Group By Your Columns'):
        col1, col2, col3 = st.columns(3)
        with col1:
            groupby_cols = st.multiselect('Choose Your Column to Groupby', options=list(data.columns))
        with col2:
            operation_col=st.selectbox("choose column for operation", options=list(data.columns))
        with col3:
            operation=st.selectbox('choose operations', options=['sum','max','min','mean','median','count'])
        if(groupby_cols):
            result=data.groupby(groupby_cols).agg(
                 newcol=(operation_col,operation)
            ).reset_index()
            st.dataframe(result)
            st.subheader(':rainbow[DATA Visualization]',divider='rainbow')
            graphs=st.selectbox('chosse your graphs',options=['line','bar','scatter','pie','sunburst'])
            if(graphs== 'line'):
                x_axis = st.selectbox('choose x axis', options=list(result.columns))
                y_axis = st.selectbox('choose y axis', options=list(result.columns))
                color = st.selectbox('color information',options=[None]+list(result.columns))
                fig=px.line(data_frame=result,x=x_axis,y=y_axis,color=color,markers='o')
                st.plotly_chart(fig)
            elif(graphs=='bar'):
                x_axis = st.selectbox('choose x axis', options=list(result.columns))
                y_axis = st.selectbox('choose y axis', options=list(result.columns))
                color = st.selectbox('color information', options=[None] + list(result.columns))
                facet_col=st.selectbox('column information',options=[None] + list(result.columns))
                fig = px.bar(data_frame=result, x=x_axis, y=y_axis, color=color, facet_col=facet_col,barmode='group')
                st.plotly_chart(fig)
            elif(graphs == 'scatter'):
                x_axis = st.selectbox('choose x axis', options=list(result.columns))
                y_axis = st.selectbox('choose y axis', options=list(result.columns))
                color = st.selectbox('color information', options=[None] + list(result.columns))
                size=st.selectbox('size column',options=[None] + list(result.columns))
                fig = px.scatter(data_frame=result, x=x_axis, y=y_axis, color=color,size=size)
                st.plotly_chart(fig)
            elif(graphs == 'pie'):
                values = st.selectbox('choose numerical values',options=list(result.columns))
                names  = st.selectbox('choose labels', options=list(result.columns))
                fig = px.pie(data_frame=result, values=values,names=names)
                st.plotly_chart(fig)
            elif(graphs =='sunburst'):
                path = st.multiselect('choose your path',options=list(result.columns))
                fig = px.sunburst(data_frame=result,path=path, values='newcol')
                st.plotly_chart(fig)







   




