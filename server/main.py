import requests
import pymongo

from fastapi import FastAPI
from typing import Union
from datetime import datetime

'''
Python: FastAPI , MongoDB , Line pay , ECpay
'''

app = FastAPI()

# EC Pay


# Line Pay API


# MongoDB


# Function
def get_size(bytes, suffix="B"):
    """
    Scale bytes to its proper format
    e.g:
        1253656 => '1.20MB'
        1253656678 => '1.17GB'
    """
    factor = 1024
    for unit in ["", "K", "M", "G", "T", "P"]:
        if bytes < factor:
            return f"{bytes:.2f}{unit}{suffix}"
        bytes /= factor

# API 

'''
+--------+
|  RULE  |
+--------+

# file
- root // 管理者端
  +-- server // 伺服器狀態 
    +-- status // 伺服器狀態 ✅
  +-- dashboard // 管理者後台
    +-- login // 登入 ✅
    +-- newresturant // 新增餐廳 ✅
    +-- changepassword // 修改密碼
    +-- newadmin // 新增管理者
    +-- deleteadmin // 刪除管理者
    +-- delresturant // 刪除餐廳
    +-- usernumber // 會員人數
    +-- resturantnumber // 餐廳數量
    +-- order // 訂單
        +-- ordernumber // 訂單數量
    +-- money // 營業額
        +-- money // 營業額
- client // 客戶端
    +-- register // 註冊
    +-- login // 登入
        +-- forgetpasswd //忘記密碼
    +-- favorite // 收藏
    +-- resturant // 餐廳
        +-- menu // 餐廳菜單
        +-- list // 餐廳列表
        +-- detail // 餐廳詳細資料
    +-- order // 訂單
        +-- list // 訂單列表
        +-- detail // 訂單詳細資料
    +-- payment // 付款
        +-- linepay // Line Pay
        +-- ecpay // EC Pay
        +-- binancepay // Binance Pay
    +-- profile // 個人資料
        +-- edit // 編輯個人資料
        +-- changepassword // 修改密碼
        +-- delete // 刪除帳號
    +-- history // 歷史紀錄
        +-- order // 訂單紀錄
            +-- reoder // 重新訂購
            +-- review // 評論
        +-- payment // 付款紀錄
    +-- paymentmethod // 付款方式
        +-- add // 新增付款方式
        +-- delete // 刪除付款方式
- resturant // 餐廳端
    +-- login // 登入
        +-- forgetpasswd //忘記密碼
    +-- menu // 菜單
        +-- add // 新增菜單
        +-- edit // 編輯菜單
        +-- delete // 刪除菜單
    +-- order // 訂單
        +-- list // 訂單列表
        +-- detail // 訂單詳細資料
    +-- resturantprofile // 餐廳資料
- test // 測試端

'''

@app.get("/test")
async def read_root():
    return {"Hello": "World"}

@app.get("/test/{item_id}")
async def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}

@app.get("/root/server/status")
async def server_status():
    import psutil
    import platform
    # OS
    uname = platform.uname()
    System = uname.system
    Release = uname.release
    Version = uname.version
    Machine = uname.machine
    Processor = uname.processor
    # CPU
    cpu_usage = psutil.cpu_percent()
    cpu_type = platform.processor()
    usage_list = [(i,percent) for i,percent in enumerate(psutil.cpu_percent(percpu=True,interval=1))]
    # Memory
    svmem = psutil.virtual_memory()
    total_memory = get_size(svmem.total)
    used_memory = get_size(svmem.used)
    memory_percent = svmem.percent
    # Disk
    disk = psutil.disk_usage('/')
    used_disk = get_size(disk.used)
    total_disk = get_size(disk.total)
    # Platform
    platform_info = platform.system()
    # Time
    time = datetime.now()


    return {
        "cpu_type": cpu_type,
        "cpu_usage": cpu_usage,
        "usage_list": usage_list,
        "total_memory": total_memory,
        "used_memory": used_memory,
        "memory_percent": memory_percent,
        "total_disk": total_disk,
        "used_disk": used_disk,
        "platform": platform_info,
        "time": time,
        "System": System,
        "Release": Release,
        "Version": Version,
        "Machine": Machine,
        "Processor": Processor,
    }

@app.post("/root/dashboard/login")
async def dashboard_login(username: str , password: str ):
    mymogo = pymongo.MongoClient("mongodb://localhost:27017/")
    mydb = mymogo["adminaccount"]
    mycol = mydb["account"]
    myquery = { "username": username, "password": password }
    mydoc = mycol.find(myquery)
    if mydoc.count() == 0:
        return {"status": "admin not found!"}
    else:
        return {"status": "success"}

@app.post("/root/dashboard/newresturant")
async def new_resturant(resturantname: str , owner : str , passwd : str):
    mymogo = pymongo.MongoClient("mongodb://localhost:27017/")
    mydb = mymogo["resturantaccount"]
    mycol = mydb["account"]
    mydict = { "resturantname": resturantname, "owner": owner, "passwd": passwd }
    mycol.insert_one(mydict)
    return mycol.find_one(mydict)

@app.post("/root/dashboard/changepassword")
async def changepassword(username: str,new_passwd:str):
    mymogo = pymongo.MongoClient("mongodb://localhost:27017/")
    mydb = mymogo["adminaccount"]
    mycol = mydb["account"]
    myquery = { "username": username }
    newvalues = { "$set": { "password": new_passwd } }
    mycol.update_one(myquery, newvalues)
    return {"status": "success"}
