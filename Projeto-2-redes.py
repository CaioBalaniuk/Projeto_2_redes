import networkx as nx
import matplotlib.pyplot as plt
import random

def criar_topologia():
    grafo = nx.Graph()  # Cria a topologia da rede

    # Nós da rede
    raiz = "Core"
    agregacao = ["Agregacao 1", "Agregacao 2"]
    borda = ["Borda e1", "Borda e2", "Borda e3", "Borda e4"]
    hosts_e1 = [f"Host e1-{i}" for i in range(1, 11)]  # 10 hosts
    hosts_e2 = [f"Host e2-{i}" for i in range(1, 11)]  # 10 hosts
    hosts_e3 = [f"Host e3-{i}" for i in range(1, 7)]   # 6 hosts
    hosts_e4 = [f"Host e4-{i}" for i in range(1, 7)]   # 6 hosts

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

    # Atribuir endereços IP e máscaras de sub-rede
    ips = {}
    ip_base = "227.189.2."

    # Atribuir IPs para hosts
    for i, host in enumerate(hosts_e1):
        ips[host] = f"{ip_base}{i + 1}"  # e1: 227.189.2.1 a 227.189.2.10
    for i, host in enumerate(hosts_e2):
        ips[host] = f"{ip_base}{i + 33}"  # e2: 227.189.2.33 a 227.189.2.42
    for i, host in enumerate(hosts_e3):
        ips[host] = f"{ip_base}{i + 65}"  # e3: 227.189.2.65 a 227.189.2.70
    for i, host in enumerate(hosts_e4):
        ips[host] = f"{ip_base}{i + 81}"  # e4: 227.189.2.81 a 227.189.2.86

    # Atribuir IPs para switches de borda
    ips[borda[0]] = f"{ip_base}11"  # Borda e1
    ips[borda[1]] = f"{ip_base}43"  # Borda e2
    ips[borda[2]] = f"{ip_base}71"  # Borda e3
    ips[borda[3]] = f"{ip_base}87"  # Borda e4

    # Atribuir IPs para switches de agregação
    ips[agregacao[0]] = f"{ip_base}129"  # Agregacao 1
    ips[agregacao[1]] = f"{ip_base}193"  # Agregacao 2

    # Atribuir IP para a raiz
    ips[raiz] = f"{ip_base}254"

    return grafo, ips

def ping(grafo, ips, origem, destino):
    # Simula o comando ping entre 2 nós da rede
    if nx.has_path(grafo, origem, destino):
        caminho = nx.shortest_path(grafo, origem, destino)
        latencia_total = sum(grafo[origem][destino]['latencia'] for origem, destino in zip(caminho, caminho[1:]))
        print(f"PING {ips[destino]}: Caminho = {caminho}, Latência Total = {latencia_total}ms")
    else:
        print(f"PING {ips[destino]}: Destino inalcançável")

def traceroute(grafo, ips, origem, destino):
    # Simula o comando traceroute entre dois nós da rede
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
    # Gera o diagrama visual
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

def gerar_tabela_roteamento(grafo, ips):
    print("\nTABELA DE ROTEAMENTO PARA CADA NÓ:\n")
    
    for nodo in grafo.nodes:
        print(f"\nTabela de Roteamento para {nodo} ({ips[nodo]}):")
        print(f"{'Destino':<20} {'Próximo Salto':<20} {'Caminho'}")
        print("-" * 60)

        for destino in grafo.nodes:
            if nodo != destino:
                if nx.has_path(grafo, nodo, destino):
                    caminho = nx.shortest_path(grafo, nodo, destino)  # Encontra o menor caminho
                    proximo_salto = caminho[1] if len(caminho) > 1 else destino  # Próximo nó no caminho
                    print(f"{destino:<20} {proximo_salto:<20} {caminho}")
                else:
                    print(f"{destino:<20} {'-':<20} {'Sem caminho disponível'}")

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

# Gerar a tabela de roteamento
gerar_tabela_roteamento(grafo, ips)
