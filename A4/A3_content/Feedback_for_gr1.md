## Peer Feedback — Group 1

Your use case is clear and relevant to the architectural discipline. 
We especially liked that you avoided trying to automate whether a facade is generally “beautiful” and instead translated the architectural intent into more measurable aspects such as facade materials and colours.

A strong part of the work is the way you investigated the IFC model rather than assuming that the facade could be identified only through `IfcWall`. 
You recognised that the facade also contains elements such as `IfcWindow`, `IfcPlate`, `IfcMember`, `IfcBeam` and `IfcCovering`, which makes the proposed tool more realistic.

The team diagram also strengthens the proposal. 
It clearly shows the workflow from loading model properties, filtering different IFC classes, collecting the relevant element IDs, checking material and colour information, comparing the results, and finally separating the output into compliant elements and issues. 
This makes the overall logic of the proposed tool much easier to understand.

We also think it is good that the output is divided into:

- compliant elements;
- elements/issues requiring review;
- missing information.

This is better than only returning pass/fail because it allows the tool to distinguish between an actual design problem and missing BIM information.

### Suggestions for improvement

The main area that could be developed further is the comparison logic.

Your diagram contains a comparison stage, but it is still not completely clear how materials and colours are classified as compliant or non-compliant.

For example, the client requirement says that white, green and blue shades should be avoided. 
It would strengthen the tool if you defined exactly how the Python script decides whether an RGB value should be classified as white, green or blue.

Without defined thresholds, two people could interpret the same RGB value differently.

The same applies to materials. The IFC contains detailed material names such as:

`DTU_Masonry_Brick_Natural_Yellow_Mat`

but the client requirement is more general and refers to material categories such as brick, stone, concrete, wood, metallic and bio-based materials.

It would therefore be useful to explain whether your tool will:

- compare exact material names; or
- map IFC material names into broader material categories.

The second approach may be more reusable across different IFC models because material naming conventions can vary between projects.

### Facade identification

Your diagram shows separate filters for several IFC classes, which is a good approach.

However, the criteria for deciding whether each object is actually part of the external facade could be explained more clearly.

For `IfcWall`, you already mention:

`Pset_WallCommon.IsExternal`

But classes such as:

- `IfcPlate`
- `IfcMember`
- `IfcBeam`
- `IfcCovering`

may not have the same property.

Therefore, one useful improvement would be to clearly define the facade-selection rule for each IFC class.

This would make the filter stages shown in your team diagram easier to reproduce in the final Python tool.

### Multiple materials

You correctly identified that one facade element can contain more than one material, especially windows with both frame and glass materials.

It would be useful to clarify how the final result for one element is determined.

Will the whole window be classified as non-compliant if one component fails, or will each material/component be reported separately?

Clarifying this would make the output more transparent.

### Diagram feedback

The overall structure of the team diagram is logical

This would connect very well with your three proposed result types: compliant, non-compliant and missing information.

### Small documentation points

The identification **“Building 2601 – B308”** could be clarified so that the same project/building terminology is used consistently throughout the README.

The headings around A2d and A2e could also be checked because both appear to refer to “Tool Idea” in parts of the documentation.

### Questions for the group

We would be interested in hearing your answers to these questions:

1. How will the tool define when an RGB value is considered white, green or blue?
2. Will IFC material names be checked directly, or classified into broader material categories?
3. How will facade elements without `IsExternal` be identified?
4. If an element contains several materials and only one fails, how will the final result be reported?
5. How will the tool distinguish between **non-compliant information** and **missing information**?

## Overall feedback

Overall, we think the use case has a strong connection between the architectural requirement, the IFC information and the proposed automated workflow.

The IFC investigation and team diagram show that you have already identified an important challenge: the facade is made from several IFC classes and cannot be identified using one simple filter.
