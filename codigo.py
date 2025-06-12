import pyodbc
import pandas
import math  

# realiza a conexão com o BD 
connection =pyodbc.connect(
    'DRIVER={ODBC DRIVER 17 for SQL Server};'
    'SERVER=regulus.cotuca.unicamp.br;'
    'DATABASE=BD*****;'
    'UID=BD*****;'
    'PWD=BD****'
)

cursor = connection.cursor()


'''

       /\
      /  \  
     /____\   A V I S O 
    /      \  ---------- D E S C U L P E  OS  C O M E N T A R I O S  O F E N C I V O S  TO  F A Z E N D O  I S S O  JA  S E M  P A C I E N C I A 

'''



#Formula de conversão de Latitude, Longitude para KM no caso em relação ao Centro de distribuição
def formula_haversine(lat1, lon1, lat2, lon2):
    R = 6371  # É o raio da Terra em km
    
    # Converte todos os valores para float (AVISO: Se tirar isso o codigo quebra kkkkkk, não retire é serio)
    lat1, lon1, lat2, lon2 = float(lat1), float(lon1), float(lat2), float(lon2)
    
    # Daqui pra baixo é umas contass do krlh em resumo é a formula apenas isso👍(OBS: são 3:44 to com preguiça de explicar fds)
    dlat = math.radians(lat2 - lat1)
    dlon = math.radians(lon2 - lon1)
    lat1_rad = math.radians(lat1)
    lat2_rad = math.radians(lat2)

    a = (math.sin(dlat / 2) ** 2) + math.cos(lat1_rad) * math.cos(lat2_rad) * (math.sin(dlon / 2) ** 2)
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    return R * c


def calcular_distancia(): #Esta função vai pegar os dados do Centro de Distribuicao e dos Clientes e transformar em Km

    #Aqui estou pegando os dados do Centro de Distribuicao
    centro = cursor.execute('SELECT latitude, longitude FROM CentroDistribuicao').fetchone()# esse fet tem uma explicação no Site do sql (suponho eu q o lite e o server seja a mesma bosta)

    #Aqui é uma macacada do krlh em resumo puxa a loc do centro de distribuição
    if not centro:
        print(" Nenhum centro de distribuição encontrado.")
        return
    latitude_centro, longitude_centro = centro
    print(f"Centro: {latitude_centro}, {longitude_centro}")


    #Aqui estamos pegando os dados dos Clientes, Daqui pra baixo começa uma macacada do krlhh em resumo (cambiarra) <--- sla como escreve sou analfabeto
    cursor.execute('SELECT codigoCliente, nome, cidade, latitude, longitude FROM Clientes')# Aqui puxa os dados da dboClientes (OBS: ainda nao dei commit la no git mas ja faço isso)
    clientes = cursor.fetchall()# Aqui é a mesmisima coisa tem no site do sql
    print(f"Clientes encontrados: {len(clientes)}")# Deixei isso como luxo se quiser pode tirar 

    # Só se não achar clientes resumo é luxo tbm pode tirar se quiser
    if not clientes:
        print(" Nenhum cliente encontrado.")
        return

    distancias = []

    # Aqui é a junção das funções não recomendo mexer tbm (OBS: deu um trampo da poha) 
    for cliente in clientes:
        codigo, nome, cidade, lat_cli, lon_cli = cliente
        dist = formula_haversine(latitude_centro, longitude_centro, lat_cli, lon_cli)# Esse principalmente
        distancias.append((codigo, nome, cidade, dist))# AQui só joga naquela lista e fds✌

    distancias.sort(key=lambda x: x[3], reverse=True)# Aqui ordena se quiser fazer ao contraio é só trocar o reverse=False

    print("\n Clientes por ordem de distância (Do maior para o menor):")# Aqui é bem auto explicativo
    for codigo, nome, cidade, dist in distancias:
        print(f" Cliente {nome} (ID {codigo}, {cidade}) está a {dist:.2f} km do centro.")# usei .format por preguiça mesmo, esqueci de falar o id é o codigo do pedido


calcular_distancia() # aq só chama, PODE IGNORAR






