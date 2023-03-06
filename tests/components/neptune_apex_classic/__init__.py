"""Tests for the Neptune Apex Classic component."""

from unittest.mock import AsyncMock, MagicMock, patch

from homeassistant.const import CONF_HOST, CONF_NAME, CONF_PASSWORD, CONF_USERNAME

TEST_USER_INPUT_WITH_AUTH = {
    CONF_HOST: "1.2.3.4",
    CONF_NAME: "Test Name",
    CONF_USERNAME: "admin",
    CONF_PASSWORD: "1234",
}

TEST_USER_INPUT_NO_AUTH = {
    CONF_HOST: "1.2.3.4",
    CONF_NAME: "Test Name",
}

TEST_CONFIG_RESULT = {
    CONF_HOST: "1.2.3.4",
    CONF_NAME: "Test Name",
    CONF_USERNAME: "admin",
    CONF_PASSWORD: "1234",
    "serial-number": "UniqueSerialNumber",
}


def _create_mock_connection(serial: str | None) -> MagicMock:
    mock = MagicMock()
    type(mock).get_serial_number = AsyncMock(return_value=serial)
    return mock


def _patch_config_flow_connection(mock: MagicMock):
    return patch(
        "homeassistant.components.neptune_apex_classic.config_flow.ApexConnection",
        return_value=mock,
    )


def _patch_async_setup_entry():
    return patch(
        "homeassistant.components.neptune_apex_classic.async_setup_entry",
        return_value=True,
    )
