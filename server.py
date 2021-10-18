from aiohttp import web
import pymongo
import json
import bson
from bson import json_util

def get_database():
    try:
      client = pymongo.MongoClient("mongodb+srv://tabs7:halexguillen@wachimingo.aorej.mongodb.net/microempresa?ssl=true&retrywrites=false&ssl_cert_reqs=CERT_NONE", connectTimeoutMS=30000, socketTimeoutMS=None, connect=False, maxPoolsize=1)
    #   print(client.microempresa)
    except pymongo.errors.ConnectionFailure as e:
      print(e)
    return client['microempresa']

# print (get_database())

def getBills():
    try:
      dbCon = get_database()
      bills = dbCon["bills"]
      records = bills.find()
      recordArray = []
      for item in records:
        # This does not give a very readable output
        recordArray.append(item)
        # print(item)
      return  json.loads(json_util.dumps(recordArray))
    except Exception as err:
     print("Error in query_db -> ", err)

# print (getBills())

def getPendingOrdersDB(query):
    dbCon = get_database()
    bills = dbCon["bills"]
    # detailedBills = dbCon["detailedBills"]
    records = bills.find(query)
    recordArray = []
    for item in records:
    #   detailedRecords = detailedBills.find({"bill":item.get('_id')})
    #   setattr(item, dishes, detailedRecords)
    #   print(item.get('_id'))
      recordArray.append(item)
    #   print(item)
    return  json.loads(json_util.dumps(recordArray))

# getBills()


async def index(request):
    return web.json_response({'message': 'success'})

async def getAllBills(request):
    data = getBills()
    return web.json_response(data)

async def getPendingOrders(request):
    print(request)
    query = { "status": "Pending" }
    records = getPendingOrdersDB(query)
    
    return web.json_response(records)

app = web.Application()
app.add_routes([web.get('/', index)])
app.add_routes([web.get('/getAllBills', getAllBills)])
app.add_routes([web.get('/api/v1/bills/orders', getPendingOrders)])
app.add_routes([web.post('/api/v1/bills/orders', getPendingOrders)])

if __name__ == '__main__':
    web.run_app(app)