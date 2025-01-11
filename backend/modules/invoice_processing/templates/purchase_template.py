from dataclasses import dataclass
from typing import List, Dict

@dataclass
class PurchaseTemplate:
    required_fields: List[str] = [
        'supplier_name',
        'invoice_number', 
        'purchase_date',
        'total_amount'
    ]
    
    optional_fields: List[str] = [
        'tax_amount',
        'discount',
        'payment_terms'
    ]
    
    field_mappings: Dict[str, str] = {
        'supplier': 'supplier_name',
        'invoice_no': 'invoice_number',
        'date': 'purchase_date',
        'total': 'total_amount'
    }
    
    def validate_structure(self, data: dict) -> bool:
        return all(field in data for field in self.required_fields)
