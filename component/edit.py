import os
import discord
from dotenv import load_dotenv

from component.general import BasicViewComponent, AssignRoleSelector, RemoveRoleSelector, CancelButton
from embed.edit import EditEmbed
from embed.general import GeneralEmbed

from content.view.edit import EditViewContent

from constant.usage_limits import USAGE_LIMIT
from constant.guild_operation import GUILD_OPERATION
from constant.db.key_info import DB_KEY_INFO
from constant.db.guild_info import DB_GUILD_INFO
from constant.edit_operation import EDIT_OPERATION

from utils.logs import LogUtils
from utils.mongodb import MongoDBUtils
from utils.key import KeyUtils
from utils import general

load_dotenv()
DATABASE_NAME = os.getenv('DATABASE_NAME')
GUILD_COLLECTION_NAME = os.getenv('GUILD_COLLECTION_NAME')


class KeepEditingButton(discord.ui.Button):

    def __init__(self, ctx, key_info):
        super().__init__(
            style=discord.ButtonStyle.success,
            emoji=EditViewContent.keep_editing_button_emoji,
            label=EditViewContent.keep_editing_button_label,
            row=0,
            custom_id=EditViewContent.keep_editing_button_id,
        )
        self.ctx = ctx
        self.key_info = key_info

    async def callback(self, interaction: discord.Interaction):
        from view.edit import EditView
        identifier = KeyUtils.get_key_identifier_by_timestamp(timestamp=self.key_info[DB_KEY_INFO.CREATED_AT])
        key_info = KeyUtils.get_key_info_by_identifier(guild=interaction.guild, identifier=identifier)
        this_embed, this_view = EditView.get_editing_embed_and_view(ctx=self.ctx, key_info=key_info)
        await interaction.response.edit_message(embed=this_embed, view=this_view)


class DoneButton(discord.ui.Button):

    def __init__(self, row=0):
        super().__init__(
            style=discord.ButtonStyle.grey,
            label=EditViewContent.done_button_label,
            row=row,
            custom_id=EditViewContent.done_button_id,
        )

    async def callback(self, interaction: discord.Interaction):
        await interaction.response.edit_message(
            view=None,
            embed=None,
            content=EditViewContent.done_button_callback_content,
        )


class ActivateButton(discord.ui.Button):

    def __init__(self, ctx, key_info):
        self.ctx = ctx
        self.key_info = key_info
        if self.key_info[DB_KEY_INFO.STATUS]:
            self.status = [
                EditViewContent.activate_button_label,
                EditViewContent.activate_button_emoji,
            ]
        else:
            self.status = [
                EditViewContent.activate_button_label,
                EditViewContent.inactivate_button_emoji,
            ]
        super().__init__(
            style=discord.ButtonStyle.danger,
            emoji=self.status[1],
            label=self.status[0],
            row=0,
            custom_id=EditViewContent.status_button_id,
        )

    async def callback(self, interaction: discord.Interaction):
        from view.edit import EditView

        current_status = self.key_info[DB_KEY_INFO.STATUS]
        new_status = not current_status

        identifier = KeyUtils.get_key_identifier_by_timestamp(timestamp=self.key_info[DB_KEY_INFO.CREATED_AT])
        MongoDBUtils.update_by_keys(
            db_name=DATABASE_NAME,
            collection_name=GUILD_COLLECTION_NAME,
            query_key=DB_GUILD_INFO.ID,
            query_val=interaction.guild_id,
            data_to_insert=new_status,
            sub_keys=[DB_GUILD_INFO.KEYS_INFO, identifier, DB_KEY_INFO.STATUS],
        )
        this_embed = EditEmbed.get_changed_status_embed(key_info=self.key_info, status_new=new_status)
        this_view = EditView.get_keep_editing_view(ctx=self.ctx, key_info=self.key_info)
        await interaction.response.edit_message(embed=this_embed, view=this_view)

        LogUtils.log_key_edited_history(
            interaction=interaction,
            identifier=identifier,
            event=EDIT_OPERATION.UPDATE_STATUS,
            old_value=current_status,
        )
        LogUtils.log_guild_activity(
            guild=interaction.guild,
            user=interaction.user,
            event=GUILD_OPERATION.EDIT_STATUS,
            description=[self.key_info[DB_KEY_INFO.NAME], new_status],
        )
        await general.update_server_dashboard(guild=interaction.guild)


