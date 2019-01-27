Algorithmes pour la décision en entreprise
BE_1 Heuristiques
2019
École Centrale de Lyon – Algorithme pour la décision en entreprise – BE_1 1
PESEUX Paul


# INTRODUCTION

Lors de ce BE, nous mettons en pratique les connaissances théoriques acquises lors du cours d'Algorithme pour la décision en entreprise. Pour ce faire nous nous concentrons premièrement sur un problème combinatoire, le Voyageur de Commerce, donc discret. Ensuite nous nous intéressons à un problème d'optimisation continu.

Pour ces deux problématiques, on utilise des heuristiques. Il s'agit de techniques basées sur l’intuition et/ou sur une reproduction des phénomènes observés dans le vivant. Observer la nature qui via le processus d'évolution a pu converger vers une solution adaptée est souvent une très bonne idée.

On ne cherchera pas nécessairement la meilleure solution, mais une solution de bonne qualité pour un temps de calcul acceptable. En effet pour les problèmes combinatoires, comparer toutes les solutions (un nombre fini) et choisir l'optimale est totalement irréalisable.
Ces méthodes s’appuient sur de l’exploration opportuniste de l’espace de des solutions autour de deux concepts : l’apprentissage et l’intensification. Une alternance entre ces deux phases est à la base des méthodes présentées ici.



# 1. Le voyageur de commerce
Dans une première partie on s’intéresse au Problème du Voyageur de commerce. Ce problème consiste à déterminer le parcours d'un ensemble de points de coût minimum.
Si j'ai des cousins à Lille, Paris et Marseille, il est clair que je vais parcourir la France dans l'ordre précité, et non Lille, Marseille Paris.
Cependant pour un nombre important de points, la solution est beaucoup moins triviale !
En effet ce problème est un problème NP-Complet. Ainsi le nombre de cycles hamiltoniens croit de manière trop importante avec le nombre de points pour pouvoir utiliser des algorithmes qui parcourt en entier l'espace des solutions en des temps de calcul raisonnable.
Prenons le cas de N villes. En supposant le point de départ fixé, on dispose donc de N-1 choix pour la première ville visitée. Ensuite il nous reste puis N-2 choix. Finalement on a (N-1) ! cycles hamiltoniens. Pour 50 villes, on arrive à temps de calcul de X Milliards d’années en prenant une microseconde comme temps de calcul pour un trajet ! D’où la nécessité d’utiliser des heuristiques qui permettent de ne pas tester toutes les solutions.

### 1.1 Algorithme glouton
La méthode la plus simple (après l'aléatoire) qui vient à l'esprit est de se déplacer de proche en proche.Ainsi l’algorithme du Glouton du plus proche voisin fonctionne de cette façon. Il s'agit une méthode constructiviste : on construit itérativement un chemin qui se termine en solution acceptable. En effet on se refuse de repasser par une même ville

L’algorithme est donc le suivant :

\begin{itemize}[listparindent=\parindent]
\item Initialisation : Solution partielle $S  = [\text{point de départ}]$
 et Liste tabou $T=[]$

 \item Tant que toutes les villes n’ont pas été parcourues :
 - Intensification : Calcul des distances entre la ville actuelle $s = S[-1]$ et toutes les villes n’appartenant pas à $T$

\end{itemize}
• 
• Diversification : s’ = min {d(s,s’) | s’∉ 𝑻 }
• Déplacement en s’, S = S + [s']
• Ajout de s’ à la liste tabou

#### 1.1.1 Cas des villes placées sur un cercle

Ce cas a été impémenté sous \textit{Python}. Les villes sont réparties aléatoirement (on tire un $\theta$ uniformément sur $0, 2\pi$) sur un cercle de rayon $R$. On remarque que ce $R$ n'est pas important pour notre problème.
Lorsque $n$ est grand le parcours devient optimal. En effet cette longueur tend vers $2\pi$.
Pour obtenir ce résultat on a générer $10$ fois pour chaque $n$ une topologie et ensuite appliquer l'algorithme Glouton. On a ensuite conservé la moyenne des longueurs de parcours afin d'obtenir cette visualisation.

De façon assez surprenante on remarque que l'estimation obtenue est pour $n$ grand, légèrement supérieure à $2\pi$. Dans le cas de la solution optimale, le parcours est un convexe inscrit dans le cercle untié, son périmètre est donc inférieure à $2\pi$.

On présente ici une visualisation du parcours obtenu pour $200$ villes.



#### 1.1.2 Cas des villes placées aléatoirement dans un carré

Dans le cas précédent, l'algorithme Glouton donnait des résultats satisfaisants. Cependant la topologie était très simple. On va complexifier cette dernière.

On se place désormais dans le cas de $n$ villes placées aléatoirement dans un carré de côté 1. Une fois encore le côté du carré n'est pas important, le problème étant invariant par homotétie. Les ordonnées et les abscisses des villes sont issus de tirages aléatoires indépendants uniformes sur $0,1$.

En appliquant la même méthode, on obtient 



### 1.2 Le recuit Simulé
Des résultats numériques précédents, on comprend l'importance d'une plus performante. En effet le cas de villes placées sur un cercle n'est qu'un cas d'école et le cas 1.1.2 est davantage rencontré en pratique. Par ailleurs nous avons montré plus haut l'importance d'heuristique de par le caractère combinatoire du problème.

Le principe du recuit simulé repose sur une suite de solutions, c'est à dire de parcours qui converge vers une solution acceptable. L'idée, qui repose sur une analogie physique avec les matériaux, est de générer à partir de la dernière solution obtenue une solution alternative. Cette solution alternative remplace la précédente si et seulement si une condition (qui dépend de l'avancée de notre recherche) est satisfaite. Ainsi le pseudo code donne :


De cette définition il est nécessaire de définit **générer** et la **condition d'acceptation**. 

#### Generer
L'idée derrière la fonction **générer** est de _décroiser_ les noeuds du parcours qui ne sont moralement pas optimaux. Ainsi dans un cas simple, pour passer de $A-D-C-B$ à $A-C-D-B$, il faut renverser l'ordre des villes entre les points extrêmes du croisement. Ainsi pour générer une solution alternative, on peut tirer aléatoirement deux villes et renverser l'ordre des villes intermédiaires dans le parcours de la solution actuelle. Ainsi le pseudo code donne.

#### Condition d'acceptation

