"""RemoteStore Stat Tracking Tests."""
import os
import shutil

from pytest import fixture
from pytest import mark
from pytest import raises

import proxystore as ps
from .utils import FILE_DIR
from .utils import FILE_STORE
from .utils import GLOBUS_STORE
from .utils import LOCAL_STORE
from .utils import mock_third_party_libs
from .utils import REDIS_STORE


@fixture(scope="session", autouse=True)
def init():
    """Set up test environment."""
    mpatch = mock_third_party_libs()
    if os.path.exists(FILE_DIR):
        shutil.rmtree(FILE_DIR)  # pragma: no cover
    yield mpatch
    mpatch.undo()
    if os.path.exists(FILE_DIR):
        shutil.rmtree(FILE_DIR)  # pragma: no cover


@mark.parametrize(
    "store_config",
    [LOCAL_STORE, FILE_STORE, REDIS_STORE, GLOBUS_STORE],
)
def test_init_stats(store_config) -> None:
    """Test Initializing Stat tracking."""
    store = store_config["type"](
        store_config["name"],
        **store_config["kwargs"],
    )

    with raises(ValueError):
        # Check raises an error because stats are not tracked by default
        store.stats()

    store = store_config["type"](
        store_config["name"],
        **store_config["kwargs"],
        stats=True,
    )

    assert isinstance(store.stats(), dict)


def test_stat_tracking() -> None:
    """Test stat tracking of store."""
    store = ps.store.init_store("local", "local", stats=True)

    p = store.proxy([1, 2, 3])
    ps.proxy.resolve(p)

    stats = store.stats()

    assert "get" in stats
    assert "set" in stats

    assert stats["get"]["calls"] == 1
    assert stats["set"]["calls"] == 1
