from . import exception, model


def allocate(line: model.OrderLine, batches: list[model.Batch]) -> str:
    try:
        batch = next(b for b in sorted(batches) if b.can_allocate(line))
    except StopIteration:
        raise exception.OutOfStock(line.sku)

    batch.allocate(line)
    return batch.id
