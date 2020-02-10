import pytest

from IncognitoChain.Helpers.Logging import *
from IncognitoChain.Objects.AccountObject import get_accounts_in_shard

receiver = get_accounts_in_shard(5)[0]
sender = get_accounts_in_shard(4)[0]
send_amount = 1000


@pytest.mark.parametrize('fee,privacy', [(-1, 0), (2, 0), (-1, 1), (2, 1)])
def test_send_prv_cross_shard_with_fee_privacy(fee, privacy):
    INFO(f"Verify send PRV to another address Xshard successfully with privacy={privacy} fee={fee}")
    STEP(1, "Get sender balance")
    sender_bal = sender.get_prv_balance()
    INFO(f"Sender balance before: {sender_bal}")

    STEP(2, "Get receiver balance")
    receiver_bal = receiver.get_prv_balance()
    INFO(f"receiver balance before: {receiver_bal}")

    STEP(3, " send PRV")
    send_transaction = sender.send_prv_to(receiver, send_amount, fee=fee, privacy=privacy)
    INFO("Transaction ID: " + send_transaction.get_tx_id())
    assert_true(send_transaction.get_error_msg() != 'Can not create tx', "transaction failed",
                "make transaction success")

    STEP(4, "Subcribe transaction")
    send_transaction_result = send_transaction.subscribe_transaction()

    STEP(5, "Subcribe cross transaction by privatekey")
    receiver.subscribe_cross_output_coin()

    STEP(6, "Check sender balance")
    sender_bal_after = sender.get_prv_balance()
    INFO(f"sender balance after: {sender_bal_after}")
    assert_true(sender_bal_after == sender_bal - send_amount - send_transaction.get_transaction_by_hash().get_fee(),
                "something wrong")  # when privacy=1, ws cannot get fee

    STEP(7, "Check receiver balance")
    receiver_bal_after = receiver.get_prv_balance()
    INFO(f"receiver balance after: {receiver_bal_after}")
    assert_true(receiver_bal_after == receiver_bal + send_amount, "something wrong")

    STEP(8, "Check transaction privacy")
    if privacy == 0:
        assert_true(not send_transaction.is_private_transaction(), "transaction must be no privacy ",
                    "transaction is not privacy")

    if privacy == 1:
        assert_true(send_transaction.is_private_transaction(), "transaction must be no privacy ",
                    "transaction is not privacy")