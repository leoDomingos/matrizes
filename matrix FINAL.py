# Aluno: Leonardo Domingos
# DRE: 120168324








# TODO:
# OTIMIZAÇAOOOO







# imports
from typing import List, Union
from abc import abstractmethod
import os



class Matriz:
    """Classe base abstrata para todas as matrizes"""
    
    def __init__(self, linhas: int, colunas: int):
        self.linhas = linhas
        self.colunas = colunas
    
    def __add__(self, outra):
        """Soma de matrizes (sobrecarga do operador +)"""
        if self.linhas != outra.linhas or self.colunas != outra.colunas:
            raise ValueError("Dimensões incompatíveis para soma")
        return self._somar(outra)
    
    def __sub__(self, outra):
        """Subtração de matrizes (sobrecarga do operador -)"""
        if self.linhas != outra.linhas or self.colunas != outra.colunas:
            raise ValueError("Dimensões incompatíveis para subtração")
        return self._subtrair(outra)
    
    def __mul__(self, outro):
        """Multiplicação por escalar ou matriz (sobrecarga do operador *)"""
        if isinstance(outro, (int, float)):
            return self._multiplicar_por_escalar(outro)
        else:
            if self.colunas != outro.linhas:
                raise ValueError("Dimensões incompatíveis para multiplicação!")
            return self._multiplicar_por_matriz(outro)
    
    @abstractmethod
    def _somar(self, outra):
        pass
    
    @abstractmethod
    def _subtrair(self, outra):
        pass
    
    @abstractmethod
    def _multiplicar_por_escalar(self, escalar: float):
        pass
    
    @abstractmethod
    def _multiplicar_por_matriz(self, outra):
        pass
    
    @abstractmethod
    def transposta(self):
        pass
    
    @abstractmethod
    def traco(self) -> float:
        pass
    
    @abstractmethod
    def determinante(self) -> float:
        pass
    
    @abstractmethod
    def __str__(self):
        pass




class MatrizRegular(Matriz):
    """Implementação para matrizes regulares m x n"""
    
    # def __init__(self, dados: Union[List[List[float]], int], colunas: int = None):
    #     if isinstance(dados, int):
    #         self.dados = [[0.0 for _ in range(colunas)] for _ in range(dados)]
    def __init__(self, dados: Union[List[List[float]], int], colunas: int = None):
        if isinstance(dados, int):
            super().__init__(dados, colunas)
            self.dados = [[0.0 for _ in range(colunas)] for _ in range(dados)]
        else:
            linhas = len(dados)
            colunas = len(dados[0]) if linhas > 0 else 0
            super().__init__(linhas, colunas)
            self.dados = [linha.copy() for linha in dados]
    
    def _somar(self, outra):
        resultado = MatrizRegular(self.linhas, self.colunas)
        for i in range(self.linhas):
            for j in range(self.colunas):
                resultado.dados[i][j] = self.dados[i][j] + outra.dados[i][j]
        return resultado
    
    def _subtrair(self, outra):
        resultado = MatrizRegular(self.linhas, self.colunas)
        for i in range(self.linhas):
            for j in range(self.colunas):
                resultado.dados[i][j] = self.dados[i][j] - outra.dados[i][j]
        return resultado
    
    def _multiplicar_por_escalar(self, escalar: float):
        resultado = MatrizRegular(self.linhas, self.colunas)
        for i in range(self.linhas):
            for j in range(self.colunas):
                resultado.dados[i][j] = self.dados[i][j] * escalar
        return resultado
    
    def _multiplicar_por_matriz(self, outra): # MELHROAR
        resultado = MatrizRegular(self.linhas, outra.colunas)
        for i in range(self.linhas):
            for j in range(outra.colunas):
                resultado.dados[i][j] = sum(self.dados[i][k] * outra.dados[k][j] for k in range(self.colunas))
        return resultado
    
    def transposta(self):
        resultado = MatrizRegular(self.colunas, self.linhas)
        for i in range(self.linhas):
            for j in range(self.colunas):
                resultado.dados[j][i] = self.dados[i][j]
        return resultado
    
    def traco(self) -> float:
        if self.linhas != self.colunas:
            raise ValueError("Traço só definido para matrizes quadradas")
        return sum(self.dados[i][i] for i in range(self.linhas))
    
    def determinante(self) -> float:
        if self.linhas != self.colunas:
            raise ValueError("Determinante só definido para matrizes quadradas")
        # Implementação simplificada - na prática, Gauss
        if self.linhas == 1:
            return self.dados[0][0]
        elif self.linhas == 2:
            return self.dados[0][0] * self.dados[1][1] - self.dados[0][1] * self.dados[1][0]
        else:
            det = 0.0
            for j in range(self.colunas):
                det += ((-1) ** j) * self.dados[0][j] * self._submatriz(0, j).determinante()
            return det
    
    def _submatriz(self, linha: int, coluna: int):
        return MatrizRegular([
            [self.dados[i][j] for j in range(self.colunas) if j != coluna]
            for i in range(self.linhas) if i != linha
        ])
    
    def __str__(self):
        return "\n".join(" ".join(f"{x:.2f}" for x in linha) for linha in self.dados)




