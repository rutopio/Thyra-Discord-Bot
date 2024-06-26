class UserUtils():

    @staticmethod
    def get_guild_member_info_by_user_id(guild, user_id):
        this_user = guild.get_member(int(user_id))
        user_data = {}
        if this_user:
            user_data['mention'] = this_user.mention
            user_data['id'] = user_id
            user_data['nick'] = this_user.nick
            user_data['display_name'] = this_user.display_name
            user_data['roles'] = [role.mention for role in this_user.roles]
            user_data['top_role'] = this_user.top_role.mention
            user_data['created_at'] = this_user.created_at
            user_data['joined_at'] = this_user.joined_at
            user_data['display_avatar'] = this_user.display_avatar.url
            user_data['raw_status'] = this_user.raw_status
        return user_data
