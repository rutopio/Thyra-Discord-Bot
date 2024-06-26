import discord

from component.general import BasicViewComponent, CancelButton
from component.remove import RemoveAllKeysConfirmButton, RemoveKeyConfirmButton
from embed.remove import RemoveEmbed
from contents.view.remove import RemoveViewContent

from constants.db.key_info import DB_KEY_INFO
from utils.key import KeyUtils


class RemoveView():

    def get_removing_key_embed_and_view(ctx, key_info):
        key_name, role_message, _ = KeyUtils.get_key_info_content(
            ctx=ctx,
            key_info=key_info,
            show_history=False,
        )
        this_embed = RemoveEmbed.get_removing_key_embed(
            key_name=key_name,
            role_message=role_message,
            key_type=key_info[DB_KEY_INFO.TYPE],
        )

        this_view = BasicViewComponent()
        confirm_button = RemoveKeyConfirmButton(ctx=ctx, key_info=key_info)
        cancel_button = CancelButton()
        this_view.add_item(confirm_button)
        this_view.add_item(cancel_button)

        return this_embed, this_view

    def get_removing_all_embed_and_view(ctx):
        this_embed = RemoveEmbed.get_removing_all_check_embed()

        this_view = BasicViewComponent()
        confirm_button = RemoveAllKeysConfirmButton(ctx=ctx)
        cancel_button = CancelButton()
        this_view.add_item(confirm_button)
        this_view.add_item(cancel_button)

        return this_embed, this_view
