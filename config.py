import pymysql

TOKEN = '6450552357:AAHs1wRghLDP5E5sjjYB7ndeXlIdPMq5dlw'

conn = pymysql.connect(
    host='db4free.net',
    user='nazarrudenok',
    password='nazarkoqweA228rty',
    database='auctiondb'
)

with conn.cursor() as c:
    c.execute("SELECT * FROM application")
    data = c.fetchall()
    print(data)