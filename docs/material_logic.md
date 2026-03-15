# Material Logic for BOM Calculations

## Key Assumptions
- Bar Structure: Wood-framed base (2x4 studs + plywood), metal lath for stone adhesion, mortar for installation, stone veneer on sides, natural stone slab on top.
- Shape Handling: Rectangular or L-shapes (two rectangles joined at a corner).
- Units: Dimensions in feet; outputs in linear feet (lumber), square feet (areas), bags (mortar), etc.
- Waste Factor: Applied to all materials (default 10%).
- Material Standards:
  - Lumber: 2x4 studs every 16" on center for framing.
  - Plywood: 3/4" pressure-treated (PT) for base.
  - Metal Lath: 2.5 lb/sq ft expanded metal.
  - Mortar: 1 bag covers ~45 sq ft (at 1/2" thickness).
  - Stone Veneer: Thin veneer; coverage in sq ft.
  - Stone Top: Natural slab; dimensions match bar top.

## Calculation Steps
1. Determine Total Dimensions: Perimeter and base area based on shape.
2. Framing Lumber: Perimeter * 2 + supports (every 16" on center).
3. Plywood Base: Length * width.
4. Metal Lath: Sides + base area.
5. Mortar Bags: Based on total stone area / 45.
6. Stone Veneer: Height * perimeter.
7. Stone Countertop: Base area.

All adjusted for waste factor.