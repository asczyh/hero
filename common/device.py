"""Airtest connection helpers for the MuMu Android emulator."""

from airtest.core.api import connect_device

from config import settings


def connect_mumu():
    """Connect Airtest to the configured MuMu ADB device."""
    return connect_device(settings.AIRTEST_DEVICE_URI)
