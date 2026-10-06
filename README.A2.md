# A2 - IFC Fire evacuation checker
Group: Group 07
Focus area: Fire evacuation

## A2a: About our group
### Python coding level
Our group's total Python coding level is: 2 - Neutral
### Role: analyst

## A2b: Identify claim
### Building selected
Building #2608/ Building 308, based on 26-08-A-ClientReport-Anon.pdf provided in DTU Learn
### Claim to fact check
In the report's section (1.2.6 Fire Safety and Egress) states a coordinated fire egress strategy. 
The claim choosen for A2 is: 
"... evacuation stairs and emergency exits is carefully arranged to ensure that the maximum escape route distance does not exceed 25 m."

The report also contains related claims
- Two additional evacuation stairs are positioned on the west and east sides
- Each evacuation stair has at least 1.0 m clear width
- External escape stairs are separated from the interior by fire rated doors
- The main entrance and public spaces such as the auditorium have at least 1.20 m effective door width
- Escape doors open in the direction of egress
### Why this claim was selected
This claim was choosen because it builds on the issue identified in A1. The analysis in A1 showed that the IFC model may not contain enough information to clearly identify and assess the fire evacuation system.
The claim also allows several types og BIM information to be checked, including geometry, spaces, doors, stairs and evacuation distances.

The proposed tool should therefore give one of three results:
- PASS - the model contains enough information and the claim is supported
- FAIL - the model contains enough information, but the claim is not supported
- NOT VERIFIABLE - important information is missing or unclear, so the claim can not be checked reliably.
The NOT VERIFIABLE result is important because missing information in the IFC model does not automatically mean that the building is unsafe or does not comply with fire regulations. 

## A2c: Use case
### How would the claim be checked
1. Define the requirements of the claim, including the maximum escape route distance of 25 m.
2. Load the IFC model using Python and IfcOpenShell.
3. Check whether the model contains the necessary information about spaces, doors, stairs, exits and connections between spaces.
4. Identify the spaces and building elements that are relevant to the evacuation route.
5. Create a connection between spaces, doors, stairs and exits to represent possible escape routes.
6. Check additional information where available, such as stair width, door width, fire rating information and door opening directions.

### When should it be checked
In the design and modeling phase, after the fire egress concept has bee modelled and again after any change to room layout, door, stairs or external exits. 

### What information does this claim rely on
The check requires:
- Spaces and their geometry
- Doors, stairs and emergency exits
- Connections between the elements
- Relevant dimenstions and fire safety properties
- The 25 m. requirement from the design report

### BIM purpose required
- Primary: Analyse - derive route lengths and validate the claim against model data.
- Supporting: Gather - extract IFC data and detect missing information.
- Supporting: Communicate - report pass/fail/not verifiable results to the decision makers.

### Closest BIM use
- The primary BIM use would be Code Validation/Model checking. The task would compare facts derived from the model with project criteria
- The secondary BIM use would be Analysis. A analysis would be given of the fire evacuation route in building 308.

### BPMN diagram
<img width="751" height="332" alt="image" src="https://github.com/user-attachments/assets/760e6ea4-5811-4af7-90a5-cca46c93a7e8" />

Figure 1: Fire escape route check

## A2d - Scope the use case
The purpose of the tool is to determine whether IFC model contains sufficient and reliable information to evaluate the selected fire evacuation claim and, where possible, verify the claim using model derived geometry, relationships, properties, and calculated route distances. Where the required is incomplete or ambiguous, the tool will report the claim as not verifiable rather than interpreting missing data as non compliance. 
<img width="838" height="223" alt="image" src="https://github.com/user-attachments/assets/911cd230-dab3-432c-b333-a679303fa990" />
Figur 2: Diagram for tool
