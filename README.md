# API de Gestión de Usuarios

¡Bienvenido a la API de Gestión de Usuarios! Este proyecto es una solución robusta y escalable para gestionar datos de usuarios, construida con FastAPI. Proporciona un conjunto de endpoints para el registro de usuarios, inicio de sesión, gestión de perfiles y más, garantizando un manejo seguro y eficiente de la información de los usuarios.

## Características

- **Registro de Usuarios**: Crear nuevas cuentas de usuario con correo electrónico y contraseña.
- **Inicio de Sesión**: Autenticar usuarios y generar tokens JWT para la gestión de sesiones.
- **Gestión de Perfiles de Usuario**: Actualizar perfiles de usuario, incluyendo nombre, correo electrónico y otros detalles personales.
- **Gestión de Contraseñas**: Hashing seguro de contraseñas y funcionalidad de restablecimiento de contraseña.
- **Autenticación OAuth2**: Autenticación segura utilizando OAuth2 con flujo de contraseña.
- **Manejo de Excepciones**: Manejo robusto de errores con respuestas de excepciones personalizadas.

## Tecnologías Utilizadas

- **Python 3.12**
- **FastAPI**
- **Pydantic**
- **SQLAlchemy**
- **Alembic**
- **JWT**
- **MySQL**
- **Docker**

## Configuración

### Prerrequisitos

- Python 3.x instalado en tu máquina
- Docker (opcional, para despliegue en contenedores)

### Instalación

1. **Clonar el repositorio**:
    ```bash
    git clone https://github.com/tuusuario/api-gestion-usuarios.git
    cd api-gestion-usuarios
    ```

2. **Crear un entorno virtual**:
    ```bash
    python -m venv venv
    source venv/bin/activate   # En Windows usar `venv\Scripts\activate`
    ```

3. **Instalar dependencias**:
    ```bash
    pip install -r requirements.txt
    ```

4. **Variables de Entorno**:
    - Crea un archivo `.env` en la raíz del proyecto y añade las siguientes variables:
        ```bash
        DATABASE_URL=
        SECRET_KEY=
        ALGORITHM=HS256
        ACCESS_TOKEN_EXPIRE_MINUTES=30
        MAIL_USERNAME=
        MAIL_FROM=
        MAIL_PASSWORD=
        MAIL_PORT=587
        MAIL_SERVER=smtp.gmail.com
        ```
    - Reemplaza los valores con tu configuración de base de datos y credenciales de correo electrónico.


4. **Iniciar la aplicación**:
    ```bash
    uvicorn main:app --reload
    ```

5. **La API estará disponible en**:
    ```
    http://localhost:8000
    ```

### Despliegue con Docker

1. **Construir la imagen de Docker**:
    ```bash
    docker build -t user-service .
    ```

2. **Ejecutar el contenedor de Docker**:
    ```bash
    docker run -d -p 8000:8000 user-service
    ```
## Contribuciones

¡Las contribuciones son bienvenidas! Por favor, haz un fork del repositorio y abre una pull request con tus cambios. Asegúrate de seguir el estilo de código establecido e incluir pruebas para cualquier nueva funcionalidad.


Siéntete libre de personalizar esta descripción según las especificaciones de tu proyecto.