from sqlalchemy import create_engine, MetaData, Table, Integer, String, \
    Column, ForeignKey,  Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

metadata = MetaData()
Base = declarative_base()


class Object(Base):
    __tablename__ = 'objects'
    metadata = metadata
    id = Column(Integer, primary_key=True, autoincrement=True)
    name_and_address = Column(String(), unique=True, nullable=False)
    number = Column(Integer(), nullable=False)
    description = Column(String())
    is_free_departure_prohibited = Column(Boolean(), nullable=False)
    is_free_jkh_passage_prohibited = Column(Boolean(), nullable=False)
    is_free_delivery_passage_prohibited = Column(Boolean(), nullable=False)
    is_free_collection_passage_prohibited = Column(Boolean(), nullable=False)
    is_free_garbtrucks_passage_prohibited = Column(Boolean(), nullable=False)
    is_free_post_passage_prohibited = Column(Boolean(), nullable=False)
    is_free_taxi_passage_prohibited = Column(Boolean(), nullable=False)
    barriers = relationship("Objects_Barriers", backref="object")


class Barrier(Base):
    __tablename__ = 'barriers'
    metadata = metadata
    id = Column(Integer, primary_key=True, autoincrement=True)
    number = Column(Integer())
    description = Column(String())
    gsm_number_vp = Column(String(50))
    sip_number_vp = Column(String(50))
    camera_url = Column(String())
    camdirect_url = Column(String())
    objects = relationship("Objects_Barriers", backref="barrier")


class Objects_Barriers(Base):
    __tablename__ = 'objects_barriers'
    metadata = metadata
    id = Column(Integer, primary_key=True, autoincrement=True)
    barrier_id = Column(ForeignKey("barriers.id"))
    object_id = Column(ForeignKey("objects.id"))


class User(Base):
    __tablename__ = 'users'
    metadata = metadata
    id = Column(Integer, primary_key=True, autoincrement=True)
    login = Column(String(), unique=True)
    password_sha256 = Column(String(100))
    role = Column(String(50))
