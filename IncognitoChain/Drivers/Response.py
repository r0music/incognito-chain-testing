import json

import IncognitoChain.Helpers.Logging as Log


class Response:
    def __init__(self, json_response):
        self.response = json_response
        Log.DEBUG(f'\n{json.dumps(self.response, indent=3)}')

    def is_success(self):
        if self.response['Error'] is None:
            return True
        return False

    def get_error_trace(self):
        if self.response['Error'] is None:
            return ''
        return self.response['Error']['StackTrace'][0:256]

    def get_error_msg(self):
        if self.response['Error'] is None:
            return None
        return self.response['Error']['Message']

    def find_in_result(self, string):
        for k, v in self.response["Result"].items():
            if k == str(string):
                return True
        return False

    def get_result(self, string=None):
        if string is None:
            return self.response['Result']
        return self.response['Result'][string]

    def get_tx_id(self):
        return self.get_result("TxID")

    def get_beacon_height(self):
        return self.get_result("BeaconHeight")

    def get_pde_pool_pairs(self):
        return self.get_result("PDEPoolPairs")

    def get_pde_share(self):
        return self.get_result("PDEShares")

    def get_token_id_1(self):
        return self.get_result("TokenID1Str")

    def get_token_id_2(self):
        return self.get_result("TokenID2Str")

    def get_returned_1_amount(self):
        return self.get_result("Returned1Amount")

    def get_returned_2_amount(self):
        return self.get_result("Returned2Amount")

    def get_contributed_1_amount(self):
        return self.get_result("Contributed1Amount")

    def get_contributed_2_amount(self):
        return self.get_result("Contributed2Amount")

    def get_fee(self):
        try:
            return self.response['Result']['Result']['Fee']
        except KeyError:
            return self.response['Result']['Fee']

    def get_privacy(self):
        return self.get_result("IsPrivacy")

    def get_balance(self):
        return self.get_result()

    def get_block_height(self):
        return self.get_result("BlockHeight")

    def subscribe_transaction(self):
        from IncognitoChain.Objects.IncognitoTestCase import SUT
        return SUT.full_node.subscription().subscribe_pending_transaction(self.get_tx_id())

    def is_private_transaction(self):
        from IncognitoChain.Objects.IncognitoTestCase import SUT
        result = SUT.full_node.transaction().get_tx_by_hash(self.get_tx_id())
        if result.get_privacy() is True and \
                result.get_result()['ProofDetail']['InputCoins'][0]['CoinDetails']['Value'] == 0:
            return True
        return False

    def get_transaction_by_hash(self):
        from IncognitoChain.Objects.IncognitoTestCase import SUT
        return SUT.full_node.transaction().get_tx_by_hash(self.get_tx_id())