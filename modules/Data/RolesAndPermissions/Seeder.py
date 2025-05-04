
from modules.Data.RolesAndPermissions.DataRolePermissions import ALL_PERMISSIONS, ROLE_PERMISSIONS
from modules.Data.RolesAndPermissions.PermissionService import PermissionService
from modules.Data.RolesAndPermissions.RoleService import RoleService
from shared.extensions import db


def seed_roles_and_permissions():
    # 1) Crear/actualizar permisos
    existing = PermissionService.all_names()
    for name, desc in ALL_PERMISSIONS.items():
        if name not in existing:
            PermissionService.get_or_create(name, desc)

    # 2) Crear/actualizar roles
    for role_name in ROLE_PERMISSIONS:
        RoleService.get_or_create(role_name, description=f"Rol {role_name}")

    # 3) Asignar permisos a roles
    for role_name, perm_names in ROLE_PERMISSIONS.items():
        role = RoleService.get_or_create(role_name)
        for pname in perm_names:
            perm = PermissionService.get_or_create(pname, ALL_PERMISSIONS[pname])
            RoleService.assign_permission(role, perm)

    # 4) Commit final
    db.session.commit()
