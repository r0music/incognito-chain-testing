import copy
import json

from IncognitoChain.Helpers.TestHelper import l6
from IncognitoChain.Objects import BlockChainInfoBaseClass
from IncognitoChain.Objects.AccountObject import Account
from libs.AutoLog import INFO


class BeaconBestStateDetailInfo(BlockChainInfoBaseClass):

    def print_committees(self):
        all_committee_in_all_shard_dict = self.get_shard_committees()
        for key, value in all_committee_in_all_shard_dict.items():
            for info in value:
                public_key = info.get_inc_public_key()
                shard_id = self.is_he_a_committee(public_key)
                for auto_staking in self.get_auto_staking_committees():
                    if auto_staking.get_inc_public_key() == public_key:
                        auto_staking_info = self.is_this_committee_auto_stake(public_key)
                validator_number = len(value)
                INFO(f"{l6(public_key)} - {shard_id} - {validator_number} - {auto_staking_info}")

    def get_block_hash(self):
        return self.data["BestBlockHash"]

    def get_previous_block_hash(self):
        return self.data["get_previous_block_hash"]

    def get_epoch(self):
        return self.data["Epoch"]

    def get_beacon_height(self):
        return self.data["BeaconHeight"]

    def get_beacon_proposer_index(self):
        return self.data["BeaconProposerIndex"]

    def get_current_random_number(self):
        return self.data["CurrentRandomNumber"]

    def get_current_random_time_stamp(self):
        return self.data["CurrentRandomTimeStamp"]

    def is_random_number(self):
        return self.data["IsGetRandomNumber"]

    def get_max_beacon_committee_size(self):
        return self.data["MaxBeaconCommitteeSize"]

    def get_min_beacon_committee_size(self):
        return self.data["MinBeaconCommitteeSize"]

    def get_max_shard_committee_size(self):
        return self.data["MaxShardCommitteeSize"]

    def get_min_shard_committee_size(self):
        return self.data["MinShardCommitteeSize"]

    def get_active_shard(self):
        return self.data["ActiveShards"]

    def get_shard_handle(self):
        return self.data["ShardHandle"]

    def get_best_shard_hash(self, shard_number):
        return self.data['BestShardHash'][str(shard_number)]

    def get_best_shard_height(self, shard_number):
        return self.data['BestShardHeight'][str(shard_number)]

    def get_beacon_committee(self):
        raw_beacon_committee_list = self.data['BeaconCommittee']
        beacon_committee_objs = []
        for obj in raw_beacon_committee_list:
            beacon_committee_obj = _Committee(obj)
            beacon_committee_objs.append(beacon_committee_obj)
        return beacon_committee_objs

    def get_beacon_pending_validator(self):
        raw_beacon_pending_validator_list = self.data['BeaconPendingValidator']
        beacon_pending_validator_objs = []
        for obj in raw_beacon_pending_validator_list:
            beacon_pending_validator_obj = _Committee(obj)
            beacon_pending_validator_objs.append(beacon_pending_validator_obj)
        return beacon_pending_validator_objs

    def get_shard_committees(self, shard_num=None, validator_number=None):
        """

        :param shard_num:
        :param validator_number:
        :return: Return one _Committee obj shard_num and validator_num are specified
        Return list of _Committee obj if only shard_num is specify
        Return dict of {shard_num: _Committee} obj if only shard_num and validator_num are specify
        """
        obj_list = []
        committee_dict_raw = self.data['ShardCommittee']  # get all committee in all shard

        if shard_num is not None and validator_number is not None:  # get a specific committee
            committee_raw = committee_dict_raw[str(shard_num)][validator_number]
            committee_obj = _Committee(committee_raw)
            return committee_obj
        elif shard_num is not None and validator_number is None:  # get all committee in a shard
            committee_list_raw = committee_dict_raw[str(shard_num)]
            for committee_raw in committee_list_raw:
                committee_obj = _Committee(committee_raw)
                obj_list.append(committee_obj)
            return obj_list
        elif shard_num is None and validator_number is None:
            dict_objs = {}
            list_objs = []
            for key, value in committee_dict_raw.items():
                for info in value:
                    obj = _Committee(info)
                    list_objs.append(obj)
                dict_objs.update({key: list_objs})
                list_objs = []
            return dict_objs
        else:
            return

    def _get_shard_pending_validator(self):
        return self.data['ShardPendingValidator']

    def get_shard_pending_validator(self, shard_num, validator_number):
        return _Committee(self._get_shard_pending_validator()[str(shard_num)][validator_number])

    def get_auto_staking_committees(self, auto_staking_number=None):
        auto_staking_objs = []
        raw_auto_staking_list_raw = self.data['AutoStaking']

        if auto_staking_number is not None:  # get a specific committee auto staking
            auto_staking_raw = raw_auto_staking_list_raw[(auto_staking_number)]
            auto_staking_obj = _Committee(auto_staking_raw)
            return auto_staking_obj
        elif auto_staking_number is None:  # get all committee auto staking
            for auto_staking_raw in raw_auto_staking_list_raw:
                auto_staking_obj = _Committee(auto_staking_raw)
                auto_staking_objs.append(auto_staking_obj)
            return auto_staking_objs

    def is_he_a_committee(self, account):
        """
        Function to find shard committee number by using Account or public key
        :param account: Account obj or public key
        :return: shard committee number
        """
        if type(account) == str:
            public_key = account
        elif type(account) == Account:
            public_key = account.public_key
        else:
            public_key = ''

        number_of_shards = self.get_active_shard()
        for shard_number in range(0, number_of_shards):
            committees_in_shard = self.get_shard_committees(shard_number)
            for committee in committees_in_shard:
                if committee.get_inc_public_key() == public_key:
                    return shard_number
        return False

    def is_this_committee_auto_stake(self, account):
        """
        Function to check committee auto stake by using Account or public key
        :param account: Account obj or public key
        :return: True if it matches, else False
        """
        if type(account) == str:
            public_key = account
        elif type(account) == Account:
            public_key = account.public_key
        else:
            public_key = ''

        committees_auto_staking = self.get_auto_staking_committees()
        for committee in committees_auto_staking:
            if committee.get_inc_public_key() == public_key:
                return committee.is_auto_staking()
        return

    # TODO: Will update after getting the data
    def get_candidate_shard_waiting_current_random(self):
        return self.data["CandidateShardWaitingForCurrentRandom"]

    def get_candidate_beacon_waiting_current_random(self):
        return self.data["CandidateBeaconWaitingForCurrentRandom"]

    def get_candidate_beacon_waiting_next_random(self):
        return self.data["CandidateBeaconWaitingForNextRandom"]

    def get_candidate_shard_waiting_next_random(self):
        return self.data["CandidateShardWaitingForNextRandom"]

    def get_reward_receiver(self):
        return self.data["RewardReceiver"]

    def get_current_shard_committee_size(self, shard_number):
        committee_list_in_shard = self.get_shard_committees(shard_number)
        return len(committee_list_in_shard)


