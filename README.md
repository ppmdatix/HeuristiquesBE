**WARNING:** YOU SHOULD READ THIS readme with https://hackmd.io/

:::info 
**Année:** 2019
**Ecole:** École Centrale de Lyon 
**Cours:** Algorithme pour la décision en entreprise
**Activité:** BE 1
**Elève:** PESEUX Paul
**Professeur** Monsieur Liaudet
:::

# INTRODUCTION

Lors de ce BE, nous mettons en pratique les connaissances théoriques acquises lors du cours d'Algorithme pour la décision en entreprise. Pour ce faire nous nous concentrons premièrement sur un problème combinatoire, le Voyageur de Commerce, donc discret. Ensuite nous nous intéressons à un problème d'optimisation continu.

Pour ces deux problématiques, on utilise des heuristiques. Il s'agit de techniques basées sur l’intuition et/ou sur une reproduction des phénomènes observés dans le vivant. Observer la nature qui via le processus d'évolution a pu converger vers une solution adaptée est souvent une très bonne idée.

On ne cherchera pas nécessairement la meilleure solution, mais une solution de bonne qualité pour un temps de calcul acceptable. En effet pour les problèmes combinatoires, comparer toutes les solutions (un nombre fini) et choisir l'optimale est totalement irréalisable.
Ces méthodes s’appuient sur de l’exploration opportuniste de l’espace de des solutions autour de deux concepts : l’apprentissage et l’intensification. Une alternance entre ces deux phases est à la base des méthodes présentées ici.


