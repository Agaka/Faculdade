import random

class Processo:
    def __init__(self, id, tempo_execucao, tempo_chegada, prioridade):
        self.id = id
        self.tempo_execucao = tempo_execucao
        self.tempo_restante = tempo_execucao
        self.tempo_chegada = tempo_chegada
        self.prioridade = prioridade
        self.tempo_inicio = None
        self.tempo_espera = 0

    def __str__(self):
        return f"Processo[{self.id}]: tempo_execucao={self.tempo_execucao}, tempo_restante={self.tempo_restante}, tempo_chegada={self.tempo_chegada}, prioridade={self.prioridade}"

def fcfs(processos):
    # Inicializa o tempo atual e a lista de histórico
    tempo_atual = 0
    historico = []

    # Ordena os processos por tempo de chegada
    processos_ordenados = sorted(processos, key=lambda x: x.tempo_chegada)

    # Itera pelos processos ordenados
    for processo in processos_ordenados:
        # Verifica se o tempo atual é menor que o tempo de chegada do processo
        if tempo_atual < processo.tempo_chegada:
            # Se o tempo atual é menor que o tempo de chegada, avança o tempo atual.
            tempo_atual = processo.tempo_chegada

        # Define o tempo de início e tempo de espera do processo
        processo.tempo_inicio = tempo_atual
        processo.tempo_espera = tempo_atual - processo.tempo_chegada

        # Executa o processo enquanto houver tempo restante
        while processo.tempo_restante > 0:
            # Registra o tempo no histórico, decrementa o tempo restante e avança o tempo atual
            historico.append((tempo_atual, processo.id, processo.tempo_restante))
            processo.tempo_restante -= 1
            tempo_atual += 1

    # Correção para garantir que o tempo comece em 1 na impressão do histórico.
    historico_corrigido = [(t + 1, pid, trest - 1) for t, pid, trest in historico if trest > 0]
    return historico_corrigido

def sjf_preemptivo(processos):
    # Inicializa o tempo atual e as listas de processos prontos e histórico
    tempo_atual = 0
    processos_prontos = []
    historico = []

    # Ordena os processos por tempo de chegada
    processos_ordenados = sorted(processos, key=lambda x: x.tempo_chegada)

    # Inicializa os tempos de início e restante para cada processo
    for processo in processos:
        processo.tempo_inicio = None
        processo.tempo_restante = processo.tempo_execucao

    # Enquanto houver processos não concluídos ou prontos
    while processos_ordenados or processos_prontos:
        # Move processos que chegaram para a lista de prontos
        while processos_ordenados and processos_ordenados[0].tempo_chegada <= tempo_atual:
            processo = processos_ordenados.pop(0)
            processos_prontos.append(processo)
            # Ordena os processos prontos pelo tempo restante
            processos_prontos.sort(key=lambda x: x.tempo_restante)

        # Executa o processo pronto com menor tempo restante
        if processos_prontos:
            processo_atual = processos_prontos[0]
            # Define o tempo de início se ainda não estiver definido
            if processo_atual.tempo_inicio is None:
                processo_atual.tempo_inicio = tempo_atual

            # Decrementa o tempo restante e registra no histórico
            processo_atual.tempo_restante -= 1
            historico.append((tempo_atual + 1, processo_atual.id, processo_atual.tempo_restante))

            # Remove o processo da lista de prontos se concluído
            if processo_atual.tempo_restante == 0:
                processos_prontos.pop(0)
        else:
            # Se nenhum processo estiver pronto, apenas avança o tempo
            historico.append((tempo_atual + 1, 'nenhum processo', None))

        # Avança o tempo atual
        tempo_atual += 1

    # Calcula o tempo de espera para cada processo
    for processo in processos:
        if processo.tempo_inicio is not None:
            processo.tempo_espera = processo.tempo_inicio - processo.tempo_chegada
        else:
            # Se o processo nunca começou, o tempo de espera é zero
            processo.tempo_espera = 0

    return historico


def sjf_nao_preemptivo(processos):
    # Inicializa o tempo atual, a lista de processos prontos e o histórico
    tempo_atual = 0
    processos_prontos = []
    historico = []

    # Ordena os processos por tempo de chegada
    processos_ordenados = sorted(processos, key=lambda x: x.tempo_chegada)

    # Inicializa o tempo restante e o tempo de início de cada processo
    for processo in processos:
        processo.tempo_restante = processo.tempo_execucao
        processo.tempo_inicio = None

    while processos_ordenados or processos_prontos:
        # Adiciona processos que chegaram à lista de prontos
        while processos_ordenados and processos_ordenados[0].tempo_chegada <= tempo_atual:
            processo = processos_ordenados.pop(0)
            processos_prontos.append(processo)
            # Ordena a lista de processos prontos pelo tempo de execução (SJF)
            processos_prontos.sort(key=lambda x: x.tempo_execucao)

        if processos_prontos:
            # Executa o processo com menor tempo de execução
            processo_atual = processos_prontos.pop(0)
            if processo_atual.tempo_inicio is None:
                processo_atual.tempo_inicio = tempo_atual

            # Executa o processo até que o tempo restante seja zero
            while processo_atual.tempo_restante > 0:
                historico.append((tempo_atual + 1, processo_atual.id, processo_atual.tempo_restante - 1))
                processo_atual.tempo_restante -= 1
                tempo_atual += 1

            # Calcula o tempo de espera do processo
            processo_atual.tempo_espera = processo_atual.tempo_inicio - processo_atual.tempo_chegada
        else:
            # Se não houver processos prontos, avança o tempo
            tempo_atual += 1

    return historico


