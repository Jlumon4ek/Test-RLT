import asyncio
from motor.motor_asyncio import AsyncIOMotorClient
from pymongo.server_api import ServerApi
import logging
from datetime import datetime, timedelta, timezone
import json

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

    while start < end:
        labels.append(start.strftime("%Y-%m-%dT%H:%M:%S"))

        if group_type == "month":
            if start.month == 12:
                next_period_start = start.replace(year=start.year + 1, month=1, day=1)
            else:
                next_period_start = start.replace(month=start.month + 1, day=1)
        elif group_type == "day":
            next_period_start = start + timedelta(days=1)
        elif group_type == "hour":
            next_period_start = start + timedelta(hours=1)

        aggregation = await collection.aggregate([
            {"$match": {
                "dt": {"$gte": start, "$lt": next_period_start}
            }},
            {"$group": {
                "_id": None,
                "total": {"$sum": "$value"}
            }}
        ]).to_list(None)

        if aggregation:
            dataset.append(aggregation[0]['total'])
        else:
            dataset.append(0)  # Append 0 if no data is found

        start = next_period_start

    # For 'hour' group type, include the last label without adding data
    if group_type == "hour" and labels[-1] != end.strftime("%Y-%m-%dT%H:%M:%S"):
        labels.append(end.strftime("%Y-%m-%dT%H:%M:%S"))
        dataset.append(0)

    # For 'day' and 'month' group types, ensure the last period is not added if it goes beyond the end
    if group_type in ["day", "month"] and labels[-1] == end.strftime("%Y-%m-%dT%H:%M:%S"):
        labels.pop()
        dataset.pop()

    # Convert the result to JSON format with double quotes
    result = {
        "dataset": dataset,
        "labels": labels
    }

    return json.dumps(result)




