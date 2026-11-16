# A3: Teach — Group 07

Course: 41934 Advanced Building Information Modeling (BIM), Fall 2026  
Group: 07  
Focus area: Fire evacuation/egress  
Target role: BIM Analyst  
Target learning level: Level 2  

## Tutorial title

*Checking IFC Fire-Egress Data with IfcOpenShell*

## Summary

A tutorial showing BIM analysts how to inspect IFC spaces, doors, fire-exit properties and space boundaries with Python and IfcOpenShell, then decide whether a model contains enough information for reliable evacuation checking.

## Learning need

During our previous BIM analysis, we found that an IFC model may contain visible doors, stairs and spaces while still lacking the information and relationships needed for reliable automated fire-evacuation analysis.

Our learning need is:

How can a BIM analyst use Python and IfcOpenShell to determine whether an IFC model contains sufficient fire-egress information before attempting automated route analysis?


## Learning objectives

After completing the tutorials, participants should be able to:

1. Open an IFC model using IfcOpenShell.
2. Identify relevant IFC classes for fire evacuation.
3. Read Pset_DoorCommon.FireExit.
4. Inspect IfcRelSpaceBoundary.
5. Explain why geometry alone is insufficient for reliable evacuation checking.
6. Determine whether an IFC is READY or contains INSUFFICIENT DATA.

## Tutorial formats

We use two separate tutorial formats.

### Tutorial 1 — Markdown

[Open Tutorial 1: Markdown](Tutorial_1_Markdown.md)

### Tutorial 2 — Jupyter Notebook

[Open Tutorial 2: Jupyter Notebook](Tutorial_2_Jupyter.ipynb)


