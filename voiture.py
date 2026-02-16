import pandas as pd
import glob
import networkx as nx
import matplotlib.pyplot as plt
import random

files = glob.glob("data/*.csv")

df_list = []

for f in files:
    df_list.append(pd.read_csv(f))

df = pd.concat(df_list)

print(df.head())
print(f"Nombre total de lignes : {len(df)}")

# Échantillon aléatoire simple
#df = df.sample(50)

# Prendre les N premières marques les plus fréquentes
top_marques = df["make"].value_counts().head(5).index
df = df[df["make"].isin(top_marques)]
df = df.sample(min(80, len(df)))



print(f"Nombre de lignes après filtrage : {len(df)}")


G = nx.Graph()

carburants = ["Essence", "Diesel", "Électrique"]

for _, row in df.iterrows():
    G.add_edge(row["make"], row["model"])

modeles_vus = set()
for _, row in df.iterrows():
    modele = row["model"]
    
    if modele not in modeles_vus:
        #carburant = random.choice(carburants)
        
        if "tesla" in modele.lower() or "leaf" in modele.lower():
             carburant = "Électrique"
        elif "prius" in modele.lower():
             carburant = "Hybride"
        else:
             carburant = random.choice(["Essence", "Diesel"])
        
        G.add_edge(modele, carburant)
        modeles_vus.add(modele)


marques = set()
modeles = set()

for _, row in df.iterrows():
    marques.add(row["make"])
    modeles.add(row["model"])

for node in G.nodes():
    if node in marques:
        G.nodes[node]['subset'] = 0
    elif node in modeles:
        G.nodes[node]['subset'] = 1
    elif node in carburants:
        G.nodes[node]['subset'] = 2


pos = nx.spring_layout(G, k=0.5, iterations=50, seed=42)


print("\n" + "="*80)
print("ANALYSES DU GRAPHE")
print("="*80)


# 1. INFO

print("\n1. INFORMATIONS GÉNÉRALES")
print("-" * 40)
print(f"Nombre de nœuds : {G.number_of_nodes()}")
print(f"Nombre d'arêtes : {G.number_of_edges()}")
print(f"Densité du graphe : {nx.density(G):.4f}")
print(f"Le graphe est connexe : {nx.is_connected(G)}")


# 2 PARCOURS EN LARGEUR (BFS - Breadth First Search)

print("\n2. PARCOURS EN LARGEUR (BFS)")
print("-" * 40)
# Choisir un nœud de départ (une marque)
noeud_depart = list(marques)[0]
print(f"Départ depuis : {noeud_depart}")

bfs_edges = list(nx.bfs_edges(G, noeud_depart))
print(f"Ordre de visite BFS (premiers 10) : ")
for i, (u, v) in enumerate(bfs_edges[:10]):
    print(f"  {i+1}. {u} → {v}")


# 3 PARCOURS EN PROFONDEUR (DFS)

print("\n3. PARCOURS EN PROFONDEUR (DFS)")
print("-" * 40)
print(f"Départ depuis : {noeud_depart}")

dfs_edges = list(nx.dfs_edges(G, noeud_depart))
print(f"Ordre de visite DFS (premiers 10) : ")
for i, (u, v) in enumerate(dfs_edges[:10]):
    print(f"  {i+1}. {u} → {v}")


# 4 PLUS COURT CHEMIN (DIJKSTRA)

print("\n4. PLUS COURT CHEMIN (ALGORITHME DE DIJKSTRA)")
print("-" * 40)

# Trouver le chemin entre une marque et un carburant
if len(list(marques)) > 0 and len(carburants) > 0:
    marque_exemple = list(marques)[0]
    carburant_exemple = carburants[0]
    
    try:
        chemin = nx.shortest_path(G, marque_exemple, carburant_exemple)
        print(f"Chemin le plus court de '{marque_exemple}' à '{carburant_exemple}' :")
        print(" → ".join(chemin))
        print(f"Longueur du chemin : {len(chemin) - 1} arêtes")
    except nx.NetworkXNoPath:
        print(f"Pas de chemin entre {marque_exemple} et {carburant_exemple}")


# 5 CENTRALITÉ (Importance des nœuds)

print("\n5. MESURES DE CENTRALITÉ")
print("-" * 40)

# Centralité de degré (nombre de connexions)
degree_centrality = nx.degree_centrality(G)
top_degree = sorted(degree_centrality.items(), key=lambda x: x[1], reverse=True)[:5]
print("Top 5 nœuds par degré (nombre de connexions) :")
for node, centrality in top_degree:
    print(f"  {node}: {centrality:.4f} ({G.degree(node)} connexions)")

# Centralité d'intermédiarité (nœuds "ponts")
betweenness = nx.betweenness_centrality(G)
top_betweenness = sorted(betweenness.items(), key=lambda x: x[1], reverse=True)[:5]
print("\nTop 5 nœuds par intermédiarité (importance comme 'pont') :")
for node, centrality in top_betweenness:
    print(f"  {node}: {centrality:.4f}")

# Centralité de proximité (distance moyenne aux autres)
closeness = nx.closeness_centrality(G)
top_closeness = sorted(closeness.items(), key=lambda x: x[1], reverse=True)[:5]
print("\nTop 5 nœuds par proximité (distance moyenne aux autres) :")
for node, centrality in top_closeness:
    print(f"  {node}: {centrality:.4f}")


