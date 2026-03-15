def validate_positive(value):
    """Validate that value is positive."""
    return value > 0

def validate_dimensions(length, width, height):
    """Validate bar dimensions."""
    return all(validate_positive(dim) for dim in [length, width, height])