import discord

from component.general import BasicViewComponent, AssignRoleSelector, RemoveRoleSelector, CancelButton
from component.edit import KeepEditingButton, DoneButton, ActivateButton, RenameKeyButton, AdjustUsageLimitButton, GenMoreOTPsButton, EditAssignRoleButton, EditRemoveRoleButton, SaveRoleButton

from constant.enum.key_type import KEY_TYPE
from constant.db.key_info import DB_KEY_INFO


class EditView():

    def get_editing_embed_and_view(ctx, key_info):
        from embed.edit import EditEmbed
        this_embed = EditEmbed.get_editing_embed(ctx=ctx, key_info=key_info)

        this_view = BasicViewComponent()

        activate_button = ActivateButton(ctx=ctx, key_info=key_info)
        rename_button = RenameKeyButton(ctx=ctx, key_info=key_info)
        this_view.add_item(activate_button)
        this_view.add_item(rename_button)

        if key_info[DB_KEY_INFO.TYPE] == KEY_TYPE.LIMITED_KEY:
            adjust_times_button = AdjustUsageLimitButton(ctx=ctx, key_info=key_info)
            this_view.add_item(adjust_times_button)
        elif key_info[DB_KEY_INFO.TYPE] == KEY_TYPE.PROTECTED_KEY:
            adjust_otp_button = GenMoreOTPsButton(ctx=ctx, key_info=key_info)
            this_view.add_item(adjust_otp_button)

        assign_roles_button = EditAssignRoleButton(ctx=ctx, key_info=key_info)
        remove_roles_button = EditRemoveRoleButton(ctx=ctx, key_info=key_info)
        cancel_button = DoneButton(row=2)

        this_view.add_item(assign_roles_button)
        this_view.add_item(remove_roles_button)
        this_view.add_item(cancel_button)

        return this_embed, this_view

    def get_keep_editing_view(ctx, key_info):
        this_view = BasicViewComponent()
        keep_editing_button = KeepEditingButton(ctx=ctx, key_info=key_info)
        done_button = DoneButton()
        this_view.add_item(keep_editing_button)
        this_view.add_item(done_button)
        return this_view
