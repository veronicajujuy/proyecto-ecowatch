# EcoWatch - Sistema de Monitoreo Ambiental

Este proyecto permite la gestión de logs ambientales en tiempo real, almacenamiento en caché, persistencia en base de datos y generación de reportes ejecutivos. Está desarrollado con Python, utilizando patrones de diseño y estructuras de datos eficientes para garantizar modularidad y extensibilidad.

## Funcionalidades Principales

- Carga de logs desde archivos `.csv`.
- Validación y persistencia de datos en base de datos (MySQL).
- Mantenimiento de logs recientes en memoria utilizando `SortedDict`.
- Simulación del avance del tiempo para depuración del cache.
- Generación de reportes personalizados.
- Interfaz de consola para seleccionar tipos de reportes.

## Estructura del Proyecto

```
.
├── data/
│   └── logs_ambientales_ecowatch.csv
├── domain/
│   ├── log_entry.py
│   └── models.py
├── cache/
│   ├── cache_temporal_logs.py
│   └── depurador_logs.py
├── infraestructure/
│   ├── database.py
│   └── ...
├── reports/
│   ├── reports_strategy.py
│   ├── reports_factory.py
│   └── ...
├── services/
│   ├── log_loader.py
│   └── log_repository.py
├── main.py
└── README.md
```

## Requisitos

- Python 3.10+
- Pandas
- SQLAlchemy
- MySQL

Instalación de dependencias:

```bash
pip install -r requirements.txt
```

## Uso del Proyecto

1. **Configurar la base de datos**:
   - Crear la base de datos en MySQL.
   - Ajustar el archivo `database.py` con los datos de conexión.

2. **Armar un .env**
    Crear en la raiz del proyecto un archivo .env con las siguientes variables:
    DB_HOST=...
    DB_PORT=...
    DB_USER=...
    DB_PASSWORD=...
    DB_NAME=...

3. **Cargar logs desde CSV** (una sola vez si ya están cargados):
   - Descomentar las líneas de carga en `main.py`.
   ```python
    # cargar_datos_desde_csv()  # Descomentar solo si hace falta cargar datos
   ```

4. **Ejecutar el programa**:
   ```bash
   python main.py
   ```

5. **Seleccionar tipo de reporte** desde el menú por consola.


## Patrones de Diseño Utilizados

- **Factory**: selección de tipo de reporte.
- **Strategy**: lógica interna de cada tipo de reporte.
- **Decorator (conceptual)**: para mostrar los reportes pausadamente.

## Consideraciones Finales

- La documentación detallada se encuentra en la carpeta **documentación** en un archivo .docx
- El simulador de tiempo (`simular_tiempo`) y la interfaz para reportes avanzados estarán implementados en futuras iteraciones.
- El sistema fue desarrollado con foco en claridad, modularidad y futuras extensiones.

## Autor
Veronica Valdez