from src.router import osc_in_callbacks


def test_on_receive_osc_routes_value():
    osc_in_callbacks.ROUTER_STATE.clear()
    osc_in_callbacks.onReceiveOSC(
        dat=None,
        rowIndex=0,
        message='',
        byteData=b'',
        timeStamp=0.0,
        address='/fader/1',
        args=[0.75],
        peer=None,
    )
    assert osc_in_callbacks.ROUTER_STATE.get('fader_1') == 0.75
