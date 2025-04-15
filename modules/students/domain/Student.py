from typing import Optional, List
from datetime import datetime

class Student:
    def __init__(
        self,
        id: Optional[int] = None,
        first_name: Optional[str] = None,
        last_name: str = "",
        email: str = "",
        password: str = "",
        active: bool = False,
        confirmed_at: Optional[datetime] = None,
        fs_uniquifier: Optional[str] = None,
        ci: str = "",
        expedito_ci: str = "",
        fecha_nacimiento: Optional[datetime] = None,
        phone_number: Optional[int] = None,
        school_id: Optional[int] = None,
        course: str = "",
        department: str = "",
        province: str = "",
        roles: Optional[List[str]] = None
    ):
        self.id = id
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.password = password
        self.active = active
        self.confirmed_at = confirmed_at
        self.fs_uniquifier = fs_uniquifier
        self.ci = ci
        self.expedito_ci = expedito_ci
        self.fecha_nacimiento = fecha_nacimiento
        self.phone_number = phone_number
        self.school_id = school_id
        self.course = course
        self.department = department
        self.province = province
        self.roles = roles or []


    def __str__(self):
        return f"Student: {self.first_name} {self.last_name} - {self.email}"