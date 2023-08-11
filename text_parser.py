from pyparsing import Combine, Keyword, Word, nums, alphas, alphanums, Group, OneOrMore, Suppress

at_symbol = Suppress('@')
hash_symbol = Suppress('#')
dollar_symbol = Suppress('$')
insert_symbol = hash_symbol
delete_symbol = Suppress("-")
modify_symbol = Suppress(">")
description_pattern = Combine(OneOrMore(Word(alphanums + " ")))("description")
amount_pattern = dollar_symbol + Word(nums + "." + nums)("amount")
quantity_pattern = Word(nums)("quantity")
line_number_pattern = Word(nums)("line_number")

def parse_text_message(text_message):
    customer_name = None
    line_items = []
    name_parser = at_symbol + Word(alphas + " ")
    item_parser = hash_symbol + Group(Word(alphanums + " ") + dollar_symbol + Word(nums + "." + nums) + Word(nums))
    
    parser = OneOrMore(name_parser | item_parser)

    result = parser.parseString(text_message)

    for item in result:
        if isinstance(item, str):
            customer_name = item.strip()
        else:
            description, price, quantity = item
            line_items.append({
                'description': description,
                'price': price,
                'quantity': quantity
            })

    return customer_name, line_items

def parse_invoice_number_text(invoice_number_text):
    invoice_number = None
    invoice_number_parser = Keyword("Invoice", caseless=True) + Word(nums)("invoice_number")
    result = invoice_number_parser.parse_string(invoice_number_text)
    invoice_number = {"invoice_id":  result.invoice_number}
    return invoice_number

def parse_delete_line_item_text(delete_line_item_text):
    delete_object = None
    line_number = []
    
    delete_line_item_parser = OneOrMore(delete_symbol + line_number_pattern)
    result = delete_line_item_parser.parse_string(delete_line_item_text)

    for item in result:
        line_number.append({"line_number" :item})

    delete_object = {"delete": line_number}
    return delete_object

def parse_insert_line_item_text(insert_line_item_text):
    description = None
    amount = None
    quantity = None
    line_items = []
   
    insert_line_item_parser = OneOrMore(insert_symbol + Group(description_pattern + amount_pattern + quantity_pattern))
    result = insert_line_item_parser.parse_string(insert_line_item_text)
    for item in result:
        description, amount, quantity = item
        line_items.append({
            'description': description,
            'amount': amount,
            'quantity': quantity
        })

    return line_items

def parse_modify_line_item_text(modify_line_item_text):
    description = None
    amount = None
    quantity = None
    line_number = None
    line_items = []

    modify_line_item_parser = OneOrMore(modify_symbol + Group(line_number_pattern + description_pattern + amount_pattern + quantity_pattern))
    result = modify_line_item_parser.parse_string(modify_line_item_text)

    for item in result: 
        line_number, description, amount, quantity = item
        line_items.append({
            'line_number': line_number,
            'description': description,
            'amount': amount,
            'quantity': quantity
        })

    return line_items

def parse_invoice_text(invoice_text):
    pass