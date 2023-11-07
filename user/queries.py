from user.models import PlantationUser

def is_delivery_man(user: PlantationUser) -> bool:
    return user.is_authenticated and user.is_delivery_man

def is_admin(user: PlantationUser) -> bool:
    return user.is_authenticated and user.is_admin

def is_staff(user: PlantationUser) -> bool:
    return user.is_authenticated and user.is_staff

def is_general(user: PlantationUser) -> bool:
    return user.is_authenticated and user.is_general


def is_superuser(user: PlantationUser) -> bool:
    return user.is_authenticated and user.is_superuser

def is_supplier(user: PlantationUser) -> bool:
    return user.is_authenticated and user.is_superuser


def is_management(user: PlantationUser) -> bool:
    return user.is_authenticated and user.is_superuser or user.is_admin


def switch_all(user: PlantationUser, role: str):
    user.is_admin = False
    user.is_general = False
    user.is_staff = False
    user.is_delivery_man = False
    user.role = role

    if role == "G":
        user.is_general = True
    elif role == "S":
        user.is_staff = True
    elif role == "D":
        user.is_delivery_man = True
    elif role == "A":
        user.is_admin = True
    elif role == "N":
        user.is_active = False

    return user