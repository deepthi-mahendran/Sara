"""Tests for CORS allow-origin configuration."""
import importlib
import os

import pytest


@pytest.fixture()
def reload_main(monkeypatch):
    def _reload(**env):
        monkeypatch.setenv("SECRET_KEY", "test-secret-key-for-pytest")
        for key, value in env.items():
            if value is None:
                monkeypatch.delenv(key, raising=False)
            else:
                monkeypatch.setenv(key, value)
        import app.main as main

        return importlib.reload(main)

    return _reload


def test_default_cors_includes_live_demo(reload_main, monkeypatch):
    main = reload_main(CORS_ORIGINS=None)
    origins = main._cors_allow_origins()
    expected_origins = [
        "http://127.0.0.1:5500",
        "http://localhost:5500",
        "http://127.0.0.1:8080",
        "http://localhost:8080",
        "https://sara-deepthi-mahendrans-projects.vercel.app",
        "https://sara-seven-ashen.vercel.app",
    ]
    assert sorted(origins) == sorted(expected_origins)


def test_cors_origins_env_override(reload_main):
    main = reload_main(CORS_ORIGINS="https://example.com, http://localhost:3000")
    assert main._cors_allow_origins() == [
        "https://example.com",
        "http://localhost:3000",
    ]
