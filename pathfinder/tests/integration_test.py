# -*- coding: utf-8 -*-
from random import sample, randint

import gevent
from numpy.random.mtrand import choice
from raiden_contracts.contract_manager import ContractManager

from pathfinder.pathfinding_service import PathfindingService
from pathfinder.tests.config import NUMBER_OF_NODES, NUMBER_OF_CHANNELS
from pathfinder.tests.fixtures import Mock, Web3
from raiden_libs.blockchain import BlockchainListener

from pathfinder.token_network import TokenNetwork


def test_integration(
    generate_raiden_clients,
    ethereum_tester,
    wait_for_blocks,
    web3: Web3,
    contracts_manager: ContractManager,
    blockchain_listener: BlockchainListener

):
    blockchain_listener.required_confirmations = 1
    nodes = generate_raiden_clients(5)
    channels = [list(choice(nodes, 2, replace=False)) for _ in range(10)]


    pathfinding_service = PathfindingService(
        web3,
        contracts_manager,
        transport=Mock(),
        token_network_listener=blockchain_listener,
        follow_networks=[nodes[0].contract.address]
    )
    pathfinding_service.token_network_listener.start()
    for channel in channels:

        c1, c2 = channel[0], channel[1]
        c1.open_channel(c2.address)
        ethereum_tester.mine_blocks(1)
        gevent.sleep(1)

    pathfinding_service.token_network_listener.stop()
    print(pathfinding_service.token_networks[0].G.edges())

    """
        amount1, amount2 = randint(1, 100), randint(1, 100)
        c1.deposit_to_channel(c2.address, amount1)
        c2.deposit_to_channel(c1.address, amount2)
        ethereum_tester.mine_blocks(1)
        print(c1.sync_open_channels())
        print(c2.sync_open_channels())
        for key in pathfinding_service.token_networks.keys():
            print(pathfinding_service.token_networks[key].G.nodes())"""
    """
    for channel_id in range(NUMBER_OF_CHANNELS):
        private_key1, private_key2 = random.sample(private_keys, 2)
        address1 = Address(private_key_to_address(private_key1))
        address2 = Address(private_key_to_address(private_key2))
        fee1 = abs(random.gauss(0.0002, 0.0001))
        fee2 = abs(random.gauss(0.0002, 0.0001))
        signature1 = forge_fee_signature(private_key1, fee1)
        signature2 = forge_fee_signature(private_key2, fee2)
        token_network.handle_channel_opened_event(
            channel_id,
            address1,
            address2
        )

        # deposit to channels
        deposit1, deposit2 = random.sample(range(1000), 2)
        address1, address2 = token_network.channel_id_to_addresses[channel_id]
        token_network.handle_channel_new_deposit_event(
            channel_id,
            address1,
            deposit1
        )
        token_network.handle_channel_new_deposit_event(
            channel_id,
            address2,
            deposit2 )
        """
    """ Test confirmed and unconfirmed events. """
    """events_confirmed = []
    events_unconfirmed = []
    blockchain_listener.add_confirmed_listener(
        'ChannelOpened',
        lambda e: events_confirmed.append(e)
    )
    blockchain_listener.add_unconfirmed_listener(
        'ChannelOpened',
        lambda e: events_unconfirmed.append(e)
    )
    nodes = generate_raiden_clients(5)
    channels = [list(choice(nodes, 2, replace=False)) for _ in range(10)]
    print (channels, len(channels))
    # start the blockchain listener
    blockchain_listener.start()
    for channel in channels:
        c1, c2 = channel[0], channel[1]
        c1.open_channel(c2.address)
        amount1, amount2 = randint(1, 100), randint(1, 100)
        c1.deposit_to_channel(c2.address, amount1)
        c2.deposit_to_channel(c1.address, amount2)
        ethereum_tester.mine_blocks(1)
        print (c1.sync_open_channels())
        print (c2.sync_open_channels())
    blockchain_listener.stop()"""

