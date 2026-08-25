"""Z-Stage wiring for the shared firmware-upload dialog.

The dialog itself (model / view / controller) is device-agnostic and lives in
``microdrop_utils.firmware_upload_dialog``; here we just build one wired to
the peripheral live_state, publisher, topics, and the slimmed port-only
panel (the mr-box firmware is bundled — nothing to configure beyond the
port and timeout).
"""

from microdrop_utils.firmware_upload_dialog.controller import (
    FirmwareUploadDialogController,
)

from peripheral_controller.consts import (
    CANCEL_FIRMWARE_UPLOAD,
    FIRMWARE_UPLOAD_FINISHED,
    FIRMWARE_UPLOAD_LOG,
    FIRMWARE_UPLOAD_STARTED,
)
from peripheral_controller.datamodels import upload_firmware_publisher

from ..live_state import peripheral_live_state
from .model import ZStageFirmwareUploadModel
from .view import zstage_firmware_upload_view


def make_firmware_upload_controller():
    """A firmware-upload dialog controller wired for the mr-box board."""
    return FirmwareUploadDialogController(
        live_state=peripheral_live_state,
        upload_publisher=upload_firmware_publisher,
        cancel_topic=CANCEL_FIRMWARE_UPLOAD,
        started_topic=FIRMWARE_UPLOAD_STARTED,
        log_topic=FIRMWARE_UPLOAD_LOG,
        finished_topic=FIRMWARE_UPLOAD_FINISHED,
        model=ZStageFirmwareUploadModel(),
        panel_view=zstage_firmware_upload_view,
        intro_message="Flash the bundled firmware to the mr-box peripheral "
        "board (Z-Stage). A connected board is disconnected "
        "first to free its port, then reconnected when the "
        "upload ends. Press Upload to start.",
        dialog_title="Upload Z-Stage Firmware",
    )
