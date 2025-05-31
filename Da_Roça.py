
# Parâmetros fixos
VELOCIDADE_MEDIA = 60  # km/h
TEMPO_ABASTECIMENTO = 0.5  # 30 minutos
TEMPO_ENTREGA = 0.5  # 30 minutos
CENTRO = (0, 0)  # Localização do centro de distribuição


clientes = [
    {'nome': 'Ana', 'x': 10, 'y': 20},
    {'nome': 'Bruno', 'x': 15, 'y': 25},
    {'nome': 'Carlos', 'x': 5, 'y': 5},
    {'nome': 'Daniela', 'x': 30, 'y': 10}, 
    {'nome': 'Eduardo', 'x': 2, 'y': 8},
]

clientes_nao_atendidos = clientes.copy()
motoristas = ['Motorista 1', 'Motorista 2']



def distancia(p1, p2):
    return ((p1['x'] - p2['x'])**2 + (p1['y'] - p2['y'])**2) ** 0.5

def distancia_para_centro(cliente):
    return (cliente['x']**2 + cliente['y']**2) ** 0.5

def cliente_mais_longe(clientes):
    return max(clientes, key=distancia_para_centro)

def cliente_mais_proximo(origem, candidatos):
    if not candidatos:
        return None
    return min(candidatos, key=lambda c: distancia(origem, c))



while motoristas and clientes_nao_atendidos:
    motorista = motoristas.pop(0)
    horas_trabalhadas = 0
    rota = []

    # Cliente mais longe como ponto inicial
    cliente_inicial = cliente_mais_longe(clientes_nao_atendidos)
    rota.append(cliente_inicial)
    clientes_nao_atendidos.remove(cliente_inicial)

    horas_trabalhadas += TEMPO_ABASTECIMENTO + TEMPO_ENTREGA

    while horas_trabalhadas <= 8:
        cliente_atual = rota[-1]
        proximo_cliente = cliente_mais_proximo(cliente_atual, clientes_nao_atendidos)

        if not proximo_cliente:
            break

        dist = distancia(cliente_atual, proximo_cliente)
        tempo_deslocamento = dist / VELOCIDADE_MEDIA
        tempo_retorno = distancia_para_centro(proximo_cliente) / VELOCIDADE_MEDIA

        tempo_total = tempo_deslocamento + TEMPO_ABASTECIMENTO + TEMPO_ENTREGA + tempo_retorno

        if horas_trabalhadas + tempo_total > 8:
            break  # não cabe mais cliente

        # adiciona cliente à rota
        rota.append(proximo_cliente)
        clientes_nao_atendidos.remove(proximo_cliente)
        horas_trabalhadas += tempo_deslocamento + TEMPO_ABASTECIMENTO + TEMPO_ENTREGA

        #Se estiver entre 3h e 5h, adiciona 1h
        if 3 <= horas_trabalhadas <= 5:
            horas_trabalhadas += 1

    # Resultado da rota do motorista
    nomes_rota = [c['nome'] for c in rota]
    print(f"{motorista} fará a rota: {nomes_rota}, tempo total estimado: {horas_trabalhadas:.2f}h")
