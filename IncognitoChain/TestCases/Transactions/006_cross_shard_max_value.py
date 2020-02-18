import re

from IncognitoChain.Helpers.Logging import *
from IncognitoChain.Objects.AccountObject import get_accounts_in_shard

receiver = get_accounts_in_shard(5)[0]
sender = get_accounts_in_shard(4)[0]
send_amount = 10000
max_fee = 900000000000000
max_send_amount = 1000000000000000001


def setup_function():
    sender_bal = sender.get_prv_balance()
    assert sender_bal >= max_fee + send_amount, '!!! Not enough prv to run this test, skip'


def test_send_prv_privacy_x_shard_max_value():
    INFO("""
         Verify send PRV to another address:
         -  > 10 mil PRV unsuccess
         - Tx fee = 100000000000 PRV success
         """)
    STEP(1, "Get sender balance")
    receiver_bal = receiver.get_prv_balance()
    INFO(f"Sender Balance: {receiver_bal}")

    STEP(2, "Get receiver balance")
    sender_bal = sender.get_prv_balance()
    INFO(f"Receiver Balance: {sender_bal}")
    assert sender_bal != 0, "Sender balance = 0, stop this testcase"

    STEP(3, "From address3 send prv to address1 - max value")
    # send amount = 1000000000000000000
    step3_result = sender.send_prv_to(receiver, max_send_amount)
    assert step3_result.get_error_msg() == 'Can not create tx', "something went wrong, this tx must failed"
    assert re.search(r'Not enough coin', step3_result.get_error_trace().get_message()), "something went so wrong"

    STEP(4, "From address3 send prv to address1 - max value fee ")
    # send with fee = 10000000000000 PRV
    step4_result = sender.send_prv_to(receiver, send_amount, fee=max_fee)
    assert step4_result.get_error_msg() == 'Can not create tx', "something went wrong, this tx must failed"
    assert re.search(r'input value less than output value',
                     step4_result.get_error_trace().get_message()), "something went so wrong"