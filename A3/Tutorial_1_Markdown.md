# Tutorial 1 — Checking IFC Fire-Egress Data with IfcOpenShell

## Introduction

In this tutorial, you will learn how to use Python and IfcOpenShell to check whether an IFC model contains enough information for an automated fire-evacuation analysis.

The purpose is not to calculate a complete evacuation route. Instead, we first check whether the IFC contains the information needed to make such an analysis reliable.

The main question is:

> Does the IFC model contain enough fire-egress information for an automated evacuation check?

---

## Learning objectives

After completing this tutorial, you should be able to:

1. Open an IFC model using IfcOpenShell.
2. Find relevant IFC classes such as `IfcSpace` and `IfcDoor`.
3. Check whether doors contain the `FireExit` property.
4. Check whether the IFC contains `IfcRelSpaceBoundary`.
5. Decide whether the model is ready for automated fire-egress analysis.

---

# 1. Install IfcOpenShell

Open command promt on your computer

Run:

```bash
py -m pip install ifcopenshell
```

If `py` does not work, try:

```bash
python -m pip install ifcopenshell
```

To check that IfcOpenShell is installed correctly, run:

```bash
py -c "import ifcopenshell; print(ifcopenshell.version)"
```

If a version number appears, the installation was successful.

---

# 2. Open an IFC model

Create a Python file or use the Python terminal.

Start by importing the required libraries:

```python
from pathlib import Path
import ifcopenshell
```

Now define the location of your IFC model:

```python
MODEL_PATH = Path(
    r"C:\Users\YOUR_USERNAME\Documents\models\B308X.ifc"
)
```

Change the path so that it points to the IFC file on your own computer.

Check that the file exists:

```python
if not MODEL_PATH.is_file():
    raise FileNotFoundError(
        f"No IFC file found at {MODEL_PATH}"
    )
```

Open the model:

```python
model = ifcopenshell.open(MODEL_PATH)

print("IFC schema:", model.schema)
```

### Example output

```text
IFC schema: IFC4X3_ADD2
```

The exact output depends on the IFC model you are using.

---

# 3. Check the important IFC classes

For fire-egress analysis, several IFC classes are useful.

We will inspect:

- `IfcSpace`
- `IfcDoor`
- `IfcStair`
- `IfcStairFlight`
- `IfcBuildingStorey`
- `IfcRelSpaceBoundary`

Run:

```python
classes = [
    "IfcSpace",
    "IfcDoor",
    "IfcStair",
    "IfcStairFlight",
    "IfcBuildingStorey",
    "IfcRelSpaceBoundary",
]

for ifc_class in classes:
    objects = model.by_type(ifc_class)

    print(
        ifc_class,
        len(objects)
    )
```

### Example output from Building 308

```text
IfcSpace 3
IfcDoor 101
IfcStair 1
IfcStairFlight 1
IfcBuildingStorey 6
IfcRelSpaceBoundary 0
```

---

## What do these classes mean?

### IfcSpace

`IfcSpace` represents spaces or areas inside the building.

For evacuation analysis, spaces can represent the starting locations of people.

### IfcDoor

`IfcDoor` represents doors.

Doors can connect spaces and may form part of an evacuation route.

### IfcStair and IfcStairFlight

These represent vertical circulation between storeys.

They are especially important in multi-storey buildings.

### IfcBuildingStorey

This represents the storeys of the building.

### IfcRelSpaceBoundary

This relationship can describe which building elements are connected to a space.

For example, it can help identify which doors belong to or connect to a space.

---

## Question

The Building 308 model contains:

```text
IfcDoor = 101
IfcSpace = 3
IfcRelSpaceBoundary = 0
```

Is the presence of 101 doors enough to automatically create a reliable evacuation network?

**Answer:** No.

The program still needs reliable information about which spaces the doors connect.

---

# 4. Check the FireExit property

Next, we check whether the doors contain information identifying emergency exits.

Import the property-set function:

```python
from ifcopenshell.util.element import get_pset
```

Get all doors:

