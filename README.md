# Nexus-Inventory

# Descripción
Proyecto educativo desarrollado por un equipo de 3 estudiantes: 2 del ciclo DAW y 1 del ciclo ASIX.

# Instrucciones básicas

## Requisitos iniciales

Este proyecto requiere:

- **Python 3.13**
- **pip**

---

## Instalación de Python según sistema operativo

### Fedora
```bash
sudo dnf install python3.13 python3.13-pip
```

### Ubuntu / Debian
```bash
sudo add-apt-repository ppa:deadsnakes/ppa -y
sudo apt update
sudo apt install python3.13 python3.13-venv python3.13-distutils
```

### macOS
```bash
brew install python@3.13
```

### Windows
1. Descargar **Python 3.13** desde https://www.python.org
2. Durante la instalación, marcar la opción **“Add Python to PATH”**

---

## Instalación de pip

Si pip no está disponible, instálalo manualmente:

```bash
curl -sS https://bootstrap.pypa.io/get-pip.py -o get-pip.py
python3.13 get-pip.py
pip install --upgrade pip
```

Una vez instalado, puedes eliminar el archivo descargado:

```bash
rm get-pip.py
```

### Verificar la instalación

```bash
python3.13 --version
```

Salida esperada:
```
Python 3.13.x
```

```bash
python3.13 -m pip --version
```

Salida esperada:
```
pip 25.x from .../python3.13/site-packages/pip (python 3.13)
```

---

## Entorno virtual (venv)

Se recomienda trabajar dentro de un entorno virtual antes de instalar las dependencias.

### Crear el entorno virtual
```bash
python3.13 -m venv myenv
```

> `myenv` es un nombre de ejemplo y puede modificarse.

### Activar el entorno virtual

**Linux / macOS**
```bash
source myenv/bin/activate
```

**Windows (PowerShell)**
```powershell
.\myenv\Scripts\activate
```

---

## Instalación de dependencias

### Dependencias del proyecto (obligatorias)
```bash
pip install -r requirements.txt
```

> **Nota:**
> Este proyecto utiliza **SimpleJWT** para la autenticación JWT.
> Si no está instalado en tu entorno, instálalo manualmente:
```bash
pip install djangorestframework-simplejwt
```

### Dependencias de testing (opcionales)
```bash
pip install -r test-requirements.txt
```

---

## Ejecución del proyecto

### Iniciar el servidor local
Disponible en: http://127.0.0.1:8000

```bash
python manage.py runserver
```

### Iniciar el servidor escuchando en todas las interfaces
Útil para conexión local con un frontend:

```bash
python manage.py runserver 0.0.0.0:8000
```

---

## Migraciones de base de datos

Ejecutar solo si la terminal lo indica o tras cambios en los modelos:

```bash
python manage.py makemigrations
python manage.py migrate
```

---

## Pre-commit

### Instalar y ejecutar los hooks
```bash
pip install pre-commit
pre-commit install
pre-commit run --all-files
```

### Actualizar hooks (si se modifica `.pre-commit-config.yaml`)
```bash
pre-commit autoupdate
pre-commit install
```

---

## Ejecución de tests

### Ejecutar todos los tests
```bash
python -m pytest
```

### Ejecutar un test específico
```bash
python -m pytest tests/test_example.py
```

### .env
#### Crear el archivo .env
Para usar sentry en el proyecto se debe crear el archivo .env y incluir la siguiente variable de entorno:

```bash
SENTRY_DSN="url_proporcionada_por_sentry"
```

### Flujo de configuración del backend

El proyecto utiliza `django-configurations` para gestionar diferentes entornos de ejecución. La configuración se selecciona mediante el flag `--settings` o la variable de entorno `DJANGO_SETTINGS_MODULE`.

#### Diagrama de flujo

```
┌─────────────────────────────────────────────────────────────────┐
│                    Configuración de Base de Datos               │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│   ┌──────────────┐                      ┌──────────────────┐    │
│   │    Local     │                      │      Docker      │    │
│   │   (SQLite)   │                      │   (PostgreSQL)   │    │
│   └──────┬───────┘                      └────────┬─────────┘    │
│          │                                        │             │
│          ▼                                        ▼             │
│   db.sqlite3 (local)                    Variables de entorno    │
│                                                                 │
│   ┌──────────────┐                      ┌──────────────────┐    │
│   │     Test     │                      │    Production    │    │
│   │  (:memory:)  │                      │   (PostgreSQL)   │    │
│   └──────────────┘                      └──────────────────┘    │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

#### Entornos disponibles

| Entorno   | Base de datos | Uso                              |
|-----------|---------------|----------------------------------|
| Local     | SQLite3       | Desarrollo local sin Docker     |
| Docker    | PostgreSQL    | Contenedor con PostgreSQL       |
| Test      | SQLite3       | Ejecución de tests              |
| Production| PostgreSQL    | Entorno de producción           |

#### Selección de entorno

El entorno se selecciona automáticamente según el contexto de ejecución:

1. **Desarrollo local**: Usar configuración `Local` (SQLite)
2. **Contenedor Docker**: Usar configuración `Docker` (PostgreSQL)
3. **CI/Tests**: Usar configuración `Test` (SQLite en memoria)

Para desarrollo local, el proyecto usa SQLite3 por defecto, por lo que no se necesita configurar PostgreSQL. Para ejecutar en contenedor o producción, es necesario configurar las variables de entorno de PostgreSQL.

### Cómo ejecutar con Docker

#### Construcción de la imagen

```bash
# Construir imagen
docker build -t nexus-inventory-backend .

# O con docker-compose
docker-compose up --build
```

#### Ejecución del contenedor

```bash
# Con docker-compose
docker-compose up -d

# Con docker directo
docker run -d \
  -e DATABASE_NAME=nexus_inventory \
  -e DATABASE_USERNAME=postgres \
  -e DATABASE_PASSWORD=postgres \
  -e DATABASE_HOST=db \
  -e DATABASE_PORT=5432 \
  -p 8000:8000 \
  nexus-inventory-backend
```

#### Ver logs

```bash
docker-compose logs -f backend
```

#### Detener contenedores

```bash
docker-compose down
```

### Flujo de configuración del backend

```
┌─────────────────────────────────────────────────────────────────┐
│                    Dockerización del Backend                    │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│   ┌──────────────┐                      ┌──────────────────┐    │
│   │  Dockerfile  │                      │  docker-compose  │    │
│   └──────┬───────┘                      └────────┬─────────┘    │
│          │                                       │              │
│          ▼                                       ▼              │
│   Imagen Docker                            Orquestación         │
│   + PostgreSQL                             + PostgreSQL         │
│   + Backend                                + Backend            │
│                                                                 │
│   ┌──────────────┐                      ┌──────────────────┐    │
│   │  GitHub CI   │                      │       .env       │    │
│   └──────────────┘                      └──────────────────┘    │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

#### Pasos para ejecutar

1. **Instalar Docker/Podman** en la máquina local
2. **Construir la imagen**: `docker build -t nexus-inventory-backend .`
3. **Ejecutar con docker-compose**: `docker-compose up --build`
4. **Verificar funcionamiento**: Acceder a `http://localhost:8000/` o `http://localhost:8000/admin/`
