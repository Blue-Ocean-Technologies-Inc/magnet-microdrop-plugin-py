"""Z-Stage view for the shared firmware-upload dialog: only a port section
(the firmware is bundled — there is no source to pick and no Pico options)
next to the shared log console."""

from traitsui.api import (
    HGroup,
    HSplit,
    Item,
    Label,
    RangeEditor,
    UItem,
    VGroup,
    View,
    spring,
)

from microdrop_style.icons.icons import (
    ICON_AUTOMATION,
    ICON_DELETE,
    ICON_REFRESH,
    ICON_USB,
)
from microdrop_utils.firmware_upload_dialog.view import LogViewEditor
from microdrop_utils.traitsui_qt_helpers import (
    HoverScrollEnumEditor,
    IconButtonEditor,
    IconToggleEditor,
)

# Left: the port/timeout options. Right: the log console, permanently visible
# on the other side of a draggable splitter.
zstage_firmware_upload_view = View(
    HSplit(
        VGroup(
            VGroup(
                HGroup(
                    Item(
                        "auto_port",
                        label="Auto-detect port",
                        editor=IconToggleEditor(
                            on_glyph=ICON_AUTOMATION,
                            off_glyph=ICON_USB,
                            tooltip="On: the backend finds the board itself "
                            "(the connected board's port). "
                            "Off: use the port selected here.",
                        ),
                    ),
                    Item(
                        "selected_port_entry",
                        label="Port",
                        editor=HoverScrollEnumEditor(values_name="available_ports"),
                        enabled_when="not auto_port",
                        springy=True,
                    ),
                    UItem(
                        "refresh_ports",
                        editor=IconButtonEditor(
                            glyph=ICON_REFRESH, tooltip="Re-scan serial ports"
                        ),
                    ),
                ),
                Item(
                    "upload_timeout_s",
                    label="Timeout (s)",
                    editor=RangeEditor(low=0, high=10000, mode="spinner"),
                    tooltip="Kill the upload if it runs longer than this "
                    "many seconds (0 = no timeout)",
                ),
                label="Device & port",
                show_border=True,
                enabled_when="not uploading",
            ),
            # Only this column scrolls (vertically) when the dialog is short —
            # the log console on the right has its own scrollbars.
            scrollable=True,
        ),
        VGroup(
            HGroup(
                Label("Upload log"),
                spring,
                UItem(
                    "clear_log",
                    editor=IconButtonEditor(glyph=ICON_DELETE, tooltip="Clear the log"),
                ),
            ),
            UItem("upload_log", editor=LogViewEditor()),
            show_border=True,
            springy=True,
        ),
    ),
    resizable=True,
)
