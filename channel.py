from constants import *

class Channel:
    def __init__(self, id) -> None:
        self.id = id
    
    def get_role_id(self) -> int:
        match self.id:
            case ChannelId.neu:
                return RoleId.neu
            case ChannelId.skytils:
                return RoleId.skytils
            case ChannelId.skyhanni:
                return RoleId.skyhanni
            case ChannelId.bazaar_notifier:
                return RoleId.bazaar_notifier
            case ChannelId.skyblock_addons:
                return RoleId.skyblock_addons
            case _:
                return None