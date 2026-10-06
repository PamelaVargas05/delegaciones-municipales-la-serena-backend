# PENDIENTES - Evaluación Sumativa 2

## Estado actual del proyecto

El proyecto se encuentra desplegado y funcionando en AWS EC2.

### Infraestructura completada

- [x] Instancia EC2 creada en Amazon Linux 2023.
- [x] Python instalado.
- [x] Entorno virtual creado en `/var/www/negocio/venv`.
- [x] Git instalado.
- [x] Proyecto clonado desde GitHub.
- [x] Nginx instalado y funcionando.
- [x] Gunicorn instalado y funcionando como servicio.
- [x] MariaDB 10.11 instalada y funcionando.
- [x] PHP instalado.
- [x] PHP-FPM funcionando.
- [x] phpMyAdmin instalado y accesible.

---

## Proyecto Django

- [x] Proyecto Django funcionando.
- [x] Apps existentes:
  - `delegaciones`
  - `solicitudes`
- [x] Modelos creados.
- [x] Migraciones creadas y aplicadas.
- [x] Django conectado a MariaDB.
- [x] Superusuario creado.
- [x] Django Admin operativo.
- [x] Archivos estáticos recopilados con `collectstatic`.

---

## Base de datos

Base utilizada:

```text
delegaciones_db


PARA EL PHPMYADMIN
django_user
Admin1234

Tablas principales creadas:
delegaciones_delegacion
delegaciones_meta
solicitudes_vecino
solicitudes_solicitudvecinal
django_migrations
django_admin_log
django_session
auth_user



Registros de prueba creados
Se crearon registros desde Django Admin:
- [x] Delegación
- [x] Meta
- [x] Vecino
- [x] Solicitud Vecinal
La solicitud vecinal aparece correctamente en el frontend público.
Frontend
- [x] Diseño frontend personalizado.
- [x] Bootstrap funcionando.
- [x] Navbar institucional.
- [x] Footer.
- [x] Listado de solicitudes.
- [x] Búsqueda.
- [x] Filtro por delegación.
- [x] Estados con badges.
- [x] Detalle de solicitud.
- [x] Formulario de nueva solicitud.
- [x] Botones Modificar y Eliminar restringidos para usuarios públicos.
Página actual:
http://44.209.235.150/

Django Admin:
http://44.209.235.150/admin/

phpMyAdmin:
http://44.209.235.150/phpmyadmin/

PENDIENTES
1. Vista pública de Delegaciones
Revisar si existe una vista pública de la app delegaciones.
Si no existe, crear una vista que muestre:
Nombre
Dirección
Teléfono
Encargado

Agregar navegación hacia esta vista desde el navbar.
Mantener visibles los botones:
Agregar
Modificar
Eliminar
Buscar

No es obligatorio que Modificar y Eliminar funcionen desde el frontend público.
2. Probar CRUD completo en Django Admin
Probar todas las entidades:
Delegaciones
- [ ] Crear
- [ ] Visualizar
- [ ] Modificar
- [ ] Eliminar
- [ ] Buscar
Metas
- [ ] Crear
- [ ] Visualizar
- [ ] Modificar
- [ ] Eliminar
Vecinos
- [ ] Crear
- [ ] Visualizar
- [ ] Modificar
- [ ] Eliminar
- [ ] Buscar
Solicitudes Vecinales
- [ ] Crear
- [ ] Visualizar
- [ ] Modificar
- [ ] Eliminar
- [ ] Buscar por folio
- [ ] Buscar por RUT
- [ ] Buscar por ciudadano
- [ ] Filtrar por estado
- [ ] Filtrar por delegación
3. Revisar requirements.txt
Confirmar que tenga al menos:
Django
python-dotenv
mysqlclient
gunicorn

Las versiones deberían quedar fijadas.
4. Configuración final de producción
Al finalizar todas las pruebas, cambiar en AWS:
DEBUG=False

Verificar que:
ALLOWED_HOSTS=44.209.235.150,127.0.0.1,localhost

Después reiniciar Gunicorn:
sudo systemctl restart gunicorn

Verificar:
sudo systemctl status gunicorn --no-pager

5. Revisar servicios AWS antes de la presentación
Entrar a AWS y ejecutar:
cd /var/www/negocio
source venv/bin/activate

Después:
sudo systemctl status mariadb --no-pager
sudo systemctl status gunicorn --no-pager
sudo systemctl status nginx --no-pager
sudo systemctl status php-fpm --no-pager
python manage.py check

Todos los servicios deben aparecer:
active (running)

6. Actualizar proyecto desde GitHub
Si se hacen cambios en Visual Studio Code:
En computador local
git add .
git commit -m "descripcion del cambio"
git push

En AWS
cd /var/www/negocio
git pull
sudo systemctl restart gunicorn

Si se cambian archivos estáticos:
python manage.py collectstatic --noinput
sudo systemctl restart nginx

Si se modifican modelos:
python manage.py makemigrations
python manage.py migrate

7. Evidencias obligatorias para la evaluación
Tomar capturas de:
AWS
- [ ] Instancia EC2 en ejecución.
- [ ] IP pública.
- [ ] Terminal de Amazon Linux.
- [ ] Entorno virtual activo.
- [ ] Gunicorn active (running).
- [ ] Nginx active (running).
- [ ] MariaDB active (running).
- [ ] Aplicación funcionando desde la IP pública.
GitHub
- [ ] Repositorio.
- [ ] Historial de commits.
- [ ] README.
- [ ] .gitignore.
- [ ] Evidencia de git clone en EC2.
Django
- [ ] models.py.
- [ ] Migraciones.
- [ ] showmigrations.
- [ ] Django Admin.
- [ ] CRUD.
- [ ] Frontend.
- [ ] Solicitudes obtenidas mediante ORM.
phpMyAdmin
- [ ] Base delegaciones_db.
- [ ] Lista de tablas.
- [ ] Estructura de tablas.
- [ ] Registros almacenados.
- [ ] Relación entre SolicitudVecinal y Delegación.
Inteligencia Artificial
- [ ] Prompts utilizados.
- [ ] Respuestas obtenidas.
- [ ] Evidencia de uso de ChatGPT/Copilot.
- [ ] Explicar qué partes del proyecto fueron apoyadas por IA.
8. Documento técnico
Crear documento Word o PDF con:
Descripción del proyecto
- Objetivo.
- Problemática.
- Sistema de gestión de Delegaciones Municipales de La Serena.
Arquitectura
- Proyecto Django.
- Apps delegaciones y solicitudes.
- Modelos.
- ForeignKey.
- MariaDB.
- Django ORM.
- Gunicorn.
- Nginx.
- AWS EC2.
Evidencias
Agregar las capturas indicadas anteriormente.
IA
Incluir prompts utilizados y explicar cómo fueron aplicados.
9. Seguridad final
Antes de entregar:
- [ ] Confirmar que .env NO esté en GitHub.
- [ ] Confirmar que db.sqlite3 NO esté en GitHub.
- [ ] Confirmar que .venv NO esté en GitHub.
- [ ] No publicar contraseñas.
- [ ] No publicar SECRET_KEY.
- [ ] Mantener credenciales solo en .env.
Comandos útiles
Activar entorno:
cd /var/www/negocio
source venv/bin/activate

Verificar Django:
python manage.py check

Ver migraciones:
python manage.py showmigrations

Ver servicios:
sudo systemctl status mariadb --no-pager
sudo systemctl status gunicorn --no-pager
sudo systemctl status nginx --no-pager
sudo systemctl status php-fpm --no-pager

Reiniciar servicios:
sudo systemctl restart gunicorn
sudo systemctl restart nginx
sudo systemctl restart mariadb
sudo systemctl restart php-fpm

Actualizar desde GitHub:
git pull

Estado general
AWS EC2              ✅
GitHub                ✅
MariaDB               ✅
Django ORM            ✅
Migraciones           ✅
Django Admin          ✅
Gunicorn              ✅
Nginx                 ✅
Frontend solicitudes  ✅
phpMyAdmin            ✅

Frontend delegaciones ⬜
CRUD Admin final      ⬜
DEBUG=False           ⬜
Capturas entrega      ⬜
Documento técnico     ⬜
Presentación final    ⬜


Después de guardarlo, súbelo también a GitHub:

```powershell
git add PENDIENTES.md
git commit -m "docs: agregar pendientes para continuidad del proyecto"
git push

Los prompts eso despues de te mando captura jeje avisame cualquier cosa, igual te lo deje casi listo, son cosas simples que faltan modifaciones como el frontend para que se vea mas bonitos y el crud pero no se si habia que hacerlo por eso lo deje como pendiente