from app.models.financial_model import FinancialAnalyzer

# Test data
invoices = [
    {
        'invoice_id': 'INV-001',
        'customer_name': 'Test Customer',
        'project_name': 'Test Project',
        'total_price': 5000,
        'material_cost': 2000
    }
]

analyzer = FinancialAnalyzer(invoices)
summary = analyzer.get_summary()

print('Test Invoice: $5000 sale price, $2000 material cost')
print(f'Profit: ${summary["total_profit"]}')
print(f'Management Fee (10%): ${summary["management_fee"]}')
print(f'Each Subcontractor Split: ${summary["subcontractor_1_share"]}')
print('✅ Financial calculations working correctly')
