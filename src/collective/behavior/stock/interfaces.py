from collective.behavior.stock.schema import StockSchema


class IStock(StockSchema):
    """Interface for behavior: Stock"""

    def initial_stock():  # pragma: no cover
        """Sum of initial stocks"""

    def stock():  # pragma: no cover
        """Sum of stocks"""

    def stocks(sort_order='ascending'):  # pragma: no cover
        """Returns catalog brains of stock."""

    def sub_stock(value):  # pragma: no cover
        """Decrease stock by value and return the real subtracted value."""

    def add_stock(value):  # pragma: no cover
        """Add stock by value and return the real added value."""
