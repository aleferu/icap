#!/usr/bin/env bash

# Imprime qué comandos son utilizados y para en error
set -xe

# Generación del documento
# Nombre del documento es un placeholder atm
pdflatex -jobname="proyecto_icap" main.tex

# Done
printf "\nDONE!\n"
