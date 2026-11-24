import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st

#Konfigurasi
st.set_page_config(page_title="Dashboard Analisis Harga Berlian", layout="wide")
st.markdown(
    """
    <style>
    [class*="st-key-bg_kpi"] {
        background-color: #111A2B;
        border: 2px solid #FFFFFF;
        padding: 16px;
    }
    
    [class*="st-key-bg_bar"] {
        background-color: #111A2B;
        border: 2px solid #FFFFFF;
        padding: 16px;
    }
    
    [class*="st-key-bg_scatter"] {
        background-color: #111A2B;
        border: 2px solid #FFFFFF;
        padding: 16px;
    }
    
    [class*="st-key-bg_heatmap"] {
        background-color: #111A2B;
        border: 2px solid #FFFFFF;
        padding: 16px;
    }
    </style>
    """,
    unsafe_allow_html=True,
)
sns.set_theme(style = "darkgrid")

# Load Data
path = "https://raw.githubusercontent.com/mwaskom/seaborn-data/master/diamonds.csv"

df_dashboard = pd.read_csv(path)


# Fitur Filter
st.sidebar.header("Filter Dashboard")

cut_value = ["Fair", "Good", "Very Good", "Premium", "Ideal"]
selected_cut = st.sidebar.multiselect(
    label="Kualitas Potongan Berlian",
    options=cut_value,
    default=cut_value
)

color_value = ["D", "E", "F", "G", "H", "I", "J"]
selected_color = st.sidebar.multiselect(
    label="Warna Berlian",
    options=color_value,
    default=color_value
)

clarity_value = [
    "I1", "SI2", "SI1", "VS2",
    "VS1", "VVS2", "VVS1", "IF"
]
selected_clarity = st.sidebar.multiselect(
    label="Kejernihan Berlian",
    options=clarity_value,
    default=clarity_value
)

price_value = (
    int(df_dashboard["price"].min()),
    int(df_dashboard["price"].max())
)

selected_price = st.sidebar.slider(
    label="Rentang Harga Berlian ($)",
    min_value=price_value[0],
    max_value=price_value[1],
    value=price_value,
    step=100
)

df_filtered = df_dashboard[
    (df_dashboard["cut"].isin(selected_cut)) &
    (df_dashboard["color"].isin(selected_color)) &
    (df_dashboard["clarity"].isin(selected_clarity)) &
    (df_dashboard["price"].between(
        selected_price[0], selected_price[1]
    ))
]

if df_filtered.empty:
    st.warning(
        "Tidak ada data yang sesuai dengan filter. "
        "Silakan ubah pilihan filter."
    )
    st.stop()


# Membuat Judul Dashboard
st.title("DASHBOARD ANALISIS HARGA BERLIAN")
st.caption("Dashboard Analisis Dataset Diamonds - Praktikum Sains Data")


# Membuat KPI
with st.container(border=True, key="bg_kpi"):

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric(
            "Jumlah Data Berlian",
            f"{len(df_filtered):,}"
        )

    with col2:
        st.metric(
            "Rata-Rata Harga",
            f"${df_filtered['price'].mean():,.2f}"
        )

    with col3:
        st.metric(
            "Harga Tertinggi",
            f"${df_filtered['price'].max():,.0f}"
        )

    with col4:
        st.metric(
            "Rata-Rata Karat",
            f"{df_filtered['carat'].mean():.2f}"
        )


# Persiapan Data Visualisasi
urutan_cut = ["Fair", "Good", "Very Good", "Premium", "Ideal"]

harga_per_cut = (
    df_filtered.groupby("cut", observed=False)["price"]
    .mean()
    .reindex(urutan_cut)
    .dropna()
    .reset_index()
)


# Fungsi Pengaturan Grafik
def atur_grafik(fig, ax, label_x, label_y):

    warna_kartu = "#111A2B"
    warna_teks = "#FFFFFF"
    warna_grid = "#2A3550"

    fig.patch.set_facecolor(warna_kartu)
    ax.set_facecolor(warna_kartu)

    ax.set_xlabel(label_x, color=warna_teks)
    ax.set_ylabel(label_y, color=warna_teks)

    ax.tick_params(colors=warna_teks)

    ax.grid(color=warna_grid)
    ax.set_axisbelow(True)

    for spine in ax.spines.values():
        spine.set_color(warna_grid)