class MatrizQuadrada(MatrizRegular):
    """Implementação otimizada para matrizes quadradas"""
    
    def __init__(self, dados: List[List[float]]):
        if len(dados) != len(dados[0]):
            raise ValueError("Matriz quadrada deve ter dimensões n x n")
        super().__init__(dados)



class MatrizTriangular(MatrizQuadrada):
    """Classe base para matrizes triangulares"""
    
    def determinante(self) -> float:
        """Determinante é o produto dos elementos da diagonal"""
        det = 1.0
        for i in range(self.linhas):
            det *= self.dados[i][i]
        return det



class MatrizTriangularInferior(MatrizTriangular):
    """Implementação para matrizes triangulares inferiores"""
    
    def __init__(self, dados: List[List[float]]):
        super().__init__(dados)
        # Verifica se é triangular inferior
        for i in range(self.linhas):
            for j in range(i+1, self.colunas):
                if self.dados[i][j] != 0:
                    # print(i, j)
                    raise ValueError("Matriz não é triangular inferior")


class MatrizTriangularSuperior(MatrizTriangular):
    """Implementação para matrizes triangulares superiores"""
    
    def __init__(self, dados: List[List[float]]):
        super().__init__(dados)
        # Verifica se é triangular superior
        for i in range(self.linhas):
            for j in range(i):
                if self.dados[i][j] != 0:
                    raise ValueError("Matriz não é triangular superior")


class MatrizDiagonal(MatrizTriangular):
    """Implementação para matrizes diagonais"""
    
    def __init__(self, dados: List[List[float]]):
        super().__init__(dados)
        # Verifica se é diagonal
        for i in range(self.linhas):
            for j in range(self.colunas):
                if i != j and self.dados[i][j] != 0:
                    raise ValueError("Matriz não é diagonal")

