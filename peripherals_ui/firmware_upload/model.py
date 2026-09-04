"""Z-Stage options model for the shared firmware-upload dialog.

The mr-box peripheral board is flashed by the firmware bundled inside the
installed mr_box_peripheral_board package, so unlike the Pico boards there is
no firmware source to pick and no upload options beyond the port and the
timeout: the shared model is narrowed to exactly that, and the ride-along
Pico-only payload fields are pinned to their defaults.
"""

import serial.tools.list_ports

from peripheral_controller.consts import (
    BUNDLED_MR_BOX_FIRMWARE_DESCRIPTION,
    MR_BOX_HWID,
)

from microdrop_utils.firmware_upload_dialog.consts import PORT_ENTRY_SEPARATOR
from microdrop_utils.firmware_upload_dialog.model import FirmwareUploadModel


class ZStageFirmwareUploadModel(FirmwareUploadModel):
    """Options for one mr-box firmware-upload request, plus the live log."""

    @staticmethod
    def _scan_port_entries():
        """Dropdown entries for every serial port, mr-box hardware-id ports
        first."""
        ports = sorted(
            serial.tools.list_ports.comports(),
            key=lambda p: (MR_BOX_HWID not in str(p.hwid), str(p.device)),
        )
        return [f"{p.device}{PORT_ENTRY_SEPARATOR}{p.description}" for p in ports]

    def validation_problems(self):
        """Human-readable reasons the upload can't start (empty when OK)."""
        if not self.auto_port and not self.selected_port_entry:
            return ["Manual port mode is on but no port is selected."]
        return []

    def upload_request_kwargs(self):
        """Keyword payload for the upload publisher: the port and timeout are
        what the mr-box flash honours (empty port = backend auto-resolution);
        the Pico-only fields ride along at their defaults."""
        return dict(
            firmware_source=BUNDLED_MR_BOX_FIRMWARE_DESCRIPTION,
            single_file="",
            port="" if self.auto_port else self.selected_port_device(),
            device_id="",
            update_config=False,
            skip_filesystem_format=False,
            reset_after_upload=True,
            dry_run=False,
            upload_timeout_s=self.upload_timeout_s,
        )
