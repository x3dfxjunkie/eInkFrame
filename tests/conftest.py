"""Pytest configuration and shared fixtures for sd_monitor tests."""

from typing import Generator
from unittest.mock import MagicMock, patch

import pytest


@pytest.fixture
def mock_subprocess_popen() -> Generator:
    """Mock subprocess.Popen for testing frame_manager subprocess calls.

    Returns:
        tuple: A tuple of (mock_popen, mock_process) where:
            - mock_popen: MagicMock of subprocess.Popen class
            - mock_process: MagicMock of the subprocess instance
                - poll() returns None (process is running)
                - pid is set to 12345

    Example:
        def test_something(mock_subprocess_popen):
            mock_popen, mock_process = mock_subprocess_popen
            # Now subprocess.Popen calls will be mocked
    """
    with patch("sd_monitor.subprocess.Popen") as mock_popen:
        mock_process = MagicMock()
        mock_process.poll.return_value = None  # Process is running
        mock_process.pid = 12345
        mock_popen.return_value = mock_process
        yield mock_popen, mock_process


@pytest.fixture
def mock_subprocess_run() -> Generator:
    """Mock subprocess.run for testing sudo operations.

    Mocks all subprocess.run calls to avoid actual system command execution.
    Default return value has returncode=0 (success).

    Yields:
        MagicMock: Mock of subprocess.run function with returncode=0

    Example:
        def test_cleanup(mock_subprocess_run):
            # subprocess.run calls will be captured but not executed
            assert mock_subprocess_run.call_count > 0
    """
    with patch("sd_monitor.subprocess.run") as mock_run:
        mock_run.return_value = MagicMock(returncode=0)
        yield mock_run


@pytest.fixture
def temp_sd_path(tmp_path) -> str:
    """Create a temporary directory to simulate SD card path.

    Provides a temporary filesystem location that mimics an SD card mount point,
    allowing tests to work with real file operations in isolation.

    Args:
        tmp_path: Built-in pytest fixture for temporary directories

    Returns:
        str: Path to a temporary directory (e.g., '/tmp/pytest-123/test_sd')

    Example:
        def test_read_refresh_time(temp_sd_path):
            # temp_sd_path is '/tmp/pytest-xxx/test_sd'
            refresh_file = Path(temp_sd_path) / "refresh_time.txt"
            refresh_file.write_text("300")
    """
    sd_dir = tmp_path / "test_sd"
    sd_dir.mkdir()
    return str(sd_dir)


@pytest.fixture
def mock_sd_mount_base(tmp_path, monkeypatch) -> str:
    """Mock SD_MOUNT_BASE to use a temporary directory.

    Redirects the SD_MOUNT_BASE module constant to a temporary path, allowing
    tests to work with isolated mount point detection without affecting the system.

    Args:
        tmp_path: Built-in pytest fixture for temporary directories
        monkeypatch: Built-in pytest fixture for modifying module attributes

    Returns:
        str: Temporary mount base path (e.g., '/tmp/pytest-123/media')

    Example:
        def test_sd_detection(mock_sd_mount_base):
            # SD_MOUNT_BASE now points to temporary directory
            assert sd_monitor.SD_MOUNT_BASE == '/tmp/pytest-xxx/media'
    """
    sd_mount = tmp_path / "media"
    sd_mount.mkdir()
    monkeypatch.setattr("sd_monitor.SD_MOUNT_BASE", str(sd_mount))
    return str(sd_mount)


@pytest.fixture
def mock_os_listdir() -> Generator:
    """Mock os.listdir for SD card detection tests.

    Allows control over directory listing results during tests, enabling
    simulation of SD card mount point appearance and disappearance.

    Yields:
        MagicMock: Mock of os.listdir function

    Example:
        def test_sd_detection(mock_os_listdir):
            mock_os_listdir.return_value = ["usb_disk", "another_disk"]
    """
    with patch("sd_monitor.os.listdir") as mock_listdir:
        yield mock_listdir


@pytest.fixture
def mock_os_path_isdir() -> Generator:
    """Mock os.path.isdir for directory verification tests.

    Controls path type checking to differentiate between files and directories
    without requiring actual filesystem operations.

    Yields:
        MagicMock: Mock of os.path.isdir function

    Example:
        def test_directory_detection(mock_os_path_isdir):
            mock_os_path_isdir.side_effect = [False, True]  # First is file, second is dir
    """
    with patch("sd_monitor.os.path.isdir") as mock_isdir:
        yield mock_isdir


