## Peer Feedback — Group 3

Your accessibility use case is relevant to the architectural discipline and has a clear societal value. 
We think it is especially strong that you have translated a broad idea such as “the building should be accessible” into more specific checks such as:

- accessible movement between floors;
- sufficient door widths;
- accessible alternatives to stairs;
- hallway accessibility;
- accessible bathroom provision.

This makes the claim much more suitable for an automated BIM checking tool.

Another strong point is that you connect the IFC model with an external requirement source, BR18, instead of treating the IFC information itself as the requirement. This makes the intended workflow clear.

We also think the distinction between the tool performing the checks and the architect/designer making the final design decisions is good. The tool supports the design process without pretending to replace professional judgement.

### Information requirements

Your information requirements identify several useful IFC elements, including:

- `IfcStair`;
- `IfcTransportElement`;
- `IfcDoor`;
- `IfcSpace`;
- door `OverallWidth`;
- information about floors, hallways and bathrooms.

The use of `OverallWidth` for doors is a particularly clear example because it gives the tool a measurable value that can be compared with your stated accessibility requirement.

You have also identified important learning needs yourselves, especially:

- determining which floors a stair or elevator connects;
- identifying the function of `IfcSpace`;
- determining hallway width;
- identifying accessible bathrooms.

These are important issues because simply finding an IFC object is not necessarily enough to prove that the accessibility requirement is satisfied.

### Suggestions for improvement

The biggest point we would suggest improving is the way **relationships between elements are checked**.

For example, your current logic appears to say:

```text
IfcStair exists
↓
Look for IfcTransportElement
↓
Elevator exists
```

However, simply finding both a stair and an elevator somewhere in the building does not necessarily prove equal access.

The more important question is:

> Does the accessible alternative connect the same relevant floors or destinations as the stair?

For example:

```text
Stair connects Floor 1 → Floor 2 → Floor 3

Elevator connects Floor 1 → Floor 2 only
```

In this case, an elevator exists, but Floor 3 may still not have equivalent accessible access.

It would therefore strengthen the tool if the check became:

```text
Find stair
↓
Determine connected storeys
↓
Find accessible vertical alternative
↓
Determine its connected storeys
↓
Compare connectivity
```

### Door width

The door-width check is one of your clearest measurable checks.

You state that the tool will compare `IfcDoor.OverallWidth` with **0.77 m**.

It would be useful to clarify what happens when.

This prevents missing IFC data from accidentally being interpreted as a design failure.

### IfcSpace classification

The `IfcSpace` part probably needs more development.

You mention using `IfcSpaceType` to determine whether spaces are hallways, rooms or bathrooms. 
It would be useful to check exactly what information is actually available in the model for distinguishing these functions.
So defining a reliable space-classification method would improve the proposed tool significantly.


### Team diagram feedback

The team diagram has a clear overall structure:

The separation between **Report Issues** and **Generate accessibility compliance results** is good because it makes the final outputs understandable.

However, the diagram currently seems quite focused on `IfcSpace`.

Since your written use case also depends heavily on:

- `IfcDoor`;
- `IfcStair`;
- `IfcTransportElement`;
- building storeys;

we think those information inputs should also be visible in the diagram.

This would better represent the full scope described in your README.

### Questions for the group

We would be interested in hearing how you plan to answer these questions:

1. How will you determine which storeys a stair and elevator connect?
2. How will you identify whether an `IfcSpace` is a hallway, bathroom or another type of room?
3. How will you calculate hallway width if it is not stored as a simple IFC property?
4. What happens if `IfcDoor.OverallWidth` or another required value is missing?
5. How will you distinguish an accessible bathroom from a normal bathroom?
6. If an elevator exists but does not serve all the same floors as the stairs, how will the tool classify the result?
7. As the manager group, how will you combine the separate accessibility checks into one higher-level conclusion?

## Overall feedback

Overall, we think the accessibility use case is strong because it connects an important architectural and societal issue with measurable IFC information and regulatory requirements.

The door-width check is already quite concrete, while the more complex parts — especially **space classification, storey connectivity, hallway width and accessible alternatives to stairs** — need clearer rules before they can be automated reliably.

The next important step would be to focus less on whether individual IFC objects simply **exist**, and more on whether the correct **relationships and equivalent accessible routes** exist.

If those relationships are defined clearly, the tool could provide a useful and transparent accessibility review during the design phase.
