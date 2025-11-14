
import math

############################################
# ONLY EDIT THIS PART OF THE CODE FOR CONFIG
cuts = [
    [-0.2, 2, 2.5, 4, 4.5, 6.9],
    [-0.2, 2.5, 3, 4.5, 5, 6.5, 7, 9.2],
    [0.1, 2.6]
]
############################################

vertexList = {}
faceList = {}

walls = []
fans = []
inlets = []
outlets = []

cellSize = 0.1

class Face:
    def __init__(self, vertices, faceType = "wall"):
        self.vertices = vertices
        self.faceType = faceType 

        faceList[hashVertexList(vertices)] = self
    
    def getString(self):
        return f"({" ".join([str(x.number) for x in self.vertices])})"

class Block:
    def createFaces(self):
        # order:
        # bottom, left, back, right, front, top
        self.faces.append(createFace(self.vertices[0:4]))
        self.faces.append(createFace([self.vertices[0], self.vertices[1], self.vertices[5], self.vertices[4]]))
        self.faces.append(createFace([self.vertices[1], self.vertices[2], self.vertices[6], self.vertices[5]]))
        self.faces.append(createFace([self.vertices[2], self.vertices[3], self.vertices[7], self.vertices[6]]))
        self.faces.append(createFace([self.vertices[0], self.vertices[3], self.vertices[7], self.vertices[4]]))
        self.faces.append(createFace([self.vertices[4], self.vertices[5], self.vertices[6], self.vertices[7]]))

    def __init__(self, vertices, hasInlet = False):
        self.vertices = vertices
        self.faces = []
        self.createFaces()

        if (hasInlet):
            self.faces[-1].inlet = True
    
    def getBlockCount(self):
        blockX = round(abs(self.vertices[0].x - self.vertices[-2].x) // cellSize)
        blockY = round(abs(self.vertices[0].y - self.vertices[-2].y) // cellSize)
        blockZ = round(abs(self.vertices[0].z - self.vertices[-2].z) // cellSize)

        return (blockX, blockY, blockZ)
    
    def getString(self):
        nx, ny, nz = self.getBlockCount()
        return f"hex ({" ".join([str(x.number) for x in self.vertices])}) ({nx} {ny} {nz}) simpleGrading (1 1 1)"


class Vertex:
    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z
        self.number = len(vertexList) 

        vertexList[(x,y,z)] = self 

    def getString(self):
        return f"({self.x} {self.y} {self.z})"

def createVertex(x, y, z):
    if ((x,y,z) in vertexList):
        return vertexList[(x,y,z)]
    
    return Vertex(x,y,z)

def createFace(vertices):
    # somehow hash all of the 
    verticesHash = hashVertexList(vertices)

    if (verticesHash in faceList):
        return faceList[verticesHash]
    
    return Face(vertices)

def hashVertexList(vertices):
    return " ".join([str(x.number) for x in vertices])

def main():
    # FLOW
    # from the cuts dict, create all possible vertices. 
    for x in cuts[0]:
        for y in cuts[1]:
            for z in cuts[2]:
                createVertex(x,y,z)
    
    to_write = """ /*--------------------------------*- C++ -*----------------------------------*\\
  =========                 |
  \\      /  F ield         | OpenFOAM: The Open Source CFD Toolbox
   \\    /   O peration     | Website:  https://openfoam.org
    \\  /    A nd           | Version:  12
     \\/     M anipulation  |
\\*---------------------------------------------------------------------------*/
FoamFile
{
    format      ascii;
    class       dictionary;
    object      blockMeshDict;
}
// * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * //\n"""
    to_write += "vertices (\n"
    count = 0
    for vertex in vertexList.values():
        to_write += "\t" + vertex.getString() + f" // {count}\n"
        count += 1
    to_write += ");\n\n"    

    to_write += "blocks (\n"

    count = 0
    for i in range(len(cuts[0])-1):
        for j in range(len(cuts[1])-1):
            for k in range(len(cuts[2])-1):
                blockVertices = []
                blockVertices.append(createVertex(cuts[0][i], cuts[1][j], cuts[2][k]))
                blockVertices.append(createVertex(cuts[0][i+1], cuts[1][j], cuts[2][k]))
                blockVertices.append(createVertex(cuts[0][i+1], cuts[1][j+1], cuts[2][k]))
                blockVertices.append(createVertex(cuts[0][i], cuts[1][j+1], cuts[2][k]))

                blockVertices.append(createVertex(cuts[0][i], cuts[1][j], cuts[2][k+1]))
                blockVertices.append(createVertex(cuts[0][i+1], cuts[1][j], cuts[2][k+1]))
                blockVertices.append(createVertex(cuts[0][i+1], cuts[1][j+1], cuts[2][k+1]))
                blockVertices.append(createVertex(cuts[0][i], cuts[1][j+1], cuts[2][k+1]))

                thisBlock = Block(blockVertices)

                if i == 0:
                    walls.append(thisBlock.faces[4])
                if i == len(cuts[0])-2:
                    walls.append(thisBlock.faces[2])
                if j == 0:
                    outlets.append(thisBlock.faces[1])
                if j == len(cuts[1])-2:
                    inlets.append(thisBlock.faces[3])
                if k == 0:
                    walls.append(thisBlock.faces[0])
                if k == len(cuts[2])-2:
                    # if i and j are odd then its an inlet btw
                    if (i % 2 == 1) and (j % 2 == 1):
                        fans.append(thisBlock.faces[5])
                    else:
                        walls.append(thisBlock.faces[5])

                to_write += "\t" + thisBlock.getString() + f" // {count}\n"
                count += 1
    
    to_write += ");\n\n"

    to_write += "boundary (\n"
    to_write += "walls {\n"
    to_write += "\t type wall; \n"
    to_write += "\t faces (\n"
    for face in walls:
        to_write += "\t\t" + face.getString() + "\n"
    to_write += "\t);\n"
    to_write += "}\n\n"

    to_write += "inlet {\n"
    to_write += "\t type patch; \n"
    to_write += "\t faces (\n"
    for face in inlets:
        to_write += "\t\t" + face.getString() + "\n"
    to_write += "\t);\n"
    to_write += "}\n\n"

    to_write += "outlet {\n"
    to_write += "\t type patch; \n"
    to_write += "\t faces (\n"
    for face in outlets:
        to_write += "\t\t" + face.getString() + "\n"
    to_write += "\t);\n"
    to_write += "}\n\n"

    count = 0
    for face in fans:
        count += 1
        to_write += "fan" + str(count) + " {\n"
        to_write += "\t type patch;\n"
        to_write += "\t faces (\n"
        to_write += "\t\t" + face.getString() + "\n"
        to_write += "\t);\n"
        to_write += "}\n"
    to_write += ");\n"

    with open("blockMeshDict", "w") as file:
        file.write(to_write)

if __name__ == "__main__":
    main()