#!/usr/bin/env python
# encoding:utf8

import csv
import os


# Carrega linhas de um arquivo CSV para um arquivo destino com exceção da última
# coluna
def carrega_csv(nome_do_arquivo, array_destino):
    with open(nome_do_arquivo, 'r') as f:
        reader = csv.reader(f)
        for r in reader:
            if len(r) == 0: continue
            array_destino.append(r)
    f.close()


class ItemDeProbabilidade:
    def __init__(self, item_name, column_number):
        self.item_name = item_name
        self.column_number = column_number
        self.yes = 1.0
        self.no = 1.0

    def nome_do_item(self):
        return self.item_name

    def incrementa_yes(self):
        self.yes += 1

    def incrementa_no(self):
        self.no += 1

    def imprime(self):
        print "Column: " + str(self.column_number) + "/" + self.item_name + "/" + str(self.yes) + "/" + str(self.no)

classes_do_modelo = set([])
def obtem_classes():
    classes_do_modelo = set([])

    for linha in base_de_dados:
        classes_do_modelo.add(linha[(len(linha) - 1)])
    return classes_do_modelo


def calcula_v():
    global total_v, global_yes, global_no

    for linha in base_de_dados:
        if linha in ['\n', '\r\n'] == '':
            continue
        total_v += 1

        if linha[len(linha) - 1] == list(classes_do_modelo)[0]:
            global_yes += 1
        else:
            global_no += 1


def obtem_itens_da_base_de_dados():
    for linha in base_de_dados:

        if linha in ['\n', '\r\n'] == '':
            continue

        for indice_coluna in range(len(linha) - 1):

            # se é lista vazia
            if (len(items_de_probabilidade) == 0):
                lineItem = ItemDeProbabilidade(linha[indice_coluna], indice_coluna)

                if linha[len(linha) - 1] == list(classes_do_modelo)[0]:
                    lineItem.incrementa_yes()
                else:
                    lineItem.incrementa_no()

                items_de_probabilidade.append(lineItem)
                continue

            containItemLine = False

            # If line item is on array
            for item in items_de_probabilidade:
                if item.nome_do_item() == linha[indice_coluna]:
                    containItemLine = True
                    if linha[len(linha) - 1] == list(classes_do_modelo)[0]:
                        item.incrementa_yes()
                    else:
                        item.incrementa_no()

            # If is a new line on array
            if (containItemLine == False):
                lineItem = ItemDeProbabilidade(linha[indice_coluna], indice_coluna)
                if linha[len(linha) - 1] == list(classes_do_modelo)[0]:
                    lineItem.incrementa_yes()
                else:
                    lineItem.incrementa_no()
                items_de_probabilidade.append(lineItem)


def monta_modelo_naive_bayes():
    modelo_naive_bayes["v"] = total_v
    modelo_naive_bayes["global"] = {}
    modelo_naive_bayes["global"][list(classes_do_modelo)[0]] = global_yes / total_v
    modelo_naive_bayes["global"][list(classes_do_modelo)[1]] = global_no / total_v
    for indice in range(len(items_de_probabilidade)):
        modelo_naive_bayes[items_de_probabilidade[indice].item_name] = {}
        modelo_naive_bayes[items_de_probabilidade[indice].item_name][list(classes_do_modelo)[0]] = items_de_probabilidade[
                                                                                  indice].yes / global_yes
        modelo_naive_bayes[items_de_probabilidade[indice].item_name][list(classes_do_modelo)[1]] = items_de_probabilidade[
                                                                                 indice].no / global_no


print "----------"

# V total de elementos classificadores(yes, no, etc)
total_v = 0.0
global_yes = 0.0
global_no = 0.0

base_de_dados = []
teste_de_dados = []
carrega_csv('tempo.csv', base_de_dados)
carrega_csv('teste.csv', teste_de_dados)

os.system('clear')

items_de_probabilidade = []

modelo_naive_bayes = {}

classes_do_modelo = obtem_classes()
print "Classes = " + str(classes_do_modelo)

# Calcula v e mostra v
calcula_v()
print "v = " + str(total_v) + " y = " + str(global_yes) + " n = " + str(global_no)

obtem_itens_da_base_de_dados()
'''for item in items_de_probabilidade:
    item.imprime()'''

# Monta modelo Naive Bayes
monta_modelo_naive_bayes()
print modelo_naive_bayes

# Lê teste de dados
for linha in teste_de_dados:
    probablidade_yes = modelo_naive_bayes['global'][list(classes_do_modelo)[0]]
    probablidade_no = modelo_naive_bayes['global'][list(classes_do_modelo)[1]]

    for coluna in linha:
        probablidade_yes *= modelo_naive_bayes[str(coluna)][list(classes_do_modelo)[0]]
        probablidade_no *= modelo_naive_bayes[str(coluna)][list(classes_do_modelo)[1]]

if probablidade_yes > probablidade_no:
    print "Maior probabilidade de " + str(list(classes_do_modelo)[0])
else:
    print "Maior probabilidade de " + str(list(classes_do_modelo)[1])
