# A4 – IFC Fire Evacuation Checker
**Group:** Group 07  
**Focus area:** Fire evacuation  

### 1. Problem / claim the tool addresses

The project needs to determine whether the IFC model for Building 308 contains enough reliable information to assess fire evacuation design. 
Incomplete fire-safety attributes, missing dimensions, and insufficient spatial relationships can make it difficult to verify the intended evacuation strategy from the BIM model.

The checker focuses on identifying missing or incomplete information in the IFC model rather than verifying compliance with building regulations.

### 2. Where the problem was identified

The problem was identified in the Group 07 A1 analysis of the Building 308 IFC model, which highlighted missing fire-safety properties and incomplete spatial information. The project brief also refers to section 1.2.6 "Fire Safety and Egress," in "26-08-A-ClientReport-Anon.pdf" as the source of the fire-evacuation claims to be investigated.

### 3. Description of the tool

The A4 IFC Fire Evacuation Checker is a standalone Python program that opens an IFC model using IfcOpenshell and prints a structured, read-only report in the terminal. It examines "IfcDoor," "IfcSpace", "IfcZone", "IfcStair", and "IfcStairFlight" elements.

The current Python implementation produces six sections:

1. **Model overview** — counts the selected IFC element classes and records whether their 3D geometry can be read.
2. **Fire evacuation identification** — counts "FireExit = True", "FireExit = False", and unspecified values for doors, spaces, and zones in the chosen property sets.
3. **Fire-safety properties** — checks whether selected property sets and property values are present; also lists other properties whose names suggest relevance to fire, egress, or width.
4. **Door geometry and widths** — reports "OverallWidth" values, groups nominal door widths above or below 1.20 m, lists door names and GlobalIds, and counts explicit "ClearWidth" / "EffectiveWidth" values where present.
5. **Stair geometry and location** — reports stairs and stair flights, available coordinates and documented clear/effective widths.
6. **Escape routes and connections** — counts "IfcRelSpaceBoundary" relationships and explains what cannot be concluded from that count.

**Important limitations:**

- **No fire-code compliance pass/fail decision is calculated.** The current program reports data availability and uses statuses such as NOT CHECKED and NOT VERIFIED for matters outside its analysis. The proposed "PASS / FAIL / NOT VERIFIABLE" classification is "not implemented" as a regulatory rules engine.
- **The 1.20 m door-width threshold is only a screening comparison**, not a universally applicable requirement. "OverallWidth" is nominal width, not verified clear passage width.

### 4. Instructions to run the tool

**Requirements:** A Windows computer with Python, VS Code or another terminal, and an IFC file such as `B308X(1).ifc`. An internet connection may be needed the first time to install IfcOpenShell.

**Option A — Select an IFC file in a popup window (recommended)**

1. Save the Python checker, `A4_main_output_fixed.py`, to your computer. If the submitted file is named `main.py`, use `main.py` in the commands below instead.
2. Open the folder containing the Python file in VS Code (**File → Open Folder**).
3. Open **Terminal → New Terminal**.
4. Run:

   ```powershell
   python -u "A4_main_output_fixed.py"
   ```

5. The program attempts to install **IfcOpenShell** automatically if it is not installed for the Python interpreter being used. If installation fails, run `python -m pip install ifcopenshell` in the terminal and retry.
6. In the file-selection window, choose `B308X(1).ifc` (or another `.ifc` file). The IFC model does **not** need to be in the same folder as the script.
7. Read the **seven-section fire evacuation report** in the VS Code terminal. The program shows a startup message, then model-analysis progress, and finally the report.

**Option B — Pass the IFC file path directly**

```powershell
python -u "A4_main_output_fixed.py" "C:\Users\<your-user>\Downloads\B308X(1).ifc"
```

Replace `<your-user>` and the path with the actual file location. This bypasses the popup. If `python` selects a different Python environment from VS Code, use **Python: Select Interpreter** and choose the interpreter with IfcOpenShell installed, or run the command with the full path to that interpreter.

**Troubleshooting:** If nothing appears, confirm that you are running the **Python `.py` file**, not pasting `from ...` or `import ...` statements into PowerShell. If the chooser seems absent, check behind VS Code. If the terminal reports a missing IFC file, check the selected path and filename. The script opens the IFC model with `ifcopenshell.open(...)`; it does not connect to a live Bonsai session.

## Advanced Building Design

### 5. Relevant design stage (A, B, C or D)

**Primarily Stage C, and also Stage D** — during detailed model development, coordination, and review, when IFC objects, dimensions, property sets, and geometry should be sufficiently developed for automated model-data checks. It can also be used earlier **if** the model already includes the required information; missing fields in an early-stage model should be understood as a data gap, not automatically a design failure.

*The exact naming of Stages A–D is course-specific; this recommendation describes when the checker becomes practically useful rather than asserting a formal stage definition.*

### 6. Subjects and disciplines that might use it

- **BIM coordinators / BIM managers:** audit IFC data completeness and identify missing properties.
- **Fire-safety engineers / consultants:** identify what fire-egress data exists and what requires further verification.
- **Architects / building designers:** review door widths, exit flags, space data, and design-model coordination.
- **Structural / stair designers:** inspect IFC stair and stair-flight objects and available widths or positions.
- **Project teams / reviewers:** document information gaps before more detailed evacuation or compliance analysis.

### 7. IFC information required for the tool to work

**Essential to run:**

- A valid, readable **`.ifc` file** with an IFC project and elements of the classes being checked (empty categories can still be reported).
- IFC objects with **GlobalIds**, so individual elements can be identified in the output.

**Required for specific, useful checks:**

| IFC data | Used for |
|---|---|
| `IfcDoor` and `OverallWidth` | Door inventory and nominal width screening |
| `Pset_DoorCommon.FireExit` | Fire-exit identification for doors |
| `Pset_DoorCommon.FireRating`, `SelfClosing`, `SmokeStop` | Presence/absence of door fire and smoke properties |
| `IfcSpace`, `IfcZone` and `Pset_SpaceFireSafetyRequirements.FireExit` | Space/zone inventory and documented fire-exit flags |
| `IfcStair`, `IfcStairFlight` and relevant property sets | Stair inventory, relevant reported properties and available widths |
| `ClearWidth` or `EffectiveWidth` in IFC property sets | Explicitly documented passage or stair width values |
| 3D representations and placements | Readable geometry counts, geometry centers and stair XY positions |
| `IfcRelSpaceBoundary` | Number of available space-boundary relationships **only** |
| IFC length units | Converting model dimensions to metres |

Missing or unpopulated properties appear as **not specified**, **without value**, or **not available**, depending on the report section. Data-quality findings should be reviewed by project specialists against the applicable project brief, the architectural/fire strategy, and governing requirements.

---

**Submission summary:** This tool helps Group 07 assess **whether Building 308's IFC model contains accessible fire-evacuation data**. It is an early-stage **information-quality checker**, not a completed evacuation-route simulator or fire-code compliance certifier.
