# Inventario con checkout

Sistema de inventario que avisa a varios servicios cuando un producto queda con stock
bajo y cobra las compras a través de una API externa de pagos. Es el caso de estudio de
la Unidad 3 de Metodología de Sistemas II, Verificación y Validación con herramientas.

## Instalación

```
python3.13 -m venv .venv
.venv/bin/pip install -r requirements-dev.txt
```

## Calidad

- Antes de abrir un PR, leer la [Definition of Done](DEFINITION_OF_DONE.md).
- Los issues se cargan con las plantillas de `.github/ISSUE_TEMPLATE`.

## Pre-commit hook

`hooks/pre-commit` corre en orden black, ruff y pytest con el umbral de cobertura de la
DoD. Si un paso falla, el commit se aborta. Se activa una vez por clon:

```
git config core.hooksPath hooks
```

## Análisis estático

- SonarQube local en Docker, con la configuración de `sonar-project.properties` y el
  `coverage.xml` que genera `pytest --cov --cov-report=xml`.
- Dependencias: `pip-audit -r requirements.txt`.
