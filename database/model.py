from sqlalchemy import MetaData, Table, Column, ForeignKey, Integer, String,Date


metadata = MetaData()

# main table, corresponds to excel table
report = Table(
    "report",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("company", ForeignKey("company.id", ondelete="CASCADE")),
    Column("fact", ForeignKey("data_stamp.id", ondelete="CASCADE")),
    Column("forecast", ForeignKey("data_stamp.id", ondelete="CASCADE")),
    Column("date", Date, nullable=True),
)

# company name table
company = Table(
    "company",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("name", String(128)),
)

# table with qliq, qoil partition
data_stamp = Table(
    "data_stamp",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("qliq", ForeignKey("data_frame.id", ondelete="CASCADE")),
    Column("qoil", ForeignKey("data_frame.id", ondelete="CASCADE")),
)

# table with datas
data_frame = Table(
    "data_frame",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("data1", Integer),
    Column("data2", Integer),
)
