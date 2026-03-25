"""Konfigurace logování pro celý projekt.

Používá Python stdlib logging místo print() — profesionální přístup
s konfigurovatelnou úrovní a formátem.
"""

import logging
import sys


def setup_logger(name: str, level: int = logging.INFO) -> logging.Logger:
    """Vytvoří nakonfigurovaný logger.

    Args:
        name: Název loggeru (typicky __name__ modulu).
        level: Úroveň logování (default INFO).

    Returns:
        Nakonfigurovaný logger.
    """
    logger = logging.getLogger(name)
    logger.setLevel(level)

    # Přidej handler jen pokud ještě žádný nemá (zamezí duplicitním výpisům)
    if not logger.handlers:
        handler = logging.StreamHandler(sys.stdout)
        handler.setLevel(level)
        formatter = logging.Formatter(
            fmt="%(asctime)s | %(levelname)-8s | %(name)s | %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S",
        )
        handler.setFormatter(formatter)
        logger.addHandler(handler)

    return logger
