import math

def calculate_bom(length, width, height, shape='rectangular', waste_factor=10, **kwargs):
    """
    Calculate Bill of Materials for a stone bar.

    Args:
        length (float): Main length in ft
        width (float): Main width in ft
        height (float): Height in ft
        shape (str): 'rectangular' or 'l-shape'
        waste_factor (float): Waste percentage
        **kwargs: For L-shape: leg_length, leg_width

    Returns:
        dict: BOM with quantities
    """
    if shape == 'rectangular':
        perimeter = 2 * (length + width)
        base_area = length * width
    elif shape == 'l-shape':
        leg_length = kwargs.get('leg_length', 0)
        leg_width = kwargs.get('leg_width', 0)
        # L-shape: two rectangles sharing a corner
        perimeter = 2 * (length + width) + 2 * (leg_length + leg_width) - 2 * 1  # subtract shared edge
        base_area = length * width + leg_length * leg_width
    else:
        raise ValueError("Unsupported shape")

    # Lumber (2x4s): perimeter * 2 plates + studs every 16" (1.33 per sq ft)
    total_lumber_ft = (perimeter * 2) + (base_area / 1.33)
    adjusted_lumber = total_lumber_ft * (1 + waste_factor / 100)

    # Plywood base
    adjusted_plywood = base_area * (1 + waste_factor / 100)

    # Metal lath: sides + base
    lath_area = 2 * height * perimeter + base_area
    adjusted_lath = lath_area * (1 + waste_factor / 100)

    # Mortar: ~45 sq ft per bag
    stone_area = lath_area + base_area  # veneer + top
    mortar_bags = stone_area / 45
    adjusted_mortar = mortar_bags * (1 + waste_factor / 100)

    # Stone veneer: sides only
    veneer_area = height * perimeter
    adjusted_veneer = veneer_area * (1 + waste_factor / 100)

    # Stone top
    adjusted_top_area = base_area * (1 + waste_factor / 100)

    bom = {
        "lumber_ft": round(adjusted_lumber, 2),
        "plywood_sq_ft": round(adjusted_plywood, 2),
        "lath_sq_ft": round(adjusted_lath, 2),
        "mortar_bags": math.ceil(adjusted_mortar),
        "veneer_sq_ft": round(adjusted_veneer, 2),
        "top_sq_ft": round(adjusted_top_area, 2),
        "top_dimensions": f"{length} x {width} ft" if shape == 'rectangular' else f"Main: {length}x{width}, Leg: {kwargs.get('leg_length',0)}x{kwargs.get('leg_width',0)} ft"
    }
    return bom