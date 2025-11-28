# VARIAaBLES TO CHANGE

# An array that specifies which approximate points to "probe around". 
toProbe = []
seatCoords = [
    [1.30, 2.35, 3.35, 4.35, 5.30],
    [0.80, 2.12, 3.38, 4.70, 6.00, 7.34],
    [1.28]
]
for x in seatCoords[0]:
    for y in seatCoords[1]:
        for z in seatCoords[2]:
            toProbe.append([x,y,z])

cellSize = 0.1


# --------------------------
# NO NEED TO TOUCH ANYTHING AFTER THIS 
# --------------------------

toPrint = """
/*--------------------------------*- C++ -*----------------------------------*\\
=========                 |
\\      /  F ield         | OpenFOAM: The Open Source CFD Toolbox
 \\    /   O peration     | Website:  https://openfoam.org
  \\  /    A nd           | Version:  12
   \\/     M anipulation  |
-------------------------------------------------------------------------------
Description
Writes out values of fields from cells nearest to specified locations.

\\*---------------------------------------------------------------------------*/


points
(
"""

# Generate probes file first
for i, point in enumerate(toProbe):
    # Get the points nearest to this one

# put like Hey guys this is awesome
    toPrint += f"\t({point[0]} {point[1]} {point[2]})\n"

toPrint += """);

fields  (U);

#includeEtc "caseDicts/functions/probes/probes.cfg"

// ************************************************************************* //
"""

with open("probeComparison", "w") as file:
    file.write(toPrint)