import jsonrpcclient
import json


def test_ping():
    response = jsonrpcclient.request('http://127.0.0.1:27000/jsonrpc', 'ping')
    assert response is not None
    assert isinstance(response, jsonrpcclient.Response)
    assert response.data.ok
    assert response.data.jsonrpc == '2.0'
    assert response.data.result == 'pong'


def test_status():
    response = jsonrpcclient.request('http://127.0.0.1:27000/jsonrpc', 'status')
    assert response is not None
    assert isinstance(response, jsonrpcclient.Response)
    assert response.data.ok
    assert response.data.jsonrpc == '2.0'
    assert isinstance(response.data.result, dict)
    assert 'track' in response.data.result
    assert 'player' in response.data.result
    assert 'live_lyric' in response.data.result
    assert isinstance(response.data.result['track'], dict)
    assert isinstance(response.data.result['player'], dict)
    assert isinstance(response.data.result['live_lyric'], str)
    assert 'provider' in response.data.result['track']
    assert 'title' in response.data.result['track']
    assert 'artists' in response.data.result['track']
    assert 'album' in response.data.result['track']
    assert 'duration' in response.data.result['track']
    assert isinstance(response.data.result['track']['provider'], str)
    assert isinstance(response.data.result['track']['title'], str)
    assert isinstance(response.data.result['track']['artists'], list)
    assert isinstance(response.data.result['track']['album'], str)
    assert isinstance(response.data.result['track']['duration'], float)
