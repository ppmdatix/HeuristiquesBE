import numpy as np
import pandas as pd
import random as rd
from matplotlib import pyplot as plt



def generationProbleme(n=10):
    names = [str(i) for i in range(n)]
    villes = dict((i,[rd.random(),rd.random()]) for i in range(n))
    matriceDistance = pd.DataFrame(index=names, columns=names)
    for i in range(n):
        for j in range(n):
            matriceDistance[str(i)][ str(j)] = np.sqrt((villes[i][0] - villes[j][0])**2 + (villes[i][1] - villes[j][1])**2)

    return names, villes, matriceDistance

def generationProblemeCercle(n=10):
    names = [str(i) for i in range(n)]
    villes = {}
    for i in range(n):
        theta = 2 * np.pi * rd.random()
        y = {i:[np.cos(theta),np.sin(theta)]}
        villes = {**villes, **y}
    
    matriceDistance = pd.DataFrame(index=names, columns=names)
    for i in range(n):
        for j in range(n):
            matriceDistance[str(i)][ str(j)] = np.sqrt((villes[i][0] - villes[j][0])**2 + (villes[i][1] - villes[j][1])**2)

    return names, villes, matriceDistance


def vizuResult(solution,villes):
    X = [villes[i][0] for i in villes]
    Y = [villes[i][1] for i in villes]
    Xchemin = [villes[i][0] for i in solution]
    Ychemin = [villes[i][1] for i in solution]
    plt.figure(figsize=(8,8))
    plt.plot(Xchemin, Ychemin,linestyle='dashed')
    plt.scatter(X,Y, marker="s",s=50, color = "red")
    plt.title("Path ")
    plt.show()
    plt.close()
    return True

def poidsSolution(solution, matriceDistance):
    N = len(solution)
    output = 0
    for i in range(N-1):
        output += matriceDistance[str(solution[i])][str(solution[i+1])]
    output += matriceDistance[str(solution[0])][str(solution[N-1])]
    return float(output/N)

def vizuEvolution(couts):
    plt.plot(couts)
    plt.title("Path cost evolution according to iterations")
    plt.show()
    plt.close()
    return True





