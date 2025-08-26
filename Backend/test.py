from pymongo import MongoClient
import socket
import pymongo.errors

# Test host resolution
try:
    print(f"Resolving 127.0.0.1: {socket.gethostbyname('127.0.0.1')}")
except Exception as e:
    print(f"Resolution failed: {str(e)}")

# Test admin user with SCRAM-SHA-1
ADMIN_URI = "mongodb://admin:securepassword@localhost:27017"
print(f"Testing ADMIN_URI: {ADMIN_URI}")

try:
    client = MongoClient(ADMIN_URI, serverSelectionTimeoutMS=5000, connectTimeoutMS=5000)
    client.admin.command("ping")
    print("MongoDB connection successful with admin user (SCRAM-SHA-1)")
    # Test operation
    db = client["bh_assurance"]
    collection = db["test_collection"]
    collection.insert_one({"test": "data"})
    print("Insert operation successful")
    result = collection.find_one({"test": "data"})
    print(f"Find operation successful: {result}")
    client.close()

except Exception as e:
    print(f"Unexpected error: {str(e)}")