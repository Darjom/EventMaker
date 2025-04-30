from typing import List, Optional
from ..domain.GroupRepository import GroupRepository
from ..domain.Group import Group
from .persistence.GroupMapping import GroupMapping
from shared.extensions import db


class PostgresGroupRepository(GroupRepository):
    def save(self, group: Group) -> Group:
        group_mapping = GroupMapping.from_domain(group)
        db.session.add(group_mapping)
        db.session.commit()
        return group_mapping.to_domain()

    def find_by_id(self, group_id: int) -> Optional[Group]:
        group_mapping = GroupMapping.query.get(group_id)
        return group_mapping.to_domain() if group_mapping else None

    def find_by_area(self, area_id: int) -> List[Group]:
        groups = GroupMapping.query.filter_by(id_area=area_id).all()
        return [g.to_domain() for g in groups]

    def find_by_delegation(self, delegation_id: int) -> List[Group]:
        groups = GroupMapping.query.filter_by(id_delegacion=delegation_id).all()
        return [g.to_domain() for g in groups]

    def assign_tutor_to_group(self, group_id: int, tutor_id: int) -> None:
        """Assigns a tutor to an existing group"""
        from .persistence.GroupMapping import GroupMapping
        from modules.user.infrastructure.persistence.UserMapping import UserMapping

        group = GroupMapping.query.get(group_id)
        tutor = UserMapping.query.get(tutor_id)

        if not group or not tutor:
            raise ValueError("Group or Tutor not found")

        if tutor not in group.tutores:
            group.tutores.append(tutor)
            db.session.commit()