def check_fire_properties(model):
    properties = ["FireExit", "FireRating",
                  "SelfClosing", "SmokeStop"]

    result = {name: 0 for name in properties}

    for door in model.by_type("IfcDoor"):
        psets = get_psets(door)
        door_common = psets.get("Pset_DoorCommon", {})

        for name in properties:
            if door_common.get(name) is not None:
                result[name] += 1

    return result
