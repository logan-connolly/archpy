class OutOfStock(Exception):
    def __init__(self, sku: str) -> None:
        super().__init__(f"Could not find a batch that fulfill {sku=}.")
