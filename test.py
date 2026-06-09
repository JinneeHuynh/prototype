import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px

# Cấu hình trang (phải là lệnh Streamlit đầu tiên)
st.set_page_config(page_title="Dashboard Doanh Thu Mẫu", layout="wide")

# --- Tiêu đề chính của dashboard ---
st.title("📊 Dashboard Phân Tích Doanh Thu")

# --- 1. Tạo dữ liệu mẫu (hoặc tải từ file CSV) ---
@st.cache_data
def load_data():
    np.random.seed(42)
    dates = pd.date_range(start='2024-01-01', periods=200, freq='D')
    sales = np.random.randint(100, 1000, size=200)
    regions = np.random.choice(['Miền Bắc', 'Miền Trung', 'Miền Nam'], size=200)
    products = np.random.choice(['Sản phẩm A', 'Sản phẩm B', 'Sản phẩm C'], size=200)
    df = pd.DataFrame({'Ngày': dates, 'Doanh số': sales, 'Khu vực': regions, 'Sản phẩm': products})
    return df

df = load_data()

# --- 2. Sidebar: Nơi chứa các bộ lọc ---
st.sidebar.header("🔍 Bộ lọc dữ liệu")
selected_regions = st.sidebar.multiselect(
    "Chọn Khu vực",
    options=df['Khu vực'].unique(),
    default=df['Khu vực'].unique()
)

selected_products = st.sidebar.multiselect(
    "Chọn Sản phẩm",
    options=df['Sản phẩm'].unique(),
    default=df['Sản phẩm'].unique()
)

# Bộ lọc khoảng thời gian
col_date1, col_date2 = st.sidebar.columns(2)
with col_date1:
    start_date = st.date_input("Từ ngày", df['Ngày'].min())
with col_date2:
    end_date = st.date_input("Đến ngày", df['Ngày'].max())

# --- 3. Áp dụng bộ lọc vào dữ liệu ---
filtered_df = df[
    (df['Khu vực'].isin(selected_regions)) &
    (df['Sản phẩm'].isin(selected_products)) &
    (df['Ngày'] >= pd.to_datetime(start_date)) &
    (df['Ngày'] <= pd.to_datetime(end_date))
]

# --- 4. Hiển thị các chỉ số KPI ---
# Tạo 3 cột để hiển thị số liệu
col1, col2, col3 = st.columns(3)

with col1:
    total_sales = filtered_df['Doanh số'].sum()
    st.metric("💰 Tổng doanh thu", f"{total_sales:,.0f} VNĐ")

with col2:
    avg_sales = filtered_df['Doanh số'].mean()
    st.metric("📈 Doanh thu trung bình/ngày", f"{avg_sales:,.0f} VNĐ")

with col3:
    total_orders = len(filtered_df)
    st.metric("🧾 Tổng số giao dịch", f"{total_orders:,}")

# --- 5. Vẽ biểu đồ ---
st.divider() # Vẽ một đường kẻ phân cách
st.subheader("📈 Xu hướng Doanh thu theo thời gian")

# Tạo biểu đồ đường (line chart) với Plotly
revenue_trend = filtered_df.groupby('Ngày')['Doanh số'].sum().reset_index()
fig_line = px.line(revenue_trend, x='Ngày', y='Doanh số', title="Doanh thu hàng ngày")
st.plotly_chart(fig_line, use_container_width=True)

# Tạo 2 cột cho biểu đồ so sánh
col_chart1, col_chart2 = st.columns(2)

with col_chart1:
    st.subheader("🏆 Doanh thu theo Sản phẩm")
    product_sales = filtered_df.groupby('Sản phẩm')['Doanh số'].sum().reset_index()
    fig_bar = px.bar(product_sales, x='Sản phẩm', y='Doanh số', title="Tổng doanh thu từng sản phẩm")
    st.plotly_chart(fig_bar, use_container_width=True)

with col_chart2:
    st.subheader("🗺️ Doanh thu theo Khu vực")
    region_sales = filtered_df.groupby('Khu vực')['Doanh số'].sum().reset_index()
    fig_pie = px.pie(region_sales, values='Doanh số', names='Khu vực', title="Tỷ lệ đóng góp doanh thu theo khu vực")
    st.plotly_chart(fig_pie, use_container_width=True)

# --- 6. Hiển thị bảng dữ liệu đã lọc ---
st.divider()
st.subheader("📋 Bảng dữ liệu chi tiết")
st.dataframe(filtered_df)