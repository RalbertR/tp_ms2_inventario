# Definition of Done

Una tarea de este repositorio está terminada cuando cumple los seis criterios de abajo.
Si falta uno solo, el PR no se integra a `main`. La DoD vale igual para todas las tareas,
sean bugs, features, deuda técnica o documentación. Lo que cambia entre una historia y
otra son los criterios de aceptación, que van en cada issue.

## 1. Integridad de compilación

- [ ] `python -m compileall -q inventario tests` termina sin errores.
- [ ] La suite corre con los warnings convertidos en errores, así que un
      `DeprecationWarning` o un `ResourceWarning` frena la integración igual que un fallo.

## 2. Pruebas automatizadas en verde

- [ ] `pytest` pasa el 100% de los tests. Un solo test en rojo bloquea el merge.
- [ ] Todo bug corregido trae un test que reproduce el fallo y que fallaba antes del arreglo.
- [ ] Ningún test unitario llama a la API de pagos real ni a otro servicio externo.
      Para eso se usan stubs o mocks.

## 3. Umbral mínimo de cobertura

- [ ] La cobertura total del paquete `inventario`, medida con ramas, es de 80% o más.
- [ ] Ningún módulo que el PR crea o modifica queda por debajo del 80%.
- [ ] El reporte de `pytest --cov` se pega en la descripción del PR.

## 4. Revisión por pares obligatoria

- [ ] El PR tiene al menos una aprobación de otro integrante del equipo.
      El autor no cuenta como revisor.
- [ ] El revisor recorre este checklist y deja comentarios en el diff si algo no cierra.
- [ ] Todas las conversaciones del PR quedan resueltas antes del merge.

## 5. Gobernanza de estilo

- [ ] `black --check .` no reformatea ningún archivo.
- [ ] `ruff check .` no reporta errores con las reglas de `pyproject.toml`.
- [ ] No se desactivan reglas con `# noqa` sin explicar el motivo en el PR.

## 6. Documentación técnica al día

- [ ] Las funciones con lógica de negocio no trivial tienen docstring.
- [ ] Si cambia lo que el sistema manda o espera de la API de pagos, se actualiza
      `docs/contrato_pagos.md` en el mismo PR.
- [ ] Si cambian comandos de instalación, de tests o de herramientas, se actualiza el README.
