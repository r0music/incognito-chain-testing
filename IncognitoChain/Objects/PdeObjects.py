import copy

from IncognitoChain.Helpers.Logging import INFO, WARNING, DEBUG
from IncognitoChain.Helpers.TestHelper import extract_incognito_addr, l6
from IncognitoChain.Helpers.Time import WAIT
from IncognitoChain.Objects import BlockChainInfoBaseClass


class PDEStateInfo(BlockChainInfoBaseClass):

    def get_waiting_contributions(self):
        raw_waiting_list = self.data['WaitingPDEContributions']
        waiting_contribute_objs = []
        for k, v in raw_waiting_list.items():
            waiting_contribute_data = {k: v}
            waiting_contribute_obj = _WaitingContribution(waiting_contribute_data)
            waiting_contribute_objs.append(waiting_contribute_obj)
        return waiting_contribute_objs

    def find_waiting_contribution_of_user(self, account, pair_id=None, token_id=None):
        """

        :param account:
        :type account: Account obj Payment addr
        :param pair_id:
        :type pair_id:
        :param token_id:
        :type token_id:
        :return:
        :rtype:
        """
        user_payment_addr = extract_incognito_addr(account)
        contribution_list = []

        INFO(f'Finding pair id {pair_id} of user {l6(user_payment_addr)} in PDE contribution waiting list')
        waiting_contributions = self.get_waiting_contributions()
        for contribution in waiting_contributions:
            addr = contribution.get_contributor_address()
            p_id = contribution.get_pair_id()
            token = contribution.get_token_id()

            match = True if addr == user_payment_addr else False
            if pair_id is not None:
                match = True if (p_id == pair_id) and match else False
            if token_id is not None:
                match = True if (token == token_id) and match else False

            if match:
                INFO(f'Found contribution of token {l6(contribution.get_token_id())} '
                     f'at beacon {contribution.get_beacon_height()} '
                     f'with amount {contribution.get_amount()}')
                contribution_list.append(contribution)

        if len(contribution_list) == 0:
            INFO(f'Payment addr {l6(user_payment_addr)} '
                 f'is not in PDE contribution waiting list with pair id: {pair_id}')
        return contribution_list

    def get_pde_pool_pairs(self):
        pool_pair_objs = []
        pool_pair_raw = self.data['PDEPoolPairs']
        for k, v in pool_pair_raw.items():
            pool_pair_data = {k: v}
            pool_pair_obj = _PoolPair(pool_pair_data)
            pool_pair_objs.append(pool_pair_obj)
        return pool_pair_objs

    def _get_contributor_rewards(self, user=None, token1=None, token2=None):
        DEBUG('==================================================================================================')
        of_user = 'any' if user is None else l6(extract_incognito_addr(user))
        tok1 = 'any' if token1 is None else l6(token1)
        tok2 = 'any' if token1 is None else l6(token2)
        INFO(f'Getting PDE reward of contributor and tokens at beacon height time stamp {self.get_beacon_time_stamp()}:'
             f' {of_user}:{tok1}-{tok2}')

        reward_pool = []
        reward_pool_raw = self.data['PDETradingFees']
        for k, v in reward_pool_raw.items():
            reward_raw_data = {k: v}
            reward_obj = _PdeReward(reward_raw_data)

            DEBUG(f"Checking reward: {reward_obj}")
            match = True
            debug_msg = ''
            if user is not None:
                user = extract_incognito_addr(user)
                if user == reward_obj.get_payment_k():
                    match = True
                    debug_msg += f'user {of_user} | '
                else:
                    DEBUG(f'NOT Match user {of_user}')
                    continue
            # breakpoint()
            if token1 is not None and token2 is not None:
                if token1 == reward_obj.get_token1_id() and token2 == reward_obj.get_token2_id():
                    debug_msg += f'token 1->1, 2->2 {tok1}-{tok2} | '
                    match = True
                elif token1 == reward_obj.get_token2_id() and token2 == reward_obj.get_token1_id():
                    debug_msg += f'token 1->2, 2->1 {tok2}-{tok1} | '
                    match = True
                else:
                    match = False

            if match:
                DEBUG(f"MATCH {debug_msg}: {reward_obj}")
                reward_pool.append(reward_obj)
        if not reward_pool:  # empty list
            INFO("Not found")
        return reward_pool

    def get_contributor_reward(self, user=None, token1=None, token2=None):
        """
        :param user: Account or payment k
        :param token1:
        :param token2:
        :return: int value if found one, list of int if found many
        """
        share_objects = self._get_contributor_rewards(user, token1, token2)
        list_amount = []
        for obj in share_objects:
            list_amount.append(obj.get_amount())

        if len(list_amount) == 1:
            return list_amount[0]
        elif len(list_amount) > 1:
            return list_amount
        return None

    def _get_pde_shares(self, user=None, token1=None, token2=None):
        DEBUG('==================================================================================================')
        of_user = 'any' if user is None else l6(extract_incognito_addr(user))
        tok1 = 'any' if token1 is None else l6(token1)
        tok2 = 'any' if token1 is None else l6(token2)
        INFO(f'Getting share of user and tokens at beacon height time stamp {self.get_beacon_time_stamp()}: '
             f'{of_user}:{tok1}-{tok2}')

        pde_share_raw = self.data['PDEShares']
        pde_share_objs = []
        for k, v in pde_share_raw.items():
            pde_share_data = {k: v}
            pde_share_obj = _PdeShare(pde_share_data)

            DEBUG(f"Checking share: {pde_share_obj}")
            match = True
            debug_msg = ''
            if user is not None:
                user = extract_incognito_addr(user)
                if user == pde_share_obj.get_payment_k():
                    match = True
                    debug_msg += f'user {of_user} | '
                else:
                    DEBUG(f'NOT Match user {of_user}')
                    continue
            # breakpoint()
            if token1 is not None and token2 is not None:
                if token1 == pde_share_obj.get_token1_id() and token2 == pde_share_obj.get_token2_id():
                    debug_msg += f'token 1->1, 2->2 {tok1}-{tok2} | '
                    match = True
                elif token1 == pde_share_obj.get_token2_id() and token2 == pde_share_obj.get_token1_id():
                    debug_msg += f'token 1->2, 2->1 {tok2}-{tok1} | '
                    match = True
                else:
                    match = False

            if match:
                DEBUG(f"MATCH {debug_msg}: {pde_share_obj}")
                pde_share_objs.append(pde_share_obj)
        if not pde_share_objs:  # empty list
            INFO("Not found")
        return pde_share_objs

    def get_pde_shares_amount(self, user=None, token1=None, token2=None):
        """

        :param user: Account or payment k
        :param token1:
        :param token2:
        :return: int value if found one, list of int if found many
        """
        share_objects = self._get_pde_shares(user, token1, token2)
        list_amount = []
        for obj in share_objects:
            list_amount.append(obj.get_share_amount())

        if len(list_amount) == 1:
            return list_amount[0]
        elif len(list_amount) > 1:
            return list_amount

    def get_beacon_time_stamp(self):
        return self.data["BeaconTimeStamp"]

    def get_rate_between_token(self, token1, token2):
        pool_pair = self.get_pde_pool_pairs()
        for pair in pool_pair:
            if pair.get_token1_id() == token1:
                if pair.get_token2_id() == token2:
                    return [pair.get_token1_pool_value(), pair.get_token2_pool_value()]
            elif pair.get_token2_id() == token1:
                if pair.get_token1_id() == token2:
                    return [pair.get_token2_pool_value(), pair.get_token1_pool_value()]

    def sum_share_pool_of_pair(self, user=None, token1=None, token2=None):
        INFO(f'Calculating sum share of pair...')
        share_pool = self.get_pde_shares_amount(user, token1, token2)
        sum_pool = sum(share_pool) if type(share_pool) is list else share_pool
        INFO(f'Sum share = {sum_pool}')
        return sum_pool

    def sum_contributor_reward_of_pair(self, user=None, token1=None, token2=None):
        INFO(f'Calculating PDE reward of pair...')
        reward_pool = self.get_contributor_reward(user, token1, token2)
        sum_reward = sum(reward_pool) if type(reward_pool) is list else reward_pool
        INFO(f'Sum reward = {sum_reward}')
        return sum_reward

    def get_contributor_of_pair(self, token1, token2):
        contributor_list = []
        for pair in self._get_pde_shares(None, token1, token2):
            contributor = pair.get_payment_k()
            if contributor not in contributor_list:
                contributor_list.append(contributor)

        return contributor_list


