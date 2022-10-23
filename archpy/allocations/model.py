from __future__ import annotations

import datetime
import dataclasses
from typing import Optional


@dataclasses.dataclass(frozen=True)
class OrderLine:
    orderid: str
    sku: str
    qty: int


@dataclasses.dataclass
class Batch:
    def __init__(
        self, id: str, sku: str, qty: int, eta: Optional[datetime.date] = None
    ) -> None:
        self.id = id
        self.sku = sku
        self.eta = eta
        self._purchase_qty = qty
        self._allocations: set[OrderLine] = set()

    def __eq__(self, __o: Batch) -> bool:
        if not isinstance(__o, Batch):
            return False
        return self.id == __o.id

    def __hash__(self) -> str:
        return self.id

    def __gt__(self, __o: Batch) -> bool:
        if not isinstance(__o, Batch):
            return NotImplemented
        if self.eta is None:
            return False
        if __o.eta is None:
            return True
        return self.eta > __o.eta

    @property
    def allocated_quantity(self) -> int:
        return sum(line.qty for line in self._allocations)

    @property
    def available_quantity(self) -> int:
        return self._purchase_qty - self.allocated_quantity

    def can_allocate(self, line: OrderLine) -> bool:
        return line.qty <= self.available_quantity and line.sku == self.sku

    def allocate(self, line: OrderLine):
        if self.can_allocate(line):
            self._allocations.add(line)

    def deallocate(self, line: OrderLine):
        if self.can_allocate(line):
            self._allocations.remove(line)
