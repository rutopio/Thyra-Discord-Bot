import discord

from contents.embed.list import ListEmbedContent
from constants.enum.key_type import KEY_TYPE
from constants.enum.context_type import CONTEXT_TYPE
from constants.constants import CONSTANT
from constants.db.key_info import DB_KEY_INFO
from utils import general
from utils.key import KeyUtils


class ListEmbed():

    def get_list_embed(ctx, list_key_type=KEY_TYPE.ALL_KEYS):

        embed_contents_dict = {
            KEY_TYPE.REGULAR_KEY: [
                ListEmbedContent.regular_key_list_title,
                ListEmbedContent.regular_key_list_description,
            ],
            KEY_TYPE.LIMITED_KEY: [
                ListEmbedContent.limited_key_list_title,
                ListEmbedContent.limited_key_list_description,
            ],
            KEY_TYPE.PROTECTED_KEY: [
                ListEmbedContent.protected_key_list_title,
                ListEmbedContent.protected_key_list_description,
            ],
            KEY_TYPE.ALL_KEYS: [
                ListEmbedContent.all_keys_list_title,
                ListEmbedContent.all_keys_list_description,
            ],
        }

        embed_content = embed_contents_dict[list_key_type]

        this_embed = discord.Embed(title=embed_content[0], description=embed_content[1], color=CONSTANT.EMBED_COLOR)

        key_infos = KeyUtils.get_key_infos(ctx.guild)
        if list_key_type != KEY_TYPE.ALL_KEYS:
            for key_info in key_infos:
                if key_info[DB_KEY_INFO.TYPE] != list_key_type:
                    continue
                key_name, key_basic_info, _ = KeyUtils.get_key_info_content(
                    ctx=ctx,
                    key_info=key_info,
                    show_history=False,
                    show_status=False,
                    show_type=False,
                )

                this_embed.add_field(
                    name=key_name,
                    value=general.truncate_text(text=key_basic_info, content_type=CONTEXT_TYPE.FIELD_VALUE),
                    inline=False,
                )

        else:
            keys_name_dict = {
                ListEmbedContent.regular_key_name: [],
                ListEmbedContent.limited_key_name: [],
                ListEmbedContent.protected_key_name: [],
            }
            for key_info in key_infos:
                list_key_type = key_info[DB_KEY_INFO.TYPE]
                if list_key_type == KEY_TYPE.REGULAR_KEY:
                    keys_name_dict[ListEmbedContent.regular_key_name].append(key_info[DB_KEY_INFO.NAME])
                elif list_key_type == KEY_TYPE.LIMITED_KEY:
                    keys_name_dict[ListEmbedContent.limited_key_name].append(key_info[DB_KEY_INFO.NAME])
                elif list_key_type == KEY_TYPE.PROTECTED_KEY:
                    keys_name_dict[ListEmbedContent.protected_key_name].append(key_info[DB_KEY_INFO.NAME])

            for key_type_name, keys_name in keys_name_dict.items():
                if keys_name:
                    keys_content = f'> ' + f'\n> '.join(keys_name)
                    this_embed.add_field(
                        name=key_type_name,
                        value=general.truncate_text(keys_content, content_type=CONTEXT_TYPE.FIELD_VALUE),
                        inline=False,
                    )

        return this_embed
