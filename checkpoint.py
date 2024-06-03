from constants import ChannelId
from logger import log
from datetime import datetime

class RolesCheckpoint:
    def __init__(self) -> None:
        self.init = True
        self.message_id = None
        self.channel_id = None

    def get_data(self):
        try:
            f = open('./data/roles.txt', 'r')
            count = 1
            for _ in f:
                line = _.strip()
                if count == 1:
                    self.message_id = int(line)
                elif count == 2:
                    self.channel_id = int(line)
                count += 1
            f.close()
        except FileNotFoundError: 
            print('File Not Found')
        finally:
            self.init = False

    def save_data(self):
        f = open('./data/roles.txt', 'w')
        if self.init or self.message_id is None or self.channel_id is None:
            return
        f.write(f'{self.message_id}\n{self.channel_id}')
        f.close()

class UpdatesCheckpoint:
    def __init__(self) -> None:
        self.init = True
        self.neu = None
        self.skytils = None
        self.skyhanni = None
        self.bazaar_notifier = None
        self.skyblock_addons = None

    def get_data_by_channel(self, id: int) -> int:
        match id:
            case ChannelId.neu:
                return self.neu
            case ChannelId.skytils:
                return self.skytils
            case ChannelId.skyhanni:
                return self.skyhanni
            case ChannelId.bazaar_notifier:
                return self.bazaar_notifier
            case ChannelId.skyblock_addons:
                return self.skyblock_addons
            case _:
                return None
            
    def set_data_by_channel(self, channel_id: int, message_id: int) -> int:
        match channel_id:
            case ChannelId.neu:
                self.neu = message_id
            case ChannelId.skytils:
                self.skytils = message_id
            case ChannelId.skyhanni:
                self.skyhanni = message_id
            case ChannelId.bazaar_notifier:
                self.bazaar_notifier = message_id
            case ChannelId.skyblock_addons:
                self.skyblock_addons = message_id
            case _:
                print(f'Channel not recognized [{channel_id}]')

    def get_data(self):
        try:
            f = open('./data/updates.txt', 'r')
            count = 1
            for _ in f:
                line = _.strip()
                if count == 1:
                    self.neu = int(line)
                elif count == 2:
                    self.skytils = int(line)
                elif count == 3:
                    self.skyhanni = int(line)
                elif count == 4:
                    self.bazaar_notifier = int(line)
                elif count == 5:
                    self.skyblock_addons = int(line)
                count += 1
            f.close()
        except FileNotFoundError: 
            print('File Not Found')
        finally:
            self.init = False
    
    def save_data(self):
        if self.init:
            return
        f = open('./data/updates.txt', 'w')
        data = f'{self.neu}\n{self.skytils}\n{self.skyhanni}\n{self.bazaar_notifier}\n{self.skyblock_addons}'
        log(f'Data to save:\n{data}')
        count = data.count('\n')
        if count > 6 or len(data) > 120:
            log('DATA MIGHT BE CORRUPTED')
            log('Saving to logs.txt')
            f.open('./logs.txt', 'a')
            f.write(f'\n\n[{datetime.now()}] Data to save bigger than expected\n{data}')
            log('Saved to logs.txt -> aborting saving to data.txt')
        f.write(data)
        f.close