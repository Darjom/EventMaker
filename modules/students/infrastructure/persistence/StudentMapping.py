from modules.students.domain.Student import Student
from modules.user.infrastructure.persistence.UserMapping import UserMapping
from shared.extensions import db


class StudentMapping(UserMapping):


    phone_number = db.Column(db.Integer, nullable=True)
    course = db.Column(db.String(50), nullable=True)
    department = db.Column(db.String(50), nullable=True)
    province = db.Column(db.String(50), nullable=True)

    __mapper_args__ = {
        'polymorphic_identity': 'student',
    }

    def to_domain(self):
        return Student(
            id=self.id,
            first_name=self.first_name,
            last_name=self.last_name,
            email=self.email,
            password=self.password,
            active=self.active,
            confirmed_at=self.confirmed_at,
            fs_uniquifier=self.fs_uniquifier,
            ci=self.ci,
            expedito_ci=self.expedito_ci,
            fecha_nacimiento=self.fecha_nacimiento,
            phone_number=self.phone_number,
            school_id=self.school_id,
            course=self.course,
            department=self.department,
            province=self.province,
            roles=[role.name for role in self.roles] if self.roles else []
        )

    @classmethod
    def from_domain(cls, student_domain):
        return cls(
            id=student_domain.id,
            first_name=student_domain.first_name,
            last_name=student_domain.last_name,
            email=student_domain.email,
            password=student_domain.password,
            active=student_domain.active,
            confirmed_at=student_domain.confirmed_at,
            fs_uniquifier=student_domain.fs_uniquifier,
            ci=student_domain.ci,
            expedito_ci=student_domain.expedito_ci,
            fecha_nacimiento=student_domain.fecha_nacimiento,
            phone_number=student_domain.phone_number,
            school_id=student_domain.school_id,
            course=student_domain.course,
            department=student_domain.department,
            province=student_domain.province
        )