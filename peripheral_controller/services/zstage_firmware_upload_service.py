# (C) Copyright 2024-2026 Blue Ocean Technologies, Inc., Toronto, ON
# All rights reserved.
#
# This software is provided without warranty under the terms of the AGPL-3.0
# license included in LICENSE and may be redistributed only under the
# conditions described in the aforementioned license. The license is also
# available online at https://www.gnu.org/licenses/agpl-3.0.txt
#
# Thanks for using Microdrop open source!

"""Firmware-upload mixin for the z-stage magnet (mr-box peripheral board).

The shared PeripheralFirmwareUploadService owns the whole run — port
resolution (an explicit port, else the connected proxy's own, releasing the
proxy via cleanup() so the uploader gets exclusive port access), the upload
thread, cancel/timeout handling, the started / log / finished topics, and the
monitoring restart afterwards. The mr-box board is not a MicroPython Pico
though: it is flashed by the firmware bundled inside the installed
mr_box_peripheral_board package, so only the flash step is overridden here to
run ``python -m mr_box_peripheral_board.bin.upload -p <port>`` as a
subprocess, streaming every output line onto the upload-log topic (the
dialog's console) and the regular log file.
"""

# Standard library imports.
import os
import subprocess
import sys
import threading

# Enthought library imports.
from traits.api import Instance, provides

# Microdrop package imports.
from peripheral_device_controller_base.services.peripheral_firmware_upload_service import (  # noqa: E501 -- dotted module path can't be shortened
    PeripheralFirmwareUploadService,
)

# Microdrop utils imports.
from microdrop_utils.dramatiq_peripheral_serial_proxy import (
    DramatiqPeripheralSerialProxy,
)

# Local imports.
from ..interfaces.i_peripheral_control_mixin_service import (
    IPeripheralControlMixinService,
)

# Logger import.
from logger.logger_service import get_logger

logger = get_logger(__name__)

MR_BOX_UPLOAD_COMMAND = [sys.executable, "-m", "mr_box_peripheral_board.bin.upload"]


@provides(IPeripheralControlMixinService)
class ZStageFirmwareUploadService(PeripheralFirmwareUploadService):
    """Flashes the mr-box peripheral board's bundled firmware.

    Cancel (and the request's timeout, which sets the same cancel event) kills
    the uploader subprocess via a watcher thread, so a hung flash can always
    be aborted; the run then reports failure through the normal finish path.
    Of the shared UploadFirmwareData payload only ``port`` and
    ``upload_timeout_s`` matter here — the Pico-only options are ignored.
    """

    proxy = Instance(DramatiqPeripheralSerialProxy)

    def _flash_firmware(self, data, port, cancel_event):
        command = list(MR_BOX_UPLOAD_COMMAND)
        if port:
            command += ["-p", port]
        self._publish_upload_log_line(f"Running: {' '.join(command)}")
        process = subprocess.Popen(
            command,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            errors="replace",
            bufsize=1,
            creationflags=(subprocess.CREATE_NO_WINDOW if os.name == "nt" else 0),
        )
        # The reader below blocks on the subprocess's output, so cancel /
        # timeout (both set cancel_event) must kill the process from a
        # watcher thread to unblock it.
        watcher = threading.Thread(
            target=self._kill_process_on_cancel,
            args=(process, cancel_event),
            daemon=True,
        )
        watcher.start()
        try:
            for line in process.stdout:
                self._publish_upload_log_line(line.rstrip())
            returncode = process.wait()
        finally:
            # Unblock the watcher for runs that were never cancelled.
            cancel_event.set()
        if returncode != 0:
            self._publish_upload_log_line(f"Uploader exited with code {returncode}.")
        return returncode == 0

    @staticmethod
    def _kill_process_on_cancel(process, cancel_event):
        cancel_event.wait()
        if process.poll() is None:
            process.kill()
