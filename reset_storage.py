# Delete PKL files

import os

files_to_create = ["app/storage/salas.pkl", "app/storage/sessoes.pkl", "app/storage/filmes.pkl", "app/storage/pagamentos.pkl"]
for file in os.listdir():
    if file.endswith(".pkl"):
        os.remove(file)

# Create files
for file in files_to_create:
    f = open(file, "w")