```python
doors = model.by_type("IfcDoor")
```

Now inspect the first ten doors:

```python
for door in doors[:10]:

    fire_exit = get_pset(
        door,
        "Pset_DoorCommon",
        "FireExit"
    )

    print(
        door.GlobalId,
        door.Name,
        "FireExit =",
        fire_exit
    )
```

Possible results could look like:

```text
Door01 Entrance FireExit = True
Door02 Internal Door FireExit = False
Door03 Door FireExit = None
```

The value means:

```text
True  = the door is explicitly marked as a fire exit
False = the door is explicitly marked as not being a fire exit
None  = the information is missing
```

---

# 5. Count FireExit information

We can count how many doors contain each type of value.

Run:

```python
true_exits = 0
false_exits = 0
missing_fire_exit = 0

for door in doors:

    value = get_pset(
        door,
        "Pset_DoorCommon",
        "FireExit"
    )

    if value is True:
        true_exits += 1

    elif value is False:
        false_exits += 1

    else:
        missing_fire_exit += 1


print(
    "FireExit=True:",
    true_exits
)

print(
    "FireExit=False:",
    false_exits
)

print(
    "FireExit missing:",
    missing_fire_exit
)
```

For the Building 308 model used by Group 07, no explicit `FireExit` information was found.

---

## Why is this important?

A program should not automatically assume that a door is an emergency exit because it:

- is located on an external wall;
- is wide;
- is close to the outside;
- or has a certain name.

These assumptions may be wrong.

For a reliable BIM check, the information should be explicitly defined in the IFC or come from another justified information source.

---

# 6. Check space boundaries

Next, check whether the model contains `IfcRelSpaceBoundary`.

Run:

```python
boundaries = model.by_type(
    "IfcRelSpaceBoundary"
)

print(
    "Total space boundaries:",
    len(boundaries)
)
```

For Building 308, the result was:

```text
Total space boundaries: 0
```

This is important because the program does not have explicit space-boundary information that could help determine which spaces are connected to which doors.

---

# 7. Check whether boundaries reference doors

If the model contains space boundaries, we can check whether any of them point to doors.

Run:

```python
door_boundaries = 0

for rel in boundaries:

    element = getattr(
        rel,
        "RelatedBuildingElement",
        None
    )

    if (
        element is not None
        and element.is_a("IfcDoor")
    ):

        door_boundaries += 1


print(
    "Space boundaries related to doors:",
    door_boundaries
)
```

### Example output

```text
Space boundaries related to doors: 0
```

---

# 8. Create an information-readiness check

Now we combine the previous checks into one function.

Copy the following code:

```python
from ifcopenshell.util.element import get_pset


def check_egress_readiness(model):

    spaces = model.by_type(
        "IfcSpace"
    )

    doors = model.by_type(
        "IfcDoor"
    )

    boundaries = model.by_type(
        "IfcRelSpaceBoundary"
    )

    exit_count = 0
    missing_fire_exit = 0
    door_boundary_count = 0


    for door in doors:

        value = get_pset(
            door,
            "Pset_DoorCommon",
            "FireExit"
        )

        if value is True:

            exit_count += 1

        elif value is None:

            missing_fire_exit += 1


    for rel in boundaries:

        element = getattr(
            rel,
            "RelatedBuildingElement",
            None
        )

        if (
            element is not None
            and element.is_a("IfcDoor")
        ):

            door_boundary_count += 1


    issues = []


    if not spaces:

        issues.append(
            "No IfcSpace objects"
        )


    if not doors:

        issues.append(
            "No IfcDoor objects"
        )


    if not boundaries:

        issues.append(
            "No IfcRelSpaceBoundary relationships"
        )


    if (
        boundaries
        and door_boundary_count == 0
    ):

        issues.append(
            "No space boundaries related to doors"
        )


    if exit_count == 0:

        issues.append(
            "No explicit FireExit=True door"
        )


    if missing_fire_exit > 0:

        issues.append(
            f"{missing_fire_exit} doors "
            "have no FireExit value"
        )


    if issues:

        status = "INSUFFICIENT DATA"

    else:

        status = "READY"


    return status, issues
```

