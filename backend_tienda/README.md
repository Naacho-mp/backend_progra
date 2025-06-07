# PASOS PARA INICIALIZAR EL PROYECTO

1.- Crear tu propio Entorno Virtual (venv)

2.- Instalar las Librerias y Dependencias adjuntos en el archivo "Requirements.txt", en tu entorno virtual

3.- Crea tu Schema en tu Base de datos

3.- Crear archivo .env en la raiz del Proyecto con sus credenciales de la BD:

    - DB_NAME = tienda_online
    - DB_USER = tu_user
    - DB_PASSWORD = tu_pass
    - DB_HOST = localhost
    - DB_PORT = 3306

4.- Correr el Proyecto con "Python manage.py runserver"