# Membuat Visualisasi Barplot
with st.container(border=True, key="bg_bar"):

    st.markdown("**Rata-Rata Harga Berlian Berdasarkan Kualitas Potongan**")

    fig1, ax1 = plt.subplots()

    sns.barplot(
        data=harga_per_cut,
        x="cut",
        y="price",
        color="#2F80FF",
        ax=ax1
    )

    atur_grafik(
        fig1, ax1,
        "Kualitas Potongan",
        "Rata-Rata Harga ($)"
    )

    for container in ax1.containers:
        ax1.bar_label(
            container,
            fmt="$%.0f",
            color="white",
            fontsize=9,
            padding=3
        )

    st.pyplot(fig1, use_container_width=True)
    plt.close(fig1)


# Membuat Visualisasi Boxplot dan Pie Chart
col_boxplot, col_pie = st.columns(2)


# Visualisasi Boxplot
with col_boxplot:

    with st.container(border=True, key="bg_boxplot"):

        st.markdown("**Distribusi Harga Berlian Berdasarkan Kualitas Potongan**")

        fig2, ax2 = plt.subplots()

        sns.boxplot(
            data=df_filtered,
            x="cut",
            y="price",
            order=urutan_cut,
            color="#2F80FF",
            ax=ax2
        )

        atur_grafik(
            fig2, ax2,
            "Kualitas Potongan",
            "Harga Berlian ($)"
        )

        st.pyplot(fig2, use_container_width=True)
        plt.close(fig2)


# Visualisasi Pie Chart
with col_pie:

    with st.container(border=True, key="bg_pie"):

        st.markdown("**Proporsi Berlian Berdasarkan Kualitas Potongan**")

        jumlah_cut = (
            df_filtered["cut"]
            .value_counts()
            .reindex(urutan_cut)
            .dropna()
        )

        fig3, ax3 = plt.subplots()

        fig3.patch.set_facecolor("#111A2B")
        ax3.set_facecolor("#111A2B")

        ax3.pie(
            jumlah_cut,
            labels=jumlah_cut.index,
            autopct="%1.1f%%",
            startangle=90,
            textprops={"color": "white"},
            wedgeprops={
                "edgecolor": "#111A2B",
                "linewidth": 2
            }
        )

        ax3.axis("equal")

        st.pyplot(fig3, use_container_width=True)
        plt.close(fig3)


# Membuat Visualisasi Histogram dan Heatmap
col_histogram, col_heatmap = st.columns(2)


# Visualisasi Histogram
with col_histogram:

    with st.container(border=True, key="bg_histogram"):

        st.markdown("**Distribusi Frekuensi Harga Berlian**")

        fig4, ax4 = plt.subplots()

        sns.histplot(
            data=df_filtered,
            x="price",
            bins=30,
            color="#2F80FF",
            edgecolor="#FFFFFF",
            ax=ax4
        )

        atur_grafik(
            fig4, ax4,
            "Harga Berlian ($)",
            "Frekuensi"
        )

        st.pyplot(fig4, use_container_width=True)
        plt.close(fig4)

# Visualisasi Heatmap
with col_heatmap:

    with st.container(border=True, key="bg_heatmap"):

        st.markdown("**Heatmap Korelasi Antarvariabel Numerik**")

        kolom_numerik = [
            "carat", "depth", "table",
            "price", "x", "y", "z"
        ]

        korelasi_df = df_filtered[kolom_numerik].corr()

        fig5, ax5 = plt.subplots()

        fig5.patch.set_facecolor("#111A2B")
        ax5.set_facecolor("#111A2B")

        sns.heatmap(
            korelasi_df,
            annot=True,
            fmt=".2f",
            cmap="crest",
            linewidths=1,
            linecolor="#111A2B",
            ax=ax5
        )

        ax5.tick_params(colors="white")

        st.pyplot(fig5, use_container_width=True)
        plt.close(fig5)

# View Dataset
with st.expander("**Dataset Overview**"):

    st.write(
        f"Jumlah baris data: {len(df_filtered):,}"
    )

    st.dataframe(
        df_filtered,
        use_container_width=True
    )