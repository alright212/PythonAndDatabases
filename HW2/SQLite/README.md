
See kood loob SQLite'i andmebaasi nimega diner1.db, et talletada teavet sööklate ja nende teenusepakkujate kohta. Andmebaasis on kaks tabelit: CANTEEN ja PROVIDER. Kood lisab nendesse tabelitesse andmed ja seejärel esitab tabelitele konkreetse teabe hankimiseks päringu.
# Impordi libary ja loo ühendus SQLite'i andmebaasiga

```
import sqlite3

connection = sqlite3.connect("diner1.db")
cursor = connection.cursor()
```
Impordime vajaliku sqlite3 libary ja loome ühenduse SQLite andmebaasiga diner1.db. SQL-käskude täitmiseks luuakse kursoriobjekt (cursor object).
# Loo tabelid: CANTEEN ja PROVIDER

```
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
```
CREATE TABLE SQL-i käske kasutatakse tabelite PROVIDER ja CANTEEN loomiseks andmebaasis. PROVIDER tabelis on veerud ID ja ProviderName, CANTEEN tabelis on veerud ID, ProviderID, Name, Location, time_open ja time_closed.
# Sisesta andmed tabelitesse: CANTEEN ja PROVIDER

```
cursor.executemany("""
INSERT INTO PROVIDER (ID, ProviderName) VALUES (?, ?)
""", providers)

cursor.executemany("""
INSERT INTO CANTEEN (ID, ProviderID, Name, Location, time_open, time_closed) VALUES (?, ?, ?, ?, ?, ?)
""", canteens)

cursor.execute("""
INSERT INTO CANTEEN (ID, ProviderID, Name, Location, time_open, time_closed) VALUES (7, 4, 'BitStop KOHVIK', 'IT College, Raja 4c', '9.30', '16.00')
""")
```
Käsku INSERT SQL kasutatakse andmete sisestamiseks tabelitesse PROVIDER ja CANTEEN. Provideri ja Canteeni andmed salvestatakse listi ning listi andmete sisestamiseks vastavatesse tabelitesse kasutatakse meetodit executemany(). IT Kolledži söökla sisestatakse eraldi execute() meetodiga.
# Tee päring andmebaasist

### 1. Retrieve'i sööklad, mis on avatud 09.00-16.20
```
cursor.execute("""
SELECT * FROM CANTEEN WHERE time_open <= '9.00' AND time_closed >= '16.20'
""")
result = cursor.fetchall()

for row in result:
    print(row)
```
SELECT SQL-käsku kasutatakse tabelist CANTEEN ridade retrive'imeks, kus time_open on väiksem või võrdne '9.00' ja time_closed on suurem või võrdne '16.20'. Toodud tulemused prinditakse Python konsooli.
### 2. Retrieve'i Baltic Restaurants Estonia AS poolt teenindatavad sööklad
```
cursor.execute("""
SELECT c.* FROM CANTEEN c JOIN PROVIDER p ON c.ProviderID = p.ID WHERE p.ProviderName = 'Baltic Restaurants Estonia AS'
""")
result = cursor.fetchall()

for row in result:
    print(row)
```
Käsku SELECT SQL kasutatakse tabelist CANTEEN ridade retrieve'miseks, mida teenindab Provider nimega "Baltic Restaurants Estonia AS". Toimingut JOIN kasutatakse tabelite CANTEEN ja PROVIDER kombineerimiseks veeru ProviderID alusel. Tulemused prinditakse Python konsooli.

# Commiti muudatused ja sulge andmebaasiühendus

```
connection.commit()
connection.close()
```
Skripti lõpuks kinnitatakse andmebaasis tehtud muudatused ja ühendus andmebaasiga suletakse.

# Kokkuvõte

Kood teeb järgmist:

- Impordib vajaliku sqlite3 libary ja loob ühenduse SQLite'i andmebaasiga.

- Loob andmebaasis tabelid PROVIDER ja CANTEEN.

- Sisestab listi abil andmed tabelitesse PROVIDER ja CANTEEN.

- Pärib 09.00-16.20 avatud sööklate otsimiseks tabelist CANTEEN.

- Teeb päringu CANTEEN ja PROVIDER tabelitest, et leida "Baltic Restaurants Estonia AS" poolt teenindatavaid sööklaid.

- Sooritab muudatused andmebaasis ja sulgeb ühenduse.