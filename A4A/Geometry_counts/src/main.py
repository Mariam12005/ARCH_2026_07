def geometry_center(element, settings):
    try:
        vertices = ifcopenshell.geom.create_shape(settings, element).geometry.verts
        if len(vertices) < 3:
            return None
        x, y, z = vertices[::3], vertices[1::3], vertices[2::3]
        return [round((min(a) + max(a)) / 2, 3) for a in (x, y, z)]
    except Exception:
        return None