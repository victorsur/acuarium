# Prompt SSD para Frontend Vue CRUD

Crea un frontend en Vue.js para un CRUD completo de las entidades definidas en openapi
Debes respetar el sistema de carpetas ya establecido en el proyecto y seguir principios de buenas prácticas como SOLID, clean Code y demás.
En caso de duda siempre tienes que preguntar antes de realizar cualquier cambio o de crear cualquier código.
Quiero que los formularios tenga validaciones.
Los mensajes de error serán notificaciones simples.
Deseo que la estructura sea modular y permita añadir nuevas entidades fácilmente en el futuro.
Quiero utilizar un sistema de login para el frontend, con autenticación JWT, para proteger las rutas de administración del CRUD. El sistema de login debe permitir a los usuarios autenticarse y obtener un token JWT que se utilizará para acceder a las rutas protegidas del CRUD.
Este sistema de login debe incluir un formulario de inicio de sesión, validación de credenciales y manejo de tokens JWT para mantener la sesión del usuario. Además, el frontend debe manejar la expiración del token y redirigir al usuario al formulario de inicio de sesión cuando el token haya expirado o sea inválido.
El sistema de login permite los roles de usuario, para que solo los usuarios con el rol adecuado puedan acceder a las rutas protegidas del CRUD. Por ejemplo, solo los usuarios con el rol "ROLE_ADMIN" podrían acceder a las rutas de administración del CRUD, mientras que otros roles podrían tener acceso limitado o no tener acceso en absoluto.
Tanto la modificación como el borrado de objetos deben estar protegidos por el sistema de login, asegurando que solo los usuarios autenticados y autorizados puedan realizar estas acciones. El frontend debe verificar el token JWT antes de permitir cualquier operación de modificación o eliminación, y mostrar mensajes de error apropiados si el usuario no tiene los permisos necesarios.
El admin tiene todos los privilegios y el usuario normal solo puede modificar los objetos creados por él mismo, sin poder modificar los objetos creados por otros usuarios ni eliminarlos.
Debes crear el sistema de login en el back (incluido el repositorio de credenciales en BBDD y demás), para luego proteger las rutas del CRUD y asegurarte de que solo los usuarios autenticados puedan acceder a ellas.
El sistema de login en el back lo debes implantar sabiendo que el proyecto ya tiene una base de datos MySQL configurada, por lo que debes crear las tablas necesarias para almacenar las credenciales de los usuarios y sus roles. Además, debes implementar la lógica de autenticación utilizando JWT, asegurándote de que el backend pueda generar tokens JWT válidos y verificar su autenticidad en cada solicitud al CRUD.
El sistema de login debe integrarse con el backend, utilizando los endpoints de autenticación JWT proporcionados por API Platform. El frontend debe enviar las credenciales del usuario al backend, recibir el token JWT en caso de éxito y almacenarlo de manera segura (por ejemplo, en localStorage o cookies) para su uso en futuras solicitudes al backend.


El frontend debe:

- Lo primero crear un sistema de login con autenticación JWT para proteger las rutas del CRUD.
- Crear pestañas para cada componente (Pez, Acuario, Luz y mantenimiento).
- Listar, crear, modificar y eliminar cada entidad usando los endpoints REST generados por API Platform.
- Adaptar los formularios a los campos de cada entidad, respetando los campos obligatorios y opcionales según `openapi.yaml`.
- Usar axios para las peticiones HTTP.
- Mostrar mensajes de éxito/error y actualizar el listado tras cada operación.
- Tomar como referencia el listado de Pez ya existente.
- Conectar con la base de datos MySQL configurada en el proyecto.

## Detalles
- Los formularios deben contemplar la creación, modificación y borrado de los objetos.
- El listado debe mostrar todos los campos de cada entidad.
- La estructura del frontend debe ser modular, permitiendo añadir nuevas entidades fácilmente.
- El repositorio de cada entidad debe gestionarse correctamente en la base de datos MySQL.

---
