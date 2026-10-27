# Contrato con la API de pagos

`PasarelaHttp` es el único lugar del sistema que habla con la API externa de pagos.
El resto del código solo conoce la interfaz `PasarelaDePagos` y el `ResultadoPago`.

## Cobro

`POST {url_base}/v1/cobros`

Cabecera obligatoria: `Authorization: Bearer <api_key>`

Cuerpo que envía el sistema:

| Campo   | Tipo   | Descripción                                |
|---------|--------|--------------------------------------------|
| `monto` | number | Total a cobrar en pesos, con dos decimales |
| `token` | string | Token de la tarjeta generado en el front   |

Respuesta que espera el sistema:

| Campo    | Tipo   | Descripción                                   |
|----------|--------|-----------------------------------------------|
| `estado` | string | `aprobado` o `rechazado`                      |
| `id`     | string | Identificador de la transacción, si se aprobó |
| `motivo` | string | Causa del rechazo, si se rechazó              |
