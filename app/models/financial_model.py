from typing import List, Dict
from app.models.invoice_model import Invoice

class FinancialAnalyzer:
    """Analyze financial data for Stone Bar Studio projects."""
    
    MANAGEMENT_FEE_PERCENT = 10  # "The Dad Tax"
    
    def __init__(self, invoices: List[Dict] = None):
        """
        Initialize with a list of invoice dictionaries.
        
        Args:
            invoices: List of invoice dicts (from JSON)
        """
        self.invoices = invoices or []
    
    def get_project_profit(self, invoice: Dict) -> float:
        """Calculate profit for a single project."""
        total_price = invoice.get('total_price', 0)
        material_cost = invoice.get('material_cost', 0)
        return total_price - material_cost
    
    def get_management_fee(self, invoice: Dict) -> float:
        """Calculate 10% management fee on profit."""
        profit = self.get_project_profit(invoice)
        return profit * (self.MANAGEMENT_FEE_PERCENT / 100)
    
    def get_subcontractor_split(self, invoice: Dict) -> Dict[str, float]:
        """
        Calculate split for two subcontractors after management fee.
        
        Returns: {"subcontractor_1": amount, "subcontractor_2": amount}
        """
        profit = self.get_project_profit(invoice)
        mgmt_fee = self.get_management_fee(invoice)
        remaining = profit - mgmt_fee
        
        # Split remaining 50/50 between two subcontractors ("The Boys")
        split_amount = remaining / 2
        
        return {
            "subcontractor_1": round(split_amount, 2),
            "subcontractor_2": round(split_amount, 2)
        }
    
    def get_total_revenue(self) -> float:
        """Sum of all project sale prices."""
        return sum(inv.get('total_price', 0) for inv in self.invoices)
    
    def get_total_material_cost(self) -> float:
        """Sum of all material costs."""
        return sum(inv.get('material_cost', 0) for inv in self.invoices)
    
    def get_total_profit(self) -> float:
        """Total profit across all projects."""
        return self.get_total_revenue() - self.get_total_material_cost()
    
    def get_total_management_fee(self) -> float:
        """10% of total profit."""
        return self.get_total_profit() * (self.MANAGEMENT_FEE_PERCENT / 100)
    
    def get_total_subcontractor_payout(self) -> float:
        """Total remaining after management fee, split between two contractors."""
        return self.get_total_profit() - self.get_total_management_fee()
    
    def get_subcontractor_share(self) -> float:
        """Per-subcontractor share (50% of remaining after mgmt fee)."""
        return self.get_total_subcontractor_payout() / 2
    
    def get_summary(self) -> Dict:
        """Get complete financial summary."""
        return {
            "total_revenue": round(self.get_total_revenue(), 2),
            "total_material_cost": round(self.get_total_material_cost(), 2),
            "total_profit": round(self.get_total_profit(), 2),
            "management_fee": round(self.get_total_management_fee(), 2),
            "total_subcontractor_payout": round(self.get_total_subcontractor_payout(), 2),
            "subcontractor_1_share": round(self.get_subcontractor_share(), 2),
            "subcontractor_2_share": round(self.get_subcontractor_share(), 2),
            "num_projects": len(self.invoices)
        }
    
    def get_project_details(self) -> List[Dict]:
        """Get detailed breakdown for each project."""
        details = []
        for inv in self.invoices:
            profit = self.get_project_profit(inv)
            mgmt_fee = self.get_management_fee(inv)
            splits = self.get_subcontractor_split(inv)
            
            details.append({
                "invoice_id": inv.get('invoice_id', 'Unknown'),
                "customer": inv.get('customer_name', 'Unknown'),
                "project": inv.get('project_name', 'Unknown'),
                "sale_price": inv.get('total_price', 0),
                "material_cost": inv.get('material_cost', 0),
                "profit": round(profit, 2),
                "management_fee": round(mgmt_fee, 2),
                "subcontractor_1": splits["subcontractor_1"],
                "subcontractor_2": splits["subcontractor_2"]
            })
        
        return details