@pytest.fixture
def mock_os_access() -> Generator:
    """Mock os.access for permission checking tests.

    Controls permission verification results to test handling of accessible
    and inaccessible mount directories.

    Yields:
        MagicMock: Mock of os.access function

    Example:
        def test_permissions(mock_os_access):
            mock_os_access.return_value = False  # Simulate no read/execute access
    """
    with patch("sd_monitor.os.access") as mock_access:
        yield mock_access


@pytest.fixture
def mock_os_path_exists() -> Generator:
    """Mock os.path.exists for file existence checks.

    Controls file existence verification to test handling of missing or present
    configuration files without actual filesystem I/O.

    Yields:
        MagicMock: Mock of os.path.exists function

    Example:
        def test_missing_config(mock_os_path_exists):
            mock_os_path_exists.return_value = False  # Simulate missing file
    """
    with patch("sd_monitor.os.path.exists") as mock_exists:
        yield mock_exists


@pytest.fixture
def mock_signal_sigterm() -> Generator:
    """Mock signal.SIGTERM for process termination.

    Currently unused but available for advanced process signal testing.
    Note: signal.SIGTERM is typically accessed directly, not mocked.

    Yields:
        MagicMock: Mock of signal.SIGTERM
    """
    with patch("sd_monitor.signal.SIGTERM") as mock_sigterm:
        mock_sigterm.SIGTERM = 15
        yield mock_sigterm


@pytest.fixture
def mock_time_sleep() -> Generator:
    """Mock time.sleep to speed up tests.

    Prevents test slowdown from intentional delays in the polling loop.
    Allows verification that sleep() is called with correct intervals.

    Yields:
        MagicMock: Mock of time.sleep function

    Example:
        def test_polling_interval(mock_time_sleep):
            # Test runs instantly instead of sleeping for 2 seconds
            mock_time_sleep.assert_called_with(2)
    """
    with patch("sd_monitor.time.sleep") as mock_sleep:
        yield mock_sleep


@pytest.fixture
def reset_global_state(monkeypatch) -> Generator:
    """Reset global state variables between tests.

    Ensures test isolation by resetting module-level globals before and after each test.
    This prevents state leakage between tests that modify sd_monitor.process or
    sd_monitor.sd_was_removed.

    Args:
        monkeypatch: Built-in pytest fixture for modifying module attributes

    Yields:
        None

    Example:
        def test_process_state(reset_global_state):
            # Both globals start as None/False
            assert sd_monitor.process is None
            assert sd_monitor.sd_was_removed is False
    """
    monkeypatch.setattr("sd_monitor.process", None)
    monkeypatch.setattr("sd_monitor.sd_was_removed", False)
    yield
    # Cleanup after test
    monkeypatch.setattr("sd_monitor.process", None)
    monkeypatch.setattr("sd_monitor.sd_was_removed", False)


@pytest.fixture
def capture_subprocess_calls() -> Generator:
    """Capture all subprocess calls made during test execution.

    Records all Popen and run calls along with their arguments and keyword arguments.
    Useful for integration testing that needs to verify exact command-line arguments
    without actually executing system commands.

    Yields:
        list: List of tuples: (call_type, args, kwargs)
            - call_type: "Popen" or "run"
            - args: tuple of positional arguments
            - kwargs: dict of keyword arguments

    Example:
        def test_subprocess_calls(capture_subprocess_calls):
            # Make some subprocess calls
            sd_monitor.start_frame_manager("/tmp/sd")
            # Inspect captured calls
            assert len(capture_subprocess_calls) > 0
            call_type, args, kwargs = capture_subprocess_calls[0]
    """
    calls = []

    def capture_popen(*args, **kwargs):
        calls.append(("Popen", args, kwargs))
        return MagicMock()

    def capture_run(*args, **kwargs):
        calls.append(("run", args, kwargs))
        return MagicMock(returncode=0)

    with patch("sd_monitor.subprocess.Popen", side_effect=capture_popen):
        with patch("sd_monitor.subprocess.run", side_effect=capture_run):
            yield calls


