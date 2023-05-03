from sqlalchemy import create_engine, Column, Integer, String, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker

Base = declarative_base()


class Provider(Base):
    __tablename__ = "provider"
    id = Column(Integer, primary_key=True)
    provider_name = Column(String, nullable=False)

    canteens = relationship("Canteen", back_populates="provider")


class Canteen(Base):
    __tablename__ = "canteen"
    id = Column(Integer, primary_key=True)
    provider_id = Column(Integer, ForeignKey("provider.id"))
    name = Column(String, nullable=False)
    location = Column(String, nullable=False)
    time_open = Column(String, nullable=False)
    time_closed = Column(String, nullable=False)

    provider = relationship("Provider", back_populates="canteens")


engine = create_engine("sqlite:///diner2_sqlalchemy.db")
Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)
session = Session()

providers = [
    Provider(id=1, provider_name="Rahva Toit"),
    Provider(id=2, provider_name="Baltic Restaurants Estonia AS"),
    Provider(id=3, provider_name="TTÜ Sport OÜ"),
    Provider(id=4, provider_name="Bitstop Kohvik OÜ")
]

canteens = [
    Canteen(provider_id=2, name="Main Building Deli Cafe", location="Ehitajate tee 5, U01 building", time_open="9.00",
            time_closed="16.30"),
    Canteen(provider_id=2, name="Main Building Daily Lunch Restaurant", location="Ehitajate tee 5, U01 building",
            time_open="9.00", time_closed="16.30"),
    Canteen(provider_id=1, name="U06 Building Canteen", location="U06 building", time_open="9.00", time_closed="16.00"),
    Canteen(provider_id=2, name="Natural Science Building Canteen", location="Akadeemia tee 15, SCI building",
            time_open="9.00", time_closed="16.00"),
    Canteen(provider_id=2, name="ICT Building Canteen", location="Raja 15/Mäepealse 1", time_open="9.00",
            time_closed="16.00"),
    Canteen(provider_id=3, name="Sports Building Canteen", location="Männiliiva 7, S01 building", time_open="11.00",
            time_closed="20.00"),
    Canteen(provider_id=4, name="BitStop KOHVIK", location="IT College, Raja 4c", time_open="9.30", time_closed="16.00")
]

session.add_all(providers)
session.add_all(canteens)
session.commit()

canteens_9_to_1620 = session.query(Canteen).filter(Canteen.time_open <= "9.00", "16.20" <= Canteen.time_closed).all()
for canteen in canteens_9_to_1620:
    print(canteen.id, canteen.name, canteen.location, canteen.time_open, canteen.time_closed)

canteens_by_baltic = session.query(Canteen).join(Provider).filter(
    Provider.provider_name == "Baltic Restaurants Estonia AS").all()

for canteen in canteens_by_baltic:
    print(canteen.id, canteen.name, canteen.location, canteen.time_open, canteen.time_closed)

session.close()
