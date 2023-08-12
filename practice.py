import json

dictStr = str({"1": 10, "2": 50, "12": 100}).replace("\'", "\"")
dict = json.loads(dictStr)

productId = 2

if (str(productId) in dict.keys()):
    print("Yes")
else:
    print('no')


print(json.loads(dict)["1"])
