# modules/roles/config.py

# 1) Todos los permisos únicos de la aplicación
ALL_PERMISSIONS = {
    # Permisos para convocatorias
    "event:create": "Crear nuevas convocatorias",
    "event:read":   "Ver convocatorias existentes",
    "event:update": "Modificar convocatorias",
    "event:delete": "Eliminar convocatorias",
    # Permisos para Usuarios
    "user:create":  "Crear nuevos usuarios",
    # Permisos para areas
    "area:create":  "Crear nuevas áreas",
    "area:read":    "Ver áreas existentes",
    "area:update":  "Modificar áreas",
    "area:delete":  "Eliminar áreas",
    # Permisos para categorias
    "category:create": "Crear nuevas categorías",
    "category:read":  "Ver categorías existentes",
    "category:update": "Modificar categorías",
    "category:delete": "Eliminar categorías",
    # Permisos para inscripciones
    "inscription:create": "Incribir a convocatorias",
    "inscription:read":  "Ver inscripciones",
    "inscription:delete": "Eliminar inscripciones",
    # Permisos para gestionar estudiantes
    "student:create":   "Registrar estudiantes",
    "student:read":     "Ver estudiantes",
    "student:update":   "Editar información estudiante",
    "student:delete":   "Eliminar estudiante",
}

# 2) Mapeo de qué permisos tiene cada rol
ROLE_PERMISSIONS = {
    "admin": [
        "event:create", "event:read", "event:update", "event:delete",
        "user:create",
        "area:create", "area:read", "area:update", "area:delete",
        "category:create", "category:read", "category:update", "category:delete",
    ],
    "moderator": [
        "event:read", "event:update",
        "area:read", "area:update",
        "category:read", "category:update",
    ],
    "student": [
        "inscription:create", "inscription:read", "inscription:delete",
        "student:update",
    ],
    "tutor": [
        "inscription:create", "inscription:read", "inscription:delete",
        "student:create", "student:read", "student:update", "student:delete",
    ],
    "master": [

        ],
    "colaborador": [

        ],
}
