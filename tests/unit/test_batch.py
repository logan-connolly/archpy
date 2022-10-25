from archpy.domain.allocations import model


def generate_batch_and_line(sku, batch_qty, line_qty):
    batch = model.Batch(id="batch-001", sku=sku, qty=batch_qty)
    line = model.OrderLine(orderid="order-ref", sku=sku, qty=line_qty)
    return batch, line


def test_can_allocate_if_available_greater_than_required():
    batch, line = generate_batch_and_line("SMALL-TABLE", 20, 2)
    assert batch.can_allocate(line)


def test_cannot_allocate_if_available_less_than_required():
    batch, line = generate_batch_and_line("SMALL-TABLE", 2, 20)
    assert not batch.can_allocate(line)


def test_cannot_allocate_if_skus_do_not_match():
    batch = model.Batch(id="batch-001", sku="sku-1", qty=10)
    line = model.OrderLine(orderid="line-001", sku="different", qty=2)
    assert not batch.can_allocate(line)


def test_can_allocate_multiple_line_items():
    batch = model.Batch(id="batch-001", sku="sku-1", qty=10)
    batch.allocate(model.OrderLine(orderid="order-1", sku="sku-1", qty=1))
    batch.allocate(model.OrderLine(orderid="order-1", sku="sku-1", qty=3))
    assert batch.allocated_quantity == 4


def test_can_deallocate_line_item():
    batch = model.Batch(id="batch-001", sku="sku-1", qty=10)
    line = model.OrderLine(orderid="line-001", sku="sku-1", qty=2)
    batch.allocate(line)
    assert batch.available_quantity == 8
    batch.deallocate(line)
    assert batch.available_quantity == 10


def test_allocate_is_idempotent():
    batch = model.Batch(id="batch-001", sku="sku-1", qty=10)
    line = model.OrderLine(orderid="line-001", sku="sku-1", qty=2)
    batch.allocate(line)
    batch.allocate(line)
    assert batch.available_quantity == 8
