from __future__ import annotations

from archpy.adapters.repository import Repository
from archpy.domain.allocations import service
from archpy.domain.allocations.model import OrderLine


class InvalidSku(Exception):
    pass


def is_valid_sku(sku, batches):
    return sku in {b.sku for b in batches}


def allocate(line: OrderLine, repo: Repository, session) -> str:
    batches = repo.list()
    if not is_valid_sku(line.sku, batches):
        raise InvalidSku(f"Invalid sku {line.sku}")
    batchref = service.allocate(line, batches)
    session.commit()
    return batchref
