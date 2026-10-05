#!/bin/bash
# Comandos para despliegue en AWS EC2 (Ubuntu)

sudo apt update
sudo apt install python3 python3-venv python3-pip git -y
# Instalar dependencias de MySQL para el conector
sudo apt install default-libmysqlclient-dev build-essential -y

git clone https://github.com/tu_usuario/tu_repo_terriia.git
cd tu_repo_terriia

python3 -m venv venv
source venv/bin/activate

pip install -r requirements.txt

python manage.py makemigrations
python manage.py migrate

python manage.py runserver 0.0.0.0:8000
