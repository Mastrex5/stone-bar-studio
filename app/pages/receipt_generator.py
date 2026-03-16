import streamlit as st
from app.models.invoice_model import Invoice
from app.utils.pdf_generator import PDFGenerator
from app.utils.data_handler import load_projects, save_invoice, load_invoices
import json

def show_page():
    st.title("Invoice & Receipt Generator")
    st.markdown("Create professional invoices for your stone bar projects.")
    
    # Initialize session state for invoice form
    if 'invoice' not in st.session_state:
        st.session_state.invoice = Invoice()
    
    # Tabs for different views
    tab1, tab2, tab3 = st.tabs(["Create Invoice", "View Saved Invoices", "Invoice History"])
    
    with tab1:
        st.subheader("Create New Invoice")
        
        # Load existing projects
        projects = load_projects()
        
        # Option to create from existing BOM or blank
        col1, col2 = st.columns(2)
        with col1:
            use_existing_bom = st.checkbox("Use existing BOM from Planning Studio")
        
        selected_bom = {}
        if use_existing_bom and projects:
            project_indices = [f"Project {i+1}" for i in range(len(projects))]
            selected_idx = st.selectbox("Select a project BOM", range(len(projects)), 
                                       format_func=lambda i: f"Project {i+1} - {projects[i].get('top_dimensions', 'Unknown')}")
            selected_bom = projects[selected_idx]
        
        st.markdown("---")
        st.subheader("Customer Information")
        
        col1, col2 = st.columns(2)
        with col1:
            customer_name = st.text_input("Customer Name", value=st.session_state.invoice.customer_name)
            customer_phone = st.text_input("Customer Phone", value=st.session_state.invoice.customer_phone)
        with col2:
            customer_email = st.text_input("Customer Email", value=st.session_state.invoice.customer_email)
            customer_address = st.text_area("Customer Address", value=st.session_state.invoice.customer_address, height=80)
        
        st.markdown("---")
        st.subheader("Project Information")
        
        project_name = st.text_input("Project Name", value=st.session_state.invoice.project_name)
        
        st.markdown("---")
        st.subheader("Pricing")
        
        col1, col2 = st.columns(2)
        with col1:
            material_cost = st.number_input("Material Cost ($)", min_value=0.0, step=100.0, 
                                           value=st.session_state.invoice.material_cost)
        with col2:
            labor_cost = st.number_input("Labor Cost ($)", min_value=0.0, step=100.0,
                                        value=st.session_state.invoice.labor_cost)
        
        # Calculate and display pricing
        total = material_cost + labor_cost
        deposit = total * 0.5
        balance = total - deposit
        
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Total Price", f"${total:,.2f}")
        with col2:
            st.metric("Deposit (50%)", f"${deposit:,.2f}")
        with col3:
            st.metric("Balance Due", f"${balance:,.2f}")
        
        st.markdown("---")
        
        # Update session state and create invoice
        if st.button("Generate Invoice & PDF", type="primary"):
            invoice = Invoice(
                customer_name=customer_name,
                customer_phone=customer_phone,
                customer_email=customer_email,
                customer_address=customer_address,
                project_name=project_name or "Stone Bar Project",
                bom_data=selected_bom,
                material_cost=material_cost,
                labor_cost=labor_cost
            )
            
            st.session_state.invoice = invoice
            st.success(f"✅ Invoice {invoice.invoice_id} created successfully!")
            st.write(f"**Invoice Details:**")
            st.json(invoice.to_dict())
    
    with tab2:
        st.subheader("Preview & Download Invoice")
        
        if st.session_state.invoice and st.session_state.invoice.customer_name:
            invoice = st.session_state.invoice
            
            st.write(f"**Invoice ID:** {invoice.invoice_id}")
            st.write(f"**Customer:** {invoice.customer_name}")
            st.write(f"**Project:** {invoice.project_name}")
            st.write(f"**Total:** ${invoice.get_total_price():,.2f}")
            
            col1, col2, col3 = st.columns(3)
            with col1:
                if st.button("📥 Download PDF"):
                    try:
                        pdf_buffer = PDFGenerator.generate_invoice_pdf(invoice)
                        st.download_button(
                            label="📥 Download Invoice PDF",
                            data=pdf_buffer.getvalue(),
                            file_name=f"{invoice.invoice_id}.pdf",
                            mime="application/pdf"
                        )
                        st.success("✅ PDF ready for download!")
                    except Exception as e:
                        st.error(f"Error generating PDF: {e}")
            
            with col2:
                if st.button("💾 Save Invoice"):
                    save_invoice(invoice)
                    st.success(f"✅ Invoice {invoice.invoice_id} saved!")
            
            with col3:
                if st.button("🗑️ Clear"):
                    st.session_state.invoice = Invoice()
                    st.rerun()
        else:
            st.info("Create an invoice first using the 'Create Invoice' tab.")
    
    with tab3:
        st.subheader("Saved Invoices")
        
        invoices = load_invoices()
        if invoices:
            for inv in invoices:
                with st.expander(f"{inv['invoice_id']} - {inv['customer_name']}"):
                    st.write(f"**Date:** {inv['date']}")
                    st.write(f"**Project:** {inv['project_name']}")
                    st.write(f"**Total:** ${inv['total_price']:,.2f}")
                    st.write(f"**Deposit:** ${inv['deposit']:,.2f}")
                    st.write(f"**Balance Due:** ${inv['balance_due']:,.2f}")
                    
                    if st.button(f"Download {inv['invoice_id']}", key=f"download_{inv['invoice_id']}"):
                        try:
                            invoice_obj = Invoice.from_dict(inv)
                            pdf_buffer = PDFGenerator.generate_invoice_pdf(invoice_obj)
                            st.download_button(
                                label="📥 Download PDF",
                                data=pdf_buffer.getvalue(),
                                file_name=f"{inv['invoice_id']}.pdf",
                                mime="application/pdf",
                                key=f"pdf_btn_{inv['invoice_id']}"
                            )
                        except Exception as e:
                            st.error(f"Error: {e}")
        else:
            st.info("No saved invoices yet. Create one in the 'Create Invoice' tab.")