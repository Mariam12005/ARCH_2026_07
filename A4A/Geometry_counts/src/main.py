def count_elements(model):
    return {
        "doors": len(model.by_type("IfcDoor")),
        "spaces": len(model.by_type("IfcSpace")),
        "zones": len(model.by_type("IfcZone")),
        "stairs": len(model.by_type("IfcStair")),
        "stair_flights": len(model.by_type("IfcStairFlight"))
    }