class RenameKeyButton(discord.ui.Button):

    def __init__(self, ctx, key_info):
        super().__init__(
            style=discord.ButtonStyle.success,
            emoji=EditViewContent.rename_key_button_emoji,
            label=EditViewContent.rename_key_button_label,
            row=0,
            custom_id=EditViewContent.rename_key_button_id,
        )
        self.ctx = ctx
        self.key_info = key_info

    async def callback(self, interaction: discord.Interaction):
        key_name = self.key_info[DB_KEY_INFO.NAME]
        await interaction.response.send_modal(
            RenameKeyModal(
                title=EditViewContent.rename_key_modal_title,
                key_info=self.key_info,
                ctx=self.ctx,
            ))


class RenameKeyModal(discord.ui.Modal):

    def __init__(self, ctx, key_info, custom_id=EditViewContent.rename_key_modal_id, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.ctx = ctx
        self.key_info = key_info
        self.add_item(
            discord.ui.InputText(
                label=EditViewContent.rename_key_modal_input_label,
                placeholder=EditViewContent.rename_key_modal_input_placeholder,
                max_length=100,
                custom_id=EditViewContent.rename_key_modal_input_id,
                value=self.key_info[DB_KEY_INFO.NAME],
            ))

    async def callback(self, interaction: discord.Interaction):
        from view.edit import EditView

        old_name = self.key_info[DB_KEY_INFO.NAME]
        new_name = general.encode_text(string=str(self.children[0].value))
        this_view = EditView.get_keep_editing_view(ctx=self.ctx, key_info=self.key_info)

        if len(new_name) > USAGE_LIMIT.MAX_LENGTH_OF_KEY_NAME():
            name_too_long_embed = GeneralEmbed.get_name_too_long_embed(key_name=new_name)
            await interaction.response.edit_message(embed=name_too_long_embed, view=this_view)
            return

        if KeyUtils.is_same_name_key_exists(guild=interaction.guild, new_key_name=new_name):
            same_key_name_exist_embed = GeneralEmbed.get_same_key_name_exist_embed(key_name=new_name)
            await interaction.response.edit_message(embed=same_key_name_exist_embed, view=this_view)
            return

        this_embed = EditEmbed.get_renamed_embed(old_key_name=old_name, new_key_name=new_name)
        await interaction.response.edit_message(embed=this_embed, view=this_view)

        self.key_info[DB_KEY_INFO.PREVIOUS_NAME].append(old_name)
        identifier = KeyUtils.get_key_identifier_by_timestamp(timestamp=self.key_info[DB_KEY_INFO.CREATED_AT])

        MongoDBUtils.update_by_keys(
            db_name=DATABASE_NAME,
            collection_name=GUILD_COLLECTION_NAME,
            query_key=DB_GUILD_INFO.ID,
            query_val=interaction.guild_id,
            data_to_insert=new_name,
            sub_keys=[DB_GUILD_INFO.KEYS_INFO, identifier, EDIT_OPERATION.RENAME],
        )
        MongoDBUtils.update_by_keys(
            db_name=DATABASE_NAME,
            collection_name=GUILD_COLLECTION_NAME,
            query_key=DB_GUILD_INFO.ID,
            query_val=interaction.guild_id,
            data_to_insert=self.key_info[DB_KEY_INFO.PREVIOUS_NAME],
            sub_keys=[DB_GUILD_INFO.KEYS_INFO, identifier, DB_KEY_INFO.PREVIOUS_NAME],
        )
        MongoDBUtils.remove_by_keys(
            db_name=DATABASE_NAME,
            collection_name=GUILD_COLLECTION_NAME,
            query_key=DB_GUILD_INFO.ID,
            query_val=interaction.guild_id,
            sub_keys=[DB_GUILD_INFO.KEYS_UID, identifier],
        )
        MongoDBUtils.update_by_keys(
            db_name=DATABASE_NAME,
            collection_name=GUILD_COLLECTION_NAME,
            query_key=DB_GUILD_INFO.ID,
            query_val=interaction.guild_id,
            data_to_insert=new_name,
            sub_keys=[DB_GUILD_INFO.KEYS_UID, identifier],
        )
        LogUtils.log_key_edited_history(
            interaction=interaction,
            identifier=identifier,
            event=EDIT_OPERATION.RENAME,
            old_value=old_name,
        )
        LogUtils.log_guild_activity(
            guild=interaction.guild,
            user=interaction.user,
            event=GUILD_OPERATION.EDIT_NAME,
            description=[old_name, new_name],
        )
        await general.update_server_dashboard(guild=interaction.guild)


class AdjustUsageLimitButton(discord.ui.Button):

    def __init__(self, ctx, key_info):
        super().__init__(
            style=discord.ButtonStyle.success,
            emoji=EditViewContent.adjust_usage_limit_button_emoji,
            label=EditViewContent.adjust_usage_limit_button_label,
            row=0,
            custom_id=EditViewContent.adjust_usage_limit_button_id,
        )
        self.ctx = ctx
        self.key_info = key_info

    async def callback(self, interaction: discord.Interaction):
        key_name = self.key_info[DB_KEY_INFO.NAME]
        await interaction.response.send_modal(
            AdjustUsageLimitModal(
                title=EditViewContent.adjust_usage_limit_modal_title,
                key_info=self.key_info,
                ctx=self.ctx,
            ))


class AdjustUsageLimitModal(discord.ui.Modal):

    def __init__(self, ctx, key_info, custom_id=EditViewContent.adjust_usage_limit_modal_id, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.ctx = ctx
        self.key_info = key_info
        self.add_item(
            discord.ui.InputText(
                label=EditViewContent.adjust_usage_limit_modal_input_label,
                value=self.key_info[DB_KEY_INFO.COUNT],
                custom_id=EditViewContent.adjust_usage_limit_modal_input_id,
                placeholder=EditViewContent.adjust_usage_limit_modal_input_placeholder,
            ))

    async def callback(self, interaction: discord.Interaction):
        from view.edit import EditView

        this_view = EditView.get_keep_editing_view(ctx=self.ctx, key_info=self.key_info)
        key_name = self.key_info[DB_KEY_INFO.NAME]
        current_limit = self.key_info[DB_KEY_INFO.COUNT]
        new_limit = self.children[0].value

        if not new_limit.isdigit() or int(new_limit) < 1:
            invalid_number_embed = GeneralEmbed.get_invalid_value_embed(value=new_limit)
            await interaction.response.edit_message(embed=invalid_number_embed, view=this_view)
            return

        new_limit = int(new_limit)

        if new_limit > USAGE_LIMIT.MAX_NUMBER_OF_KEY_USAGE_LIMIT():
            too_many_usage_embed = GeneralEmbed.get_usage_limit_too_many_embed(number=new_limit)
            await interaction.response.edit_message(embed=too_many_usage_embed, view=this_view)
            return

        current_used_times = len(
            self.key_info[DB_KEY_INFO.USED_MEMBERS]) if DB_KEY_INFO.USED_MEMBERS in self.key_info.keys() else 0

        if new_limit < current_used_times:
            too_small_number_embed = GeneralEmbed.get_new_usage_limit_too_small_embed(
                num_used_users=current_used_times,
                new_times_value=new_limit,
            )
            await interaction.response.edit_message(embed=too_small_number_embed, view=this_view)
            return

        this_embed = EditEmbed.get_adjusted_embed(
            key_info=self.key_info,
            old_times_value=current_limit,
            new_times_value=new_limit,
        )
        await interaction.response.edit_message(embed=this_embed, view=this_view)

        identifier = KeyUtils.get_key_identifier_by_timestamp(timestamp=self.key_info[DB_KEY_INFO.CREATED_AT])
        MongoDBUtils.update_by_keys(
            db_name=DATABASE_NAME,
            collection_name=GUILD_COLLECTION_NAME,
            query_key=DB_GUILD_INFO.ID,
            query_val=interaction.guild_id,
            data_to_insert=int(new_limit),
            sub_keys=[DB_GUILD_INFO.KEYS_INFO, identifier, DB_KEY_INFO.COUNT],
        )

        LogUtils.log_key_edited_history(
            interaction=interaction,
            identifier=identifier,
            event=EDIT_OPERATION.UPDATE_USAGE_COUNT,
            old_value=current_limit,
        )
        LogUtils.log_guild_activity(
            guild=interaction.guild,
            user=interaction.user,
            event=GUILD_OPERATION.EDIT_USAGE_COUNT,
            description=[key_name, new_limit],
        )
        await general.update_server_dashboard(guild=interaction.guild)


class GenMoreOTPsButton(discord.ui.Button):

    def __init__(self, ctx, key_info):
        super().__init__(
            style=discord.ButtonStyle.success,
            emoji=EditViewContent.gen_more_otps_button_emoji,
            label=EditViewContent.gen_more_otps_button_label,
            row=0,
            custom_id=EditViewContent.gen_more_otps_button_id,
        )
        self.ctx = ctx
        self.key_info = key_info

    async def callback(self, interaction: discord.Interaction):
        key_name = self.key_info[DB_KEY_INFO.NAME]
        await interaction.response.send_modal(
            GenMoreOTPsModal(
                title=EditViewContent.gen_more_otps_modal_title,
                key_info=self.key_info,
                ctx=self.ctx,
            ))


class GenMoreOTPsModal(discord.ui.Modal):

    def __init__(self, ctx, key_info, custom_id=EditViewContent.gen_more_otps_modal_id, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.add_item(
            discord.ui.InputText(
                label=EditViewContent.gen_more_otps_modal_input_label,
                custom_id=EditViewContent.gen_more_otps_modal_input_id,
                placeholder=EditViewContent.gen_more_otps_modal_input_placeholder,
            ))
        self.ctx = ctx
        self.key_info = key_info

    async def callback(self, interaction: discord.Interaction):
        from view.edit import EditView

        this_view = EditView.get_keep_editing_view(ctx=self.ctx, key_info=self.key_info)
        key_name = self.key_info[DB_KEY_INFO.NAME]
        current_value = self.key_info[DB_KEY_INFO.COUNT]
        append_value = self.children[0].value

        if not append_value.isdigit() or int(append_value) < 1:
            invalid_number_embed = GeneralEmbed.get_invalid_value_embed(append_value)
            await interaction.response.edit_message(embed=invalid_number_embed, view=this_view)
            return

        current_value = int(current_value)
        append_value = int(append_value)
        total_value = current_value + append_value

        if total_value > USAGE_LIMIT.MAX_NUMBER_OF_PINS():
            too_many_otp_embed = GeneralEmbed.get_edited_otp_too_many_embed(
                num_current_pins=current_value,
                num_additional_pins=append_value,
            )
            await interaction.response.edit_message(embed=too_many_otp_embed, view=this_view)
            return

        random_seed = self.key_info[DB_KEY_INFO.OTPS][DB_KEY_INFO.OTPS__SEED]
        new_unused_otps = general.generate_pins_by_seed(random_seed, total_value)[current_value:total_value]
        code_attachment = general.generate_attachment_from_list(
            pin_list=new_unused_otps,
            file_name=EditViewContent.gen_more_otps_modal_attachment_name(
                key_name=key_name,
                total_value=total_value,
                current_value=current_value,
            ),
        )

        this_embed = EditEmbed.get_generated_more_otp_embed(
            key_info=self.key_info,
            num_additional_pins=append_value,
        )
        await interaction.response.edit_message(embed=this_embed, view=this_view)
        await interaction.followup.send(
            content=EditViewContent.gen_more_otps_callback_content(
                key_name=key_name,
                total_value=total_value,
                current_value=current_value,
                append_value=append_value,
            ),
            file=code_attachment,
            ephemeral=True,
        )

        identifier = KeyUtils.get_key_identifier_by_timestamp(timestamp=self.key_info[DB_KEY_INFO.CREATED_AT])

        MongoDBUtils.update_by_keys(
            db_name=DATABASE_NAME,
            collection_name=GUILD_COLLECTION_NAME,
            query_key=DB_GUILD_INFO.ID,
            query_val=interaction.guild_id,
            data_to_insert=total_value,
            sub_keys=[DB_GUILD_INFO.KEYS_INFO, identifier, DB_KEY_INFO.COUNT],
        )
        current_unused_otps = MongoDBUtils.query_by_keys(
            db_name=DATABASE_NAME,
            collection_name=GUILD_COLLECTION_NAME,
            query_key=DB_GUILD_INFO.ID,
            query_val=interaction.guild_id,
            sub_keys=[DB_GUILD_INFO.KEYS_INFO, identifier, DB_KEY_INFO.OTPS, DB_KEY_INFO.OTPS__UNUSED],
        )
        current_unused_otps.extend(new_unused_otps)
        MongoDBUtils.update_by_keys(
            db_name=DATABASE_NAME,
            collection_name=GUILD_COLLECTION_NAME,
            query_key=DB_GUILD_INFO.ID,
            query_val=interaction.guild_id,
            data_to_insert=current_unused_otps,
            sub_keys=[DB_GUILD_INFO.KEYS_INFO, identifier, DB_KEY_INFO.OTPS, DB_KEY_INFO.OTPS__UNUSED],
        )
        LogUtils.log_key_edited_history(
            interaction=interaction,
            identifier=identifier,
            event=EDIT_OPERATION.UPDATE_USAGE_COUNT,
            old_value=append_value,
        )
        LogUtils.log_guild_activity(
            guild=interaction.guild,
            user=interaction.user,
            event=GUILD_OPERATION.EDIT_GEN_OTP,
            description=[key_name, append_value],
        )

        await general.update_server_dashboard(guild=interaction.guild)


class EditAssignRoleButton(discord.ui.Button):

    def __init__(self, ctx, key_info):
        super().__init__(
            style=discord.ButtonStyle.success,
            emoji=EditViewContent.EDIT_ASSIGN_ROLES_role_button_emoji,
            label=EditViewContent.EDIT_ASSIGN_ROLES_role_button_label,
            row=1,
            custom_id=EditViewContent.EDIT_ASSIGN_ROLES_role_button_id,
        )
        self.ctx = ctx
        self.key_info = key_info

    async def callback(self, interaction: discord.Interaction):
        from view.edit import EditView

        key_name = self.key_info[DB_KEY_INFO.NAME]
        this_view = BasicViewComponent()

        max_selectable = USAGE_LIMIT.MAX_NUMBER_OF_SELECTABLE_ROLES()
        assign_roles_selector = AssignRoleSelector(max_selectable)
        confirm_button = SaveRoleButton(
            ctx=self.ctx,
            key_info=self.key_info,
            roles_selector=assign_roles_selector,
            selector_type=EDIT_OPERATION.UPDATE_ASSIGN_ROLES,
        )
        cancel_button = CancelButton(row=2)

        this_view.add_item(assign_roles_selector)
        this_view.add_item(confirm_button)
        this_view.add_item(cancel_button)

        this_embed = EditEmbed.get_editing_embed(ctx=self.ctx, key_info=self.key_info, show_history=False)
        await interaction.response.edit_message(view=this_view, embed=this_embed)


class EditRemoveRoleButton(discord.ui.Button):

    def __init__(self, ctx, key_info):
        super().__init__(
            style=discord.ButtonStyle.success,
            emoji=EditViewContent.EDIT_REMOVE_ROLES_role_button_emoji,
            label=EditViewContent.EDIT_REMOVE_ROLES_role_button_label,
            row=1,
            custom_id=EditViewContent.EDIT_REMOVE_ROLES_role_button_id,
        )
        self.ctx = ctx
        self.key_info = key_info

    async def callback(self, interaction: discord.Interaction):
        from view.edit import EditView

        key_name = self.key_info[DB_KEY_INFO.NAME]
        this_view = BasicViewComponent()

        max_selectable = USAGE_LIMIT.MAX_NUMBER_OF_SELECTABLE_ROLES()
        remove_roles_selector = RemoveRoleSelector(max_selectable)
        confirm_button = SaveRoleButton(
            ctx=self.ctx,
            key_info=self.key_info,
            roles_selector=remove_roles_selector,
            selector_type=EDIT_OPERATION.UPDATE_REMOVE_ROLES,
        )
        cancel_button = CancelButton(row=2)

        this_view.add_item(remove_roles_selector)
        this_view.add_item(confirm_button)
        this_view.add_item(cancel_button)

        this_embed = EditEmbed.get_editing_embed(ctx=self.ctx, key_info=self.key_info, show_history=False)
        await interaction.response.edit_message(view=this_view, embed=this_embed)


class SaveRoleButton(discord.ui.Button):

    def __init__(self, ctx, key_info, roles_selector, selector_type):
        super().__init__(
            style=discord.ButtonStyle.success,
            emoji=EditViewContent.save_role_button_emoji,
            label=EditViewContent.save_role_button_label,
            row=2,
            custom_id=EditViewContent.save_role_button_id,
        )
        self.ctx = ctx
        self.key_info = key_info
        self.roles_selector = roles_selector
        self.selector_type = selector_type

    async def callback(self, interaction: discord.Interaction):
        from view.edit import EditView

        key_name = self.key_info[DB_KEY_INFO.NAME]
        identifier = KeyUtils.get_key_identifier_by_timestamp(timestamp=self.key_info[DB_KEY_INFO.CREATED_AT])
        new_roles = self.roles_selector.selected_options

        this_embed = EditEmbed.get_updated_role_rules_embed(
            interaction=interaction,
            key_info=self.key_info,
            updated_roles=new_roles,
            updated_type=self.selector_type,
        )
        this_view = EditView.get_keep_editing_view(ctx=self.ctx, key_info=self.key_info)
        if self.selector_type == EDIT_OPERATION.UPDATE_ASSIGN_ROLES:
            await interaction.response.edit_message(view=this_view, embed=this_embed)
            LogUtils.log_key_edited_history(
                interaction=interaction,
                identifier=identifier,
                event=EDIT_OPERATION.UPDATE_ASSIGN_ROLES,
                old_value=self.key_info[DB_KEY_INFO.ASSIGN_ROLES],
            )
            LogUtils.log_guild_activity(
                guild=interaction.guild,
                user=interaction.user,
                event=GUILD_OPERATION.EDIT_ASSIGN_ROLES,
                description=key_name,
            )
            MongoDBUtils.update_by_keys(
                db_name=DATABASE_NAME,
                collection_name=GUILD_COLLECTION_NAME,
                query_key=DB_GUILD_INFO.ID,
                query_val=interaction.guild_id,
                data_to_insert=new_roles,
                sub_keys=[DB_GUILD_INFO.KEYS_INFO, identifier, DB_KEY_INFO.ASSIGN_ROLES],
            )
        elif self.selector_type == EDIT_OPERATION.UPDATE_REMOVE_ROLES:
            await interaction.response.edit_message(view=this_view, embed=this_embed)
            LogUtils.log_key_edited_history(
                interaction=interaction,
                identifier=identifier,
                event=EDIT_OPERATION.UPDATE_REMOVE_ROLES,
                old_value=self.key_info[DB_KEY_INFO.REMOVE_ROLES],
            )
            LogUtils.log_guild_activity(
                guild=interaction.guild,
                user=interaction.user,
                event=GUILD_OPERATION.EDIT_REMOVE_ROLES,
                description=key_name,
            )
            MongoDBUtils.update_by_keys(
                db_name=DATABASE_NAME,
                collection_name=GUILD_COLLECTION_NAME,
                query_key=DB_GUILD_INFO.ID,
                query_val=interaction.guild_id,
                data_to_insert=new_roles,
                sub_keys=[DB_GUILD_INFO.KEYS_INFO, identifier, DB_KEY_INFO.REMOVE_ROLES],
            )
        await general.update_server_dashboard(interaction.guild)
