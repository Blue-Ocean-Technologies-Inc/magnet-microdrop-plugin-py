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
from envisage.api import ServiceOffer
from traits.api import List

# Microdrop package imports.
from message_router.consts import ACTOR_TOPIC_ROUTES
from peripheral_device_controller_base.plugin import PeripheralDeviceControllerPlugin

# Local imports.
from .consts import ACTOR_TOPIC_DICT, PKG, PKG_name
from .interfaces.i_peripheral_control_mixin_service import (
    IPeripheralControlMixinService,
)
from .peripheral_controller_base import PeripheralControllerBase

# Logger import.
from logger.logger_service import get_logger

# Initialize logger
logger = get_logger(__name__)


class PeripheralControllerPlugin(PeripheralDeviceControllerPlugin):
    id = PKG + ".plugin"
    name = f"{PKG_name} Plugin"

    # This plugin contributes some actors that can be called using certain routing keys.
    actor_topic_routing = List([ACTOR_TOPIC_DICT], contributes_to=ACTOR_TOPIC_ROUTES)

    # Compose only the magnet's own mixins onto the magnet's controller base.
    _mixin_protocol = IPeripheralControlMixinService
    _controller_base_class = PeripheralControllerBase

    def _service_offers_default(self):
        """Return the service offers."""
        return [
            ServiceOffer(
                protocol=IPeripheralControlMixinService,
                factory=self._create_monitor_service,
            ),
            ServiceOffer(
                protocol=IPeripheralControlMixinService,
                factory=self._create_zstage_state_setter_service,
            ),
            ServiceOffer(
                protocol=IPeripheralControlMixinService,
                factory=self._create_firmware_upload_service,
            ),
        ]

    def _create_monitor_service(self, *args, **kwargs):
        """Returns a peripheral monitor mixin service with core functionality."""
        from .services.peripheral_monitor_mixin_service import (
            PeripheralMonitorMixinService,
        )

        return PeripheralMonitorMixinService

    def _create_zstage_state_setter_service(self, *args, **kwargs):
        """Returns a zstage mixin service to set z-stage states"""
        from .services.zstage_state_setter_service import ZStageStatesSetterMixinService

        return ZStageStatesSetterMixinService

    def _create_firmware_upload_service(self, *args, **kwargs):
        """Returns the z-stage firmware-upload mixin service."""
        from .services.zstage_firmware_upload_service import ZStageFirmwareUploadService

        return ZStageFirmwareUploadService
