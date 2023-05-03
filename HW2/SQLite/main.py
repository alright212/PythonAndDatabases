import sqlite3

connection = sqlite3.connect("diner1.db")
cursor = connection.cursor()
cursor.execute("""
CREATE TABLE PROVIDER (
    ID INTEGER PRIMARY KEY AUTOINCREMENT,
    ProviderName TEXT NOT NULL
)
""")

cursor.execute("""
CREATE TABLE CANTEEN (
    ID INTEGER PRIMARY KEY AUTOINCREMENT,
    ProviderID INTEGER,
    Name TEXT NOT NULL,
    Location TEXT NOT NULL,
    time_open TEXT NOT NULL,
    time_closed TEXT NOT NULL,
    FOREIGN KEY (ProviderID) REFERENCES PROVIDER (ID)
)
""")
providers = [
    (1, "Rahva Toit"),
    (2, "Baltic Restaurants Estonia AS"),
    (3, "TTÜ Sport OÜ"),
    (4, "Bitstop Kohvik OÜ")
]

cursor.executemany("""INSERT INTO PROVIDER (ID, ProviderName) VALUES (?, ?)""", providers)

canteens = [
    (1, 2, "Main Building Deli Cafe", "Ehitajate tee 5, U01 building", "9.00", "16.30"),
    (2, 2, "Main Building Daily Lunch Restaurant", "Ehitajate tee 5, U01 building", "9.00", "16.30"),
    (3, 1, "U06 Building Canteen", "U06 building", "9.00", "16.00"),
    (4, 2, "Natural Science Building Canteen", "Akadeemia tee 15, SCI building", "9.00", "16.00"),
    (5, 2, "ICT Building Canteen", "Raja 15/Mäepealse 1", "9.00", "16.00"),
    (6, 3, "Sports Building Canteen", "Männiliiva 7, S01 building", "11.00", "20.00")
]

cursor.executemany(
    """INSERT INTO CANTEEN (ID, ProviderID, Name, Location, time_open, time_closed) VALUES (?, ?, ?, ?, ?, ?)""",
    canteens)

cursor.execute("""
INSERT INTO CANTEEN (ID, ProviderID, Name, Location, time_open, time_closed) VALUES (7, 4, 'BitStop KOHVIK', 'IT College, Raja 4c', '9.30', '16.00')""")
cursor.execute("""
SELECT * FROM CANTEEN WHERE time_open <= '9.00' AND time_closed >= '16.20'
""")
result = cursor.fetchall()

for row in result:
    print(row)
cursor.execute("""
SELECT c.* FROM CANTEEN c JOIN PROVIDER p ON c.ProviderID = p.ID WHERE p.ProviderName = 'Baltic Restaurants Estonia AS'""")
result = cursor.fetchall()

for row in result:
    print(row)
connection.commit()
connection.close()
