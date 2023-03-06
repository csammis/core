"""Tests for the Neptune Apex Classic config flow."""
from homeassistant.components import neptune_apex_classic
from homeassistant.config_entries import SOURCE_USER
from homeassistant.core import HomeAssistant
from homeassistant.data_entry_flow import FlowResultType

from . import (
    TEST_CONFIG_RESULT,
    TEST_USER_INPUT_NO_AUTH,
    TEST_USER_INPUT_WITH_AUTH,
    _create_mock_connection,
    _patch_async_setup_entry,
    _patch_config_flow_connection,
)


async def test_config_flow_no_connection(hass: HomeAssistant) -> None:
    """Test the config flow when the server returns no serial number."""

    mocked_connection = _create_mock_connection(None)
    with _patch_config_flow_connection(mocked_connection):
        # Kick off the config flow without user input
        result = await hass.config_entries.flow.async_init(
            neptune_apex_classic.const.DOMAIN,
            context={"source": SOURCE_USER},
        )
        assert result["type"] == FlowResultType.FORM
        assert result["step_id"] == "user"
        assert result["errors"] == {}

        # Complete the config flow - should have an error with no serial number
        result = await hass.config_entries.flow.async_configure(
            result["flow_id"],
            user_input=TEST_USER_INPUT_WITH_AUTH,
        )
        assert result["type"] == FlowResultType.FORM
        assert result["step_id"] == "user"
        assert result["errors"] == {"base": "status-not-found"}


async def test_config_flow_good_connection(hass: HomeAssistant) -> None:
    """Test the config flow when the server returns a serial number."""

    mocked_connection = _create_mock_connection("UniqueSerialNumber")
    with _patch_config_flow_connection(mocked_connection), _patch_async_setup_entry():
        # Kick off the config flow without user input
        result = await hass.config_entries.flow.async_init(
            neptune_apex_classic.const.DOMAIN,
            context={"source": SOURCE_USER},
        )
        assert result["type"] == FlowResultType.FORM
        assert result["step_id"] == "user"
        assert result["errors"] == {}

        # Complete the config flow - should be okay
        result = await hass.config_entries.flow.async_configure(
            result["flow_id"],
            user_input=TEST_USER_INPUT_WITH_AUTH,
        )
        assert result["type"] == FlowResultType.CREATE_ENTRY
        assert result["title"] == TEST_USER_INPUT_WITH_AUTH["name"]
        assert result["data"] == TEST_CONFIG_RESULT


async def test_config_flow_good_connection_no_auth(hass: HomeAssistant) -> None:
    """Test the config flow when the server returns a serial number and no auth is supplied."""

    mocked_connection = _create_mock_connection("UniqueSerialNumber")
    with _patch_config_flow_connection(mocked_connection), _patch_async_setup_entry():
        # Kick off the config flow without user input
        result = await hass.config_entries.flow.async_init(
            neptune_apex_classic.const.DOMAIN,
            context={"source": SOURCE_USER},
        )
        assert result["type"] == FlowResultType.FORM
        assert result["step_id"] == "user"
        assert result["errors"] == {}

        # Complete the config flow - should be okay
        result = await hass.config_entries.flow.async_configure(
            result["flow_id"],
            user_input=TEST_USER_INPUT_NO_AUTH,
        )
        assert result["type"] == FlowResultType.CREATE_ENTRY
        assert result["title"] == TEST_USER_INPUT_NO_AUTH["name"]
        assert result["data"] == TEST_CONFIG_RESULT
