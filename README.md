# Grupo 20

## Integrantes

Iyael Lihue Pereyra - 16440/6

Nehuen Pereyra - 15926/1

---

## Información de Acceso

### Usuario Administrador
Correo: admin@admin.com
Pass: admin123

---

## Defición de API

### Centros de Ayuda

*Aclaraciones: 
El archivo que contiene el codigo correspondiente a la api de centros de ayuda se encuentra en `app/resources/api/help_center.py`.*

*Se utilizo para su desarrollo Flask nativo y Flask-WTF (para realizar las validaciones).*

*No se realizó ningun cambio adicional en el modelo.*

### Listar

**Ruta:** `/api/centros`

**Metodo:** `GET`

**Argumentos:**
- `pagina`

**Codigos de error:**
- 400 Bad Request (pagina < 1)

**Ejemplo exitoso:**
```json
{
  "centros": [
    {
      "direccion": "Av 80 e20 y 21 nro 90", 
      "email": "papa@centro.org", 
      "hora_apertura": "09:00", 
      "hora_cierre": "16:00", 
      "nombre": "Centro la Papa", 
      "telefono": "+54 294 410-2030", 
      "tipo": "Centro de Alimentos", 
      "web": "https://papa.centro.org"
    }
  ], 
  "pagina": 1, 
  "por_pagina": 4, 
  "total": 1
}
```

### Ver

**Ruta:** `/api/centro/<int:id>`

**Metodo:** `GET`

**Argumentos:**
- N/A

**Codigos de error:**
- 404 Not Found

**Ejemplo exitoso:**
```json
{
  "atributos": {
    "direccion": "Av 80 e20 y 21 nro 90", 
    "email": "papa@centro.org", 
    "hora_apertura": "09:00", 
    "hora_cierre": "16:00", 
    "nombre": "Centro la Papa", 
    "telefono": "+54 294 410-2030", 
    "tipo": "Centro de Alimentos", 
    "web": "https://papa.centro.org"
  }
}
```

### Crear

**Ruta:** `/api/centro`

**Metodo:** `POST`

**Argumentos:**
- `nombre*`
- `direccion*`
- `telefono*`
- `hora_apertura*`
- `hora_cierre*`
- `tipo*`
- `municipio*`
- `web_url`
- `email`
- `latitud`
- `longitud`

**Codigos de error:**
- 400 Bad Request

**Ejemplo sin campos opcionales:**

Cuerpo de la solicitud
```json
{
    "nombre": "Centro Vikingo",
    "direccion": "Calle 90",
    "telefono": "+54 2944 208060",
    "hora_apertura": "09:30",
    "hora_cierre": "10:00",
    "tipo": "Centro de Sangre",
    "municipio": "Avellaneda"
}
```

Cuerpo de la respuesta
```json
{
    "atributos": {
        "direccion": "Calle 90",
        "hora_apertura": "09:30",
        "hora_cierre": "10:00",
        "municipio": "Avellaneda",
        "nombre": "Centro Vikingo",
        "telefono": "+54 2944 208060",
        "tipo": "Centro de Sangre"
    }
}
```

**Ejemplo con campos opcionales:**

Cuerpo de la solicitud
```json
{
    "nombre": "Centro Vikingo",
    "direccion": "Calle 90",
    "telefono": "+54 2944 208060",
    "hora_apertura": "09:30",
    "hora_cierre": "10:00",
    "tipo": "Centro de Sangre",
    "municipio": "Avellaneda",
    "web_url": "https://vikingo.centro.org",
    "email":  "ragnar@midgard.org",
    "latitud": -20.125543,
    "longitud": 10.204012
}
```

Cuerpo de la respuesta
```json
{
    "atributos": {
        "direccion": "Calle 90",
        "email": "ragnar@midgard.org",
        "hora_apertura": "09:30",
        "hora_cierre": "10:00",
        "latitud": -20.125543,
        "longitud": 10.204012,
        "municipio": "Avellaneda",
        "nombre": "Centro Vikingo",
        "telefono": "+54 2944 208060",
        "tipo": "Centro de Sangre",
        "web_url": "https://vikingo.centro.org"
    }
}
```

**obs:** En la base de datos se cargaron 3 tipos de centro de ayuda:
- `Centro de Alimentos`
- `Centro de Ropa`
- `Centro de Sangre`
