SISTEMA DE MANEJO DE INVENTARIO


- Descripción general:
El sistema se trata básicamente de una webapp echa con Django, framework de Python que permite administrar diferentes inventarios de ítems. 


- Librerías utilizadas:
* Bootstrap : para el estilo del frontend,  puede seguir modificándose para que sea más responsivo. Ha sido diseñado para utilizar en una  pantalla de pc.
* django-jazzmin : para una mejor interfaz de usuario en el panel de administración
* reportlab : para la exportación en pdf de la información. 


- Dinámica del funcionamiento:
Solamente es posible acceder a la aplicación si se está registrado. Dentro de la aplicación existen dos tipos de usuarios con diferentes permisos.

-- Administrador
El superusuario, es el administrador de todos los inventarios y también es el único responsable de la creación de items y asignación de la cantidad total de cada uno.
Cuando un superusuario crea un inventario para un departamento, automáticamente se crea un usuario regular con el mismo nombre.

Por ejemplo, al crear el inventario del departamento de IT, se creará el usuario "it" con la contraeña "it_pass".

El administrador es capaz de acceder al panel de administración y cambiar las contraseñas para mayor seguridad.

La aplicación tiene dos formas de vista. Una para el superusuario, el cual puede acceder al inventario general, crear, editar, borrar y modificar la cantidad de cada ítem o su categoría. También puede acceder a los inventarios de cada departamento, crearlos, editarlos, borrarlos o modificarlos. 

-- Usuario regular
El usuario regular solamente puede acceder a su propio inventario (no verá la vista general de items, no podrá añadir items al inventario general ni tampoco ver los inventarios de los demás departamentos). Será capaz de añadir los items disponibles de los que haya añadido previamente el administrador y modificar la cantidad que posee en su departamento.


-- Modelado de la base de datos
Los modelos básicos son Inventario (asignado a un usuario, incluyendo el campo 'departamento' ), Item (con su cantidad total, categoría, cantidad disponible) e ItemInventory (modelo intermediario para manejar la relación entre los inventarios y los items). 
El item tiene un campo denominado "total" y un campo denonminado "disponible" . Cuando un usuario o el administrador asigna una determinada cantidad de items a algún inventario, el valor de items disponible disminuye de forma automática. A su vez no será posible asignar más items a un inventario de los que hay disponibles.


-- Exportación y búsqueda
La aplicación permite exportar los datos filtrados, por nombre o categoría, de cada inventario o del inventario general en formato pdf.


-- Contenido dinámico
Gracias a la arquitectura de Django, la aplicación ha sido desarrollada de forma dinámica, de forma tal que un solo template sirve para mostrar la información según la búsqueda, el tipo de usuario y diferentes condicionales en función de cada necesidad.




INSTALACIÓN

-Requierimientos previos
-- Para poder hacerla correr en un servidor local, es necesario tener python instalado. (página oficial  de descarga para windows https://www.python.org/ftp/python/3.11.2/python-3.11.2-amd64.exe ) y asegurarse de aceptar la inclusión en PATH.
-- También es útil tener pip instalado. (Aquí puedes encontrar una guía para esto: https://pip.pypa.io/en/stable/installation/ )
-- Y Git ( http://git-scm.com/download/win )

PRIMEROS PASOS
1) En una consola o editor de código, abrir la carpeta donde se ubicará el proyecto.
2) Crear un entorno virtual con el comando:
 python -m venv env
3) Activar el entorno virtual
 source env/Scripts/activate (en linux: source env/bin/activate)
4) Clonar el código 
git clone '#'
5) Acceder al directorio donde se encuentra manage.py e instalar los paquetes necesarios.
pip install -r requirements.txt
6) Iniciar las migraciones de la base de datos:
python manage.py makemigrations
python manage.py migrate
7) Crear un superusuario:
python manage.py createsuperuser
8) Encender el servidor:
python manage.py runserver
( # aquí se puede decidir en qué puerto se desea hacer correr el servidor de Django. El puerto por defecto es en localhost puerto 8000. Sin embargo para cambiar esto en vez de python manage.py runserver puedes escribir por ejemplo:
python manage.py runserver 127.0.0.1:80 #)

9) Acceder desde un navegador de internet (como google chrome o mozilla firefox) a 127.0.0.1:8000 (# localhost + puerto asignado por defecto)

TODO LISTO! Ya puedes utilizar la aplicación de manejo de inventario.

Recuerda que estás accediendo con el superusuario que creaste previamente, por lo que tendrás acceso a todos los departamentos y control total de la aplicación. Aún no hay ningún inventario ni item en la base de datos, pero puedes empezar a crear los que desees.

Ten presente que al crear un inventario para un departamento, automáticamente estarás creando un usuario asociado a ese inventario, que tendrá acceso únicamente a sus items e inventario.

Tendrás que crear algunos items, el usuario regular no puede crear items, solamente puede añadir los items disponibles en su inventario.


AUTENTIFICACIÓN Y SEGURIDAD
El usuario creado automáticamente, tendrá el mismo nombre que el apartamento (cambiando los espacios por _ y las mayúsculas por minúsculas) y una contraseña similar terminada en _pass.

De forma que si el departamento se llama Natural Sciences: el usuario será "natural_sciences" y la contraseña será "natural_sciences_pass'

# No te olvides de cambiar a contraseña! #
Para cambiar la contraseña de los usuarios, puedes hacerlo desde el panel de administración, cuyo link se encuentra en la barra de navegación de la webapp.
Simplemente dirígete a usuarios, selecciona el usuario deseado y modifica su contraseña.










