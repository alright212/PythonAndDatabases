
See kood on näide Pythonis populaarse Object Relational Mapper (ORM) SQLAlchemy kasutamisest SQLite andmebaaside loomiseks ja päringute tegemiseks.
# Paigaldus

Koodi käivitamiseks peab teil olema installitud Python ja sqlalchemy libary. SQLAlchemy installimiseks käivitage:
```
pip install sqlalchemy
```
# Kasutus
Kood näitab, kuidas:

- Luua SQLite'i andmebaasi jaoks tabeleid
- Sisestada andmeid tabelitesse
- Andmeid pärida tabelitest filtrite abil

# Koodi Struktuur

### Libaryite Importimine ja Klasside Määratlemine
Kood impordib vajalikud libaryd ja määratleb klassid Provider ja Canteen, mis esindavad vastavalt Provideri ja Canteeni(söökla) tabeleid SQLite'i andmebaasis. Klassid pärivad klassist Base, mis luuakse SQLAlchemy funktsiooni declarative_base() abil.
```
from sqlalchemy import create_engine, Column, Integer, String, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker

Base = declarative_base()

class Provider(Base):
    ...

class Canteen(Base):
    ...
```
# SQLite Andmebaasi Loomine
SQLite'i andmebaas luuakse funktsiooni create_engine() abil, mis loob ühenduse andmebaasiga. Sel juhul luuakse uus SQLite'i fail nimega diner2_sqlalchemy.db. Tabelite loomiseks kutsutakse välja funktsioon Base.metadata.create_all().
```
engine = create_engine("sqlite:///diner2_sqlalchemy.db")
Base.metadata.create_all(engine)
```
### Andmete Sisestamine
Andmebaasiga suhtlemiseks luuakse sessioon. Andmed sisestatakse Provideri ja Canteeni tabelitesse, kasutades meetodeid add_all() ja commit().
```
Session = sessionmaker(bind=engine)
session = Session()

providers = [ ... ]
canteens = [ ... ]

session.add_all(providers)
session.add_all(canteens)
session.commit()
```
### Andmete Päring
Teostatakse kaks päringut:

- Päring sööklate kohta, mis on avatud 09.00-16.20
- Päring "Baltic Restaurants Estonia AS" teenindatavate sööklate kohta

Tabelitest andmete pärimiseks ja filtreerimiseks kasutatakse meetodeid query() ja filter().
```
canteens_9_to_1620 = session.query(Canteen).filter(Canteen.time_open <= "9.00", "16.20" <= Canteen.time_closed).all()
canteens_by_baltic = session.query(Canteen).join(Provider).filter(Provider.provider_name == "Baltic Restaurants Estonia AS").all()
```

Tulemused prinditakse Pythoni konsooli.

```
for canteen in canteens_9_to_1620:
    print(canteen.id, canteen.name, canteen.location, canteen.time_open, canteen.time_closed)

for canteen in canteens_by_baltic:
    print(canteen.id, canteen.name, canteen.location, canteen.time_open, canteen.time_closed)
```
### Sessiooni Sulgemine
Pärast vajalike toimingute tegemist suletakse sessioon meetodi close() abil.
```
session.close()
```
## Funktsioonid

- create_engine(): loob ühenduse SQLite'i andmebaasiga

- declarative_base(): loob SQLAlchemy ORM-klasside jaoks baasklassi

- sessionmaker(): konfigureerib andmebaasiga suhtlemiseks sessionfactory

- add_all(): lisab sessioonile list of recordsid

- commit(): Kinnitab sessioonil tehtud muudatused andmebaasi