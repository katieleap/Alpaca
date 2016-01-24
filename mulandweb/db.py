# coding: utf-8

from sqlalchemy import create_engine, Table, Column, MetaData
from sqlalchemy import Integer, String, Float, ForeignKey, Sequence
from sqlalchemy import ForeignKeyConstraint
from sqlalchemy.dialects.postgresql import ARRAY
from geoalchemy2 import Geometry
from . import config

engine = create_engine(config.db_url)
meta = MetaData()

models = Table('models', meta,
    Column('id', Integer, Sequence('models_id_seq'), primary_key=True),
    Column('name', String),
    Column('zones_header', ARRAY(String, zero_indexes=True)),
    Column('agents_header', ARRAY(String, zero_indexes=True)),
    Column('agents_zones_header', ARRAY(String, zero_indexes=True)),
)

real_estate_types = Table('real_estate_types', meta,
    Column('id', Integer, primary_key=True),
    Column('description', String),
)

markets = Table('markets', meta,
    Column('id', Integer, primary_key=True),
    Column('description', String),
)

rent_adjustments = Table('rent_adjustments', meta,
    Column('types_id', Integer, ForeignKey('real_estate_types.id'), primary_key=True),
    Column('zones_id', Integer, primary_key=True),
    Column('models_id', Integer, ForeignKey('models.id'), primary_key=True),
    Column('adjustment', Float),
    ForeignKeyConstraint(['zones_id', 'models_id'], ['zones.id', 'zones.models_id']),
)

supply = Table('supply', meta,
    Column('types_id', Integer, ForeignKey('real_estate_types.id'), primary_key=True),
    Column('zones_id', Integer, primary_key=True),
    Column('models_id', Integer, ForeignKey('models.id'), primary_key=True),
    Column('nrest', Float),
    ForeignKeyConstraint(['zones_id', 'models_id'], ['zones.id', 'zones.models_id']),
)

real_estates_zones = Table('real_estates_zones', meta,
    Column('types_id', Integer, ForeignKey('real_estate_types.id'), primary_key=True),
    Column('zones_id', Integer, primary_key=True),
    Column('markets_id', Integer, ForeignKey('markets.id'), primary_key=True),
    Column('models_id', Integer, ForeignKey('models.id'), primary_key=True),
    Column('header', ARRAY(String, zero_indexes=True)),
    Column('data', ARRAY(Float, zero_indexes=True)),
    ForeignKeyConstraint(['zones_id', 'models_id'], ['zones.id', 'zones.models_id']),
)

agents = Table('agents', meta,
    Column('id', Integer, primary_key=True),
    Column('models_id', Integer, ForeignKey('models.id'), primary_key=True),
    Column('markets_id', Integer, ForeignKey('markets.id')),
    Column('aggra_id', Integer),
    Column('upperbb', Float),
    Column('data', ARRAY(Float, zero_indexes=True)),
)

zones = Table('zones', meta,
    Column('id', Integer, primary_key=True),
    Column('models_id', Integer, ForeignKey('models.id'), primary_key=True),
    Column('area', Geometry('POLYGON', srid=900913, spatial_index=True)),
    Column('data', ARRAY(Float, zero_indexes=True)),
)

demand = Table('demand', meta,
    Column('agents_id', Integer, primary_key=True),
    Column('models_id', Integer, ForeignKey('models.id'), primary_key=True),
    Column('demand', Float),
    ForeignKeyConstraint(['agents_id', 'models_id'], ['agents.id', 'agents.models_id']),
)

subsidies = Table('subsidies', meta,
    Column('agents_id', Integer, primary_key=True),
    Column('types_id', Integer, ForeignKey('real_estate_types.id'), primary_key=True),
    Column('zones_id', Integer, primary_key=True),
    Column('models_id', Integer, ForeignKey('models.id'), primary_key=True),
    Column('subsidies', Float),
    ForeignKeyConstraint(['zones_id', 'models_id'], ['zones.id', 'zones.models_id']),
    ForeignKeyConstraint(['agents_id', 'models_id'], ['agents.id', 'agents.models_id']),
)

demand_exogenous_cutoff = Table('demand_exogenous_cutoff', meta,
    Column('agents_id', Integer, primary_key=True),
    Column('types_id', Integer, ForeignKey('real_estate_types.id'), primary_key=True),
    Column('zones_id', Integer, primary_key=True),
    Column('models_id', Integer, ForeignKey('models.id'), primary_key=True),
    Column('dcutoff', Float),
    ForeignKeyConstraint(['zones_id', 'models_id'], ['zones.id', 'zones.models_id']),
    ForeignKeyConstraint(['agents_id', 'models_id'], ['agents.id', 'agents.models_id']),
)

agents_zones = Table('agents_zones', meta,
    Column('agents_id', Integer, primary_key=True),
    Column('zones_id', Integer, primary_key=True),
    Column('models_id', Integer, ForeignKey('models.id'), primary_key=True),
    Column('acc', Float),
    Column('att', Float),
    Column('data', ARRAY(Float, zero_indexes=True)),
    ForeignKeyConstraint(['zones_id', 'models_id'], ['zones.id', 'zones.models_id']),
    ForeignKeyConstraint(['agents_id', 'models_id'], ['agents.id', 'agents.models_id']),
)

bids_adjustments = Table('bids_adjustments', meta,
    Column('agents_id', Integer, primary_key=True),
    Column('types_id', Integer, ForeignKey('real_estate_types.id'), primary_key=True),
    Column('zones_id', Integer, primary_key=True),
    Column('models_id', Integer, ForeignKey('models.id'), primary_key=True),
    Column('bidadj', Float),
    ForeignKeyConstraint(['zones_id', 'models_id'], ['zones.id', 'zones.models_id']),
    ForeignKeyConstraint(['agents_id', 'models_id'], ['agents.id', 'agents.models_id']),
)

#meta.create_all(engine)
