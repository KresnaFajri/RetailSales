import streamlit as st
import seaborn as sns
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import plotly.express as px


#Baca Dataset
df = pd.read_csv('D:\My AI Project\Retail Sales Analysis\Clean Dataset.csv')
#Setting ukuran layout
st.set_page_config(
    page_title = 'Retail Sales Analysis',
    page_icon = '✅',
    layout = 'wide'
)
st.title('Retail Sales Dashboard :moneybag:')
#Buat placeholder 
placeholder = st.empty()
#Definisikan fungsi filter untuk mengambil dataset
def filter(dataset,category):
    return df[df['Product Category'] == category]

#Definisikan kolom dari masing-masing produk
beauty_df = filter(df,'Beauty')
elect_df = filter(df,'Electronic')
cloth_df = filter(df,'Clothing')

#Format urutan bulan
month_order = ['January','February','March', 'April', 'May', 'June','July','August','September', 'October','November','December']

#Atur format bulan agar datanya sesuai
df['Month'] = pd.Categorical(df['Month'], categories = month_order, ordered = True)

#Mengurutkan datanya berdasarkan kolom bulan
df = df.sort_values(by='Month')

#Buat metric untuk ditampilkan pada dashboard
total_transaction = df['Transaction ID'].count()

high_rev = np.max(df['Total Amount'])

mean_rev = np.mean(df['Total Amount'])



with placeholder.container(border = True):
    #Buat 3 kolom
    plot1,plot2,plot3 = st.columns(3)

    #isi dengan metrik. 
    st.markdown("""
<style>
[data-testid="stMetricValue"] {
    font-size: 60px;
}
</style>
""", unsafe_allow_html=True)
with st.container(border =True):
    plot1.metric(label='Rata-Rata Pendapatan', value = f'${round(mean_rev,2)}')
    plot2.metric(label='Total Pendapatan', value = f'${round(high_rev,2)}')
    plot3.metric(label='Total Transaksi',value=total_transaction)



#with placeholder.container(border = True):
 #   col1,col2,col3 = st.columns(3)
    #sns.set_theme(style='darkgrid')
    #plt.rcParams['figure.facecolor'] = 'black'
    #plt.rcParams['axes.facecolor'] = 'black'
    st.markdown("""
    <style>
    .stContainer{
        background-color:#a0a0a0;
                padding: 10px;
                border_radius:60px}
                </style>
                """,unsafe_allow_html=True)
   # plt.figure(figsize=(30,30))
    
#Definisikan baris ke dua.
with st.container(border = True):
    col1,col2,col6 = st.columns(3)
    with col1:
        st.subheader('Fluktuasi Harga Barang per Produk')
        fig = px.area(df,x = 'Month', y ='Price per Unit', color = 'Product Category')
        st.plotly_chart(fig)
    
    #plot 5, Total Pendapatan per ,col6Bulan
    with col2:
        st.subheader('Total Pendapatan Toko per Bulan')
        plt.figure(figsize=(40,40))
        sales_by_month = df.groupby('Month')['Total Amount'].sum()
        sales_df = sales_by_month.to_frame(name='Total Amount')
        sales_df = sales_df.reset_index()
        st.bar_chart(data = sales_df, x = 'Month', y = 'Total Amount')

    #Plot 6
    with col6:
            st.subheader('Grafik Kuantitas Pembelian Barang berdasarkan Gender')
            df['Month'] = pd.Categorical(df['Month'], categories = month_order, ordered = True)
            sale_by_gender = df.groupby(['Gender', 'Month'])['Quantity'].sum().reset_index()
            fig = px.bar(sale_by_gender, x = 'Month', y='Quantity', color = 'Gender', barmode='group',
                 color_discrete_map={'Male':'blue', 'Female':'orange'})
            st.plotly_chart(fig)
with st.container(border = True):
    col3,col5,col4= st.columns(3)
    with col3:
        st.markdown("""
    <style>
    .st-column {
        border: 1px solid #ccc;
        padding: 10px;
        border-radius:10px;
    }
    </style>
    """, unsafe_allow_html=True)
        unique_category = df["Product Category"].unique()
        #Visualisasikan kuantitas dari tiap kategori
        quantity_each_category = df.groupby('Product Category')['Quantity'].sum()
        quantity_df = quantity_each_category.to_frame()
        quantity_df = quantity_df.reset_index()

        #Buat visualisasi datanya
        plt.figure(figsize=(40,40))
        fig = px.pie(quantity_df,values = 'Quantity', names ='Product Category', title='Kuantitas Kategori Barang yang Habis Terjual')
        st.plotly_chart(fig)

    with col5:
        gender = df['Gender'].unique()
        gender_count = df['Gender'].value_counts()
        gender_count_df = gender_count.to_frame().reset_index()
        fig = px.pie(gender_count_df, values = 'count',names='Gender', title='Perbandingan Jumlah Gender yang Berbelanja di Toko')
        st.plotly_chart(fig)

    with col4:
        st.markdown("""
    <style>
    .st-column {
        border: 1px solid #ccc;
        padding: 10px;
    }
    </style>
    """, unsafe_allow_html=True)
    #Plot 4, Kuantitas yang terjual tiap Bulan
    #Kumpulkan data berdasarkan bulan, jenis produk dan juga kuantitas barang yang terjual
        sales_by_month_category = df.groupby(['Month', 'Product Category'])['Quantity'].sum().unstack()
    #buat persentase penjualan
        sales_percentage_df = sales_by_month_category.div(sales_by_month_category.sum(axis = 1),axis = 0)
        sales_percentage_df = sales_percentage_df.reset_index()
    #Buat visualisasinya dalam bentuk stacked bar di dalam container streamlit
        st.subheader('Persentase Penjualan tiap Kategori per Bulan')
        fig = px.bar(sales_percentage_df, x = 'Month', y= ['Beauty', 'Clothing', 'Electronics'], orientation = 'v',barmode = 'stack')
        st.plotly_chart(fig)

with st.container(border =True):
        st.subheader('Distribusi Umur Masing-Masing Pelanggan')
        st.bar_chart(df['Age'].value_counts())



