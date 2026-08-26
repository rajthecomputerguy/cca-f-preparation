from sub_agent import run_sub_agent


def main():

    customer_task = """
    Verify customer C001.
    Return the customer ID, name, and verification status.
    """

    order_task = """
    Review the order information for customer C001.
    Return the important order details.
    """

    customer_result = run_sub_agent(customer_task)

    order_result = run_sub_agent(order_task)

    print("\nCustomer Agent Result:")
    print(customer_result)

    print("\nOrder Agent Result:")
    print(order_result)


if __name__ == "__main__":
    main()