# 6 CLUSTERING (Coefficient de regroupement)
print("\n6. COEFFICIENT DE CLUSTERING")
print("-" * 40)
clustering_coef = nx.clustering(G)
avg_clustering = nx.average_clustering(G)
print(f"Coefficient de clustering moyen : {avg_clustering:.4f}")

top_clustering = sorted(clustering_coef.items(), key=lambda x: x[1], reverse=True)[:5]
print("Top 5 nœuds par clustering :")
for node, coef in top_clustering:
    print(f"  {node}: {coef:.4f}")


#7 COMPOSANTES CONNEXES
print("\n7. COMPOSANTES CONNEXES")
print("-" * 40)
if nx.is_connected(G):
    print("Le graphe est entièrement connexe (1 composante)")
else:
    composantes = list(nx.connected_components(G))
    print(f"Nombre de composantes connexes : {len(composantes)}")
    for i, comp in enumerate(composantes, 1):
        print(f"  Composante {i} : {len(comp)} nœuds")

# 8 EXCENTRICITÉ ET DIAMÈTRE
print("\n8. EXCENTRICITÉ ET DIAMÈTRE")
print("-" * 40)
if nx.is_connected(G):
    diametre = nx.diameter(G)
    rayon = nx.radius(G)
    centre = nx.center(G)
    
    print(f"Diamètre du graphe : {diametre}")
    print(f"Rayon du graphe : {rayon}")
    print(f"Centre(s) du graphe : {centre}")
else:
    print("Le graphe n'est pas connexe, impossible de calculer le diamètre")

#9 ANALYSE PAR TYPE DE CARBURANT
print("\n9. STATISTIQUES PAR TYPE DE CARBURANT")
print("-" * 40)
for carburant in carburants:
    if carburant in G:
        voisins = list(G.neighbors(carburant))
        print(f"{carburant} : {len(voisins)} modèles connectés")

#10 TOUS LES CHEMINS ENTRE DEUX NŒUDS
print("\n10. TOUS LES CHEMINS POSSIBLES (exemple)")
print("-" * 40)
if len(list(marques)) > 1:
    marque1 = list(marques)[0]
    marque2 = list(marques)[1]
    
    try:
        tous_chemins = list(nx.all_simple_paths(G, marque1, marque2, cutoff=4))
        print(f"Chemins de '{marque1}' à '{marque2}' (max 4 arêtes) :")
        for i, chemin in enumerate(tous_chemins[:5], 1):
            print(f"  Chemin {i}: {' → '.join(chemin)}")
        if len(tous_chemins) > 5:
            print(f"  ... et {len(tous_chemins) - 5} autres chemins")
    except:
        print(f"Pas de chemin trouvé entre {marque1} et {marque2}")

print("\n" + "="*80)



#VISUALISATION
plt.figure(figsize=(20, 14))

node_colors = []
node_sizes = []
for node in G.nodes():
    if node in marques:
        node_colors.append('lightblue')
        node_sizes.append(500)
    elif node in modeles:
        node_colors.append('lightgreen')
        node_sizes.append(300)
    elif node in carburants:
        node_colors.append('orange')
        node_sizes.append(800)
    else:
        node_colors.append('gray')
        node_sizes.append(300)

nx.draw(G, pos, with_labels=True, node_size=node_sizes, font_size=8, 
        node_color=node_colors, edge_color='gray', alpha=0.6, 
        font_weight='bold', linewidths=1.5, edgecolors='black')

plt.title("Graphe Marques → Modèles → Carburants")
plt.tight_layout()
plt.show()



#PLUS COURT CHEMIN
if len(list(marques)) > 0 and len(carburants) > 0:
    plt.figure(figsize=(20, 14))
    
    marque_exemple = list(marques)[0]
    carburant_exemple = carburants[0]
    
    try:
        chemin_court = nx.shortest_path(G, marque_exemple, carburant_exemple)
        
        node_colors = []
        node_sizes_path = []
        for node in G.nodes():
            if node in chemin_court:
                node_colors.append('red')
            elif node in marques:
                node_colors.append('lightblue')
            elif node in modeles:
                node_colors.append('lightgreen')
            elif node in carburants:
                node_colors.append('orange')
            else:
                node_colors.append('gray')
            
            if node in marques:
                node_sizes_path.append(500)
            elif node in modeles:
                node_sizes_path.append(300)
            elif node in carburants:
                node_sizes_path.append(800)
            else:
                node_sizes_path.append(300)
        
        edge_colors = []
        for u, v in G.edges():
            if (u in chemin_court and v in chemin_court and 
                abs(chemin_court.index(u) - chemin_court.index(v)) == 1):
                edge_colors.append('red')
            else:
                edge_colors.append('gray')
        
        edge_widths = [3 if c == 'red' else 1 for c in edge_colors]
        
        nx.draw(G, pos, with_labels=True, node_size=node_sizes_path, font_size=8,
                node_color=node_colors, edge_color=edge_colors, alpha=0.6,
                font_weight='bold', linewidths=1.5, edgecolors='black',
                width=edge_widths)
        
        plt.title(f"Plus court chemin de '{marque_exemple}' à '{carburant_exemple}' (en rouge)")
        plt.tight_layout()
        plt.show()
    except:
        print("Impossible de visualiser le chemin")