class PDEContributeInfo(BlockChainInfoBaseClass):
    """
    {
        "Status": 4,
        "TokenID1Str": "0000000000000000000000000000000000000000000000000000000000000004",
        "Contributed1Amount": 1900000,
        "Returned1Amount": 0,
        "TokenID2Str": "4129f4ca2b2eba286a3bd1b96716d64e0bc02bd2cc1837776b66f67eb5797d79",
        "Contributed2Amount": 2884986,
        "Returned2Amount": 115014
    }
"""

    def get_contribute_status(self, pair_id, check_interval=5, timeout=30):
        from IncognitoChain.Objects.IncognitoTestCase import SUT
        time = 0
        while time < timeout:
            res = SUT.REQUEST_HANDLER.dex().get_contribution_status(pair_id)
            if res.get_error_msg() is None:
                self.data = res.get_result()
                return self
            else:
                WAIT(check_interval)
        return self

    def is_none(self):
        return self.data is None

    def get_status(self):
        return self.data["Status"]

    def get_token1(self):
        return self.data["TokenID1Str"]

    def get_token2(self):
        return self.data["TokenID2Str"]

    def get_contribute_amount_token1(self):
        return self.data["Contributed1Amount"]

    def get_contribute_amount_token2(self):
        return self.data["Contributed2Amount"]

    def get_return_amount_1(self):
        return self.data["Returned1Amount"]

    def get_return_amount_2(self):
        return self.data["Returned2Amount"]

    def wait_for_contribution_status(self, pair_id, expecting_status, check_interval=10, timeout=40):
        time = 0
        while time <= timeout:
            self.get_contribute_status(pair_id)
            if self.get_status() == expecting_status:
                INFO(f'contribution status is {expecting_status} as expected')
                return self
            else:
                WAIT(check_interval)
                self.get_contribute_status(pair_id)
                time += check_interval

        WARNING(f'contribution status: {self.get_status()} is NOT as expected')
        return None


