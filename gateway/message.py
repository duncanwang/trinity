# coding: utf-8
"""
the mudule for  message
"""

class Message:
    """
    the class for message
    """
    # staticmethods
    @staticmethod
    def get_tx_msg_types():
        """
        :return: all transaction msg type
        """
        tx_types = [
            "Rsmc",
            "FounderSign",
            "Founder",
            "RsmcSign",
            "FounderFail",
            "Settle",
            "SettleSign",
            "SettleFail",
            "RsmcFail",
            "Htlc",
            "HtlcSign",
            "HtlcFail"
        ]
        return tx_types
    
    # classmethods
    @classmethod
    def get_valid_msg_types(cls):
        """
        :return: all valid message type between nodes
        """
        valid_types = [
            "RegisterChannel",
            "SyncChannelState",
            "ResumeChannel"
        ]
        valid_types = valid_types + cls.get_tx_msg_types()
        return valid_types

    @classmethod
    def check_message_is_valid(cls, data, origin="node"):
        """
        :param data: dict type \n
        :param origin: node|wallet|spv
        """
        is_valid = True
        msg_type = data.get("MessageType")
        if type(data) != dict:
            is_valid = False
        elif not msg_type:
            is_valid = False
        if origin == "node":
            if msg_type not in cls.get_valid_msg_types():
                is_valid = False
            elif not data.get("Sender"):
                return False
        return is_valid


class MessageMake:
    """
    the class for make message
    """
    @staticmethod
    def _make_common_msg_head(**kwargs):
        message = {}
        for param_name, param_value in kwargs.items():
            message[param_name] = param_value
        return message
    ###### message for wallet begin ########
    @classmethod
    def make_trigger_transaction_msg(cls, msg_type="CreateChannelMessage", **kwargs):
        """
        :param kwargs: \n
        "sender": xxx@yyy \n
        "receiver": xxx@yyy \n
        "asset_type": TNC/ETH/, \n
        "amount": 4
        """
        message = {
            "Sender": kwargs.get("sender"),
            "MessageType": msg_type,
            "Receiver": kwargs.get("receiver"),
            "MessageBody": {
                "AssetType": kwargs.get("asset_type"),
                "Value": kwargs.get("amount")
            }
        }
        message.update(
            cls._make_common_msg_head(
                Sender=kwargs.get("sender"), 
                Receiver=kwargs.get("receiver")
            )
        )
        return message

    @staticmethod
    def make_join_net_msg(sender):
        message = {
            "MessageType": "JoinNet",
            "Sender": sender
        }
        return message

    @staticmethod
    def make_ack_show_node_list(node_list):
        message = {
            "MessageType": "AckShowNodeList",
            "NodeList": list(node_list)
        }
        return message
    
    @staticmethod
    def make_ack_sync_wallet_msg(url):
        message = {
            "MessageType": "AckSyncWallet",
            "MessageBody": {
                "Url": url
            }
        }
        return message
    ###### message for wallet end ########

    ###### message for spv begin ########
    @staticmethod
    def make_node_list_msg(channel_graph):
        message = {
            "MessageType": "NodeList",
            "Nodes": channel_graph.to_json()
        }
        return message
    
    ###### message for spv end ########

    ###### message for node begin ########
    @staticmethod
    def make_resume_channel_msg(sender):
        message = {
            "MessageType": "ResumeChannel",
            "Sender": sender
        }
        return message

    @staticmethod
    def make_ack_node_join_msg(sender, receiver, node_list):
        message = {
            "MessageType": "AckJoin",
            "Sender": sender,
            "Receiver": receiver,
            "NodeList": list(node_list)
        }
        return message

    @staticmethod
    def make_sync_graph_msg(sync_type, sender, msg_type="SyncChannelState" ,**kwargs):
        """
        :param sync_type: add_single_edge|remove_single_edge|update_node_data|add_whole_graph \n
        :param kwargs: {route_graph,source,target,node,broadcast,excepts}
        """
        message = {
            "MessageType": msg_type,
            "SyncType": sync_type,
            "Sender": sender,
            "Broadcast": kwargs.get("broadcast"),
            "Source": kwargs.get("source"),
            "Target": kwargs.get("target"),
            "Excepts": kwargs.get("excepts")
        }
        if sync_type == "add_whole_graph":
            message["MessageBody"] = kwargs["route_graph"].to_json()
        elif sync_type == "add_single_edge":
            pass
        elif sync_type == "remove_single_edge":
            pass
        elif sync_type == "update_node_data":
            message["MessageBody"] = kwargs["node"]
        return message
    ###### message for node end ########

    @staticmethod
    def make_ack_router_info_msg(router):
        message = {
            "MessageType": "AckRouterInfo",
            "RouterInfo": router
        }
        return message

    @staticmethod
    def make_error_msg(msg_type="ErrorMessage", **kwargs):
        """
        :param kwargs: \n
        sender: "xxx@yyy" \n
        receiver: "xxx@yyy" \n
        reason: the description about error
        """
        message = {
            "Sender": kwargs.get("sender"),
            "Receiver": kwargs.get("receiver"),
            "MessageType": msg_type,
            "Reason": kwargs.get("reason")
        }
        return message