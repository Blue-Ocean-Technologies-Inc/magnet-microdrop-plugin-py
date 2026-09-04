# (C) Copyright 2024-2026 Blue Ocean Technologies, Inc., Toronto, ON
# All rights reserved.
#
# This software is provided without warranty under the terms of the AGPL-3.0
# license included in LICENSE and may be redistributed only under the
# conditions described in the aforementioned license. The license is also
# available online at https://www.gnu.org/licenses/agpl-3.0.txt
#
# Thanks for using Microdrop open source!

"""Tree-level conftest. Calls configure_dramatiq_broker() at module
import time so all actor registrations land on the same broker the
Redis-required tests will use. Non-Redis tests are unaffected (they
mock publish_message and never enqueue to Redis).

Mirrors dropbot_protocol_controls/tests/conftest.py from PPT-4."""

# Microdrop utils imports.
from microdrop_utils.broker_server_helpers import configure_dramatiq_broker

configure_dramatiq_broker()
