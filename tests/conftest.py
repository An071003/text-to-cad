"""Pytest configuration for watch caliber CAD project.

Ensures silent, headless execution without console window popups on Windows.
"""

import os

# Disable cadgen background daemon and warm worker pool during pytest.
# The daemon internally spawns warm workers via subprocess.Popen without CREATE_NO_WINDOW,
# which causes Windows to flash/open separate console windows and can result in
# 'the warm worker running job died mid-job' errors.
os.environ["CADGEN_DAEMON"] = "0"
