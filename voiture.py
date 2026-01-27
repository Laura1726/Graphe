import networkx as nx
import matplotlib.pyplot as plt

G = nx.Graph()

marques = ["Mazda", "BMW", "Audi", "Ferrari", "Tesla", "Renault"]

modeles = ["Mx5", "CX5", "Serie 1", "Serie 2", "M2", "M3", "A1", "A3", "RS3", "Q8", "F8", "Roma", "Model 3", "Model Y", "Zoe", "Megane E-Tech", "Twingo E"]

carburant = ["Diesel", "Essence", "Electrique"]

G.add_nodes_from(marques)
G.add_nodes_from(modeles)
G.add_nodes_from(carburant)

liaisons = [
    # Mazda
    ("Mazda","Mx5"), ("Mx5","Essence"),("Mazda","CX5"), ("CX5","Diesel"),

    # BMW
    ("BMW","Serie 1"), ("Serie 1","Essence"), ("Serie 1","Diesel"),("BMW","Serie 2"), ("Serie 2","Essence"), ("Serie 2","Diesel"),("BMW","M2"), ("M2","Essence"),("BMW","M3"), ("M3","Essence"),

    # Audi
    ("Audi","A1"), ("A1","Essence"), ("A1","Diesel"),("Audi","A3"), ("A3","Essence"), ("A3","Diesel"),("Audi","RS3"), ("RS3","Essence"),("Audi","Q8"), ("Q8","Diesel"),

    # Ferrari
    ("Ferrari","F8"), ("F8","Essence"),("Ferrari","Roma"), ("Roma","Essence"),

    # Tesla
    ("Tesla","Model 3"), ("Model 3","Electrique"),("Tesla","Model Y"), ("Model Y","Electrique"),

    # Renault électrique
    ("Renault","Zoe"), ("Zoe","Electrique"),("Renault","Megane E-Tech"), ("Megane E-Tech","Electrique"),("Renault","Twingo E"), ("Twingo E","Electrique")
]

G.add_edges_from(liaisons)

couleurs_marques = {
    "Mazda": "orange",
    "BMW": "lightblue",
    "Audi": "lightgreen",
    "Ferrari": "red",
    "Tesla": "grey",
    "Renault": "yellow"
}

node_colors = []

for node in G.nodes():
    if node in carburant:
        node_colors.append("pink")
    elif node in marques:
        node_colors.append(couleurs_marques[node])
    else:
        for m in marques:
            if G.has_edge(m, node):
                node_colors.append(couleurs_marques[m])
                break

plt.figure(figsize=(18,12))
pos = nx.spring_layout(G, seed=35)

nx.draw(G, pos, with_labels=True, node_color=node_colors,node_size=1000)

plt.title("Graphe Voitures (électrique + Renault)")
plt.show()


for u, v in G.edges():
    G[u][v]['weight'] = 1


depart = "BMW"
arrivee = "Mazda"

chemin = nx.dijkstra_path(G, depart, arrivee, weight='weight')
distance = nx.dijkstra_path_length(G, depart, arrivee, weight='weight')

print("Chemin le plus court :", chemin)
print("Distance :", distance)


bfs = list(nx.bfs_tree(G, "BMW"))

print("Parcours en largeur (BFS) depuis BMW :")
print(bfs)

