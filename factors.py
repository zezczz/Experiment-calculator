def epercent(value, true):
    """Calculate the percentage error between a value and the true value.

    Args:
        value (float): The estimated value.
        true (float): The true value.

    Returns:
        float: The percentage error.
    """
    if true == 0:
        raise ValueError("True value cannot be zero for percentage error calculation.")
    return abs((value - true) / true)

