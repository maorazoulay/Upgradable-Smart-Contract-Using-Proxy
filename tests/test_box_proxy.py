from scripts.helpful_scripts import get_account, encode_function_data
from brownie import Box, ProxyAdmin, TransparentUpgradeableProxy, Contract


def test_proxy_delegates_calls():
    account = get_account()
    from_account = {"from": account}
    box = Box.deploy(from_account)
    proxy_admin = ProxyAdmin.deploy(from_account)
    box_encoded_initializer_function = encode_function_data()
    proxy = TransparentUpgradeableProxy.deploy(
        box.address, proxy_admin, box_encoded_initializer_function, from_account
    )
    proxy_box = Contract.from_abi("Box", proxy.address, Box.abi)
    assert proxy_box.retrieve() == 0
    proxy_box.store(1, from_account)
    assert proxy_box.retrieve() == 1
