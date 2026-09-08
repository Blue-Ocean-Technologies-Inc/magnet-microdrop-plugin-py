# (C) Copyright 2024-2026 Blue Ocean Technologies, Inc., Toronto, ON
# All rights reserved.
#
# This software is provided without warranty under the terms of the AGPL-3.0
# license included in LICENSE and may be redistributed only under the
# conditions described in the aforementioned license. The license is also
# available online at https://www.gnu.org/licenses/agpl-3.0.txt
#
# Thanks for using Microdrop open source!

"""Dramatiq message handler for the peripherals (Z-Stage) UI.

Replaces the old DramatiqStatusController + DramatiqStatusViewModel pair with
the shared BaseMessageHandler (reflection dispatch, timestamped dedup guards,
and teardown() for runtime hot unload). Handlers write to PeripheralModel,
whose ``status`` trait is the Z-Stage's connected flag.
"""

# Standard library imports.
import json

# Enthought library imports.
from traits.api import Instance

# Microdrop package imports.
from peripheral_controller.consts import (
    FIRMWARE_UPLOAD_FINISHED,
    FIRMWARE_UPLOAD_LOG,
    FIRMWARE_UPLOAD_STARTED,
)
from template_status_and_controls.base_message_handler import BaseMessageHandler

# Microdrop utils imports.
from microdrop_utils.decorators import timestamped_value

# Local imports.
from .live_state import peripheral_live_state
from .model import PeripheralModel

# Logger import.
from logger.logger_service import get_logger

logger = get_logger(__name__)


class PeripheralMessageHandler(BaseMessageHandler):
    """Updates the Z-Stage model from ZStage/signals/# plus the realtime-mode
    and start-monitoring request topics the pane also listens to."""

    model = Instance(PeripheralModel)

    # PeripheralModel exposes the connection flag as ``status`` (the z_stage
    # view-model observes it), so the shared connected/disconnected handlers
    # are overridden to write that trait. Dedup guards stay.
    @timestamped_value("connected_message")
    def _on_connected_triggered(self, body):
        """Also ferry the board's serial port to live_state so the
        firmware-upload dialog keeps its port combo in sync with the
        auto-detected port. The monitor republishes a "<device>_connected"
        sentinel (not a port) when asked to start monitoring an
        already-connected board — ignore that."""
        logger.info(f"{self.model.device_name} connected: {body}")
        self.model.status = True
        port = str(body)
        if port and not port.endswith("_connected"):
            peripheral_live_state.board_port = port

    @timestamped_value("connected_message")
    def _on_disconnected_triggered(self, body):
        """Also clear the ferried port so the firmware-upload dialog shows no
        auto-detected port while disconnected."""
        logger.info(f"{self.model.device_name} disconnected: {body}")
        self.model.status = False
        self.model.realtime_mode = False
        peripheral_live_state.board_port = ""

    @timestamped_value("realtime_mode_message")
    def _on_set_realtime_mode_triggered(self, body):
        # The pane subscribes to the SET_REALTIME_MODE request topic (last
        # segment "set_realtime_mode"), not the dropbot's realtime_mode_updated.
        self.model.realtime_mode = body == "True"

    def _on_position_updated_triggered(self, body):
        self.model.position = float(body)

    def _on_start_device_monitoring_triggered(self, body):
        self.model.search_requested = True

    def _on_searching_triggered(self, body):
        """Backend connection-scan state (JSON bool). Mirrored to the model so
        the pane can disable the status-icon 'search connection' click while a
        scan is already running."""
        try:
            self.model.searching = bool(json.loads(body))
        except Exception:
            logger.error("Failed to parse searching signal", exc_info=True)

    def _on_firmware_upload_started_triggered(self, body):
        """Backend accepted an upload — ferry to the GUI thread via live_state
        (the dialog's dispatch="ui" observer applies it)."""
        peripheral_live_state.firmware_upload_message = (FIRMWARE_UPLOAD_STARTED, body)

    def _on_firmware_upload_log_triggered(self, body):
        """One uploader progress line — ferry to the GUI thread."""
        peripheral_live_state.firmware_upload_message = (FIRMWARE_UPLOAD_LOG, body)

    def _on_firmware_upload_finished_triggered(self, body):
        """Upload outcome — ferry to the GUI thread."""
        peripheral_live_state.firmware_upload_message = (FIRMWARE_UPLOAD_FINISHED, body)
