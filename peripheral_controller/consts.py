from peripheral_device_controller_base.consts import (
    cancel_firmware_upload_topic,
    firmware_upload_finished_topic,
    firmware_upload_log_topic,
    firmware_upload_started_topic,
    upload_firmware_topic,
)

# This module's package.
PKG = ".".join(__name__.split(".")[:-1])
PKG_name = PKG.title().replace("_", " ")

# mr box hardware id
MR_BOX_HWID = "VID:PID=0403:6015"

DEVICE_NAME = "ZStage"

# Topics published by this plugin
CONNECTED = f"{DEVICE_NAME}/signals/connected"
DISCONNECTED = f"{DEVICE_NAME}/signals/disconnected"
# JSON bool: True while scanning for the board, False once connected/stopped.
SEARCHING = f"{DEVICE_NAME}/signals/searching"
ZSTAGE_POSITION_UPDATED = f"{DEVICE_NAME}/signals/position_updated"

# Service Request Topics
START_DEVICE_MONITORING = f"{DEVICE_NAME}/requests/start_device_monitoring"
GO_HOME = f"{DEVICE_NAME}/requests/go_home"
MOVE_UP = f"{DEVICE_NAME}/requests/move_up"
MOVE_DOWN = f"{DEVICE_NAME}/requests/move_down"
SET_POSITION = f"{DEVICE_NAME}/requests/set_position"
RETRY_CONNECTION = f"{DEVICE_NAME}/requests/retry_connection"
UPDATE_CONFIG = f"{DEVICE_NAME}/requests/update_config"

# Firmware upload: the shared PeripheralFirmwareUploadService owns the run;
# the ZStage service overrides only the flash step to call the bundled
# `python -m mr_box_peripheral_board.bin.upload -p <port>` uploader.
UPLOAD_FIRMWARE = upload_firmware_topic(DEVICE_NAME)
CANCEL_FIRMWARE_UPLOAD = cancel_firmware_upload_topic(DEVICE_NAME)
FIRMWARE_UPLOAD_STARTED = firmware_upload_started_topic(DEVICE_NAME)
FIRMWARE_UPLOAD_LOG = firmware_upload_log_topic(DEVICE_NAME)
FIRMWARE_UPLOAD_FINISHED = firmware_upload_finished_topic(DEVICE_NAME)

# What the mr-box board is flashed with: the firmware bundled inside the
# installed mr_box_peripheral_board package (there is no user-pickable
# source). Sent as the upload request's firmware_source so the started log
# line names it.
BUNDLED_MR_BOX_FIRMWARE_DESCRIPTION = "the bundled mr-box-peripheral-board firmware"

# Protocol-driven magnet engage/retract (separate from existing
# MOVE_UP/MOVE_DOWN/SET_POSITION/GO_HOME so the protocol-side gets
# one publish + one wait_for; backend owns the retract sequence).
PROTOCOL_SET_MAGNET = f"{DEVICE_NAME}/requests/protocol_set_magnet"
MAGNET_APPLIED = f"{DEVICE_NAME}/signals/magnet_applied"

# app_globals key mirroring this device's connection state (the controller
# writes it whenever connection_active changes); consumers read it instead of
# tracking the connected/disconnected signals themselves. Keyed by device name
# so distinct peripherals don't collide.
CONNECTION_STATE_KEY = f"{DEVICE_NAME}.connection_active"

# Error Topics
ERROR = f"{DEVICE_NAME}/error"

# Topics actor declared by plugin subscribes to
ACTOR_TOPIC_DICT = {
    f"{PKG}_listener": [
        f"{DEVICE_NAME}/requests/#",
        CONNECTED,
        DISCONNECTED,
    ]
}

(
    DEFAULT_DOWN_HEIGHT_MM,
    DEFAULT_UP_HEIGHT_MM,
) = 0.5, 23.0
MIN_ZSTAGE_HEIGHT_MM, MAX_ZSTAGE_HEIGHT_MM = 0.5, 28.0
