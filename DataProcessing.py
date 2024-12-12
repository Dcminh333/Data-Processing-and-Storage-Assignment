class InMemoryKeyValueDatabase:
    def __init__(self):
        self.data = {}
        self.transaction_data = None

    def begin_transaction(self):
        if self.transaction_data is not None:
            raise Exception("Transaction already in progress")
        self.transaction_data = {}

    def put(self, key, value):
        if self.transaction_data is None:
            raise Exception("No transaction in progress")
        self.transaction_data[key] = value

    def get(self, key):
        if self.transaction_data is not None and key in self.transaction_data:
            return self.transaction_data[key]
        return self.data.get(key)

    def commit(self):
        if self.transaction_data is None:
            raise Exception("No transaction in progress")
        self.data.update(self.transaction_data)
        self.transaction_data = None

    def rollback(self):
        if self.transaction_data is None:
            raise Exception("No transaction in progress")
        self.transaction_data = None

# Example usage:
db = InMemoryKeyValueDatabase()

# should return None, because A doesn’t exist in the DB yet
print(db.get("A"))  # Output: None

# should throw an error because a transaction is not in progress
try:
    db.put("A", 5)
except Exception as e:
    print(e)  # Output: No transaction in progress

# starts a new transaction
db.begin_transaction()

# set’s value of A to 5, but its not committed yet
db.put("A", 5)

# should return None, because updates to A are not committed yet
print(db.get("A"))  # Output: None

# update A’s value to 6 within the transaction
db.put("A", 6)

# commits the open transaction
db.commit()

# should return 6, that was the last value of A to be committed
print(db.get("A"))  # Output: 6

# throws an error, because there is no open transaction
try:
    db.commit()
except Exception as e:
    print(e)  # Output: No transaction in progress

# throws an error because there is no ongoing transaction
try:
    db.rollback()
except Exception as e:
    print(e)  # Output: No transaction in progress

# should return None because B does not exist in the database
print(db.get("B"))  # Output: None

# starts a new transaction
db.begin_transaction()

# Set key B’s value to 10 within the transaction
db.put("B", 10)

# Rollback the transaction - revert any changes made to B
db.rollback()

# Should return None because changes to B were rolled back
print(db.get("B"))  # Output: None