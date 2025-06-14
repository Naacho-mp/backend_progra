# APLICACIÓN WEB TIENDA DE PRODUCTOS ELECTRÓNICOS

# Descripción de la aplicación web:

Nuestra aplicacion consiste en una tienda de productos electronicos. La cual cuenta con tres aplicaciones creadas, tales como
usuario, tienda y carrito de compras. Dentro de estas aplicaciones, para el caso de usuario se hace uso de formularios y clases entregados por el propio framework, para el caso de la aplicacion tienda se crean modelos tales como producto y categoria, creando asi 
una relacion entre ellos, y finalmente para el caso del carrito de compras se hace uso de la sessiones de usuario. 

# Instrucciones para ejecutar el proyecto

1.- Crea tu propio Entorno Virtual (venv)

2.- Instala las Librerias y Dependencias adjuntos en el archivo "Requirements.txt", en tu entorno virtual

3.- Crea tu Schema en tu Base de datos

3.- Crear archivo .env en la raiz del Proyecto con sus credenciales de la BD:

    - DB_NAME = tienda_online
    - DB_USER = tu_user
    - DB_PASSWORD = tu_pass
    - DB_HOST = localhost
    - DB_PORT = 3306

4.- Hacer las migraciones del proyecto mediante un "Python manage.py migrate"

5.- Correr el Proyecto con "Python manage.py runserver"
