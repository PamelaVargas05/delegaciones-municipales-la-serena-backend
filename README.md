# Sistema de Gestión de Delegaciones Municipales de La Serena

Aplicación web para registrar y consultar solicitudes vecinales asociadas a las
delegaciones municipales de La Serena. El proyecto incluye el frontend público
de solicitudes y el panel de administración de Django.

## Tecnologías utilizadas

- Python
- Django
- Bootstrap
- SQLite para desarrollo local
- MySQL para producción (configurable mediante variables de entorno)
- Gunicorn y Nginx como referencia para producción
- AWS EC2 como plataforma de despliegue considerada

## Aplicaciones Django

- `delegaciones/`: modelos y administración de delegaciones y metas.
- `solicitudes/`: modelos, formularios, vistas, URLs y administración de solicitudes vecinales.
- `config/`: configuración, URLs, WSGI y ASGI del proyecto.

## Estructura general

```text
config/                 Configuración principal de Django
delegaciones/           Aplicación de delegaciones municipales
solicitudes/             Aplicación de solicitudes vecinales
static/                  CSS y archivos estáticos públicos
templates/               Plantilla base compartida
deploy/                  Archivos de referencia para Gunicorn y Nginx
comandos_aws.sh          Comandos de referencia para AWS EC2
manage.py                Utilidad de administración de Django
requirements.txt         Dependencias Python
.env.example             Ejemplo de variables de entorno
```

## Instalación local

Se recomienda utilizar un entorno virtual:

```bash
python -m venv .venv
```

Activación en Windows PowerShell:

```powershell
.\.venv\Scripts\Activate.ps1
```

Activación en Linux/macOS:

```bash
source .venv/bin/activate
```

Instalar dependencias:

```bash
pip install -r requirements.txt
```

## Migraciones

Aplicar las migraciones existentes:

```bash
python manage.py migrate
```

Si se modifican modelos en el futuro, generar y aplicar nuevas migraciones:

```bash
python manage.py makemigrations
python manage.py migrate
```

## Creación de superusuario

```bash
python manage.py createsuperuser
```

## Ejecución del servidor

```bash
python manage.py runserver
```

La aplicación pública queda disponible en `/solicitudes/` y el panel de
administración en `/admin/`.

## Variables de entorno

Copiar `.env.example` como `.env` y ajustar los valores para el entorno local:

```bash
cp .env.example .env
```

En Windows PowerShell:

```powershell
Copy-Item .env.example .env
```

El proyecto usa SQLite cuando no está definida `DB_NAME`. Si se define
`DB_NAME`, configura la conexión MySQL con `DB_USER`, `DB_PASSWORD`, `DB_HOST`
y `DB_PORT`.

El archivo `.env` es local y está excluido por `.gitignore`; no debe subirse a
GitHub. `.env.example` solo contiene valores de ejemplo.

## Producción y AWS EC2

La carpeta `deploy/` contiene archivos de referencia para Gunicorn y Nginx.
`comandos_aws.sh` contiene pasos iniciales de despliegue en AWS EC2. Antes de
usar producción se deben configurar las variables de entorno, el servidor web
y la base de datos MySQL.

`mysqlclient` no se incluye actualmente en `requirements.txt` para evitar
problemas de compilación en Windows. Será necesario instalarlo posteriormente
en el servidor de producción si se utiliza MySQL, junto con sus dependencias
de sistema.
