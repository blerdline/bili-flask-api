class Invoice:
    def __init__(self, customer_name):
        self.customer_name = customer_name
        self.line_items = []
        self.total = 0


    def to_dict(self):
        return {
            'id': self.invoice_id,
            'data': self.data,
            'line_items': self.line_items,
            'total': self.calculate_total()
        }
    
    def calculate_total(self):
        total = 0
        for line_item in self.line_items:
            total += line_item.price * line_item.quantity
        self.total = total
        return total
    
    def get_current_total(self):
        return self.total
    
    def add_line_item(self, line_item):
        self.line_items.append(line_item)
    
class LineItem:
    def __init__(self, description, price, quantity):
        self.description = description
        self.price = price
        self.quantity = quantity

    def to_dict(self):
        return {
            'description': self.description,
            'price': self.price,
            'quantity': self.quantity
        }