class CalculadoraMatricial:
    """Calculadora que gerencia matrizes e realiza operações"""
    




    def __init__(self):
        self.matrizes = []
        self.nomes_matrizes = []  # Para armazenar nomes opcionais das matrizes
    
    def adicionar_matriz(self, dados: List[List[float]]):
        """Adiciona matriz à lista, detectando automaticamente seu tipo"""
        try:
            if all(dados[i][j] == 0 for i in range(len(dados)) for j in range(len(dados[0])) if i != j):
                # print("FOI")
                matriz = MatrizDiagonal(dados)
            else:
                try:
                    matriz = MatrizTriangularInferior(dados)
                except ValueError:
                    try:
                        matriz = MatrizTriangularSuperior(dados)
                    except ValueError:
                        if len(dados) == len(dados[0]):
                            matriz = MatrizQuadrada(dados)
                        else:
                            matriz = MatrizRegular(dados)
        except Exception as e:
            matriz = MatrizRegular(dados)
        
        self.matrizes.append(matriz)
        return len(self.matrizes) - 1
    

    def operacao(self, indice1: int, operador: str, indice2: Union[int, float] = None):
        """Realiza operação entre matrizes ou com escalar"""
        try:
            A = self.matrizes[indice1]
        
            # print(indice1)


            if operador == 'T':
                return A.transposta()
            elif operador == 'tr':
                return A.traco()
            elif operador == 'det':
                return A.determinante()
            
            # Verifica se é multiplicação por escalar (indice2 é número)
            if operador == '*' and type(indice2) == float:
                return A * indice2
            
            # Caso contrário, assume que é operação entre matrizes
            B = self.matrizes[indice2]
            # print(A)
            # print(B)
            if operador == '+':
                return A + B
            elif operador == '-':
                return A - B
            elif operador == '*':
                return A * B
            
            raise ValueError("Operador inválido")
        except IndexError:
            raise ValueError("Índice de matriz inválido")
        
    



    def listar_matrizes(self):
        for i, matriz in enumerate(self.matrizes):
            print(f"Matriz {i} ({matriz.__class__.__name__}):")
            print(matriz)
            print()
    









    def adicionar_matriz_com_nome(self, dados: List[List[float]], nome: str = None):
        """Adiciona matriz com nome opcional"""
        indice = self.adicionar_matriz(dados)
        if nome:
            if len(self.nomes_matrizes) <= indice:
                self.nomes_matrizes.extend([None] * (indice - len(self.nomes_matrizes) + 1))
            self.nomes_matrizes[indice] = nome
        return indice
    
    def adicionar_matriz_identidade(self, n: int, nome: str = None):
        """Cria e adiciona uma matriz identidade n x n"""
        identidade = [[1.0 if i == j else 0.0 for j in range(n)] for i in range(n)]
        return self.adicionar_matriz_com_nome(identidade, nome)
    
    def salvar_lista(self, nome_arquivo: str):
        """Salva a lista de matrizes em um arquivo"""
        with open(nome_arquivo, 'w') as f:
            for i, matriz in enumerate(self.matrizes):
                # Escreve o nome (se existir)
                nome = self.nomes_matrizes[i] if i < len(self.nomes_matrizes) else None
                # f.write(f"Matriz {i}" + (f" - {nome}" if nome else "") + "\n")
                
                # Escreve os dados da matriz
                for linha in matriz.dados:
                    f.write(" ".join(map(str, linha)) + "\n")
                f.write("\n")
    
    def carregar_lista(self, nome_arquivo: str, substituir: bool = True):
        """Carrega matrizes de um arquivo"""
        if substituir:
            self.matrizes = []
            self.nomes_matrizes = []
        
        with open(nome_arquivo, 'r') as f:
            dados_matriz = []
            nome = None
            
            for linha in f:
                linha = linha.strip()
                if not linha:
                    if dados_matriz:
                        self.adicionar_matriz_com_nome(dados_matriz, nome)
                        # print(nome)
                        dados_matriz = []
                        nome = None
                    continue
                
                if linha.startswith("Matriz"):
                    # Extrai nome se existir
                    partes = linha.split(" - ")
                    if len(partes) > 1:
                        nome = partes[1]
                else:
                    # Linha de dados da matriz
                    dados_linha = list(map(float, linha.split()))
                    dados_matriz.append(dados_linha)
            
            # Adiciona a última matriz se houver
            if dados_matriz:
                self.adicionar_matriz_com_nome(dados_matriz, nome)

def mostrar_menu():
    print("\n" + "="*50)
    print("CALCULADORA MATRICIAL - MENU PRINCIPAL")
    print("="*50)
    print("1. Imprimir matriz(es)")
    print("2. Inserir nova matriz (teclado)")
    print("3. Inserir matriz identidade")
    print("4. Inserir matriz de arquivo")
    print("5. Alterar/remover matriz(es)")
    print("6. Listar todas as matrizes")
    print("7. Realizar operações entre matrizes")
    print("8. Salvar lista de matrizes")
    print("9. Carregar lista de matrizes")
    print("10. Zerar lista de matrizes")
    print("0. Sair")
    print("="*50)

def ler_matriz_teclado():
    print("\nInsira os dados da matriz (linha por linha, valores separados por espaço):")
    print("Digite 'fim' para terminar")
    
    matriz = []
    while True:
        linha = input().strip()
        # print(linha)
        if linha.lower() == 'fim':
            break
        
        try:
            valores = list(map(float, linha.split()))
            matriz.append(valores)
        except ValueError:
            print("Entrada inválida. Digite números separados por espaços ou 'fim' para terminar")
    
    return matriz

