#!/usr/bin/env python
# encoding:utf8

import sys
import csv
import math
import os


# Carrega linhas de um arquivo CSV para um arquivo destino com exceção da última
# coluna
def carrega_csv(csv_filename, arrayDestino):
    with open(csv_filename, 'r') as f:
        reader = csv.reader(f)
        for r in reader:
            if len(r) == 0: continue
            arrayDestino.append(r)
    f.close()


baseDeDados = []


class NV_table_line_item:


    def __init__(self, item_name):
        self.item_name = item_name
        self.yes = 0
        self.no = 0

    def getName(self):
        return self.item_name

    def increment_yes(self):
        self.yes += 1

    def increment_no(self):
        self.no += 1

    def imprime(self):
        print self.item_name + "/" + str(self.yes) + "/" + str(self.no)


carrega_csv('tempo.csv', baseDeDados)

os.system('clear')

line_items = []

for linha in baseDeDados:

    # if empty list
    if (len(line_items) == 0):
        lineItem = NV_table_line_item(linha[0])

        if linha[len(linha) - 1] == 'yes':
            lineItem.increment_yes()
        else:
            lineItem.increment_no()

        line_items.append(lineItem)
        continue

    containItemLine = False

    # If line item is on array
    for item in line_items:
        if item.getName() == linha[0]:
            containItemLine = True
            if linha[len(linha) - 1] == 'yes':
                item.increment_yes()
            else:
                item.increment_no()

    # If is a new line on array
    if (containItemLine == False):
        lineItem = NV_table_line_item(linha[0])
        if linha[len(linha) - 1] == 'yes':
            lineItem.increment_yes()
        else:
            lineItem.increment_no()
        line_items.append(lineItem)

print "----------"

for item in line_items:
    item.imprime()
