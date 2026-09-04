# (C) Copyright 2024-2026 Blue Ocean Technologies, Inc., Toronto, ON
# All rights reserved.
#
# This software is provided without warranty under the terms of the AGPL-3.0
# license included in LICENSE and may be redistributed only under the
# conditions described in the aforementioned license. The license is also
# available online at https://www.gnu.org/licenses/agpl-3.0.txt
#
# Thanks for using Microdrop open source!

"""Smoke tests for the peripheral_protocol_controls package shell."""


def test_can_import_plugin():
    """Envisage Plugin.id is a Trait — accessible on an instance, not the
    class. (Class-level access raises AttributeError.)"""
    from peripheral_protocol_controls.plugin import (
        PeripheralProtocolControlsPlugin,
    )

    p = PeripheralProtocolControlsPlugin()
    assert p.id.endswith(".plugin")


def test_plugin_instantiates_with_no_columns_yet():
    from peripheral_protocol_controls.plugin import (
        PeripheralProtocolControlsPlugin,
    )

    p = PeripheralProtocolControlsPlugin()
    assert hasattr(p, "id")
    assert hasattr(p, "name")


def test_plugin_contributes_magnet_compound_column():
    """The plugin's contributed_protocol_columns default factory yields
    a list containing the magnet CompoundColumn."""
    from peripheral_protocol_controls.plugin import (
        PeripheralProtocolControlsPlugin,
    )
    from pluggable_protocol_tree.interfaces.i_compound_column import (
        ICompoundColumn,
    )

    p = PeripheralProtocolControlsPlugin()
    cols = p.contributed_protocol_columns
    assert len(cols) == 1
    assert isinstance(cols[0], ICompoundColumn)
    assert cols[0].model.base_id == "magnet"
