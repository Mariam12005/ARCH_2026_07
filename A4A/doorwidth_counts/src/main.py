def check_door_widths(model):
    scale = ifcopenshell.util.unit.calculate_unit_scale(model)

    wide = 0
    narrow = 0
    unknown = 0

    for door in model.by_type("IfcDoor"):
        width = door.OverallWidth

        if width is None or width <= 0:
            unknown += 1
        elif width * scale >= 1.20:
            wide += 1
        else:
            narrow += 1

    return {
        "width_1.20m_or_more": wide,
        "width_below_1.20m": narrow,
        "unknown_width": unknown
    }