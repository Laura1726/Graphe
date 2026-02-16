# Analyse de Graphe : Marques de Voitures → Modèles → Carburants

## Description du Projet

Ce projet implémente une analyse de graphe pour visualiser et étudier les relations entre les marques de voiture, leurs modèles et les types de carburants associés. Le graphe est construit à partir de données CSV sur les véhicules et utilise la théorie des graphes pour extraire des insights significatifs.

## Structure du Graphe

Le graphe est **tripartite** et représente trois types de nœuds :
- **Marques** (bleu clair) : Constructeurs automobiles (Chevrolet, Ford, Mercedes-Benz, etc.)
- **Modèles** (vert clair) : Modèles de véhicules spécifiques
- **Carburants** (orange) : Types de carburant (Essence, Diesel, Électrique)

### Relations
- **Marque → Modèle** : Une marque produit différents modèles
- **Modèle → Carburant** : Chaque modèle utilise un type de carburant spécifique

## Technologies et Bibliothèques Utilisées

```python
pandas        # Manipulation et analyse des données CSV
networkx      # Construction et analyse du graphe
matplotlib    # Visualisation des graphes
glob          # Lecture de fichiers multiples
```

## Fonctionnalités Implémentées

### 1. **Parcours de Graphe**

#### Parcours en Largeur
- Explore le graphe niveau par niveau
- Utilisé via `nx.bfs_edges()`
- Utile pour trouver le plus court chemin en nombre d'arêtes

#### Parcours en Profondeur (DFS)
- Explore le graphe en profondeur avant d'explorer en largeur
- Utilisé via `nx.dfs_edges()`
- Utile pour explorer toutes les branches du graphe

### 2. **Plus Court Chemin (Algorithme de Dijkstra)**
- **Algorithme** : Dijkstra (implémentation NetworkX)
- **Fonction** : `nx.shortest_path()`
- **Utilisation** : Trouve le chemin le plus court entre une marque et un type de carburant
- **Complexité** : O((V + E) log V) avec V = nœuds, E = arêtes
- **Exemple** : `Chevrolet → G-Series 1500 → Essence` (2 arêtes)

### 3. **Mesures de Centralité**

#### Centralité de Degré (`nx.degree_centrality()`)
- Mesure le nombre de connexions directes d'un nœud
- Identifie les nœuds les plus connectés (hubs)
- **Résultat typique** : Les carburants (Essence, Diesel) ont la centralité la plus élevée

#### Centralité d'Intermédiarité (`nx.betweenness_centrality()`)
- Mesure l'importance d'un nœud comme "pont" entre d'autres nœuds
- Identifie les nœuds critiques dans le réseau
- **Algorithme** : Algorithme de Brandes

#### Centralité de Proximité (`nx.closeness_centrality()`)
- Mesure la distance moyenne d'un nœud à tous les autres
- Identifie les nœuds les plus "centraux" dans le réseau

### 4. **Coefficient de Clustering**
- **Fonction** : `nx.clustering()` et `nx.average_clustering()`
- Mesure la tendance des nœuds à former des triangles
- Coefficient typique ≈ 0 pour ce type de graphe biparti/triparti

### 5. **Analyse de Connectivité**

#### Composantes Connexes
- Vérifie si le graphe est entièrement connexe
- Utilise `nx.is_connected()` et `nx.connected_components()`

#### Diamètre et Rayon
- **Diamètre** : Plus longue distance entre deux nœuds (`nx.diameter()`)
- **Rayon** : Distance minimale du centre au nœud le plus éloigné (`nx.radius()`)
- **Centre** : Ensemble des nœuds avec l'excentricité minimale (`nx.center()`)

### 6. **Tous les Chemins Possibles**
- **Fonction** : `nx.all_simple_paths()`
- Trouve tous les chemins simples (sans cycle) entre deux nœuds
- Limité à un maximum de 4 arêtes pour éviter l'explosion combinatoire

## 📈 Visualisations

### Visualisation 1 : Graphe Complet
- Affiche l'ensemble du réseau avec des couleurs distinctes par type de nœud
- Tailles de nœuds proportionnelles à leur importance
- Layout : Spring Layout (`nx.spring_layout()`)

### Visualisation 2 : Plus Court Chemin
- Met en évidence le plus court chemin entre une marque et un carburant
- Nœuds du chemin en rouge
- Arêtes du chemin épaissies et colorées en rouge

## Analyses Statistiques Produites

1. **Informations générales** : Nombre de nœuds, d'arêtes, densité
2. **Ordre de visite BFS et DFS** : Premiers 10 nœuds visités
3. **Plus court chemin** : Chemin optimal et longueur
4. **Top 5 nœuds** : Par degré, intermédiarité, proximité
5. **Clustering** : Coefficient moyen et par nœud
6. **Connectivité** : Composantes connexes
7. **Diamètre et centre** : Propriétés structurelles du graphe
8. **Statistiques par carburant** : Nombre de modèles par type
9. **Chemins multiples** : Tous les chemins possibles entre deux marques

## Concepts de Théorie des Graphes Utilisés

- **Graphe non-orienté** : Les arêtes n'ont pas de direction
- **Graphe tripartite** : Trois ensembles de nœuds distincts
- **Parcours de graphe** : BFS et DFS
- **Plus court chemin** : Algorithme de Dijkstra
- **Centralité** : Degré, intermédiarité, proximité
- **Clustering** : Coefficient de regroupement
- **Connectivité** : Composantes connexes, diamètre, rayon
- **Chemins simples** : Chemins sans cycles
