import discord

from constant.role_selector import ROLE_SELECTOR


class RoleUtils():

    def get_roles_mention_list(interaction, role_list):
        if not role_list:
            return []

        roles_mention_list = []
        for role_id in role_list:
            if role_id:
                role = discord.utils.get(interaction.guild.roles, id=int(role_id))
                if role:
                    roles_mention_list.append(role.mention)
        return roles_mention_list

    async def get_roles_mention_list_and_operate(interaction, role_list, user=None, event=None):
        if not role_list:
            return []
        if event:
            this_member = interaction.guild.get_member(int(user.id))
        roles_mention_list = []
        for role_id in role_list:
            if role_id:
                role = discord.utils.get(interaction.guild.roles, id=int(role_id))
                if role:
                    if event == ROLE_SELECTOR.ASSIGN:
                        try:
                            await this_member.add_roles(role)
                            roles_mention_list.append(role.mention)
                        except:
                            pass

                    elif event == ROLE_SELECTOR.REMOVE:
                        try:
                            await this_member.remove_roles(role)
                            roles_mention_list.append(role.mention)
                        except:
                            pass
        return roles_mention_list