class _WaitingContribution(BlockChainInfoBaseClass):
    """
    example:
    {
         "waitingpdecontribution-33737-token_prv_1341": {
            "ContributorAddressStr": "12Rrk9r3Chmt5Wibkmu2VcFSUffGZbkz2rzMWdmmB3GEu8t8RF4v2wc1gBQtkJFZmPfUP29bSXR4Wn8kDveLQBTBK5Hck9BoGRnuM7n",
            "TokenIDStr": "7b36db7edddb3a2aeda99801aaa85865b3ad6240394c4251f8c75e45fd7139e3",
            "Amount": 20000000000000,
            "TxReqID": "808eb02455463e15f54f58a362ff630744d77283c71bdf9d1d4142d18e6eea65"
         }
     }

    """

    def __init__(self, raw_data):
        super(_WaitingContribution, self).__init__(raw_data)
        raw_data = copy.copy(self.data)
        self.id, self.info = raw_data.popitem()

    def __str__(self):
        return f'{l6(self.get_contributor_address())} - {l6(self.get_token_id())} - {self.get_pair_id()} - ' \
               f'{self.get_amount()}'

    def get_contribution_id(self):
        return self.id

    def get_contributor_address(self):
        return self.info['ContributorAddressStr']

    def get_token_id(self):
        return self.info['TokenIDStr']

    def get_amount(self):
        return self.info['Amount']

    def get_tx_req_id(self):
        return self.info['TxReqID']

    def get_beacon_height(self):
        return int(self.id.split('-')[1])

    def get_pair_id(self):
        return self.id.split('-')[2]


