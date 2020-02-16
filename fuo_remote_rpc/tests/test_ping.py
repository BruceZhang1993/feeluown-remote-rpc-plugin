import jsonrpcclient
import json


def test_ping():
    response = jsonrpcclient.request('http://127.0.0.1:27000/jsonrpc', 'ping')
    assert response is not None
    assert isinstance(response, jsonrpcclient.Response)
    assert response.data.ok is True
    assert response.data.jsonrpc == '2.0'
    assert json.loads(response.data.result) == 'pong'
