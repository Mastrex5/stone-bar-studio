import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from app.models.financial_model import FinancialAnalyzer
from app.utils.data_handler import load_invoices

def show_page():
    st.title("💰 Financial Dashboard")
    st.markdown("Track profitability, costs, and subcontractor payouts.")
    
    # Load invoices
    invoices = load_invoices()
    
    if not invoices:
        st.warning("No invoices yet. Create one in the Invoice Generator to see financial data.")
        return
    
    # Initialize analyzer
    analyzer = FinancialAnalyzer(invoices)
    summary = analyzer.get_summary()
    
    st.markdown("---")
    st.subheader("Financial Overview")
    
    # Key Metrics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(
            "Total Revenue",
            f"${summary['total_revenue']:,.2f}",
            delta=f"{len(invoices)} projects"
        )
    
    with col2:
        st.metric(
            "Material Cost",
            f"${summary['total_material_cost']:,.2f}",
            delta=f"-${summary['total_material_cost']:,.2f}"
        )
    
    with col3:
        st.metric(
            "Gross Profit",
            f"${summary['total_profit']:,.2f}",
            delta=f"+{((summary['total_profit'] / summary['total_revenue'] * 100) if summary['total_revenue'] > 0 else 0):.1f}%"
        )
    
    with col4:
        st.metric(
            "Net Profit",
            f"${summary['total_profit'] - summary['management_fee']:,.2f}",
            delta=f"After 10% fee"
        )
    
    st.markdown("---")
    st.subheader("Profit Distribution")
    
    # Distribution breakdown
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric(
            "Management Fee (Dad Tax)",
            f"${summary['management_fee']:,.2f}",
            delta="10% of profit"
        )
    
    with col2:
        st.metric(
            "Subcontractor 1 (The Boy 1)",
            f"${summary['subcontractor_1_share']:,.2f}",
            delta="50% of remainder"
        )
    
    with col3:
        st.metric(
            "Subcontractor 2 (The Boy 2)",
            f"${summary['subcontractor_2_share']:,.2f}",
            delta="50% of remainder"
        )
    
    # Charts Section
    st.markdown("---")
    st.subheader("Visual Analytics")
    
    col1, col2 = st.columns(2)
    
    # Revenue vs Cost pie chart
    with col1:
        fig_pie = go.Figure(data=[
            go.Pie(
                labels=['Material Cost', 'Gross Profit'],
                values=[summary['total_material_cost'], summary['total_profit']],
                marker=dict(colors=['#ff6b6b', '#51cf66']),
                textinfo='label+percent'
            )
        ])
        fig_pie.update_layout(
            title="Revenue Breakdown",
            height=400,
            showlegend=True
        )
        st.plotly_chart(fig_pie, use_container_width=True)
    
    # Profit distribution pie chart
    with col2:
        fig_dist = go.Figure(data=[
            go.Pie(
                labels=['Management Fee', 'Subcontractor 1', 'Subcontractor 2'],
                values=[
                    summary['management_fee'],
                    summary['subcontractor_1_share'],
                    summary['subcontractor_2_share']
                ],
                marker=dict(colors=['#4ecdc4', '#45b7aa', '#2a9d8f']),
                textinfo='label+percent'
            )
        ])
        fig_dist.update_layout(
            title="Profit Distribution",
            height=400,
            showlegend=True
        )
        st.plotly_chart(fig_dist, use_container_width=True)
    
    # Project-by-project breakdown
    st.markdown("---")
    st.subheader("Project-by-Project Breakdown")
    
    project_details = analyzer.get_project_details()
    df = pd.DataFrame(project_details)
    
    # Format currency columns
    currency_cols = ['sale_price', 'material_cost', 'profit', 'management_fee', 'subcontractor_1', 'subcontractor_2']
    for col in currency_cols:
        df[col] = df[col].apply(lambda x: f"${x:,.2f}")
    
    st.dataframe(df, use_container_width=True, hide_index=True)
    
    # Bar chart: Profit per project
    st.markdown("---")
    st.subheader("Profit Trend")
    
    project_names = [p['project'] for p in project_details]
    profits = [p['profit'] for p in project_details]
    
    fig_bar = go.Figure(data=[
        go.Bar(
            x=project_names,
            y=profits,
            marker=dict(color='#51cf66'),
            text=[f"${p:,.2f}" for p in profits],
            textposition='auto'
        )
    ])
    fig_bar.update_layout(
        title="Profit by Project",
        xaxis_title="Project",
        yaxis_title="Profit ($)",
        height=400,
        showlegend=False
    )
    st.plotly_chart(fig_bar, use_container_width=True)
    
    # Summary Statistics
    st.markdown("---")
    st.subheader("Summary Statistics")
    
    if len(invoices) > 0:
        avg_profit = summary['total_profit'] / len(invoices)
        margin = (summary['total_profit'] / summary['total_revenue'] * 100) if summary['total_revenue'] > 0 else 0
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric("Average Profit per Project", f"${avg_profit:,.2f}")
        
        with col2:
            st.metric("Profit Margin", f"{margin:.1f}%")
        
        with col3:
            st.metric("Total Projects", len(invoices))
    
    # Export data
    st.markdown("---")
    st.subheader("Export")
    
    # Create CSV export
    csv_data = df.to_csv(index=False)
    st.download_button(
        label="📥 Download Project Data (CSV)",
        data=csv_data,
        file_name="stone_bar_studio_financials.csv",
        mime="text/csv"
    )