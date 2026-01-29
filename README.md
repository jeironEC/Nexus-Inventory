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
