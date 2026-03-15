import pytest
from app.models.material_calculator import calculate_bom

def test_rectangular_bom():
    bom = calculate_bom(3, 5, 3, 'rectangular', 10)
    assert 'lumber_ft' in bom
    assert bom['lumber_ft'] > 0
    assert bom['plywood_sq_ft'] == 16.5  # 3*5 * 1.1
    assert bom['veneer_sq_ft'] == 52.8  # 3 * 16 * 1.1

def test_l_shape_bom():
    bom = calculate_bom(3, 5, 3, 'l-shape', 10, leg_length=2, leg_width=4)
    assert 'lumber_ft' in bom
    assert bom['lumber_ft'] > 0