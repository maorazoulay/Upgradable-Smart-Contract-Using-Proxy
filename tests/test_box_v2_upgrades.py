from scripts.helpful_scripts import get_account, encode_function_data, upgrade
from brownie import (
    Box,
    ProxyAdmin,
    TransparentUpgradeableProxy,
    Contract,
    BoxV2,
    exceptions,
)
import pytest


def test_proxy_upgrades():
    account = get_account()
    from_account = {"from": account}
    box = Box.deploy(from_account)
    proxy_admin = ProxyAdmin.deploy(from_account)
    box_encoded_initializer_function = encode_function_data()
    proxy = TransparentUpgradeableProxy.deploy(
        box.address, proxy_admin, box_encoded_initializer_function, from_account
    )
    # Upgarde
    box_v2 = BoxV2.deploy(from_account)
    proxy_box = Contract.from_abi("BoxV2", proxy.address, BoxV2.abi)
    with pytest.raises(exceptions.VirtualMachineError):
        proxy_box.increment(from_account)
    upgrade_transaction = upgrade(
        account, proxy, box_v2.address, proxy_admin_contract=proxy_admin
    )
    upgrade_transaction.wait(1)
    assert proxy_box.retrieve() == 0
    proxy_box.increment(from_account)
    assert proxy_box.retrieve() == 1
