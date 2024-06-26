import asyncio
from motor.motor_asyncio import AsyncIOMotorClient
from pymongo.server_api import ServerApi
import logging
from datetime import datetime, timedelta, timezone

logger = logging.getLogger(__name__)

async def ping_server():
    uri = "mongodb://localhost:27017/"
    client = AsyncIOMotorClient(uri)
    try:
        await client.admin.command('ping')
        logger.info("Pinged your deployment. You successfully connected to MongoDB!")
        return True
    except Exception as e:
        logger.error(f"An error occurred: {e}")
        return False   
      

async def get_by_date(dt_from, dt_upto, group_type: str):
    uri = "mongodb://localhost:27017/"
    client = AsyncIOMotorClient(uri)
    db = client['rlt_test']
    collection = db['salaries']

    if isinstance(dt_from, str):
        start = datetime.strptime(dt_from, "%Y-%m-%dT%H:%M:%S").replace(tzinfo=timezone.utc)
    else:
        start = dt_from

    if isinstance(dt_upto, str):
        end = datetime.strptime(dt_upto, "%Y-%m-%dT%H:%M:%S").replace(tzinfo=timezone.utc)
    else:
        end = dt_upto

    labels = []
    dataset = []

    while start <= end:
        labels.append(start.strftime("%Y-%m-%dT%H:%M:%S"))

        if group_type == "month":
            period_end = (start.replace(day=1) + timedelta(days=32)).replace(day=1) - timedelta(seconds=1)
        elif group_type == "day":
            period_end = start + timedelta(days=1) - timedelta(seconds=1)
        elif group_type == "hour":
            period_end = start + timedelta(hours=1) - timedelta(seconds=1)

        aggregation = await collection.aggregate([
            {"$match": {
                "dt": {"$gte": start, "$lt": period_end + timedelta(seconds=1)}
            }},
            {"$group": {
                "_id": None,
                "total": {"$sum": "$value"}
            }}
        ]).to_list(None)

        if aggregation:
            dataset.append(aggregation[0]['total'])
        else:
            dataset.append(0)  

        if group_type == "month":
            start = (start.replace(day=1) + timedelta(days=32)).replace(day=1)
        else:
            start += timedelta(days=1) if group_type == "day" else timedelta(hours=1)

    return {"dataset": dataset, "labels": labels}


