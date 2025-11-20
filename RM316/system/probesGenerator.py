# VARIAaBLES TO CHANGE

# An array that specifies which approximate points to "probe around". 
names = [ "(6,3)", "(3,1)", "(2,5)"]
toProbe = [
    (3.37, 7.34, 1.28),
    (5.38, 3.38, 1.27),
    (1.31, 2.12, 1.27)
]
cellSize = 0.1


# --------------------------
# NO NEED TO TOUCH ANYTHING AFTER THIS 
# --------------------------

# Generate probes file first
for i, point in enumerate(toProbe):
    # Get the points nearest to this one
    points = [point]

    for x in [-1, 0, 1]:
        for y in [-1, 0, 1]:
            for z in [-1, 0, 1]:
                points.append((point[0] + x*cellSize, point[1] + y*cellSize, point[2] + y*cellSize))

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

# put like Hey guys this is awesome
    toPrint += f"// This is cell {names[i]}\n"

    for p in points:
        toPrint += f"\t ({p[0]} {p[1]} {p[2]})\n"

    toPrint += """);

fields  (U);

#includeEtc "caseDicts/functions/probes/probes.cfg"

// ************************************************************************* //
"""
    print(toPrint)

    with open("probes" + str(i+1), "w") as file:
        file.write(toPrint)