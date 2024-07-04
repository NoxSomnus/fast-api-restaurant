# Proyecto Electiva: Desarrollo de APIs con Python

Este proyecto es una API usando FastAPI sobre la gestion de inventarios y pedidos de un restaurant.

Debe utilizar el comando docker compose up para montar los contenedores dockers que soportan la base de datos PostgreSQL y la imagen de la api que es buildeada en el dockerfile

Primero debe crear un usuario y autenticarse para acceder a los endpoints de la aplicación.

Para crear un plato, primero se debe crear un menú (desayunos, almuerzos, especial de la casa, etc.) y tener los ingredientes creados inicialmente y asignarles una cantidad en el inventario.
Con base a esa información puede crear el plato.

Al hacer un pedido se debe tener un usuario creado (el que hará el pedido) y el plato que desea ordenar.
Para que el pedido sea exitoso se debe tener la cantidad suficientes de ingredientes para hacer el plato, de lo contrario, no se podrá ejecutar el pedido.
Cuando el pedido se logra crear, la aplicacion reduce la cantidad de ingredientes automaticamente del inventario.

