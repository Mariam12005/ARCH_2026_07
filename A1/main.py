from pathlib import Path
import re

# A1 FORENSIC BIM
# Group 07
# Focus Area: Fire Evacuation

IFC_FILE = Path(__file__).parent / "B308X (1).ifc"

# ============================================================
 
def count_ifc_objects(text, object_type):

    """Counts how many IFC objects of a certain type exist. Example: IFCSPACE, IFCDOOR, IFCSTAIR """
 
    pattern = rf"=\s*{object_type}\s*\("
    return len(re.findall(pattern,text,re.IGNORECASE ))
 
 
def count_property(text, property_name):

    """Counts how many times a property name appears in the IFC file."""

    pattern = rf"'{re.escape(property_name)}'"
    return len(re.findall(pattern,text,re.IGNORECASE))
 
 
# ============================================================

# MAIN PROGRAM
 
def main():
    print()
    print("=" * 60)
    print("A1 FORENSIC BIM - FIRE EVACUATION ANALYSIS")
    print("GROUP 07")
    print("=" * 60)
    print()
 
    text = IFC_FILE.read_text(encoding="utf-8",errors="ignore")
 
    # --------------------------------------------------------
 
    spaces = count_ifc_objects(text,"IFCSPACE")
    doors = count_ifc_objects(text,"IFCDOOR")
    stairs = count_ifc_objects(text, "IFCSTAIR")
 
    # --------------------------------------------------------
 
    fire_exit = count_property(text,"FireExit")
    fire_rating = count_property(text,"FireRating")
    self_closing = count_property(text,"SelfClosing")
    smoke_stop = count_property(text,"SmokeStop")
 
 
    report = []
    report.append( f"IFC model: {IFC_FILE.name}" )
    report.append("")
    report.append("IFC OBJECTS FOUND")
    report.append( "-" * 60)
    report.append( f"IfcSpace objects: {spaces}")
    report.append(f"IfcDoor objects: {doors}")
    report.append(f"IfcStair objects: {stairs}")
    report.append("")
    report.append("FIRE-SAFETY PROPERTIES FOUND")
    report.append("-" * 60)
    report.append(f"FireExit: {fire_exit}")
    report.append(f"FireRating: {fire_rating}")
    report.append(f"SelfClosing: {self_closing}")
    report.append(f"SmokeStop: {smoke_stop}")
    report.append("")
    report.append("CONCLUSION")
    report.append("-" * 60)
 
    missing_information = (fire_exit == 0 or fire_rating == 0 or self_closing == 0 or smoke_stop == 0)
 
    if missing_information:
        report.append("Model information issue identified.")
        report.append("")
        report.append("The IFC model does not contain all of the " "investigated fire-safety properties.")
        report.append("Therefore, the available IFC information is " "insufficient to reliably identify a complete " "fire evacuation system automatically.")
 
    else:
        report.append("The investigated fire-safety property names " "were found in the IFC file." )
 
    report_text = "\n".join(report)
 
    print(report_text)
    print()
    print("=" * 60)
if __name__ == "__main__":
    main()
 
