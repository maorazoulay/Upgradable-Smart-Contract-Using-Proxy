from scripts.helpful_scripts import encode_function_data, get_account, upgrade
from brownie import (
    accounts,
    network,
    Box,
    ProxyAdmin,
    TransparentUpgradeableProxy,
    Contract,
    BoxV2,
)


def main():
    account = get_account()
    from_account = {"from": account}
    print(f"Deploying to {network.show_active()}")
    box = Box.deploy(from_account, publish_source=True)

    proxy_admin = ProxyAdmin.deploy(from_account, publish_source=True)
    # initializer = box.store, 1
    box_encoded_initializer_function = encode_function_data()
    proxy = TransparentUpgradeableProxy.deploy(
        box.address,
        proxy_admin,
        box_encoded_initializer_function,
        from_account,
        publish_source=True,
    )
    print(f"Proxy deployed to {proxy}, you can now upgrade to V2!")
    proxy_box = Contract.from_abi("Box", proxy.address, Box.abi)
    proxy_box.store(1, from_account)

    # Upgarde
    box_v2 = BoxV2.deploy(from_account, publish_source=True)
    upgrade_transaction = upgrade(
        account, proxy, box_v2.address, proxy_admin_contract=proxy_admin
    )
    upgrade_transaction.wait(1)
    print("Proxy has been upgraded")
    proxy_box = Contract.from_abi("BoxV2", proxy.address, BoxV2.abi)
    proxy_box.increment(from_account)
    print(proxy_box.retrieve())
