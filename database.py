import pymongo

client = pymongo.MongoClient("mongodb://localhost:27017/")

db = client["HARSH"]
collection = db["Tracker"]

def insert_data(period,incomes,expenses,comment):
    record = {"key": period, "incomes": incomes, "expenses" : expenses, "comment": comment}
    return collection.insert_one(record)

def fetch_all_records():
    """returns a dictionary of all periods"""
    return collection.find()

def get_period(period):
    """returns the records of the given period"""
    return collection.find_one({"key": period})

# def update():
#     """updates record"""
#     data = get_period(period)

#     # Specify the updates you want to apply
#     updates = {"$set": {"comment": "Updated comment"}}

#     return collection.update_one(data, updates)

def delete(period):
    """deletes record"""
    data = get_period(period)
    return collection.delete_one(data)