from aiogram import types
from pydantic import BaseModel, Field
from datetime import datetime
from aiogram import types
from pydantic import ValidationError
from db.db import get_by_date
# from db.db import get_data_with_aggregation 

#schema
class MessageSchema(BaseModel):
    dt_from: datetime = Field(..., description="Дата и время старта агрегации в ISO формате")
    dt_upto: datetime = Field(..., description="Дата и время окончания агрегации в ISO формате")
    group_type: str = Field(..., description="Тип группировки данных")

#middleware
async def is_valid_message(message: types.Message) -> bool: 
    try:
        MessageSchema.parse_raw(message.text)
        return True
    except ValidationError:
        await message.answer("Неверный формат сообщения.")
        return False

#handler
async def register_message_handlers(dp, bot):
    @dp.message(is_valid_message)
    async def jsonMessage(message: types.Message):
        data = MessageSchema.parse_raw(message.text)
        dt_from = data.dt_from
        dt_upto = data.dt_upto
        group_type = data.group_type

        # result = await get_data_with_aggregation(dt_from, dt_upto, group_type)
        result = await get_by_date(dt_from, dt_upto, group_type)


        await message.answer(f"Результат агрегации: {result}")


