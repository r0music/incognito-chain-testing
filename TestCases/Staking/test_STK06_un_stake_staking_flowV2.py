"This testscript only use for staking flow V2."

import pytest

from Configs.Constants import coin
from Configs.Configs import ChainConfig
from Helpers.Logging import INFO, STEP
from Helpers.TestHelper import ChainHelper
from Helpers.Time import WAIT
from Objects.AccountObject import COIN_MASTER
from Objects.IncognitoTestCase import SUT
from TestCases.Staking import account_x, account_y, account_t


@pytest.mark.parametrize("the_stake, validator, receiver_reward, auto_re_stake", [
    (account_y, account_y, account_y, False),
    (account_y, account_y, account_x, False),
    (account_x, account_y, account_x, False),
    (account_x, account_y, account_y, False),
    (account_x, account_y, account_t, False),
    (account_y, account_y, account_y, True),
    (account_y, account_y, account_x, True),
    (account_x, account_y, account_x, True),
    (account_x, account_y, account_y, True),
    (account_x, account_y, account_t, True),
])
def test_un_stake_when_waiting(the_stake, validator, receiver_reward, auto_re_stake):
    beacon_bsd = SUT().get_beacon_best_state_detail_info()
    if beacon_bsd.get_auto_staking_committees(validator) is True:
        pytest.skip(f'validator {validator.validator_key} is existed in committee with auto re-stake: True')
    elif beacon_bsd.get_auto_staking_committees(validator) is False:
        validator.stk_wait_till_i_am_out_of_autostaking_list()

    COIN_MASTER.top_up_if_lower_than(the_stake, coin(1751), coin(1850))
    bal_b4_stake = the_stake.get_balance()

    INFO('Calculate & wait to execute test at block that after random time 0-5 block')
    chain_info = SUT().get_block_chain_info()
    remaining_block_epoch = chain_info.get_beacon_block().get_remaining_block_epoch()
    if remaining_block_epoch >= ChainConfig.RANDOM_TIME:
        ChainHelper.wait_till_next_beacon_height(remaining_block_epoch - ChainConfig.RANDOM_TIME)
    elif remaining_block_epoch < 5:
        ChainHelper.wait_till_next_epoch(1, ChainConfig.RANDOM_TIME)

    STEP(1, 'Staking')
    fee_stk = the_stake.stake(validator, receiver_reward, auto_re_stake=auto_re_stake).subscribe_transaction().get_fee()
    bal_af_stake = the_stake.wait_for_balance_change(from_balance=bal_b4_stake,
                                                     least_change_amount=(- fee_stk - ChainConfig.STK_AMOUNT))
    assert bal_af_stake == bal_b4_stake - fee_stk - ChainConfig.STK_AMOUNT

    validator.stk_wait_till_i_am_in_waiting_next_random()

    INFO(f'Wait 40s to shard confirm')
    WAIT(40)
    beacon_bsd = SUT().get_beacon_best_state_detail_info()
    if beacon_bsd.is_he_in_waiting_next_random(validator) is False:
        pytest.skip(f'validator {validator.validator_key} must exist in the list waiting for random')

    STEP(2, 'Un_staking')
    fee_un_stk = the_stake.stk_un_stake_tx(validator).subscribe_transaction().get_fee()
    WAIT(60)  # wait to he swap out, is not validator

    STEP(3, 'Verify validator swap out')
    beacon_bsd = SUT().get_beacon_best_state_detail_info()
    assert beacon_bsd.get_auto_staking_committees(validator) is None

    STEP(4, 'Verify balance')
    bal_af_un_stake = the_stake.wait_for_balance_change(from_balance=bal_af_stake,
                                                        least_change_amount=(ChainConfig.STK_AMOUNT - fee_un_stk),
                                                        timeout=4000)
    assert bal_af_un_stake == bal_b4_stake - fee_stk - fee_un_stk


