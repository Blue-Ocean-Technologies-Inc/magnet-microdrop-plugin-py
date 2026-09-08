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
from traits.api import Bool, Instance, Str

# Microdrop utils imports.
from microdrop_utils.dramatiq_peripheral_serial_proxy import (
    DramatiqPeripheralSerialProxy,
)
from microdrop_utils.i_dramatiq_controller_base import IDramatiqControllerBase

# Local imports.
from ..preferences import PeripheralPreferences


class IPeripheralControllerBase(IDramatiqControllerBase):
    """
    Interface for peripheral controllers.
    Provides methods for controlling and monitoring a peripheral device.
    """

    _device_name = Str
    proxy = Instance(
        DramatiqPeripheralSerialProxy, desc="The DramatiqSerialProxy object"
    )
    connection_active = Bool(
        desc="Specifies if the controller is actively listening to commands "
        "or not. So if the connection is not there, no commands will be "
        "processed except searching for s connection"
    )
    preferences = Instance(
        PeripheralPreferences,
        desc="The preferences object for the dropbot controller service",
    )