:::success
**Tous** les résultats présentés ici ont été implémentés dans des _Notebook Python_ disponnibles dans ce [répertoire](https://github.com/ppmdatix/HeuristiquesBE) qui contient tout le travail réalisé pour ce **BE**
:::



# 1. Le voyageur de commerce
Dans une première partie on s’intéresse au Problème du Voyageur de commerce. Ce problème consiste à déterminer le parcours d'un ensemble de points de coût minimum.
Si j'ai des cousins à Lille, Paris et Marseille, il est clair que je vais parcourir la France dans l'ordre précité, et non Lille, Marseille Paris.
Cependant pour un nombre important de points, la solution est beaucoup moins triviale !
En effet ce problème est un problème NP-Complet. Ainsi le nombre de cycles hamiltoniens croit de manière trop importante avec le nombre de points pour pouvoir utiliser des algorithmes qui parcourt en entier l'espace des solutions en des temps de calcul raisonnable.
Prenons le cas de N villes. En supposant le point de départ fixé, on dispose donc de N-1 choix pour la première ville visitée. Ensuite il nous reste puis N-2 choix. Finalement on a (N-1) ! cycles hamiltoniens. Pour 50 villes, on arrive à temps de calcul de X Milliards d’années en prenant une microseconde comme temps de calcul pour un trajet ! D’où la nécessité d’utiliser des heuristiques qui permettent de ne pas tester toutes les solutions.

### 1.1 Algorithme glouton
La méthode la plus simple (après l'aléatoire) qui vient à l'esprit est de se déplacer de proche en proche.Ainsi l’algorithme du Glouton du plus proche voisin fonctionne de cette façon. Il s'agit une méthode constructiviste : on construit itérativement un chemin qui se termine en solution acceptable. En effet on se refuse de repasser par une même ville

L’algorithme est donc le suivant :


```python
Input Solution=[point_de_depart], Tabou=[]
while not Toutes les villes visitées
    Intensification : Calcul des distances entre la ville actuelle s = Solution[-1] et toutes les villes n’appartenant pas à Tabou
    
    Diversification : sbis = min(d(s,sbis) for sbis not in Tabou)
    
    Déplacement en sbis, Solution = Solution + [sbis]
    Ajout de sbis à la liste Tabou
end while

```


#### 1.1.1 Cas des villes placées sur un cercle

Ce cas a été impémenté sous _Python_. Les villes sont réparties aléatoirement (on tire un $\theta$ uniformément sur $0, 2\pi$) sur un cercle de rayon $R$. On remarque que ce $R$ n'est pas important pour notre problème.
Lorsque $n$ est grand le parcours devient optimal. En effet cette longueur tend vers $2\pi$.
Pour obtenir ce résultat on a générer $10$ fois pour chaque $n$ une topologie et ensuite appliquer l'algorithme Glouton. On a ensuite conservé la moyenne des longueurs de parcours afin d'obtenir cette visualisation : 
<figure>
<img src="https://i.imgur.com/mbbWuSH.png" width="400"  />
  <figcaption>Glouton Cercle</figcaption>
</figure>


De façon assez surprenante on remarque que l'estimation obtenue est pour $n$ grand, légèrement supérieure à $2\pi$. Dans le cas de la solution optimale pour $n$ grand, le parcours est un polygone convexe inscrit dans le cercle untié, son périmètre est donc inférieure à $2\pi$.


<figure>
<img src="https://i.imgur.com/McqLigW.png" width="400"  />
  <figcaption>Glouton cercle gd nombre</figcaption>
</figure>



On présente ici une visualisation du parcours obtenu pour $20$ et $100$ villes.

<figure>
<img src="https://i.imgur.com/qjYpp1g.png" width="400"  />
  <figcaption>Glouton pour 20 villes</figcaption>
</figure>

<figure>
<img src="https://i.imgur.com/rLekumk.png" width="400"  />
  <figcaption>Glouton pour 100 villes</figcaption>
</figure>





#### 1.1.2 Cas des villes placées aléatoirement dans un carré

Dans le cas précédent, l'algorithme Glouton donnait des résultats satisfaisants. Cependant la topologie était très simple. On va complexifier cette dernière.

On se place désormais dans le cas de $n$ villes placées aléatoirement dans un carré de côté 1. Une fois encore le côté du carré n'est pas important, le problème étant invariant par homotétie. Les ordonnées et les abscisses des villes sont issus de tirages aléatoires indépendants uniformes sur $0,1$.

En appliquant la même méthode, on obtient 
<figure>
<img src="https://i.imgur.com/PyT2phJ.png" width="400"  />
  <figcaption>Glouton Carre</figcaption>
</figure>



### 1.2 Le recuit Simulé
Des résultats numériques précédents, on comprend l'importance d'une plus performante. En effet le cas de villes placées sur un cercle n'est qu'un cas d'école et le cas 1.1.2 est davantage rencontré en pratique. Par ailleurs nous avons montré plus haut l'importance d'heuristique de par le caractère combinatoire du problème.

Le principe du recuit simulé repose sur une suite de solutions, c'est à dire de parcours qui converge vers une solution acceptable. L'idée, qui repose sur une analogie physique avec les matériaux, est de générer à partir de la dernière solution obtenue une solution alternative. Cette solution alternative remplace la précédente si et seulement si une condition (qui dépend de l'avancée de notre recherche) est satisfaite. Ainsi le pseudo code donne :

```python
Input Solution
================================
while not critere_d_arret
    Solution_generee = generer(Solution)
    if condition_d_acceptation(Solution_generee)
        Solution = Solution_generee
    end if
end while
================================
Output Solution
        
```

De cette définition il est nécessaire de définit **générer**, la **condition d'acceptation** et le **critère d'arrêt**. 

#### 1.2.1 Generer
L'idée derrière la fonction **générer** est de _décroiser_ les noeuds du parcours qui ne sont moralement pas optimaux. Ainsi dans un cas simple, pour passer de $A-D-C-B$ à $A-C-D-B$, il faut renverser l'ordre des villes entre les points extrêmes du croisement. 

Graphiquement, cela donne



<figure>
<img src="https://i.imgur.com/mDJPSXx.png" width="300"  />
  <figcaption>Avec croisement</figcaption>
</figure>

<figure>
<img src="https://i.imgur.com/IAosf1x.png" width="300"  />
  <figcaption>Après  décroisement</figcaption>
</figure>


Ainsi pour générer une solution alternative, on peut tirer aléatoirement deux villes et renverser l'ordre des villes intermédiaires dans le parcours de la solution actuelle. Ainsi le pseudo code donne.

```python
Input Solution(taille=N)
================================
Tirer aléatoirement i < j <=N
for k in range(j-i + 1):
    Solution[i + k] = Solution[j-k]
================================
Output Solution    
```

#### 1.2.2 Condition d'acceptation
Pour coller avec l'analogie mécanique, la condition d'acceptation dépend d'une température décroissante. 



Dans ce **BE**, plusieurs températures ont été testées, en fonction de l'itération $n$  :
- Linéare : $T = an +b$
- Logarithmique : $T = \frac{1}{\log n}$
- Géopmétrique : $T = \alpha^n$, avec $\alpha < 1$

#### 1.2.3 Critère d'arrêt
Le critère d'arrêt le plus simple est un nombre fixe d'itération. Cependant en utilisant un tel critère, nous ne nous assurons pas une convergence de notre algorithme. Ainsi plutot que de choisir un _niter_ trop grand, on peut calculer la _log_-progression à un pas fixé et arreter lorsque l'on ne progresse plus. Voici le  code.

```pythpon
def critere_arret(n,pas,log_seuil):
    if 0 == n%pas:
        return log_seuil < log(fonction(X[n-pas]) - fonction(X[n])) 
    else:
        return False
```


# 2. Minimum d'une Fonction
Il existe de nombreuses façons d'estimer l'extremum d'une fonction sur un domaine borné. La façon explorée dans ce BE est celle des [Essaims particulaires](https://en.wikipedia.org/wiki/Particle_swarm_optimization)

## 2.1 Essaims Particulaires
![Alt Text](http://ittner.github.io/abelhas/particles.gif)







## Figures


<figure>
<img src="https://i.imgur.com/N833eV0.png" width="300"  />
  <figcaption>DropWave</figcaption>
</figure>

<figure>
<img src="https://i.imgur.com/qb2Trce.png" width="300"  />
  <figcaption>EOSSAM</figcaption>
</figure>