def prioridade_preemptivo(processos):
    # Inicializa o tempo atual, a fila de processos prontos e o histórico
    tempo_atual = 0
    fila_prontos = []
    historico = []

    # Loop principal enquanto houver processos com tempo restante
    while any(p.tempo_restante > 0 for p in processos):
        # Atualizar a fila de prontos com processos que chegaram
        for processo in processos:
            if processo.tempo_chegada <= tempo_atual and processo.tempo_restante > 0 and processo not in fila_prontos:
                fila_prontos.append(processo)

        # Ordenar a fila de prontos pela prioridade e tempo de chegada
        fila_prontos.sort(key=lambda p: (p.prioridade, p.tempo_chegada))

        if fila_prontos:
            # Executar o processo com maior prioridade
            processo_atual = fila_prontos[0]

            if processo_atual.tempo_inicio is None:
                processo_atual.tempo_inicio = tempo_atual

            historico.append((tempo_atual, processo_atual.id, processo_atual.tempo_restante))
            processo_atual.tempo_restante -= 1

            if processo_atual.tempo_restante == 0:
                fila_prontos.remove(processo_atual)
        else:
            # Nenhum processo na fila de prontos, registrar 'nenhum processo'
            historico.append((tempo_atual, 'nenhum processo', 0))

        tempo_atual += 1

    # Calcular o tempo de espera para cada processo
    for processo in processos:
        if processo.tempo_inicio is not None:
            processo.tempo_espera = processo.tempo_inicio - processo.tempo_chegada
        else:
            processo.tempo_espera = tempo_atual - processo.tempo_chegada

    # Calcular o tempo médio de espera
    tempo_total_espera = sum(p.tempo_espera for p in processos)
    tempo_medio_espera = tempo_total_espera / len(processos) if processos else 0

    # Correção para garantir que o tempo comece em 1 na impressão do histórico.
    historico_corrigido = [(t + 1, pid, r if r is not None else 0) for t, pid, r in historico]
    
    return historico_corrigido, tempo_medio_espera


def prioridade_nao_preemptivo(processos):
    # Inicializa o tempo atual, a lista de processos prontos e o histórico
    tempo_atual = 0
    processos_prontos = []
    historico = []
    processos_ordenados = sorted(processos, key=lambda x: x.tempo_chegada)

    # Inicializa o tempo restante e tempo de início para cada processo
    for processo in processos:
        processo.tempo_restante = processo.tempo_execucao
        processo.tempo_inicio = None

    while processos_ordenados or processos_prontos:
        # Adiciona processos que chegaram à lista de prontos
        while processos_ordenados and processos_ordenados[0].tempo_chegada <= tempo_atual:
            processo = processos_ordenados.pop(0)
            processos_prontos.append(processo)
            # Ordena por prioridade e, em caso de empate, por tempo de chegada
            processos_prontos.sort(key=lambda x: (x.prioridade, x.tempo_chegada))

        if processos_prontos:
            # Executa o processo com maior prioridade
            processo_atual = processos_prontos.pop(0)
            if processo_atual.tempo_inicio is None:
                processo_atual.tempo_inicio = tempo_atual

            while processo_atual.tempo_restante > 0:
                historico.append((tempo_atual + 1, processo_atual.id, processo_atual.tempo_restante - 1))
                processo_atual.tempo_restante -= 1
                tempo_atual += 1

            # Calcula o tempo de espera do processo
            processo_atual.tempo_espera = processo_atual.tempo_inicio - processo_atual.tempo_chegada
        else:
            # Se não houver processos prontos, avança o tempo
            tempo_atual += 1

    return historico


