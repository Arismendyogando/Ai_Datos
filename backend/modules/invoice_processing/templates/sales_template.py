from dataclasses import dataclass
from typing import List, Dict

@dataclass
class SalesTemplate:
    required_fields: List[str] = [
        'customer_name',
        'invoice_number',
        'sale_date',
        'total_amount'
    ]
    
    optional_fields: List[str] = [
        'tax_amount',
        'discount',
        'payment_method'
    ]
    
    field_mappings: Dict[str, str] = {
        'customer': 'customer_name',
        'invoice_no': 'invoice_number',
        'date': 'sale_date',
        'total': 'total_amount'
    }
    
    def validate_structure(self, data: dict) -> bool:
        return all(field in data for field in self.required_fields)
