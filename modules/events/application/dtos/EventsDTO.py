from typing import List
from pydantic import BaseModel
from modules.events.application.dtos.EventDTO import EventDTO


class EventsDTO(BaseModel):
    eventos: List[EventDTO]


    def getEventos(self) -> List[EventDTO]:
        return self.eventos
