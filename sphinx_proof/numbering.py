"""Numbering types shared by registration, rendering, and references."""

from sphinx.config import Config


def get_counter_type(config: Config, typ: str) -> str:
    """Return the Sphinx numbering type for a proof environment."""
    return "proof" if config.proof_shared_counter else typ