---

# 9. Run the readiness check

Run:

```python
status, issues = check_egress_readiness(
    model
)

print(
    "STATUS:",
    status
)

for issue in issues:

    print(
        "-",
        issue
    )
```

A model with missing information could produce:

```text
STATUS: INSUFFICIENT DATA

- No IfcRelSpaceBoundary relationships
- No explicit FireExit=True door
- 101 doors have no FireExit value
```

---

# 10. What does INSUFFICIENT DATA mean?

`INSUFFICIENT DATA` does not mean that the building is unsafe.

It means:

> The IFC model does not currently contain enough trustworthy information to perform the intended automated fire-egress analysis.

This distinction is important.

A BIM checking tool should not invent information in order to produce a result.

For example, the tool should not randomly select an external door and assume that it is an emergency exit.

---

# 11. Connection to IDS

The information identified in this tutorial can also be described as information requirements.

For example:

| Required information | IFC location | Purpose |
|---|---|---|
| Spaces | `IfcSpace` | Starting points for evacuation analysis |
| Doors | `IfcDoor` | Connections between areas |
| Fire exit information | `Pset_DoorCommon.FireExit` | Identify emergency exits |
| Space connectivity | `IfcRelSpaceBoundary` | Connect spaces and doors |
| Storeys | `IfcBuildingStorey` | Multi-storey context |
| Stairs | `IfcStair` / `IfcStairFlight` | Vertical circulation |

An IDS can be used to check whether required information has been delivered.

Python can then be used for more complex analysis.

The workflow becomes:

```text
Define information requirements
            ↓
Check IFC information
            ↓
Is enough information available?
        ↙             ↘
      NO               YES
       ↓                 ↓
Report missing        Perform
information           analysis
```

---

# 12. Peer exercise

Now use an IFC model available to your group.

Run:

```python
print(
    "Spaces:",
    len(model.by_type("IfcSpace"))
)

print(
    "Doors:",
    len(model.by_type("IfcDoor"))
)

print(
    "Space boundaries:",
    len(
        model.by_type(
            "IfcRelSpaceBoundary"
        )
    )
)
```

Then run:

```python
status, issues = check_egress_readiness(
    model
)

print(status)

for issue in issues:

    print("-", issue)
```

Answer the following questions.

### Question 1

How many `IfcSpace` objects are in your model?

**Answer:**

____________________________

### Question 2

How many `IfcDoor` objects are in your model?

**Answer:**

____________________________

### Question 3

How many `IfcRelSpaceBoundary` relationships are present?

**Answer:**

____________________________

### Question 4

Are any doors explicitly marked with:

```text
Pset_DoorCommon.FireExit = True
```

**Answer:**

____________________________

### Question 5

What result did the readiness check return?

```text
READY
```

or:

```text
INSUFFICIENT DATA
```

**Answer:**

____________________________

### Question 6

What information is missing from the IFC?

**Answer:**

____________________________

### Question 7

Do you agree with the program's decision?

Explain why.

**Answer:**

____________________________

---

# 13. Discussion

Consider the following question:

> If a door is located on an external wall, is that enough information to classify it automatically as an emergency exit?

Discuss this with another student.

The main point is that an automated BIM tool should avoid hidden assumptions.

---

# 14. What have we learned?

In this tutorial we used IfcOpenShell to:

- open an IFC model;
- inspect IFC classes;
- count spaces and doors;
- inspect fire-exit properties;
- inspect space boundaries;
- identify missing BIM information;
- decide whether an IFC model is ready for automated analysis.

The most important lesson is:

> **Reliable BIM automation should check its input information before producing analytical conclusions.**

Sometimes the correct result of an automated BIM check is not `PASS` or `FAIL`.

Sometimes the correct result is:

```text
INSUFFICIENT DATA
```

This allows missing information to be identified and corrected before more advanced BIM analysis is performed.
