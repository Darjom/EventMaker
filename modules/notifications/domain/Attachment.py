from dataclasses import dataclass

@dataclass
class Attachment:
    """Value Object para representar archivos adjuntos en memoria"""
    filename: str
    content: bytes
    mime_type: str

    @classmethod
    def from_memory(cls, filename: str, content: bytes, mime_type: str):
        """Factory method para crear adjuntos directamente en memoria"""
        return cls(
            filename=filename,
            content=content,
            mime_type=mime_type or "application/octet-stream"
        )
