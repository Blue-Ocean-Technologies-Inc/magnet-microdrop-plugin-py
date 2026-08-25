from traits.api import Instance, List, Str, provides

from peripheral_device_controller_base.consts import (
    DEFAULT_ALWAYS_ALLOWED_SUBTOPICS,
    FIRMWARE_UPLOAD_ALWAYS_ALLOWED_SUBTOPICS,
)
from peripheral_device_controller_base.peripheral_device_controller_base import PeripheralDeviceControllerBase

from .interfaces.i_peripheral_controller_base import IPeripheralControllerBase
from microdrop_utils.dramatiq_peripheral_serial_proxy import DramatiqPeripheralSerialProxy
from .preferences import PeripheralPreferences

from .consts import DEVICE_NAME, PKG

from logger.logger_service import get_logger
logger = get_logger(__name__, level="INFO")


@provides(IPeripheralControllerBase)
class PeripheralControllerBase(PeripheralDeviceControllerBase):
    """Backend controller for the z-stage magnet peripheral.

    All of the listener/routing/connection machinery lives in
    ``PeripheralDeviceControllerBase``; this subclass only pins the device
    identity and narrows the proxy/preferences trait types.
    """
    _device_name = Str(DEVICE_NAME)
    listener_name = Str(f"{PKG}_listener")
    proxy = Instance(DramatiqPeripheralSerialProxy)
    preferences = Instance(PeripheralPreferences)
    # Firmware upload/cancel must run while disconnected: flashing IS the
    # recovery path for a board whose firmware can't connect, and the upload
    # service itself releases the proxy (disconnecting) before flashing.
    _always_allowed_subtopics = List(
        Str,
        DEFAULT_ALWAYS_ALLOWED_SUBTOPICS + FIRMWARE_UPLOAD_ALWAYS_ALLOWED_SUBTOPICS,
    )
