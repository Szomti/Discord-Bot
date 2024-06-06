from constants import *

class Channel:
    def __init__(self, id) -> None:
        self.id = id
    
    def get_role_id(self) -> int:
        match self.id:
            case ChannelId.neu:
                return Roles.neu.id
            case ChannelId.skytils:
                return Roles.skytils.id
            case ChannelId.skyhanni:
                return Roles.skyhanni.id
            case ChannelId.bazaar_notifier:
                return Roles.bazaar_notifier.id
            case ChannelId.skyblock_addons:
                return Roles.skyblock_addons.id
            case _:
                return None