@pytest.mark.parametrize("the_stake, validator, receiver_reward, auto_re_stake", [
    pytest.param(account_y, account_y, account_y, False,
                 marks=pytest.mark.xfail(reason="auto re stake = False, can not un stake")),
    pytest.param(account_y, account_y, account_x, False,
                 marks=pytest.mark.xfail(reason="auto re stake = False, can not un stake")),
    pytest.param(account_x, account_y, account_x, False,
                 marks=pytest.mark.xfail(reason="auto re stake = False, can not un stake")),
    pytest.param(account_x, account_y, account_y, False,
                 marks=pytest.mark.xfail(reason="auto re stake = False, can not un stake")),
    pytest.param(account_x, account_y, account_t, False,
                 marks=pytest.mark.xfail(reason="auto re stake = False, can not un stake")),
    (account_y, account_y, account_y, True),
    (account_y, account_y, account_x, True),
    (account_x, account_y, account_x, True),
    (account_x, account_y, account_y, True),
    (account_x, account_y, account_t, True),
])
def test_un_stake_when_exist_pending(the_stake, validator, receiver_reward, auto_re_stake):
    beacon_bsd = SUT().get_beacon_best_state_detail_info()
    if beacon_bsd.get_auto_staking_committees(validator) is True:
        pytest.skip(f'validator {validator.validator_key} is existed in committee with auto re-stake: True')
    elif beacon_bsd.get_auto_staking_committees(validator) is False:
        validator.stk_wait_till_i_am_out_of_autostaking_list()

    COIN_MASTER.top_up_if_lower_than(the_stake, coin(1751), coin(1850))
    bal_b4_stake = the_stake.get_balance()

    STEP(1, 'Staking')
    fee_stk = the_stake.stake(validator, receiver_reward, auto_re_stake=auto_re_stake).subscribe_transaction().get_fee()
    bal_af_stake = the_stake.wait_for_balance_change(from_balance=bal_b4_stake,
                                                     least_change_amount=(- fee_stk - ChainConfig.STK_AMOUNT))
    assert bal_af_stake == bal_b4_stake - fee_stk - ChainConfig.STK_AMOUNT

    validator.stk_wait_till_i_am_in_shard_pending()

    STEP(2, 'Un_staking')
    fee_un_stk = the_stake.stk_un_stake_tx(validator).subscribe_transaction().get_fee()
    bal_af_un_stake = the_stake.wait_for_balance_change(from_balance=bal_af_stake, least_change_amount=-fee_un_stk)
    assert bal_af_un_stake == bal_af_stake - fee_un_stk

    WAIT(60)  # wait to convert status auto re-stake

    STEP(3, 'Verify auto staking is False')
    beacon_bsd = SUT().get_beacon_best_state_detail_info()
    assert beacon_bsd.get_auto_staking_committees(validator) is False


@pytest.mark.parametrize("the_stake, validator, receiver_reward, auto_re_stake", [
    pytest.param(account_y, account_y, account_y, False,
                 marks=pytest.mark.xfail(reason="auto re stake = False, can not un stake")),
    pytest.param(account_y, account_y, account_x, False,
                 marks=pytest.mark.xfail(reason="auto re stake = False, can not un stake")),
    pytest.param(account_x, account_y, account_x, False,
                 marks=pytest.mark.xfail(reason="auto re stake = False, can not un stake")),
    pytest.param(account_x, account_y, account_y, False,
                 marks=pytest.mark.xfail(reason="auto re stake = False, can not un stake")),
    pytest.param(account_x, account_y, account_t, False,
                 marks=pytest.mark.xfail(reason="auto re stake = False, can not un stake")),
    (account_y, account_y, account_y, True),
    (account_y, account_y, account_x, True),
    (account_x, account_y, account_x, True),
    (account_x, account_y, account_y, True),
    (account_x, account_y, account_t, True),
])
def test_un_stake_when_exist_shard_committee(the_stake, validator, receiver_reward, auto_re_stake):
    beacon_bsd = SUT().get_beacon_best_state_detail_info()
    if beacon_bsd.get_auto_staking_committees(validator) is True:
        pytest.skip(f'validator {validator.validator_key} is existed in committee with auto re-stake: True')
    elif beacon_bsd.get_auto_staking_committees(validator) is False:
        validator.stk_wait_till_i_am_out_of_autostaking_list()

    COIN_MASTER.top_up_if_lower_than(the_stake, coin(1751), coin(1850))
    bal_b4_stake = the_stake.get_balance()

    STEP(1, 'Staking')
    fee_stk = the_stake.stake(validator, receiver_reward, auto_re_stake=auto_re_stake).subscribe_transaction().get_fee()
    bal_af_stake = the_stake.wait_for_balance_change(from_balance=bal_b4_stake,
                                                     least_change_amount=(- fee_stk - ChainConfig.STK_AMOUNT))
    assert bal_af_stake == bal_b4_stake - fee_stk - ChainConfig.STK_AMOUNT

    validator.stk_wait_till_i_am_committee()

    STEP(2, 'Un_staking')
    fee_un_stk = the_stake.stk_un_stake_tx(validator).subscribe_transaction().get_fee()
    bal_af_un_stake = the_stake.wait_for_balance_change(from_balance=bal_af_stake, least_change_amount=-fee_un_stk)
    assert bal_af_un_stake == bal_af_stake - fee_un_stk

    WAIT(60)  # wait to convert status auto re-stake

    STEP(3, 'Verify auto staking is False')
    beacon_bsd = SUT().get_beacon_best_state_detail_info()
    assert beacon_bsd.get_auto_staking_committees(validator) is False
