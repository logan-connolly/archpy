from sqlalchemy import Column, ForeignKey, Table
from sqlalchemy.orm import registry, relationship
from sqlalchemy.types import Date, Integer, String

from archpy.domain.allocations import model as allocations_model

mapper_registry = registry()
metadata = mapper_registry.metadata

order_lines = Table(
    "order_lines",
    metadata,
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column("sku", String(255)),
    Column("qty", Integer, nullable=False),
    Column("orderid", String(255)),
)

batches = Table(
    "batches",
    metadata,
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column("sku", String(255)),
    Column("eta", Date, nullable=True),
    Column("_purchased_quantity", Integer, nullable=False),
)

allocations = Table(
    "allocations",
    metadata,
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column("orderline_id", ForeignKey("order_lines.id")),
    Column("batch_id", ForeignKey("batches.id")),
)


def start_mappers():
    lines_mapper = mapper_registry.map_imperatively(
        allocations_model.OrderLine, order_lines
    )
    mapper_registry.map_imperatively(
        allocations_model.Batch,
        batches,
        properties={
            "_allocations": relationship(
                lines_mapper, secondary=allocations, collection_class=set
            )
        },
    )
