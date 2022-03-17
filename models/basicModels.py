import sqlalchemy

metadata = sqlalchemy.MetaData()


objects_table = sqlalchemy.Table(
    "objects",
    metadata,
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True),
    sqlalchemy.Column("name_and_address", sqlalchemy.String(100), unique=True, index=True),
    sqlalchemy.Column("number", sqlalchemy.Integer()),
    sqlalchemy.Column("description", sqlalchemy.String()),
    sqlalchemy.Column("is_free_departure_prohibited", sqlalchemy.Boolean()),
    sqlalchemy.Column("is_free_jkh_passage_prohibited", sqlalchemy.Boolean()),
    sqlalchemy.Column("is_free_delivery_passage_prohibited", sqlalchemy.Boolean()),
    sqlalchemy.Column("is_free_collection_passage_prohibited", sqlalchemy.Boolean()),
    sqlalchemy.Column("is_free_garbtrucks_passage_prohibited", sqlalchemy.Boolean()),
    sqlalchemy.Column("is_free_post_passage_prohibited", sqlalchemy.Boolean()),
    sqlalchemy.Column("is_free_taxi_passage_prohibited", sqlalchemy.Boolean()),
)


barriers_table = sqlalchemy.Table(
    "barriers",
    metadata,
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True),
    sqlalchemy.Column("number", sqlalchemy.Integer()),
    sqlalchemy.Column("description", sqlalchemy.String()),
    sqlalchemy.Column("gsm_number_vp", sqlalchemy.String(50)),
    sqlalchemy.Column("sip_number_vp", sqlalchemy.String(50)),
    sqlalchemy.Column("camera_url", sqlalchemy.String(200)),
    sqlalchemy.Column("camdirect_url", sqlalchemy.String(200)),
)


objects_barriers_links_table = sqlalchemy.Table(
    "objects_barriers_links",
    metadata,
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True),
    sqlalchemy.Column("barrier_id", sqlalchemy.ForeignKey("barriers.id")),
    sqlalchemy.Column("object_id", sqlalchemy.ForeignKey("objects.id")),
)