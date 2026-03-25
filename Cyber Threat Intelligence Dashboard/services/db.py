from pymongo import MongoClient
import os
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

class DBManager:
    def __init__(self):
        mongo_uri = os.getenv("MONGO_URI", "mongodb://localhost:27017/cti_dashboard")
        self.client = MongoClient(mongo_uri)
        self.db = self.client.get_database()
        self.lookups = self.db.lookups

    def save_lookup(self, target, data, target_type):
        lookup_doc = {
            "target": target,
            "target_type": target_type,
            "timestamp": datetime.now(),
            "results": data,
            "tags": []
        }
        try:
            return self.lookups.insert_one(lookup_doc)
        except Exception as e:
            print(f"Database Error: {e}")
            return None

    def get_all_lookups(self):
        try:
            return list(self.lookups.find().sort("timestamp", -1))
        except Exception as e:
            print(f"Database Error: {e}")
            return []

    def add_tag(self, lookup_id, tag):
        from bson.objectid import ObjectId
        try:
            return self.lookups.update_one(
                {"_id": ObjectId(lookup_id)},
                {"$addToSet": {"tags": tag}}
            )
        except Exception as e:
            print(f"Database Error: {e}")
            return None

    def get_metrics(self):
        try:
            # Calculate some basic metrics for visualizations
            pipeline = [
                {"$group": {
                    "_id": "$target_type",
                    "count": {"$sum": 1}
                }}
            ]
            type_counts = list(self.lookups.aggregate(pipeline))
            return {
                "type_counts": {item["_id"]: item["count"] for item in type_counts}
            }
        except Exception as e:
            print(f"Database Error: {e}")
            return {"type_counts": {}}
