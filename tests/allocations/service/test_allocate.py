from datetime import date, timedelta

import pytest

from archpy.allocations import exception, model, service


@pytest.fixture
def today():
    return date.today()


@pytest.fixture
def tomorrow():
    return date.today() + timedelta(days=1)


def test_in_stock_batches_are_preferred(today):
    instock_batch = model.Batch(id="batch-001", sku="sku-1", qty=100, eta=None)
    enroute_batch = model.Batch(id="batch-002", sku="sku-1", qty=100, eta=today)
    line = model.OrderLine(orderid="line-001", sku="sku-1", qty=10)

    service.allocate(line, [instock_batch, enroute_batch])

    assert instock_batch.available_quantity == 90
    assert enroute_batch.available_quantity == 100


def test_in_stock_batch_id_is_returned(today):
    instock_batch = model.Batch(id="batch-001", sku="sku-1", qty=100, eta=None)
    enroute_batch = model.Batch(id="batch-002", sku="sku-1", qty=100, eta=today)
    line = model.OrderLine(orderid="line-001", sku="sku-1", qty=10)

    allocated_batch = service.allocate(line, [instock_batch, enroute_batch])

    assert instock_batch.id == allocated_batch


def test_earlier_batches_are_preferred(today, tomorrow):
    yesterday_batch = model.Batch(id="batch-001", sku="sku-1", qty=100, eta=None)
    today_batch = model.Batch(id="batch-002", sku="sku-1", qty=100, eta=today)
    tomorrow_batch = model.Batch(id="batch-002", sku="sku-1", qty=100, eta=tomorrow)
    line = model.OrderLine(orderid="line-001", sku="sku-1", qty=10)

    service.allocate(line, [tomorrow_batch, today_batch, yesterday_batch])

    assert yesterday_batch.available_quantity == 90
    assert today_batch.available_quantity == 100
    assert tomorrow_batch.available_quantity == 100


def test_out_of_stock_exception_is_raised():
    instock_batch = model.Batch(id="batch-001", sku="sku-1", qty=5, eta=None)
    line = model.OrderLine(orderid="line-001", sku="sku-1", qty=10)

    with pytest.raises(exception.OutOfStock, match=line.sku):
        service.allocate(line, [instock_batch])
