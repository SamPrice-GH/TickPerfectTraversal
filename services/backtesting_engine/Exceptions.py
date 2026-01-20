# TODO: make these more specific/meaningful, just allows us to not try/except generic Exception everywhere

class TickStreamException(Exception):
    """Raised when there is an error initializing or using the TickStream."""
    pass

class TickResamplerException(Exception):
    """Raised when there is an error during tick resampling."""
    pass

class BarCollectorException(Exception):
    """Raised when there is an error in the BarCollector."""
    pass

class BacktestException(Exception):
    """Raised when there is an error during backtesting."""
    pass