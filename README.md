# ARCH_2026_07

# A1 Forsenic BIM
 
## Group 
Group 07
 
## Focus Area
Fire evacuation
 
## Identified issues
 
The B308 IFC model contains insufficient information to identify fire evacution routes and emergency exits.
 
In IFC model no FireExit property was found on the doors or spaces.
No FireRating, SelfClosing or SmokeStop properties were found on the doors.
Therefore the geometry contains doors and a stair, but the IFC does not contain suffient semantic information to automatically determine which spaces and doors form the fire evacution system.
 
Ifc classes effected:
IfcSpace
IfcDoor
IfcStair
 
Issue type:
Model issue
 
System affected:
Space/ circulation/ fire evacuation
 
# Cause
 
The model contains very limited spatial decomposition. Only three IfcSpace objects are present and they represent generic areas rather than indivudual rooms, corridors, stair areas and evacuation routes.
 
In addition, fire-safety properties such as FireExit are not populated on spaces or doors.
 
This means that a fire evacuation route cannot reliably be generated from the IFC data.
 
# Identified possible solutions
 
Modelling
 
Model circulation and evacuation-relevant spaces explicitly.
 
Corridors, foyers, stair landings and other relevant spaces should be represented with suitable IfcSpace objects.
 
Add Pset_SpaceFireSafetyRequirement and set FireExit = TRUE for spaces that form part of the fire-escape system where appropriate.
 
For doors forming part of the escape route, populate Pset_DoorCommon properties such as:
 
FireExit
FireRating
SelfCosing
SmokeStop
 
This would allow the evacution network to be extracted automatically from the IFC.
 
## Potential Solution - tool
 
Model:
B.308.ifc
 
Location:
Spacital decomposition / IfcSpace, IfcDoor and IfcStair entities.
 
The issue was identified directly in the IFC model.
 
## Limitation
 
This analysis demonstrates an IFC modelling/information issue.
 
It does not prove that Building 308 is physically unsafe or non-compliant with Danish fire regulations because that supplied information does not include the approved fire strategy, occupancy loads or designation of emergency exists.
