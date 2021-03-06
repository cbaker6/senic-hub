from unittest import mock

from pytest import fixture


@fixture
def url(route_url):
    return route_url('configuration')


@mock.patch('senic_hub.backend.commands.supervisor.restart_program')
@mock.patch('senic_hub.backend.views.config.sleep')
@mock.patch('senic_hub.backend.views.config.stop_program')
def test_setup_create_config_returns_200_and_creates_files(
        stop_program_mock, sleep_mock, restart_program_mock,
        url, browser):
    assert browser.post_json(url, {}, status=200)
    stop_program_mock.assert_called_once_with('device_discovery')
    # TODO: Test for home-assistant being restarted once it's part of SenicOS
    restart_program_mock.assert_has_calls([
        # mock.call('homeassistant'),
        mock.call('nuimo_app')
    ])


@mock.patch('senic_hub.backend.views.config.subprocess.Popen')
def test_setup_delete_config_returns_200_and_creates_files(
        subprocess_mock, url, browser):
    assert browser.delete(url, status=200)
    subprocess_mock.assert_called_with(['/usr/bin/senic_hub_factory_reset'])
