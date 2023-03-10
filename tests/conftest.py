from pathlib import Path

import pytest
import yaml

from aiidalab.app import AiidaLabApp


@pytest.fixture
def generate_app():
    """Fixture to construct a new AiiDALabApp instance for testing."""

    def _generate_app(
        name="quantum-espresso",
        aiidalab_apps_path="/home/jovyan/apps",
        app_data=None,
        watch=False,
    ):
        if app_data is None:
            with open(
                Path(__file__).parent.absolute() / "static/app_registry.yaml"
            ) as f:
                app_data = yaml.safe_load(f)
        app = AiidaLabApp(name, app_data, aiidalab_apps_path, watch=watch)

        return app

    return _generate_app


_MONKEYPATCHED_INSTALLED_PACKAGES = [
    {"name": "aiida-core", "version": "2.2.1"},
    {"name": "jupyter_client", "version": "7.3.5"},
]


@pytest.fixture
def installed_packages(monkeypatch):
    """change the return of pip_list.
    This is to mimic the pip list command output, which returns a json string represent
    the list of installed packages."""
    from aiidalab.utils import FIND_INSTALLED_PACKAGES_CACHE

    FIND_INSTALLED_PACKAGES_CACHE.clear()  # clear the cache
    monkeypatch.setattr(
        "aiidalab.utils._pip_list",
        lambda _: _MONKEYPATCHED_INSTALLED_PACKAGES,
    )