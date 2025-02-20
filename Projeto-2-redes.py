import networkx as nx
import matplotlib.pyplot as plt
import random

def criar_topologia():

    grafo = nx.Graph() # cria topologia da rede

    # Nós da rede
    raiz = "Core"
    agregacao = ["Agregacao 1", "Agregacao 2"]
    borda = ["Borda e1", "Borda e2", "Borda e3", "Borda e4"]
    hosts_e1 = [f"Host e1-{i}" for i in range(1, 24)]
    hosts_e2 = [f"Host e2-{i}" for i in range(1, 25)]
    hosts_e3 = [f"Host e3-{i}" for i in range(1, 15)]
    hosts_e4 = [f"Host e4-{i}" for i in range(1, 15)]

    # Adicionar nós ao grafo
    grafo.add_node(raiz, tipo="switch")
    for sw in agregacao:
        grafo.add_node(sw, tipo="switch")
    for sw in borda:
        grafo.add_node(sw, tipo="switch")
    for host in hosts_e1 + hosts_e2 + hosts_e3 + hosts_e4:
        grafo.add_node(host, tipo="host")

    # Conectar nós (topologia em árvore)
    grafo.add_edge(raiz, agregacao[0], latencia=random.randint(1, 5))
    grafo.add_edge(raiz, agregacao[1], latencia=random.randint(1, 5))

    grafo.add_edge(agregacao[0], borda[0], latencia=random.randint(1, 5))
    grafo.add_edge(agregacao[0], borda[1], latencia=random.randint(1, 5))
    grafo.add_edge(agregacao[1], borda[2], latencia=random.randint(1, 5))
    grafo.add_edge(agregacao[1], borda[3], latencia=random.randint(1, 5))

    for host in hosts_e1:
        grafo.add_edge(borda[0], host, latencia=random.randint(1, 5))
    for host in hosts_e2:
        grafo.add_edge(borda[1], host, latencia=random.randint(1, 5))
    for host in hosts_e3:
        grafo.add_edge(borda[2], host, latencia=random.randint(1, 5))
    for host in hosts_e4:
        grafo.add_edge(borda[3], host, latencia=random.randint(1, 5))

    # Atribuir endereços IP
    ips = {}
    subredes = {
        "e1": iter(range(1, 32)),
        "e2": iter(range(33, 64)),
        "e3": iter(range(65, 80)),
        "e4": iter(range(81, 96)),
        "a1": iter(range(129, 192)),
        "a2": iter(range(193, 256)),
    }
    ip_base = "227.189.2."

    # Atribuir IPs para switches e hosts
    for node in grafo.nodes:
        if "e1" in node:
            ips[node] = f"{ip_base}{next(subredes['e1'])}"
        elif "e2" in node:
            ips[node] = f"{ip_base}{next(subredes['e2'])}"
        elif "e3" in node:
            ips[node] = f"{ip_base}{next(subredes['e3'])}"
        elif "e4" in node:
            ips[node] = f"{ip_base}{next(subredes['e4'])}"
        elif "Agregacao 1" in node:
            ips[node] = f"{ip_base}{next(subredes['a1'])}"
        elif "Agregacao 2" in node:
            ips[node] = f"{ip_base}{next(subredes['a2'])}"
        else:
            ips[node] = f"{ip_base}{random.randint(100, 200)}"  # IP genérico para a raiz

    return grafo, ips

def ping(grafo, ips, origem, destino):
    # simula o comando ping entre 2 nós da rede
    if nx.has_path(grafo, origem, destino):
        caminho = nx.shortest_path(grafo, origem, destino)
        latencia_total = sum(grafo[origem][destino]['latencia'] for origem, destino in zip(caminho, caminho[1:]))
        print(f"PING {ips[destino]}: Caminho = {caminho}, Latência Total = {latencia_total}ms")
    else:
        print(f"PING {ips[destino]}: Destino inalcançável")

def traceroute(grafo, ips, origem, destino):
      # simula o comando traceroute entre dois nós da rede
    if nx.has_path(grafo, origem, destino):
        caminho = nx.shortest_path(grafo, origem, destino)
        print(f"TRACEROUTE para {ips[destino]}:")
        for i, hop in enumerate(caminho):
            if i > 0:
                latencia = grafo[caminho[i - 1]][hop]['latencia']
                print(f"{i} {ips[hop]} {latencia}ms")
    else:
        print(f"TRACEROUTE {ips[destino]}: Destino inalcançável")

def criar_diagrama(grafo):
    # gera o diagrama visual
    pos = nx.spring_layout(grafo)  # Layout para o grafo
    tipos = nx.get_node_attributes(grafo, 'tipo')

    # Definir cores para os nós
    cores = ["red" if tipos[node] == "host" else "blue" for node in grafo.nodes]

    plt.figure(figsize=(15, 10))
    nx.draw(grafo, pos, with_labels=True, node_color=cores, node_size=1000, font_size=8, font_color="black", edge_color="gray")

    # Exibir pesos (latências) das arestas
    labels = nx.get_edge_attributes(grafo, 'latencia')
    nx.draw_networkx_edge_labels(grafo, pos, edge_labels=labels)

    plt.title("Topologia da Rede")
    plt.show()


# Criar a topologia da rede
grafo, ips = criar_topologia()

# Exibir a topologia criada
print("Topologia da Rede:")
for origem, destino, atributos in grafo.edges(data=True):
    print(f"{origem} <-> {destino}, Latência: {atributos['latencia']}ms")

print("\nEndereços IP:")
for node, ip in ips.items():
    print(f"{node}: {ip}")

# Testar Ping
print("\nTeste de Ping:")
ping(grafo, ips, "Host e1-1", "Host e2-10")
ping(grafo, ips, "Host e3-1", "Host e4-5")

# Testar Traceroute
print("\nTeste de Traceroute:")
traceroute(grafo, ips, "Host e1-1", "Host e2-10")
traceroute(grafo, ips, "Host e3-1", "Host e4-5")

# Criar diagrama da topologia
print("\nGerando diagrama da topologia...")
criar_diagrama(grafo)
