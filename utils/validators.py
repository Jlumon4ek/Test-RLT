from pydantic import BaseModel, Field, ValidationError
from datetime import datetime

class MessageSchema(BaseModel):
    dt_from: datetime = Field(..., description="Дата и время старта агрегации в ISO формате")
    dt_upto: datetime = Field(..., description="Дата и время окончания агрегации в ISO формате")
    group_type: str = Field(..., description="Тип группировки данных")

async def is_valid_message(message_text: str) -> bool:
    try:
        MessageSchema.parse_raw(message_text)
        return True
    except ValidationError:
        return False

def parse_message(message_text: str) -> MessageSchema:
    return MessageSchema.parse_raw(message_text)
