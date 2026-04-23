#  Plataforma de Monitoreo Industrial — DDC

Sistema web de monitoreo y registro de procesos industriales 
(Falta contexto de que logro con esto e imagenes representativas)

desarrollado con **Django 5.1** y **MySQL**.

---

## Tabla de contenidos

- [Requisitos previos](#-requisitos-previos)
- [Instalación del entorno virtual](#-1-instalación-del-entorno-virtual)
- [Dependencias del sistema (WeasyPrint)](#-2-dependencias-del-sistema-weasyprint)
- [Instalación de paquetes Python](#-3-instalación-de-paquetes-python)
- [Configuración de variables de entorno](#-4-configuración-de-variables-de-entorno)
- [Configuración de la base de datos](#-5-configuración-de-la-base-de-datos)
- [Migraciones y datos iniciales](#-6-migraciones-y-datos-iniciales)
- [Crear superusuario](#-7-crear-superusuario)
- [Ejecutar el servidor](#-8-ejecutar-el-servidor)
- [Estructura del proyecto](#-estructura-del-proyecto)
- [Stack tecnológico](#-stack-tecnológico)

---

## ✅ Requisitos previos

Antes de comenzar asegúrate de tener instalados los siguientes programas:

| Herramienta | Versión recomendada | Descarga |
|---|---|---|
| Python | 3.11 o superior | [python.org](https://www.python.org/downloads/) |
| MySQL | 8.0 o superior | [MySQL Community](https://dev.mysql.com/downloads/) o [XAMPP](https://www.apachefriends.org/) |
| MSYS2 | Última versión | [msys2.org](https://www.msys2.org/) |
| Visual Studio Build Tools | 2022 o superior | [VS Build Tools](https://visualstudio.microsoft.com/es/visual-cpp-build-tools/) |
| Git | Cualquier versión reciente | [git-scm.com](https://git-scm.com/) |

---

## 1. Instalación del entorno virtual

### 1.1 — Clonar el repositorio

```bash
git clone https://github.com/matibenavides/plataforma-monitoreo-industrial.git
cd plataforma-monitoreo-industrial
```

### 1.2 — Habilitar scripts en PowerShell (Windows) `Opcional`

En PowerShell, ejecutar **una sola vez por sesión**:

```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope Process
```

### 1.3 — Crear el entorno virtual

```powershell
virtualenv -p python3 env
python -m venv env
.\env\Scripts\Activate
```

---

## 2. Dependencias del sistema (WeasyPrint)

El proyecto utiliza **WeasyPrint** para generación de PDF, que requiere la librería Pango del sistema operativo.

### 2.1 — Instalar Pango con MSYS2

Abre la terminal de **MSYS2** y ejecuta:

```bash
pacman -S mingw-w64-x86_64-pango
```

### 2.2 — Instalar Visual Studio Build Tools

WeasyPrint necesita un compilador de C++ para algunas dependencias:

1. Descarga [Visual Studio Build Tools](https://visualstudio.microsoft.com/es/visual-cpp-build-tools/)
2. Durante la instalación, marca la casilla **"Desarrollo para el escritorio con C++"**

> ⚠️ Esta instalación ocupa aproximadamente **6.5 GB** en disco.

---

## 3. Instalación de paquetes Python

Con el entorno virtual activo, instala todas las dependencias:

```powershell
pip install -r requirements.txt
```


---

##  4. Configuración de variables de entorno

Crea un archivo `.env` en la **raíz del proyecto** con el siguiente contenido:

```env
# Configuración de Django
DJANGO_SECRET_KEY=django-insecure-reemplaza-con-una-clave-aleatoria-segura
DEBUG=True

# Configuración de la Base de Datos
DB_NAME=ddc
DB_USER=root
DB_PASSWORD=tu_contraseña_aqui
DB_HOST=127.0.0.1
DB_PORT=3306
```


---

##  5. Configuración de la base de datos

### 5.1 — Crear la base de datos en MySQL

Abre **MySQL Workbench**, **XAMPP → phpMyAdmin**, o la terminal de MySQL y ejecuta:

```sql
CREATE DATABASE ddc;
```

> Asegúrate de que el usuario y contraseña definidos en `.env` tengan permisos sobre esta base de datos.

---

##  6. Migraciones y datos iniciales

### 6.1 — Aplicar migraciones

Las migraciones ya están incluidas en el repositorio. Solo ejecuta:

```powershell
py manage.py migrate
```
> 
> utiliza directamente `migrate`, no hace falta utilizar el comando `makemigrations` ya que los archivos migratorios de los modelos están en el repositorio.

### 6.2 — Cargar datos iniciales

El proyecto incluye un fixture con todos los datos base necesarios (especies, variedades, fungicidas, líneas, sectores, turnos, etc.):

```powershell
py manage.py loaddata datos_iniciales.json
```

---

##  7. Crear superusuario

Crea el usuario administrador para acceder al panel `/admin`:

```powershell
py manage.py createsuperuser
```

Ingresa el **nombre de usuario**, **email** (opcional) y **contraseña** cuando se soliciten.
> Los datos del superuser serán necesarios para ingresar al `Login` del dashboard.

---

##  8. Ejecutar el servidor

Inicia el servidor de desarrollo:

```powershell
py manage.py runserver
```

La aplicación estará disponible en: **[http://127.0.0.1:8000](http://127.0.0.1:8000)**

El panel de administración estará en: **[http://127.0.0.1:8000/admin](http://127.0.0.1:8000/admin)**

> ⚠️ **Si tienes problemas al registrar datos con el usuario administrador:**
>
> Debes vincular el usuario `superuser` con un `Trabajador` desde el panel de administración.
>
> **Pasos:**
> 1. Ir a `/admin`
> 2. Entrar en **Cloraciones**
> 3. Seleccionar **Trabajadores**
> 4. Hacer clic en **Añadir Trabajador**
> 5. Completar el formulario, asegurándote de seleccionar:
>    - `User:` superuser
> 6. Guardar los cambios

---

##  Estructura del proyecto

```
plataforma-monitoreo-industrial/
│
├── ddc/                    # Configuración principal de Django (settings, urls, wsgi)
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
│
├── Cloraciones/            # App principal: registros de cloración
│   ├── fixtures/           # datos_iniciales.json
│   ├── migrations/
│   ├── templates/
│   ├── static/
│   ├── models.py
│   ├── views.py
│   └── urls.py
│
├── Fungicidas/             # App de registro de fungicidas
├── Temperaturas/           # App de registro de temperaturas
├── PPM/                    # App de registro de PPM
├── Productos/              # App de gestión de productos
├── Login/                  # App de autenticación
│
├── manage.py
├── requirements.txt
├── .env                    # Variables de entorno (NO versionar)
└── .gitignore
```

---

##  Stack tecnológico
 
| Tecnología | Versión | Uso |
|---|---|---|
| Python | 3.11+ | Lenguaje base |
| Django | 5.1 | Framework web |
| PyMySQL | 1.1.1 | Conector MySQL |
| WeasyPrint | 64.0 | Generación de PDF |
| python-decouple | 3.8 | Variables de entorno |
| Font Awesome | 6.6.0 | Iconografía |


---

> Desarrollado con Django 5.1 · MySQL · Python 3.11
