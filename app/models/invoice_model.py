import json
from datetime import datetime
from typing import Optional

class Invoice:
    """Invoice data model for Stone Bar Studio."""
    
    def __init__(self, invoice_id: str = None, customer_name: str = "", 
                 customer_phone: str = "", customer_email: str = "",
                 customer_address: str = "", project_name: str = "",
                 bom_data: dict = None, material_cost: float = 0.0,
                 labor_cost: float = 0.0, date: str = None):
        self.invoice_id = invoice_id or self._generate_invoice_id()
        self.customer_name = customer_name
        self.customer_phone = customer_phone
        self.customer_email = customer_email
        self.customer_address = customer_address
        self.project_name = project_name
        self.bom_data = bom_data or {}
        self.material_cost = material_cost
        self.labor_cost = labor_cost
        self.date = date or datetime.now().strftime("%Y-%m-%d")
    
    def _generate_invoice_id(self) -> str:
        """Generate unique invoice ID based on timestamp."""
        return f"INV-{datetime.now().strftime('%Y%m%d%H%M%S')}"
    
    def get_total_price(self) -> float:
        """Calculate total price (material + labor)."""
        return self.material_cost + self.labor_cost
    
    def get_deposit(self) -> float:
        """Calculate 50% deposit."""
        return self.get_total_price() * 0.5
    
    def get_balance_due(self) -> float:
        """Calculate remaining balance."""
        return self.get_total_price() - self.get_deposit()
    
    def to_dict(self) -> dict:
        """Convert invoice to dictionary for JSON storage."""
        return {
            "invoice_id": self.invoice_id,
            "customer_name": self.customer_name,
            "customer_phone": self.customer_phone,
            "customer_email": self.customer_email,
            "customer_address": self.customer_address,
            "project_name": self.project_name,
            "bom_data": self.bom_data,
            "material_cost": self.material_cost,
            "labor_cost": self.labor_cost,
            "total_price": self.get_total_price(),
            "deposit": self.get_deposit(),
            "balance_due": self.get_balance_due(),
            "date": self.date
        }
    
    @staticmethod
    def from_dict(data: dict) -> "Invoice":
        """Create Invoice from dictionary."""
        return Invoice(
            invoice_id=data.get("invoice_id"),
            customer_name=data.get("customer_name", ""),
            customer_phone=data.get("customer_phone", ""),
            customer_email=data.get("customer_email", ""),
            customer_address=data.get("customer_address", ""),
            project_name=data.get("project_name", ""),
            bom_data=data.get("bom_data", {}),
            material_cost=data.get("material_cost", 0.0),
            labor_cost=data.get("labor_cost", 0.0),
            date=data.get("date")
        )