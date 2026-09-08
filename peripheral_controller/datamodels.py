# (C) Copyright 2024-2026 Blue Ocean Technologies, Inc., Toronto, ON
# All rights reserved.
#
# This software is provided without warranty under the terms of the AGPL-3.0
# license included in LICENSE and may be redistributed only under the
# conditions described in the aforementioned license. The license is also
# available online at https://www.gnu.org/licenses/agpl-3.0.txt
#
# Thanks for using Microdrop open source!

# Standard library imports.
from typing import Optional

# Third-party imports.
from pydantic import BaseModel, ConfigDict, Field, model_validator

# Microdrop package imports.
from peripheral_device_controller_base.firmware_upload_datamodels import (
    UploadFirmwarePublisher,
)

# Local imports.
from .consts import UPLOAD_FIRMWARE


class ZStageConfigData(BaseModel):
    # This configuration ensures that if "param3" is passed, an error is raised
    model_config = ConfigDict(extra="forbid")

    # set default=None to make them truly optional
    zstage_down_position: Optional[float] = Field(default=None, ge=0.0)
    zstage_up_position: Optional[float] = Field(default=None, ge=0.0)

    @model_validator(mode="after")
    def check_up_larger_than_down(self):
        # We can only perform the comparison if BOTH values are provided
        if (
            self.zstage_up_position is not None
            and self.zstage_down_position is not None
        ):
            if self.zstage_up_position <= self.zstage_down_position:
                raise ValueError(
                    "zstage_up_position must be strictly larger than "
                    "zstage_down_position"
                )

        return self


# Firmware-upload payload + publisher are shared (peripheral base); this plugin
# only binds a publisher to its own upload topic. The mr-box flash honours the
# port and upload_timeout_s fields — the Pico-only options ride along at their
# defaults and are ignored by the ZStage flash step.
upload_firmware_publisher = UploadFirmwarePublisher(topic=UPLOAD_FIRMWARE)
