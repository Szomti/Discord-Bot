GUILD_ID = 1236358942850814084
OWNER_ID = 329246886315950082

class Role:
	def __init__(self, id: int, icon: str | None) -> None:
		self.id = id
		self.icon = icon

class Roles:
	admin = Role(1236394971536298045, None) 
	member = Role(1247277747835895819, None)
	all = Role(1236361209830182922, '♾️')
	neu = Role(1236361674924228692, '1️⃣')
	skytils = Role(1236361735334789282, '2️⃣')
	skyhanni = Role(1236361767223820348, '3️⃣')
	bazaar_notifier = Role(1236361901651263498, '4️⃣')
	skyblock_addons = Role(1236361865769255114, '5️⃣')
	full_list = [admin, all, neu, skytils, skyhanni, bazaar_notifier, skyblock_addons]
	
class ChannelId:
	bot_info = 1247273006989050029
	neu = 1236359723054399599
	skytils = 1236359738950684742
	skyhanni = 1236359779610398770
	bazaar_notifier = 1236359830030258326
	skyblock_addons = 1236359864108716213
	full_list = [neu,skytils, skyhanni, bazaar_notifier, skyblock_addons]