def main():
    calculadora = CalculadoraMatricial()
    
    while True:
        mostrar_menu()
        opcao = input("\nDigite sua opção: ")
        
        try:
            if opcao == '1':  # Imprimir matriz(es)
                if not calculadora.matrizes:
                    print("\nNenhuma matriz na lista!")
                    continue
                
                print("\nMatrizes disponíveis:")
                calculadora.listar_matrizes()
                
                indices = input("Digite os índices das matrizes a imprimir (separados por espaço) ou 't' para todas: ")
                if indices.lower() == 't':
                    calculadora.listar_matrizes()
                else:
                    try:
                        indices = list(map(int, indices.split()))
                        for i in indices:
                            if i < 0 or i >= len(calculadora.matrizes):
                                print(f"Índice {i} inválido!")
                                continue
                            print(f"\nMatriz {i}:")
                            print(calculadora.matrizes[i])
                    except ValueError:
                        print("Entrada inválida!")
            
            elif opcao == '2':  # Inserir do teclado
                nome = input("Digite um nome para a matriz (opcional): ") or None
                matriz = ler_matriz_teclado()
                if matriz:
                    indice = calculadora.adicionar_matriz_com_nome(matriz, nome)
                    print(f"\nMatriz adicionada com sucesso no índice {indice}!")
                else:
                    print("\nMatriz vazia não foi adicionada.")
            




            elif opcao == '3':  # Matriz identidade
                try:
                    n = int(input("\nDigite a dimensão n da matriz identidade n x n: "))
                    if n <= 0:
                        raise ValueError
                    nome = input("Digite um nome para a matriz (opcional): ") or None
                    indice = calculadora.adicionar_matriz_identidade(n, nome)
                    print(f"\nMatriz identidade {n}x{n} adicionada com sucesso no índice {indice}!")
                except ValueError:
                    print("\nDimensão inválida! Deve ser um número inteiro positivo.")
            




            elif opcao == '4':  # Inserir de arquivo
                nome_arquivo = input("\nDigite o nome do arquivo contendo a matriz: ")
                try:
                    with open(nome_arquivo, 'r') as f:
                        matriz = []
                        for linha in f:
                            linha = linha.strip()
                            if linha:
                                valores = list(map(float, linha.split()))
                                matriz.append(valores)
                    

                    if matriz:
                        nome = input("Digite um nome para a matriz (opcional): ") or None
                        indice = calculadora.adicionar_matriz_com_nome(matriz, nome)
                        print(f"\nMatriz carregada do arquivo e adicionada com sucesso no índice {indice}!")
                    else:
                        print("\nArquivo vazio ou formato inválido!")
                except FileNotFoundError:
                    print("\nArquivo não encontrado!")
                except ValueError:
                    print("\nFormato de arquivo inválido! Certifique-se que contém apenas números.")
            




            elif opcao == '5':  # Alterar/remover
                if not calculadora.matrizes:
                    print("\nNenhuma matriz na lista!")
                    continue
                
                print("\nMatrizes disponíveis:")
                calculadora.listar_matrizes()
                
                acao = input("\nDigite 'a' para alterar, 'r' para remover ou 'c' para cancelar: ").lower()
                
                if acao == 'c':
                    continue
                
                try:
                    indice = int(input("Digite o índice da matriz: "))
                    if indice < 0 or indice >= len(calculadora.matrizes):
                        print("Índice inválido!")
                        # print(indice)
                        continue
                    
                    if acao == 'a':
                        print(f"\nEditando matriz {indice}:")
                        print("Matriz atual:")
                        print(calculadora.matrizes[indice])
                        
                        nova_matriz = ler_matriz_teclado()
                        if nova_matriz:
                            # Remover a matriz antiga e insere a nova no mesmo índice
                            calculadora.matrizes.pop(indice)
                            # print(calculadora.matrizes.pop(indice))



                            if indice < len(calculadora.nomes_matrizes):
                                nome = calculadora.nomes_matrizes.pop(indice)
                            else:
                                nome = None
                            
                            calculadora.matrizes.insert(indice, MatrizRegular(nova_matriz))
                            if nome:
                                if len(calculadora.nomes_matrizes) <= indice:
                                    calculadora.nomes_matrizes.extend([None] * (indice - len(calculadora.nomes_matrizes) + 1))
                                calculadora.nomes_matrizes[indice] = nome
                            
                            print(f"\nMatriz {indice} alterada com sucesso!")
                    
                    elif acao == 'r':
                        confirmacao = input(f"Tem certeza que deseja remover a matriz {indice}? (s/n): ").lower()
                        if confirmacao == 's':
                            calculadora.matrizes.pop(indice)
                            if indice < len(calculadora.nomes_matrizes):
                                calculadora.nomes_matrizes.pop(indice)
                            print("\nMatriz removida com sucesso!")
                
                except ValueError:
                    print("\nÍndice inválido!")
            






            elif opcao == '6':  # Listar todas
                if not calculadora.matrizes:
                    print("\nNenhuma matriz na lista!")
                else:
                    print("\nLista de todas as matrizes:")
                    calculadora.listar_matrizes()
            




            elif opcao == '7':  # Operações
                if len(calculadora.matrizes) < 1:
                    print("\nNão há matrizes suficientes para operações!")
                    continue
                
                print("\nMatrizes disponíveis:")
                calculadora.listar_matrizes()
                
                operador = input("\nDigite a operação (+, -, *, T, tr, det): ")
                
                try:
                    if operador in ['T', 'tr', 'det']:
                        indice = int(input("Digite o índice da matriz: "))
                        resultado = calculadora.operacao(indice, operador)
                        print("\nResultado:")
                        if operador == 'T':
                            print(resultado)
                        else:
                            print(resultado)
                    else:
                        indice1 = int(input("Digite o índice da primeira matriz: "))
                        if operador == '*':
                            # Pode ser multiplicação por escalar ou por matriz
                            entrada = input("Digite o índice da segunda matriz (inteiro) ou um valor escalar (float): ")
                            if type(entrada) == float:
                                resultado = calculadora.operacao(indice1, '*', entrada)
                            else:
                                indice2 = int(entrada)
                                resultado = calculadora.operacao(indice1, '*', indice2)
                        else:
                            indice2 = int(input("Digite o índice da segunda matriz: "))
                            resultado = calculadora.operacao(indice1, operador, indice2)
                        
                        print("\nResultado:")
                        print(resultado)
                        
                        # Pergunta se deseja salvar o resultado
                        salvar = input("\nDeseja salvar o resultado na lista? (s/n): ").lower()
                        if salvar == 's':
                            nome = input("Digite um nome para a matriz resultante (opcional): ") or None
                            calculadora.matrizes.append(resultado)
                            if nome:
                                calculadora.nomes_matrizes.append(nome)
                            print(f"Resultado salvo no índice {len(calculadora.matrizes)-1}")
                except (ValueError, IndexError) as e:
                    print(f"\nErro na operação: {str(e)}")
            





            elif opcao == '8':  # Salvar lista
                if not calculadora.matrizes:
                    print("\nNenhuma matriz para salvar!")
                    continue
                
                nome_arquivo = input("\nDigite o nome do arquivo para salvar: ")
                try:
                    calculadora.salvar_lista(nome_arquivo)
                    print(f"\nLista de matrizes salva com sucesso em {nome_arquivo}!")
                except Exception as e:
                    print(f"\nErro ao salvar arquivo: {str(e)}")
            




            elif opcao == '9':  # Carregar lista
                nome_arquivo = input("\nDigite o nome do arquivo para carregar: ")
                try:
                    substituir = input("Deseja substituir a lista atual? (s/n): ").lower() == 's'
                    calculadora.carregar_lista(nome_arquivo, substituir)
                    print(f"\nMatrizes carregadas com sucesso de {nome_arquivo}!")
                except Exception as e:
                    print(f"\nErro ao carregar arquivo: {str(e)}")
            
            elif opcao == '10':  # Zerar lista
                confirmacao = input("\nTem certeza que deseja apagar todas as matrizes? (s/n): ").lower()
                if confirmacao == 's':
                    calculadora.matrizes = []
                    calculadora.nomes_matrizes = []
                    print("\nLista de matrizes zerada com sucesso!")
            




            elif opcao == '0':  # Sair
                print("\nSaindo do programa...")
                break
            





            else:
                print("\nOpção inválida! Digite um número entre 0 e 10.")
        
        except Exception as e:
            print(f"\nOcorreu um erro: {str(e)}")
        
        input("\nPressione Enter para continuar...")

if __name__ == "__main__":
    main()