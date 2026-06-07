"""Set of utilities for retrieving asset paths for the environments."""

from __future__ import annotations

from pathlib import Path

_CURRENT_FILE_DIR = Path(__file__).parent.absolute()

ENV_ASSET_DIR_V3 = _CURRENT_FILE_DIR / "assets"

# Active arm for asset routing.  Set via set_active_arm() before constructing
# any env; the default "sawyer" preserves upstream behaviour.
ACTIVE_ARM: str = "sawyer"


def set_active_arm(name: str) -> None:
    """Set the active arm for asset path routing.

    Must be called *before* constructing any environment.  The change is
    global (module-level) so set it once per process.

    Args:
        name: Arm identifier.  ``"sawyer"`` (default) uses upstream assets;
              ``"yam"`` redirects to the YAM variants where they exist.
    """
    global ACTIVE_ARM
    ACTIVE_ARM = name


def full_V3_path_for(file_name: str) -> str:
    """Retrieves the full, absolute path for a given V3 asset.

    When ``ACTIVE_ARM == "yam"``, the function looks for a YAM-specific task
    XML in ``yam_xyz/``.  Sawyer task XMLs are named ``sawyer_<task>.xml``; the
    YAM equivalents drop the ``sawyer_`` prefix (e.g. ``sawyer_xyz/sawyer_reach_v3.xml``
    → ``yam_xyz/reach_v3.xml``).  Falls back to the Sawyer path if no YAM
    variant exists.

    Args:
        file_name: Name of the asset file. Can include subdirectories.

    Returns:
        The full path to the asset file.
    """
    if ACTIVE_ARM == "yam" and file_name.startswith("sawyer_xyz/"):
        basename = Path(file_name).name
        # Strip the "sawyer_" prefix to get the task-only filename.
        task_name = basename[len("sawyer_"):] if basename.startswith("sawyer_") else basename
        yam_candidate = ENV_ASSET_DIR_V3 / "yam_xyz" / task_name
        if yam_candidate.exists():
            return str(yam_candidate)
    return str(ENV_ASSET_DIR_V3 / file_name)
