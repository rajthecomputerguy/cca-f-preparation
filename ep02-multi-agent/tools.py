def get_customer(customer_id):
    customers = {
        "C001": {
            "customer_id": "C001",
            "name": "Raju",
            "verified": True
        },
        "C002": {
            "customer_id": "C002",
            "name": "Kumar",
            "verified": False
        }
    }

    return customers.get(customer_id)