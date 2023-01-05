import random as rd
#Para enviar os dados para o banco de dados RETIRE O JOGO DA VELHA da função comentada linha 130
from datetime import datetime,timedelta
import psycopg2 as pg
#conectar com o banco de dados em connection
# Da nome as 5 células da cidade
def cell_name(city):
    if(city=="Corumba"):
        Celulas=['Celula_1','Celula_2','Celula_3','Celula_4','Celula_5']
        return Celulas
    elif(city=="Jardim"):
        Celulas=['Celula_6','Celula_7','Celula_8','Celula_9','Celula_10']
        return Celulas
# Da nome aos eNodebs, sendo um deles para cada célula
def enodeb_name(city_enodeb):
    if(city_enodeb=='Corumba'):
        eNodeBs=['eNodeB_1','eNodeB_2','eNodeB_3','eNodeB_4','eNodeB_5']
        return eNodeBs
    elif(city_enodeb=="Jardim"):
        eNodeBs=['eNodeB_6','eNodeB_7','eNodeB_8','eNodeB_9','eNodeB_10']
        return eNodeBs
# Nome das cidades usadas para o projeto
def city_name(city):
    if(city=='Corumba'):
        print('Corumba no Estado de Mato Grosso do Sul')
    elif(city=="Jardim"):
        print('Jardim no Estado de Mato Grosso do Sul')
    else:
         print('Cidades usadas neste projeto: Corumba e Jardim')
#Retornar a quantidade de MegaBytes que uma célula recebe por dia
def mega_bytes():
    return rd.randint(1000,50000)
#Número de Usuários conectados
def usuarios():
    return rd.randint(100,15000)
#Retorna a data dos dados
def calendario(periodo):
    data= datetime.today()-timedelta(days=periodo)
    dia= (data.day)
    mes= (data.month)
    ano= (data.year)
    return ('{}/{}/{}').format(dia,mes,ano)
#Retorna os dados de cada celula, trafego de dados em megabytes e numero de usuarios conectados por dia 
def dados_corumba():
    celula_1={'traf_dados':mega_bytes(),'n_usuarios':usuarios()}
    celula_2={'traf_dados':mega_bytes(),'n_usuarios':usuarios()}
    celula_3={'traf_dados':mega_bytes(),'n_usuarios':usuarios()}
    celula_4={'traf_dados':mega_bytes(),'n_usuarios':usuarios()}
    celula_5={'traf_dados':mega_bytes(),'n_usuarios':usuarios()}
    return [celula_1,celula_2,celula_3,celula_4,celula_5]
    
def dados_jardim():
    celula_6={'traf_dados':mega_bytes(),'n_usuarios':usuarios()}
    celula_7={'traf_dados':mega_bytes(),'n_usuarios':usuarios()}
    celula_8={'traf_dados':mega_bytes(),'n_usuarios':usuarios()}
    celula_9={'traf_dados':mega_bytes(),'n_usuarios':usuarios()}
    celula_10={'traf_dados':mega_bytes(),'n_usuarios':usuarios()}
    return [celula_6,celula_7,celula_8,celula_9,celula_10]
# Função principal que chamará todas as estruturas
def estrutura(cidade):
    if(cidade=='Corumba'):
        print(enodeb_name(cidade))
        print(city_name(cidade))
        print(calendario(5))
        print(dados_corumba())
    elif(cidade=='Jardim'):
        print(enodeb_name(cidade))
        print(city_name(cidade))
        print(calendario(5))
        print(dados_jardim())

def conection():#Conecta ao banco de dados e cria as tabelas, e inserção dos valores
    conn = pg.connect(dbname='postgres', user='postgres', password='12345', host='localhost', port='5432')
    cur= conn.cursor()
    cur.execute("""
    CREATE TABLE Dados(
        Celulas VARCHAR(25),
        N_usuarios INTEGER, 
        MegaBytes INTEGER, 
        eNodeBs VARCHAR(25),
        Cidade VARCHAR(25),
        Dia VARCHAR(25));""")
    for u in range(4,-1,-1):    # Insere os dados por 5 dias, inclusive o dia de hoje
        for i in range(0,5):    # Inserir dados de Corumbá
            cur.execute("""INSERT INTO Dados(
        Celulas, 
        N_usuarios, 
        MegaBytes, 
        eNodeBs, 
        Cidade, 
        Dia) VALUES(%s,%s,%s,%s,%s,%s)""",( cell_name('Corumba')[i],dados_corumba()[i]['traf_dados'],dados_corumba()[i]['n_usuarios'], enodeb_name('Corumba')[i],'Corumba',calendario(u)))
        for i in range(0,5):    # Inserir dados de Jardim
            cur.execute("""INSERT INTO Dados(
        Celulas, 
        N_usuarios, 
        MegaBytes, 
        eNodeBs, 
        Cidade, 
        Dia) VALUES(%s,%s,%s,%s,%s,%s)""",( cell_name('Jardim')[i],dados_jardim()[i]['traf_dados'],dados_jardim()[i]['n_usuarios'], enodeb_name('Jardim')[i],'Jardim',calendario(u)))
    conn.commit()
    conn.close()

def separador():
    conn = pg.connect(dbname='postgres', user='postgres', password='12345', host='localhost', port="5432")
    cur= conn.cursor()
    montante_usuarios_corumba=[]
    montante_megabytes_corumba=[]
    montante_usuarios_jardim=[]
    montante_megabytes_jardim=[]
    for i in range(4,-1,-1): #Montate de usuários conectados e megabytes usados por dia na cidade de corumba
        cur.execute("""SELECT SUM(N_usuarios) FROM dados WHERE cidade='Corumba' AND dia='{}'""".format(calendario(i)))
        usuarios_conectados_corumba=cur.fetchall()
        cur.execute("""SELECT SUM(MegaBytes) FROM dados WHERE cidade='Corumba' AND dia='{}'""".format(calendario(i)))
        megas_usados_corumba=cur.fetchall()
        montante_usuarios_corumba.append(usuarios_conectados_corumba)
        montante_megabytes_corumba.append(megas_usados_corumba)
    print("Montante de usuários conectados em corumba em 5 dias consecutivos ", montante_usuarios_corumba)
    print("Montante de MegaBytes utilizados por todas as celulas de corumba em 5 dias consecutivos",montante_megabytes_corumba)
    for i in range(4,-1,-1):#Montante de usuários conectados e megabytes usados por dia na cidade de jardim
        cur.execute("""SELECT SUM(N_usuarios) FROM dados WHERE cidade='Jardim' AND dia='{}'""".format(calendario(i)))
        usuarios_conectados_jardim=cur.fetchall()
        cur.execute("""SELECT SUM(MegaBytes) FROM dados WHERE cidade='Jardim' AND dia='{}'""".format(calendario(i)))
        megas_usados_jardim=cur.fetchall()
        montante_usuarios_jardim.append(usuarios_conectados_jardim)
        montante_megabytes_jardim.append(megas_usados_jardim)
    print("Montante de usuários conectados em jardim em 5 dias consecutivos ",montante_usuarios_jardim)
    print("Montante de MegaBytes usados em jardim em 5 dias consecutivos por todas as celulas ",montante_megabytes_jardim)
    conn.commit()
    conn.close()
#Após ter rodado o código uma vez,colocar comentado a função conection()
conection()
separador()



















