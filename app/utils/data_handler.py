import json
import os
from app.config import DATA_PATH, INVOICES_PATH

def save_project(bom):
    """Save BOM to JSON file."""
    if not os.path.exists(DATA_PATH):
        with open(DATA_PATH, 'w') as f:
            json.dump([], f)
    
    with open(DATA_PATH, 'r') as f:
        projects = json.load(f)
    
    projects.append(bom)
    
    with open(DATA_PATH, 'w') as f:
        json.dump(projects, f, indent=4)

def load_projects():
    """Load projects from JSON."""
    if not os.path.exists(DATA_PATH):
        return []
    with open(DATA_PATH, 'r') as f:
        return json.load(f)

def save_invoice(invoice):
    """Save invoice to JSON file."""
    if not os.path.exists(INVOICES_PATH):
        with open(INVOICES_PATH, 'w') as f:
            json.dump([], f)
    
    with open(INVOICES_PATH, 'r') as f:
        invoices = json.load(f)
    
    invoices.append(invoice.to_dict())
    
    with open(INVOICES_PATH, 'w') as f:
        json.dump(invoices, f, indent=4)

def load_invoices():
    """Load invoices from JSON."""
    if not os.path.exists(INVOICES_PATH):
        return []
    with open(INVOICES_PATH, 'r') as f:
        return json.load(f)