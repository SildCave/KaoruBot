

class Reaction(object):
    def __init__(self, reaction):
        self.reaction_name = reaction[0]
        self.emoji = reaction[1]
        self.guild_id = reaction[2]
        self.message_id = reaction[3]
        self.channel_id = reaction[4]
        self.user_id = reaction[5]
    
    def __str__(self):
        return f"{self.reaction_name} {self.emoji} {self.guild_id} {self.message_id} {self.channel_id} {self.user_id}"
    
class MutedUser(object):
    def __init__(self, muted_user):
        self.user_id = muted_user[0]
        self.guild_id = muted_user[1]
        self.muted = muted_user[2]
        self.muted_untill = muted_user[3]
    
    def __str__(self):
        return f"{self.user_id} {self.guild_id} {self.muted} {self.muted_untill}"