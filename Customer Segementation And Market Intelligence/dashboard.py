import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# Set page configuration
st.set_page_config(
    page_title="Customer Segmentation Dashboard",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Load data
@st.cache_data
def load_data():
    rfm = pd.read_csv("data/Online Retail RFM Clusters.csv")
    return rfm

# Main dashboard
def main():
    st.title("🎯 Customer Segmentation and Market Intelligence Platform")
    st.markdown("---")
    
    # Load data
    rfm = load_data()
    
    # Sidebar
    st.sidebar.header("Dashboard Controls")
    
    # Cluster selection
    clusters = sorted(rfm['Cluster'].unique())
    selected_clusters = st.sidebar.multiselect(
        "Select Clusters to Display",
        clusters,
        default=clusters
    )
    
    # Filter data based on selection
    filtered_data = rfm[rfm['Cluster'].isin(selected_clusters)]
    
    # Main metrics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(
            label="Total Customers",
            value=f"{len(filtered_data):,}",
            delta=f"{len(filtered_data) - len(rfm)}" if len(selected_clusters) < len(clusters) else None
        )
    
    with col2:
        avg_monetary = filtered_data['Monetary'].mean()
        st.metric(
            label="Avg Customer Value",
            value=f"${avg_monetary:,.2f}",
            delta=f"${avg_monetary - rfm['Monetary'].mean():,.2f}" if len(selected_clusters) < len(clusters) else None
        )
    
    with col3:
        avg_frequency = filtered_data['Frequency'].mean()
        st.metric(
            label="Avg Purchase Frequency",
            value=f"{avg_frequency:.1f}",
            delta=f"{avg_frequency - rfm['Frequency'].mean():.1f}" if len(selected_clusters) < len(clusters) else None
        )
    
    with col4:
        avg_recency = filtered_data['Recency'].mean()
        st.metric(
            label="Avg Days Since Last Purchase",
            value=f"{avg_recency:.0f}",
            delta=f"{avg_recency - rfm['Recency'].mean():.0f}" if len(selected_clusters) < len(clusters) else None
        )
    
    st.markdown("---")
    
    # Cluster Analysis Section
    st.header("📈 Cluster Analysis")
    
    # Create two columns for charts
    col1, col2 = st.columns(2)
    
    with col1:
        # Cluster size pie chart
        cluster_sizes = filtered_data['Cluster'].value_counts().sort_index()
        fig_pie = px.pie(
            values=cluster_sizes.values,
            names=[f"Cluster {i}" for i in cluster_sizes.index],
            title="Customer Distribution by Cluster",
            color_discrete_sequence=px.colors.qualitative.Set3
        )
        st.plotly_chart(fig_pie, use_container_width=True)
    
    with col2:
        # RFM comparison by cluster
        cluster_means = filtered_data.groupby('Cluster')[['Recency', 'Frequency', 'Monetary']].mean()
        
        fig_bar = go.Figure()
        
        fig_bar.add_trace(go.Bar(
            name='Recency (Days)',
            x=[f"Cluster {i}" for i in cluster_means.index],
            y=cluster_means['Recency'],
            yaxis='y',
            offsetgroup=1
        ))
        
        fig_bar.add_trace(go.Bar(
            name='Frequency',
            x=[f"Cluster {i}" for i in cluster_means.index],
            y=cluster_means['Frequency'],
            yaxis='y2',
            offsetgroup=2
        ))
        
        fig_bar.add_trace(go.Bar(
            name='Monetary ($)',
            x=[f"Cluster {i}" for i in cluster_means.index],
            y=cluster_means['Monetary'],
            yaxis='y3',
            offsetgroup=3
        ))
        
        fig_bar.update_layout(
            title="RFM Metrics by Cluster",
            xaxis=dict(domain=[0, 1]),
            yaxis=dict(title="Recency", title_font=dict(color="blue"), tickfont=dict(color="blue")),
            yaxis2=dict(title="Frequency", title_font=dict(color="red"), tickfont=dict(color="red"), anchor="free", overlaying="y", side="right", position=0.85),
            yaxis3=dict(title="Monetary", title_font=dict(color="green"), tickfont=dict(color="green"), anchor="free", overlaying="y", side="right", position=1),
            legend=dict(x=0.1, y=1)
        )
        
        st.plotly_chart(fig_bar, use_container_width=True)
    
    # Detailed cluster information
    st.header("🎭 Customer Personas")
    
    # Create tabs for each cluster
    if selected_clusters:
        tabs = st.tabs([f"Cluster {i}" for i in selected_clusters])
        
        personas = {
            0: {
                "name": "Loyal Customers",
                "description": "Recent, frequent, and high-spending customers. They are likely your most valuable customers.",
                "recommendations": [
                    "Implement loyalty programs",
                    "Offer exclusive previews of new products",
                    "Provide personalized recommendations",
                    "Ensure excellent customer service to retain them"
                ]
            },
            1: {
                "name": "At-Risk Customers",
                "description": "Customers who purchased long ago, with low frequency and monetary value. They might be at risk of churning.",
                "recommendations": [
                    "Send re-engagement campaigns",
                    "Offer special discounts to encourage repeat purchases",
                    "Conduct surveys to understand their needs",
                    "Implement win-back strategies"
                ]
            },
            2: {
                "name": "VIP Customers",
                "description": "Highly frequent and high-spending customers. These are your 'Whales' or 'VIPs'.",
                "recommendations": [
                    "Provide dedicated account managers",
                    "Offer exclusive high-value products",
                    "Solicit feedback for product development",
                    "Ensure they feel valued with special treatment"
                ]
            }
        }
        
        for i, tab in enumerate(tabs):
            cluster_id = selected_clusters[i]
            cluster_data = filtered_data[filtered_data['Cluster'] == cluster_id]
            persona = personas.get(cluster_id, {"name": "General Segment", "description": "General customer segment", "recommendations": ["Standard marketing campaigns"]})
            
            with tab:
                col1, col2 = st.columns([1, 2])
                
                with col1:
                    st.subheader(f"📊 Cluster {cluster_id} Metrics")
                    st.metric("Customer Count", f"{len(cluster_data):,}")
                    st.metric("Avg Recency", f"{cluster_data['Recency'].mean():.1f} days")
                    st.metric("Avg Frequency", f"{cluster_data['Frequency'].mean():.1f}")
                    st.metric("Avg Monetary", f"${cluster_data['Monetary'].mean():,.2f}")
                
                with col2:
                    st.subheader(f"🎭 {persona['name']}")
                    st.write(persona['description'])
                    
                    st.subheader("💡 Recommendations")
                    for rec in persona['recommendations']:
                        st.write(f"• {rec}")
    
    # RFM Distribution Analysis
    st.header("📊 RFM Distribution Analysis")
    
    # Create subplot for RFM distributions
    col1, col2, col3 = st.columns(3)
    
    with col1:
        fig_recency = px.histogram(
            filtered_data, 
            x='Recency', 
            color='Cluster',
            title="Recency Distribution",
            nbins=30,
            color_discrete_sequence=px.colors.qualitative.Set3
        )
        st.plotly_chart(fig_recency, use_container_width=True)
    
    with col2:
        fig_frequency = px.histogram(
            filtered_data, 
            x='Frequency', 
            color='Cluster',
            title="Frequency Distribution",
            nbins=30,
            color_discrete_sequence=px.colors.qualitative.Set3
        )
        st.plotly_chart(fig_frequency, use_container_width=True)
    
    with col3:
        fig_monetary = px.histogram(
            filtered_data, 
            x='Monetary', 
            color='Cluster',
            title="Monetary Distribution",
            nbins=30,
            color_discrete_sequence=px.colors.qualitative.Set3
        )
        st.plotly_chart(fig_monetary, use_container_width=True)
    
    # Scatter plot matrix
    st.header("🔍 RFM Relationship Analysis")
    
    fig_scatter = px.scatter_matrix(
        filtered_data,
        dimensions=['Recency', 'Frequency', 'Monetary'],
        color='Cluster',
        title="RFM Scatter Plot Matrix",
        color_discrete_sequence=px.colors.qualitative.Set3
    )
    fig_scatter.update_layout(height=600)
    st.plotly_chart(fig_scatter, use_container_width=True)
    
    # Data table
    st.header("📋 Raw Data")
    st.dataframe(filtered_data, use_container_width=True)

if __name__ == "__main__":
    main()

