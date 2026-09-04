# (C) Copyright 2024-2026 Blue Ocean Technologies, Inc., Toronto, ON
# All rights reserved.
#
# This software is provided without warranty under the terms of the AGPL-3.0
# license included in LICENSE and may be redistributed only under the
# conditions described in the aforementioned license. The license is also
# available online at https://www.gnu.org/licenses/agpl-3.0.txt
#
# Thanks for using Microdrop open source!

# Enthought library imports.
from traits.api import Instance, List, Str, provides

# Microdrop package imports.
from peripheral_device_controller_base.consts import (
    DEFAULT_ALWAYS_ALLOWED_SUBTOPICS,
    FIRMWARE_UPLOAD_ALWAYS_ALLOWED_SUBTOPICS,
)
from peripheral_device_controller_base.peripheral_device_controller_base import (
    PeripheralDeviceControllerBase,
)

# Microdrop utils imports.
from microdrop_utils.dramatiq_peripheral_serial_proxy import (
    DramatiqPeripheralSerialProxy,
)

# Local imports.
from .consts import DEVICE_NAME, PKG
from .interfaces.i_peripheral_controller_base import IPeripheralControllerBase
from .preferences import PeripheralPreferences

# Logger import.
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
