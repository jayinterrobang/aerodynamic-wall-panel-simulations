import math

vertexList = {}
faceList = {}

walls = []
fans = []

cellSize = 0.2

class Face:
    def __init__(self, vertices, faceType = "wall"):
        self.vertices = vertices
        self.faceType = faceType 

        faceList[hashVertexList(vertices)] = self
    
    def printFace(self):
        print(f"\t\t({" ".join([str(x.number) for x in self.vertices])})")

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
    
    def printBlock(self):
        nx, ny, nz = self.getBlockCount()
        print(f"hex ({" ".join([str(x.number) for x in self.vertices])}) ({nx} {ny} {nz}) simpleGrading (1 1 1)", end="")

class Vertex:
    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z
        self.number = len(vertexList) 

        print(f"new vertex: ({x}, {y}, {z})")
        vertexList[(x,y,z)] = self 

    def printVertex(self):
        print(f"({self.x} {self.y} {self.z})", end="")

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

############################################
# ONLY EDIT THIS PART OF THE CODE FOR CONFIG
cuts = [
    [0, 2.1, 2.6, 4.1, 4.6, 8.1],
    [-1, 1.2, 1.7, 3.8, 4.3, 6.4, 6.9, 8.6],
    [0, 3.6]
]
############################################

def main():
    # FLOW
    # from the cuts dict, create all possible vertices. 
    for x in cuts[0]:
        for y in cuts[1]:
            for z in cuts[2]:
                createVertex(x,y,z)
    
    count = 0
    for vertex in vertexList.values():
        vertex.printVertex()
        print(f" // {count}")
        count += 1

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
                    walls.append(thisBlock.faces[1])
                if j == len(cuts[1])-2:
                    walls.append(thisBlock.faces[3])
                if k == 0:
                    walls.append(thisBlock.faces[0])
                if k == len(cuts[2])-2:
                    # if i and j are odd then its an inlet btw
                    if (i % 2 == 1) and (j % 2 == 1):
                        fans.append(thisBlock.faces[5])
                    else:
                        walls.append(thisBlock.faces[5])

                thisBlock.printBlock()
                print(f" // {count}")
                count += 1

    print("""walls
{
\t type wall;
\t faces (""")
    for face in walls:
        face.printFace()
    print("\t)")
    print(")")

    print("""fans
{
\t type patch;
\t faces (""")
    for face in fans:
        face.printFace()
    print("\t)")
    print(")")

if __name__ == "__main__":
    main()