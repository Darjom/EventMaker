from typing import List
from pydantic import BaseModel
from modules.events.application.dtos.EventDTO import EventDTO


class EventsDTO(BaseModel):
    eventos: List[EventDTO]

    @classmethod
    def from_domain_list(cls, events: list):
        return cls(
            eventos=[EventDTO.fromDomain(event) for event in events]
        )
