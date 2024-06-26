import asyncio
from motor.motor_asyncio import AsyncIOMotorClient
from pymongo.server_api import ServerApi
import logging
from datetime import datetime, timedelta, timezone
import json
from utils.config import MONGODB_URI

logger = logging.getLogger(__name__)

client = AsyncIOMotorClient(MONGODB_URI)
db = client['rlt_test']
collection = db['salaries']

async def ping_server():
    try:
        await client.admin.command('ping')
        logger.info("Pinged your deployment. You successfully connected to MongoDB!")
        return True
    except Exception as e:
        logger.error(f"An error occurred: {e}")
        return False   

async def get_by_date(dt_from: datetime, dt_upto: datetime, group_type: str):
    labels = []
    dataset = []

    while dt_from < dt_upto:
        labels.append(dt_from.strftime("%Y-%m-%dT%H:%M:%S"))

        if group_type == "month":
            next_period_start = dt_from.replace(month=(dt_from.month % 12) + 1, year=dt_from.year + dt_from.month // 12, day=1)
        elif group_type == "day":
            next_period_start = dt_from + timedelta(days=1)
        elif group_type == "hour":
            next_period_start = dt_from + timedelta(hours=1)

        aggregation = await collection.aggregate([
            {"$match": {"dt": {"$gte": dt_from, "$lt": next_period_start}}},
            {"$group": {"_id": None, "total": {"$sum": "$value"}}}
        ]).to_list(None)

        dataset.append(aggregation[0]['total'] if aggregation else 0)
        dt_from = next_period_start

    if group_type == "hour" and labels[-1] != dt_upto.strftime("%Y-%m-%dT%H:%M:%S"):
        labels.append(dt_upto.strftime("%Y-%m-%dT%H:%M:%S"))
        dataset.append(0)

    if group_type in ["day", "month"] and labels[-1] == dt_upto.strftime("%Y-%m-%dT%H:%M:%S"):
        labels.pop()
        dataset.pop()

    return json.dumps({"dataset": dataset, "labels": labels})