@pytest.fixture
def mock_get_refresh_time() -> Generator:
    """Mock get_refresh_time function for integration tests.

    Replaces the get_refresh_time function with a mock that returns 600 by default.
    Use this when testing functions that call get_refresh_time without needing
    actual file I/O.

    Yields:
        MagicMock: Mock of get_refresh_time function

    Example:
        def test_with_mocked_time(mock_get_refresh_time):
            mock_get_refresh_time.return_value = 300
            # get_refresh_time() calls will return 300
    """
    with patch("sd_monitor.get_refresh_time") as mock_get_time:
        mock_get_time.return_value = 600
        yield mock_get_time


@pytest.fixture
def mock_start_frame_manager() -> Generator:
    """Mock start_frame_manager function for integration tests.

    Replaces the start_frame_manager function to prevent actual subprocess creation.
    Use this when testing functions that call start_frame_manager without needing
    to verify process creation details.

    Yields:
        MagicMock: Mock of start_frame_manager function

    Example:
        def test_with_mocked_frame_manager(mock_start_frame_manager):
            # start_frame_manager() calls are captured but not executed
            assert mock_start_frame_manager.call_count > 0
    """
    with patch("sd_monitor.start_frame_manager") as mock_start:
        yield mock_start


@pytest.fixture
def mock_monitor_sd_card() -> Generator:
    """Mock monitor_sd_card function for integration tests.

    Replaces the monitor_sd_card function to prevent the infinite polling loop.
    Use this when testing main() or other functions that call monitor_sd_card.

    Yields:
        MagicMock: Mock of monitor_sd_card function

    Example:
        def test_main_function(mock_monitor_sd_card):
            sd_monitor.main()
            # main() completes without hanging in infinite loop
            assert mock_monitor_sd_card.called
    """
    with patch("sd_monitor.monitor_sd_card") as mock_monitor:
        yield mock_monitor


@pytest.fixture
def mock_cleanup_stale_mounts() -> Generator:
    """Mock cleanup_stale_mounts function for integration tests.

    Replaces the cleanup_stale_mounts function to prevent actual file system
    operations. Use this when testing main() or other functions that call
    cleanup_stale_mounts.

    Yields:
        MagicMock: Mock of cleanup_stale_mounts function

    Example:
        def test_main_order(mock_cleanup_stale_mounts, mock_monitor_sd_card):
            sd_monitor.main()
            # Verify cleanup was called
            assert mock_cleanup_stale_mounts.called
    """
    with patch("sd_monitor.cleanup_stale_mounts") as mock_cleanup:
        yield mock_cleanup


@pytest.fixture
def username_pi(monkeypatch) -> str:
    """Mock USERNAME to be 'pi' for consistent tests.

    Sets USERNAME constant to "pi" to simulate running on default Raspberry Pi
    without sudo elevation.

    Args:
        monkeypatch: Built-in pytest fixture for modifying module attributes

    Returns:
        str: "pi"

    Example:
        def test_default_username(username_pi):
            assert sd_monitor.USERNAME == "pi"
            assert "/media/pi" in sd_monitor.SD_MOUNT_BASE
    """
    monkeypatch.setenv("SUDO_USER", "")
    monkeypatch.setenv("USER", "pi")
    monkeypatch.setattr("sd_monitor.USERNAME", "pi")
    return "pi"


@pytest.fixture
def username_sudo(monkeypatch) -> str:
    """Mock USERNAME to be resolved from SUDO_USER.

    Sets USERNAME constant to "sudouser" to simulate script running with sudo
    elevation from a regular user.

    Args:
        monkeypatch: Built-in pytest fixture for modifying module attributes

    Returns:
        str: "sudouser"

    Example:
        def test_sudo_username(username_sudo):
            assert sd_monitor.USERNAME == "sudouser"
            assert "/media/sudouser" in sd_monitor.SD_MOUNT_BASE
    """
    monkeypatch.setenv("SUDO_USER", "sudouser")
    monkeypatch.setenv("USER", "normaluser")
    monkeypatch.setattr("sd_monitor.USERNAME", "sudouser")
    return "sudouser"


@pytest.fixture
def autouse_print_suppression(capsys) -> Generator:
    """Suppress print output during tests for cleaner output.

    Clears captured output after each test to keep test output clean.

    Args:
        capsys: Built-in pytest fixture for capturing print output

    Yields:
        None

    Note:
        This fixture is rarely used directly. Tests typically use capsys parameter
        to assert on print output when needed.
    """
    yield
    capsys.readouterr()  # Clear captured output
