# Pre-entrega QA Automation - Saucedemo

## Propósito del proyecto
Automatizar con Selenium WebDriver y Python en [saucedemo.com] para el curso de Talento Tech.
Los tests son independientes entre sí: cada uno abre y cierra su propio navegador.

## Tecnologías utilizadas
- **Python 3**
- **Pytest**
- **Selenium WebDriver**
- **pytest-html**
- **Git y GitHub**

## Instalación de dependencias
Requisitos previos: **Python 3**, **Google Chrome** y **Git**.

```bash
pip install -r requirements.txt
```
> Opcional (recomendado): crear antes un entorno virtual con `python -m venv .venv` y activarlo
> (Mac/Linux: `source .venv/bin/activate`, Windows: `.venv\Scripts\activate`).

## Ejecución de las pruebas
Con el entorno virtual activado:
```bash
pytest
```

## Evidencias generadas
- `reports/reporte.html`: reporte con el resultado de cada test
- `reports/ejecucion.log`: log de la ejecución
- `reports/capturas/`: capturas de pantalla automáticas cuando un test falla