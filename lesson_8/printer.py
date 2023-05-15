from pymongo import MongoClient
from pprint import pprint

client = MongoClient("localhost", 27017)
db = client.insta

print("Подписчики пользователя vancityreynolds")
vancityreynolds_followers = db.followers.find({"linked_username": "vancityreynolds"})
for follower in vancityreynolds_followers:
    pprint(f"{follower.get('username')} |:| {follower.get('full_name')}")


print("\n\nПодписки пользователя vancityreynolds")
vancityreynolds_followings = db.followings.find({"linked_username": "vancityreynolds"})
for following in vancityreynolds_followings:
    pprint(f"{following.get('username')} |:| {following.get('full_name')}")


print("\n\nПодписчики пользователя ryangoslinguk")
ryangoslinguk_followers = db.followers.find({"linked_username": "ryangoslinguk"})
for follower in ryangoslinguk_followers:
    pprint(f"{follower.get('username')} |:| {follower.get('full_name')}")


print("\n\nПодписки пользователя ryangoslinguk")
ryangoslinguk_followings = db.followings.find({"linked_username": "ryangoslinguk"})
for following in ryangoslinguk_followings:
    pprint(f"{following.get('username')} |:| {following.get('full_name')}")
