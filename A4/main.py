# A4 - IFC Fire Evacuation Checker | Group 07

from pathlib import Path
import sys
import subprocess
import importlib.util

def ensure_ifcopenshell():
    """Install IfcOpenShell for this Python interpreter if unavailable."""
    if importlib.util.find_spec("ifcopenshell") is not None:
        return
    print("IfcOpenShell is not installed. Attempting installation...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "ifcopenshell"])
    except (OSError, subprocess.CalledProcessError) as exc:
        print("Could not install IfcOpenShell:", exc)
        print("Run this in the VS Code terminal:")
        print(f'  & "{sys.executable}" -m pip install ifcopenshell')
        raise SystemExit(1) from exc


ensure_ifcopenshell()

import hashlib
import json
from collections import Counter
import ifcopenshell
import ifcopenshell.geom
import ifcopenshell.util.element
import ifcopenshell.util.unit
import ifcopenshell.util.placement

CHECKS = {
    "IfcDoor": {"Pset_DoorCommon": ["FireExit", "FireRating", "SelfClosing", "SmokeStop"]},
    "IfcSpace": {"Pset_SpaceFireSafetyRequirements": ["FireExit"]},
    "IfcZone": {"Pset_SpaceFireSafetyRequirements": ["FireExit"]},
    "IfcStair": {"Pset_StairCommon": []},
    "IfcStairFlight": {"Pset_StairFlightCommon": []},
}
KEYWORDS = ("fire", "smoke", "escape", "egress", "exit", "evac", "brand", "flugt", "width", "bredde")

def get_psets(element):
    try:
        return ifcopenshell.util.element.get_psets(element, should_inherit=True)
    except Exception:
        return {}

def geometry_center(element, settings):
    try:
        vertices = ifcopenshell.geom.create_shape(settings, element).geometry.verts
        if len(vertices) < 3:
            return None
        x, y, z = vertices[::3], vertices[1::3], vertices[2::3]
        return [round((min(a) + max(a)) / 2, 3) for a in (x, y, z)]
    except Exception:
        return None

def placement_xy(element, unit_scale):
    try:
        matrix = ifcopenshell.util.placement.get_local_placement(element.ObjectPlacement)
        return [round(float(matrix[0, 3]) * unit_scale, 3),
                round(float(matrix[1, 3]) * unit_scale, 3)]
    except Exception:
        return None

def find_width(psets, scale):
    for pset_name, props in sorted(psets.items()):
        if not isinstance(props, dict):
            continue
        for name in ("ClearWidth", "EffectiveWidth"):
            v = props.get(name)
            if type(v) in (int, float) and v > 0:
                return round(float(v) * scale, 4)
    return None

def analyze(model):
    settings = ifcopenshell.geom.settings()
    settings.set("use-world-coords", True)
    scale = ifcopenshell.util.unit.calculate_unit_scale(model)
    rows = []
    for cls, required in CHECKS.items():
        for element in sorted(model.by_type(cls), key=lambda e: e.GlobalId):
            psets = get_psets(element)
            selected = {}
            for pset_name, names in required.items():
                group = psets.get(pset_name, {})
                if not isinstance(group, dict):
                    group = {}
                selected[pset_name] = {
                    "present": bool(group),
                    "values": {name: group.get(name) for name in names},
                }
            additional = []
            for group_name, properties in psets.items():
                if not isinstance(properties, dict):
                    continue
                for prop_name, value in properties.items():
                    if prop_name == "id" or value is None:
                        continue
                    if group_name in required and prop_name in required[group_name]:
                        continue
                    if any(word in (group_name + " " + prop_name).lower() for word in KEYWORDS):
                        additional.append((group_name, prop_name))
            nominal = None
            if cls == "IfcDoor":
                width = getattr(element, "OverallWidth", None)
                if type(width) in (int, float) and width > 0:
                    nominal = round(width * scale, 4)
            geo = None if cls == "IfcZone" else geometry_center(element, settings)
            rows.append({
                "class": cls, "id": element.GlobalId,
                "name": element.Name or "Unnamed",
                "psets": selected, "extra": sorted(set(additional)),
                "geometry": geo is not None, "center": geo,
                "placement": placement_xy(element, scale) if cls in ("IfcStair", "IfcStairFlight") else None,
                "nominal": nominal,
                "clear": find_width(psets, scale) if cls in ("IfcDoor", "IfcStair", "IfcStairFlight") else None,
            })
    comparison_data = [
        {k: row[k] for k in ("class", "id", "psets", "extra", "geometry", "center", "placement", "nominal", "clear")}
        for row in rows
    ]
    key = hashlib.sha256(json.dumps(comparison_data, sort_keys=True, default=str).encode()).hexdigest()[:16]
    return rows, key

def print_report(model, rows, key):
    def group(cls):
        return [r for r in rows if r["class"] == cls]
    def property_values(items, pset, name):
        return [r["psets"].get(pset, {}).get("values", {}).get(name) for r in items]
    doors, spaces, zones, stairs, flights = [group(c) for c in CHECKS]
    projects = model.by_type("IfcProject")
    project = (projects[0].Name or "Unnamed project") if projects else "Unnamed project"
    line = "=" * 72
    print("\n" + line)
    print("FIRE EVACUATION - IFC MODEL REPORT | GROUP 07")
    print("Project:", project, "| IFC:", model.schema)
    print(line)
    print("\n1. MODEL OVERVIEW")
    print(f"  {'IFC class':<18} {'Total':>7} {'3D geometry readable':>22}")
    for cls in CHECKS:
        items = group(cls)
        geo = "N/A (zone grouping)" if cls == "IfcZone" else f"{sum(r['geometry'] for r in items)} / {len(items)}"
        print(f"  {cls:<18} {len(items):>7} {geo:>22}")
    print("\n2. FIRE EVACUATION IDENTIFICATION")
    print(f"  {'Elements':<10} {'Total':>7} {'FireExit YES':>14} {'FireExit NO':>13} {'Not specified':>16}")
    for label, items, pset in [
        ("Doors", doors, "Pset_DoorCommon"),
        ("Spaces", spaces, "Pset_SpaceFireSafetyRequirements"),
        ("Zones", zones, "Pset_SpaceFireSafetyRequirements")
    ]:
        vals = property_values(items, pset, "FireExit")
        yes = sum(v is True for v in vals)
        no = sum(v is False for v in vals)
        empty = sum(v is None for v in vals)
        print(f"  {label:<10} {len(items):>7} {yes:>14} {no:>13} {empty:>16}")
    print("  NOTE: Not specified = no FireExit value in the selected Pset.")
    print("\n3. FIRE SAFETY PSETS AND PROPERTIES")
    for cls, checks in CHECKS.items():
        if not checks:
            continue
        items = group(cls)
        print(f"  {cls}: {len(items)} elements")
        for pset, names in checks.items():
            found = sum(r['psets'][pset]['present'] for r in items)
            print(f"    {pset}: present on {found}; absent on {len(items) - found}")
            for name in names:
                vals = property_values(items, pset, name)
                count = sum(v is not None for v in vals)
                print(f"      {name:<16} With value: {count:<4} Without value: {len(items)-count}")
    extra = Counter((p, n) for r in rows for p, n in r['extra'])
    print("  Other fire/egress/width properties found (up to 10):")
    if extra:
        for (p, n), count in extra.most_common(10):
            print(f"    {p}.{n}: {count} elements")
    else:
        print("    None with matching property names")
    print("\n4. DOOR GEOMETRY AND WIDTHS")
    documented = [r for r in doors if r['nominal'] is not None]
    wide = [r for r in documented if r['nominal'] >= 1.20]
    narrow = [r for r in documented if r['nominal'] < 1.20]
    unknown = [r for r in doors if r['nominal'] is None]
    print(f"  Door 3D geometry readable: {sum(r['geometry'] for r in doors)} of {len(doors)}")
    print(f"  Nominal width recorded:      {len(documented)} of {len(doors)}")
    print(f"  Nominal width >= 1.20 m:    {len(wide)} doors")
    print(f"  Nominal width < 1.20 m:     {len(narrow)} doors")
    print(f"  Nominal width unavailable:  {len(unknown)} doors")
    print(f"  Documented clear/effective width: {sum(r['clear'] is not None for r in doors)} doors")
    if documented:
        print(f"  Nominal width range: {min(r['nominal'] for r in documented):.2f} - {max(r['nominal'] for r in documented):.2f} m")
    for caption, items in [("DOORS WITH NOMINAL WIDTH >= 1.20 m", wide),
                           ("DOORS WITH NOMINAL WIDTH < 1.20 m", narrow),
                           ("DOORS WITH NO NOMINAL WIDTH", unknown)]:
        print("\n  " + caption + f" ({len(items)})")
        if not items:
            print("    None")
        else:
            for r in items:
                width = f"{r['nominal']:.2f} m" if r['nominal'] is not None else "Unknown"
                print(f"    {width:<10} | {r['name'][:28]:<28} | {r['id']}")
    print("  NOTE: Nominal width is not necessarily the effective clear passage width.")
    print("  1.20 m is a screening threshold; it does not apply to every door.")
    print("\n5. STAIR GEOMETRY AND LOCATION")
    print(f"  Stair elements: {len(stairs)} | Stair flights: {len(flights)}")
    print(f"  Stair flights with documented clear/effective width: {sum(r['clear'] is not None for r in flights)} of {len(flights)}")
    for r in stairs + flights:
        xy = r['placement'] or (r['center'][:2] if r['center'] else None)
        xy_text = f"X={xy[0]:.2f} m, Y={xy[1]:.2f} m" if xy else "Position unavailable"
        width = f"{r['clear']:.2f} m" if r['clear'] is not None else "Not specified"
        print(f"  {r['class']} | {r['name'][:25]} | {xy_text} | Clear width: {width}")
        print(f"    GlobalId: {r['id']}")
    if not stairs and not flights:
        print("  No stair/stair-flight elements found")
    print("  East/west: NOT CHECKED (model north and evacuation-stair roles not established)")
    print("\n6. ESCAPE ROUTES AND CONNECTIONS")
    boundaries = len(model.by_type('IfcRelSpaceBoundary'))
    print(f"  IfcRelSpaceBoundary relationships found: {boundaries}")
    print("  Connected escape routes: NOT CHECKED")
    print("  Escape route distances: NOT CHECKED")
    print("  NOTE: Boundaries alone do not prove usable evacuation routes.")
    print("\n7. FINAL RESULTS")
    print("  DATA CHECK                                           RESULT")
    total_exit = sum(v is True for items, pset in [
        (doors, 'Pset_DoorCommon'), (spaces, 'Pset_SpaceFireSafetyRequirements'),
        (zones, 'Pset_SpaceFireSafetyRequirements')
    ] for v in property_values(items, pset, 'FireExit'))
    ratings = sum(v is not None for v in property_values(doors, 'Pset_DoorCommon', 'FireRating'))
    print(f"  {'FireExit-marked doors/spaces/zones':<53} {total_exit}")
    print(f"  {'Doors with FireRating recorded':<53} {ratings} of {len(doors)}")
    print(f"  {'Doors with nominal width >= 1.20 m':<53} {len(wide)} of {len(doors)}")
    print(f"  {'Doors with documented clear/effective width':<53} {sum(r['clear'] is not None for r in doors)} of {len(doors)}")
    print(f"  {'Doors with readable geometry':<53} {sum(r['geometry'] for r in doors)} of {len(doors)}")
    print(f"  {'Stair flights with documented clear width':<53} {sum(r['clear'] is not None for r in flights)} of {len(flights)}")
    print(f"  {'Space boundary relationships':<53} {boundaries}")
    print("  REQUIREMENT CHECK                                   STATUS")
    print("  Clear-width compliance                             NOT VERIFIED")
    print("  East/west evacuation stair locations               NOT CHECKED")
    print("  Connected evacuation network                      NOT CHECKED")
    print("  Overall fire evacuation compliance                 NOT VERIFIED")
    print(line)

def choose_ifc_file():
    if len(sys.argv) > 1:
        return Path(sys.argv[1]).expanduser().resolve()

    try:
        from tkinter import Tk, filedialog

        root = Tk()
        root.withdraw()
        try:
            root.attributes("-topmost", True)
        except Exception:
            pass
        try:
            start_folder = Path.home() / "Downloads"
            if not start_folder.is_dir():
                start_folder = Path.home()
            selected = filedialog.askopenfilename(
                parent=root,
                title="Select the IFC model for the Group 07 fire-egress checker",
                initialdir=str(start_folder),
                filetypes=[("IFC models", "*.ifc"), ("All files", "*.*")],
            )
        finally:
            root.destroy()

        if not selected:
            print("No IFC file selected. Analysis cancelled.")
            return None
        return Path(selected).resolve()

    except (ImportError, RuntimeError, OSError) as exc:
        print("Graphical file selection is not available:", exc)
        print("Enter the full path to your IFC file (or leave empty to cancel):")
        selected = input("IFC file path: ").strip().strip('"')
        return Path(selected).expanduser().resolve() if selected else None


def load_model(path):
    if not path.is_file():
        print("ERROR: IFC model not found:", path)
        return None
    if path.suffix.lower() != ".ifc":
        print("ERROR: Please choose a .ifc file:", path)
        return None
    print("Reading IFC file:", path)
    try:
        return ifcopenshell.open(str(path))
    except Exception as exc:
        print("ERROR: Failed to open IFC model:", exc)
        return None


def main():
    print("Starting Group 07 IFC fire-egress checker...", flush=True)
    print("Python interpreter:", sys.executable, flush=True)
    print("Choose an IFC file in the popup window, or pass its full path as an argument.", flush=True)
    selected_path = choose_ifc_file()
    if selected_path is None:
        print("No IFC file selected; nothing to analyze.", flush=True)
        return 1
    print("Selected IFC file:", selected_path, flush=True)
    model = load_model(selected_path)
    if model is None:
        return 1
    print("Analyzing the IFC model. Reading property sets and 3D geometry...", flush=True)
    rows, key = analyze(model)
    print_report(model, rows, key)
    print("\nReport finished successfully.", flush=True)
    return 0

if __name__ == "__main__":
    try:
        sys.exit(main())
    except Exception as exc:
        import traceback
        print("\nERROR while running IFC checker:", exc, flush=True)
        traceback.print_exc()
        sys.exit(1)