class _PoolPair(BlockChainInfoBaseClass):
    """
        {
            "pdepool-35982-0000000000000000000000000000000000000000000000000000000000000004-7b36db7edddb3a2aeda99801aaa85865b3ad6240394c4251f8c75e45fd7139e3": {
                "Token1IDStr": "0000000000000000000000000000000000000000000000000000000000000004",
                "Token1PoolValue": 0,
                "Token2IDStr": "7b36db7edddb3a2aeda99801aaa85865b3ad6240394c4251f8c75e45fd7139e3",
                "Token2PoolValue": 0
            }
        }
    """

    def __init__(self, raw_data):
        super(_PoolPair, self).__init__(raw_data)
        raw_data = copy.copy(self.data)
        self.id, self.info = raw_data.popitem()

    def __str__(self):
        return f'{l6(self.get_token1_id())}: {l6(self.get_token2_id())} | ' \
               f'{self.get_token1_pool_value()}:{self.get_token2_pool_value()}'

    def get_pair_id(self):
        return self.id

    def get_token1_id(self):
        return self.info['Token1IDStr']

    def get_token2_id(self):
        return self.info['Token2IDStr']

    def get_token1_pool_value(self):
        return self.info['Token1PoolValue']

    def get_token2_pool_value(self):
        return self.info['Token2PoolValue']


class _PdeShare(BlockChainInfoBaseClass):
    """
    {
        "pdeshare-35982-0000000000000000000000000000000000000000000000000000000000000004-7b36db7edddb3a2aeda99801aaa85865b3ad6240394c4251f8c75e45fd7139e3-12Rrk9r3Chmt5Wibkmu2VcFSUffGZbkz2rzMWdmmB3GEu8t8RF4v2wc1gBQtkJFZmPfUP29bSXR4Wn8kDveLQBTBK5Hck9BoGRnuM7n": 0
    }
    """

    def __init__(self, raw_data):
        super(_PdeShare, self).__init__(raw_data)
        raw_data = copy.copy(self.data)
        self.id, self.info = raw_data.popitem()

    def __str__(self):
        return f'{l6(self.get_token1_id())}-{l6(self.get_token2_id())}-' \
               f'{l6(self.get_payment_k())}-{self.get_share_amount()}'

    def __eq__(self, other):
        return self.data == other.data

    def get_share_id(self):
        return self.id

    def get_share_amount(self):
        return self.info

    def get_beacon_height(self):
        return int(self.id.split('-')[1])

    def get_token1_id(self):
        return self.id.split('-')[2]

    def get_token2_id(self):
        return self.id.split('-')[3]

    def get_payment_k(self):
        return self.id.split('-')[4]


class _PdeReward(BlockChainInfoBaseClass):
    def __init__(self, raw_data):
        super(_PdeReward, self).__init__(raw_data)
        raw_data = copy.copy(self.data)
        self.key, self.value = raw_data.popitem()

    def __str__(self):
        return f'{l6(self.get_token1_id())}-{l6(self.get_token2_id())}-' \
               f'{l6(self.get_payment_k())}-{self.get_amount()}'

    def get_beacon_height(self):
        return int(self.key.split('-')[1])

    def get_token1_id(self):
        return self.key.split('-')[2]

    def get_token2_id(self):
        return self.key.split('-')[3]

    def get_payment_k(self):
        return self.key.split('-')[4]

    def get_amount(self):
        return self.value


def wait_for_user_contribution_in_waiting(user, pair_id, token_id, check_interval=10, timeout=120):
    from IncognitoChain.Objects.IncognitoTestCase import SUT
    waiting_contribution = SUT.REQUEST_HANDLER.get_latest_pde_state_info(). \
        find_waiting_contribution_of_user(user, pair_id, token_id)
    time = 0
    while time <= timeout:
        if waiting_contribution:  # list not empty
            return waiting_contribution[0]
        else:  # list is empty, continue to find
            WAIT(check_interval)
            waiting_contribution = SUT.REQUEST_HANDLER.get_latest_pde_state_info(). \
                find_waiting_contribution_of_user(user, pair_id, token_id)
            time += check_interval
    return None


def wait_for_user_contribution_out_waiting(user, pair_id, token_id, check_interval=10, timeout=120):
    from IncognitoChain.Objects.IncognitoTestCase import SUT
    waiting_contribution = SUT.REQUEST_HANDLER.get_latest_pde_state_info(). \
        find_waiting_contribution_of_user(user, pair_id, token_id)
    time = 0
    while time <= timeout:
        if not waiting_contribution:
            return
        else:
            WAIT(check_interval)
            waiting_contribution = SUT.REQUEST_HANDLER.get_latest_pde_state_info(). \
                find_waiting_contribution_of_user(user, pair_id, token_id)
            time += check_interval
    return