from pyface.action.api import Action
from pyface.action.schema.schema import SMenu
from traits.api import Instance, Str

from microdrop_utils.dramatiq_traits_helpers import DramatiqMessagePublishAction
from microdrop_utils.firmware_upload_dialog.controller import (
    FirmwareUploadDialogController,
)
from peripheral_controller.consts import START_DEVICE_MONITORING as ZSTAGE_START_DEVICE_MONITORING

from .firmware_upload.controller import make_firmware_upload_controller


class UploadFirmwareAction(Action):
    name = Str("Upload &Firmware...")
    tooltip = "Flash the mr-box peripheral board's bundled firmware"

    #: One controller for the action's lifetime: reopening raises the live
    #: dialog instead of duplicating it, and the log/options survive reopens.
    controller = Instance(FirmwareUploadDialogController)

    def perform(self, event):
        if self.controller is None:
            self.controller = make_firmware_upload_controller()
        self.controller.open()


def z_stage_menu_factory():
    z_stage_search = DramatiqMessagePublishAction(
        name="&Search Connection", topic=ZSTAGE_START_DEVICE_MONITORING)
    z_stage_menu = SMenu(
        items=[z_stage_search, UploadFirmwareAction()],
        id="zstage_tools",
        name="&Z-Stage",
    )

    return z_stage_menu

def tools_menu_factory():
    return SMenu(items=[z_stage_menu_factory()], id="peripherals_tools", name="&Peripherals")
