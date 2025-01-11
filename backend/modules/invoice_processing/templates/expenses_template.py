from dataclasses import dataclass
from typing import List, Dict

@dataclass
class ExpensesTemplate:
    required_fields: List[str] = [
        'expense_type',
        'date',
        'amount',
        'description'
    ]
    
    optional_fields: List[str] = [
        'tax_deductible',
        'payment_method',
        'receipt_number'
    ]
    
    field_mappings: Dict[str, str] = {
        'type': 'expense_type',
        'total': 'amount',
        'desc': 'description'
    }
    
    def validate_structure(self, data: dict) -> bool:
        return all(field in data for field in self.required_fields)