class _Committee(BlockChainInfoBaseClass):
    """
    data sample:
     {
         "IncPubKey": "12DNFqDkW9bNwzVT8fxZd4y2XLz1PRe3jvbHMYgrp1wUBquWpz7",
         "MiningPubKey:
                {
                  "bls": ""1EF8XFyAYtrNrFMECSPENbxtktjJCJE8faXTdChqVuBMtQNVP2Dd9stFMXKDV8BPNPtmsogV3tLePBPrfAReLp5uWRQA9ngiEivmXFr1rg1wi5Pu31M9Giqhx94ZqgaTk854qUJEGhwXUmkEztw4GKYn7Zq24EDYXGzPK9R43iW1ysWzH5HqH"",
                  "dsa": "17MtmvoQhsppwCJtcuam6DHmEpSGTaK8kNNxCcXheL5apXMe3PH"
                }
     }
    """

    def __init__(self, raw_data):
        super(_Committee, self).__init__(raw_data)
        raw_data = copy.copy(self.data)
        self._inc_public_key = raw_data['IncPubKey']
        self._bls = raw_data['MiningPubKey']['bls']
        self._dsa = raw_data['MiningPubKey']['dsa']
        self._auto_staking = raw_data['IsAutoStake'] if "IsAutoStake" in raw_data else None

    def get_inc_public_key(self):
        return self._inc_public_key

    def get_bls(self):
        return self._bls

    def get_dsa(self):
        return self._dsa

    def is_auto_staking(self):
        return self._auto_staking


