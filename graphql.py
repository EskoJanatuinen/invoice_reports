sales_orders = """query {
    sales_order(order_by: {extra_id: asc}, where: {_and: [{created_date: {_gte: "2021-06-21"}}]}) {
    order_no
    created_at
    delivery
    order_date
    created_date
    extra_id
    }
}"""

sales_orders_201 = """query {
    sales_order_row(order_by: {order_no: asc}, where: {warehouse: {_eq: 201}}) {
        order_no
        warehouse
    }
}"""
