matrice = [[1,2,3,4],[5,6,7,8],[9,10,11,12],[13,14,15,16]]

def saveMatrix(matrice, server):
    g = open(server,"w") 
    for i in matrice:
        for j in i:
            g.write(str(j))
            g.write(" ")
        g.write("\n")


def loadMatrix(server):
    g = open(server, "r")
    p = 1
    matrix = []
    for i in g.readlines():
        list = []
        c = i.split()
        for j in c:
            if '//' in j:
                break
            list.append(int(j))
        matrix.append(list)
    for i in range(len(matrix)-1):
        if len(matrix[i]) != len(matrix[i+1]):
            break
        else:
            p = p + 1
    if p == len(matrix):
        return matrix  

print("1. Load matrix")
print("2. Save matrix")
variabila = int(input("Enter an option: "))
if variabila == 1:
    print(loadMatrix("matrice.in"))
elif variabila == 2:
    saveMatrix(matrice, "matrice.out")
else:
    print("Invalid input")