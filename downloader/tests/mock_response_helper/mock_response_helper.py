# source: https://gist.github.com/evansde77/45467f5a7af84d2a2d34f3fcb357449c
from unittest import mock


def get_mock_response(status=200, text=None, raise_for_status=None):
    mock_resp = mock.Mock()
    # mock raise_for_status call w/optional error
    mock_resp.raise_for_status = mock.Mock()
    if raise_for_status:
        mock_resp.raise_for_status.side_effect = raise_for_status
    # set status code and content
    mock_resp.status_code = status
    mock_resp.text = text
    return mock_resp