def round_robin(processos, quantum):
    # Inicializa o tempo atual, o histórico e o índice do processo atual
    tempo_atual = 0
    historico = []
    indice_processo_atual = 0
    numero_processos = len(processos)

    # Inicialização dos processos
    for processo in processos:
        processo.tempo_restante = processo.tempo_execucao
        processo.tempo_inicio = None

    while any(p.tempo_restante > 0 for p in processos):
        # Seleciona o processo atual com base no índice
        processo_atual = processos[indice_processo_atual % numero_processos]
        if processo_atual.tempo_restante > 0:
            for _ in range(min(quantum, processo_atual.tempo_restante)):
                historico.append((tempo_atual + 1, processo_atual.id, processo_atual.tempo_restante - 1))
                processo_atual.tempo_restante -= 1
                tempo_atual += 1

        indice_processo_atual += 1

    # Calcula o tempo de espera de cada processo
    for processo in processos:
        # Tempo de espera é o número de vezes que o processo chegou antes de ser executado
        processo.tempo_espera = sum(1 for t, pid, _ in historico if pid == processo.id and t < processo.tempo_chegada)
    
    return historico



def imprimir_historico(historico, processos):
    # Itera sobre o histórico de execução
    for tempo, processo_id, tempo_restante in historico:
        if processo_id != 'nenhum processo':
            # Imprime informações sobre o processo em execução
            print(f"tempo[{tempo}]: processo[{processo_id}] restante={tempo_restante}")
        else:
            # Imprime quando nenhum processo está pronto
            print(f"tempo[{tempo}]: nenhum processo está pronto")

    if processos:
        # Calcula o tempo total de espera
        tempo_total_espera = sum(p.tempo_espera for p in processos)
        # Itera sobre os processos para imprimir os tempos de espera individuais
        for p in processos:
            print(f"Processo[{p.id}]: tempo_espera={p.tempo_espera}")

        # Calcula e imprime o tempo médio de espera
        tempo_medio_espera = tempo_total_espera / len(processos)
        print(f"Tempo médio de espera: {tempo_medio_espera:.1f}")
    else:
        print("Não há processos para calcular o tempo médio de espera.")




def criar_processos_aleatorios(num_processos):
    # Cria uma lista de processos com informações aleatórias
    return [Processo(i, random.randint(1, 10), random.randint(0, 5), random.randint(1, 10)) for i in range(num_processos)]


def criar_processos_manualmente(num_processos):
    processos = []
    # Solicita informações sobre cada processo
    for i in range(num_processos):
        print(f"Processo {i}:")
        tempo_execucao = int(input("Digite o tempo de execução: "))
        tempo_chegada = int(input("Digite o tempo de chegada: "))
        prioridade = int(input("Digite a prioridade: "))
        # Cria um processo com base nas informações fornecidas
        processos.append(Processo(i, tempo_execucao, tempo_chegada, prioridade))
    return processos


def main():
    processos = []
    while True:
        print("\nEscolha o algoritmo:")
        print("[1=FCFS 2=SJF Preemptivo 3=SJF Não Preemptivo 4=Prioridade Preemptivo 5=Prioridade Não Preemptivo 6=Round Robin 7=Imprime lista de processos 8=Popular processos 9=Sair]")
        escolha = input("Escolha: ")

        if escolha == "1":
            historico = fcfs(processos)
            imprimir_historico(historico, processos)
        elif escolha == "2":
            if not processos:
                print("Não há processos na lista. Adicione ou gere processos primeiro.")
            else:
                historico = sjf_preemptivo(processos)
                imprimir_historico(historico, processos)
        elif escolha == "2":
            if not processos:
                print("Não há processos na lista. Adicione ou gere processos primeiro.")
            else:
                historico = sjf_preemptivo(processos)
                imprimir_historico(historico, processos)
        elif escolha == "3":
            if not processos:
                print("Não há processos na lista. Adicione ou gere processos primeiro.")
            else:
                historico = sjf_nao_preemptivo(processos)
                imprimir_historico(historico, processos)
        elif escolha == "4":
            if not processos:
                print("Não há processos na lista. Adicione ou gere processos primeiro.")
            else:
                historico, tempo_medio_espera = prioridade_preemptivo(processos)
                imprimir_historico(historico, processos)
                print(f"Tempo médio de espera: {tempo_medio_espera:.2f}")
        elif escolha == "5":
            if not processos:
                print("Não há processos na lista. Adicione ou gere processos primeiro.")
            else:
                historico = prioridade_nao_preemptivo(processos)
                imprimir_historico(historico, processos)
        elif escolha == "6":
            quantum = int(input("Escolha o time slice: "))
            if not processos:
                print("Não há processos na lista. Adicione ou gere processos primeiro.")
            else:
                historico = round_robin(processos, quantum)
                imprimir_historico(historico, processos)
        elif escolha == "7":
            for processo in processos:
                print(processo)
        elif escolha == "8":
            num_processos = int(input("Número de processos: "))
            escolha_popular = input("Será aleatório? (s/n): ").lower()
            if escolha_popular == 's':
                processos = criar_processos_aleatorios(num_processos)
                for processo in processos:
                    print(processo)
            else:
                processos = criar_processos_manualmente(num_processos)
                for processo in processos:
                    print(processo)
        elif escolha == "9":
            break
        else:
            print("Opção inválida ou não implementada ainda.")

if __name__ == "__main__":
    main()