class BeaconBlock(BlockChainInfoBaseClass):
    INST_TYPE_DAO = 'DAO'
    INST_TYPE_SHARD = 'shard'
    INST_TYPE_BEACON = 'beacon'
    INST_TYPE_PORTAL = 'portal'

    class ShardState(BeaconBestStateDetailInfo):
        def get_height(self):
            return self.data['Height']

        def get_hash(self):
            return self.data['Hash']

        def get_cross_shard(self):
            return self.data['CrossShard']

    class BeaconInstruction(BlockChainInfoBaseClass):
        """
        example 1:
        [
           "39",
           "0",
           "beaconRewardInst",
           "{\"BeaconReward\":{\"0000000000000000000000000000000000000000000000000000000000000004\":855000000},\"PayToPublicKey\":\"1TdgrfUkGoRu365bCPoaYpXn3ceCFvG9ts4xMgPhxq8MPZwW3i\"}"
        ]

        example 2:
        [
            "42",
            "0",
            "devRewardInst",
            "{\"IncDAOReward\":{\"0000000000000000000000000000000000000000000000000000000000000004\":760000000}}"
        ]

        example 3:
        [
            "43",
            "0",
            "shardRewardInst",
            "{\"ShardReward\":{\"0000000000000000000000000000000000000000000000000000000000000004\":1800000000},\"Epoch\":898}"
        ]
        """

        class InstructionDetail(BlockChainInfoBaseClass):

            def _get_reward_dict(self):
                return self.data[self.get_type()]

            def get_type(self):
                keys = self.data.keys()
                for k in keys:
                    if "Reward" in k:
                        return k
                return None

            def get_rewarded_token(self):  # return a list of token id to receive as reward
                reward_dict = self._get_reward_dict()
                token_list = []
                for token in reward_dict.keys:
                    token_list.append(token)
                return token_list

            def get_reward_amount(self, token_id=None):
                # return amount reward of a token, or a dict of {token: reward amount ...}
                if token_id is None:
                    return self._get_reward_dict()
                return self._get_reward_dict()[token_id]

            def get_public_k_to_pay_to(self):
                return self.data['PayToPublicKey']

            def get_epoch(self):
                return self.data['Epoch']

            def get_shard_id(self):
                return self.data['ShardID']

            def get_txs_fee(self):
                return self.data['TxsFee']

            def get_shard_block_height(self):
                return self.data['ShardBlockHeight']

        def get_num_1(self):
            return self.data[0]

        def get_num_2(self):
            return self.data[1]

        def get_instruction_type(self):
            index_2 = self.data[2]
            if "Inst" in index_2:
                return self.data[2]
            return ''

        def get_instruction_detail(self):
            if self.get_instruction_type() == '':  # instruction has no type
                inst_dict_raw = json.loads(self.data[2])
            else:
                inst_dict_raw = json.loads(self.data[3])

            inst_list_obj = []
            for inst_raw in inst_dict_raw:
                inst_raw = json.loads(inst_raw)
                inst_obj = BeaconBlock.BeaconInstruction.InstructionDetail(inst_raw)
                inst_list_obj.append(inst_obj)

            return inst_list_obj

    def get_hash(self):
        return self.data["Hash"]

    def get_height(self):
        return self.data['Height']

    def get_validation_data(self):
        return self.data["ValidationData"]

    def get_block_producer(self):
        return self.data["BlockProducer"]

    def get_consensus_type(self):
        return self.data["ConsensusType"]

    def get_version(self):
        return self.data["Version"]

    def get_epoch(self):
        return self.data["Epoch"]

    def get_round(self):
        return self.data["Round"]

    def get_time(self):
        return self.data["Time"]

    def get_previous_block_hash(self):
        return self.data["PreviousBlockHash"]

    def get_next_block_hash(self):
        return self.data["NextBlockHash"]

    def get_size(self):
        return self.data["Size"]

    def get_shard_states(self, shard_id=None):
        dict_raw_shard_state = self.data["ShardStates"]
        shard_state_list_obj = []
        for _id, state in dict_raw_shard_state.item():
            shard_state_obj = BeaconBlock.ShardState(state)
            if shard_id is not None and _id == shard_id:
                return shard_state_obj
            elif shard_id is None:
                shard_state_list_obj.append(shard_state_obj)

    def get_instructions(self, inst_type=None):
        list_raw_inst = self.data["Instructions"]
        list_obj_inst = []
        for raw_inst in list_raw_inst:
            obj_inst = BeaconBlock.BeaconInstruction(raw_inst)
            list_obj_inst.append(obj_inst)

        if inst_type is None:
            return list_obj_inst

        list_obj_inst_w_type = []
        for inst in list_obj_inst:
            if inst_type in inst.get_instruction_type():
                list_obj_inst_w_type.append(inst)

        if len(list_obj_inst_w_type) == 1:
            return list_obj_inst_w_type[0]
        return list_obj_inst_w_type
