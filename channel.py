from constants import *

class Channel:
    def __init__(self, id) -> None:
        self.id = id
    
    def get_role_id(self) -> int:
        match self.id:
            case ChannelId.neu:
                return Roles.neu
            case ChannelId.skytils:
                return Roles.skytils
            case ChannelId.skyhanni:
                return Roles.skyhanni
            case ChannelId.bazaar_notifier:
                return Roles.bazaar_notifier
            case ChannelId.skyblock_addons:
                return Roles.skyblock_addons
            case _:
                return None