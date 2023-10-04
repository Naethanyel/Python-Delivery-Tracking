
class HashTable:
    def __init__(self, initial_capacity=20):
        self.list = []
        for i in range(initial_capacity):
            self.list.append([])

    # insert item into hash table
    def insert(self, key, item):
        bucket = hash(key) % len(self.list)
        bucket_list = self.list[bucket]

        # update key if it is already in the bucket
        for key_value in bucket_list:
            if key_value[0] == key:
                key_value[1] = item
                return True

        # if not, insert the item to the end of the bucket list
        key_value = [key, item]
        bucket_list.append(key_value)
        return True

    # Lookup items in hash table
    def lookup(self, key):
        bucket = hash(key) % len(self.list)
        bucket_list = self.list[bucket]
        for key_value in bucket_list:
            if key == key_value[0]:
                return key_value[1]
