import discord

from component.general import BasicViewComponent

from contents.view.detail import DetailViewContent
from constants.db.key_info import DB_KEY_INFO

from utils.key import KeyUtils
from utils import general


class ShowUnusedPIN(discord.ui.Button):

    def __init__(self, ctx, key_info):

        super().__init__(
            style=discord.ButtonStyle.success,
            label=DetailViewContent.show_unused_pin_button_label,
            emoji=DetailViewContent.show_unused_pin_button_emoji,
            row=0,
            custom_id=DetailViewContent.show_unused_pin_button_id,
        )
        self.ctx = ctx
        self.key_info = key_info

    async def callback(self, interaction: discord.Interaction):
        await interaction.response.defer()

        key_name = self.key_info[DB_KEY_INFO.NAME]
        identifier = KeyUtils.get_key_identifier_by_timestamp(timestamp=self.key_info[DB_KEY_INFO.CREATED_AT])

        current_unused_otps = self.key_info[DB_KEY_INFO.OTPS][DB_KEY_INFO.OTPS__UNUSED]
        code_attachment = general.generate_attachment_from_list(
            pin_list=current_unused_otps,
            file_name=DetailViewContent.show_unused_pin_attachment_name(key_name=key_name),
        )
        await interaction.followup.send(
            content=DetailViewContent.show_unused_pin_button_callback_content(
                key_name=key_name,
                current_unused_otps=current_unused_otps,
            ),
            file=code_attachment,
            ephemeral=True,
        )


class ShowUsedPIN(discord.ui.Button):

    def __init__(self, ctx, key_info):

        super().__init__(
            style=discord.ButtonStyle.success,
            label=DetailViewContent.show_used_pin_button_label,
            emoji=DetailViewContent.show_used_pin_button_emoji,
            row=0,
            custom_id=DetailViewContent.show_used_pin_button_id,
        )
        self.ctx = ctx
        self.key_info = key_info

    async def callback(self, interaction: discord.Interaction):
        await interaction.response.defer()
        key_name = self.key_info[DB_KEY_INFO.NAME]
        identifier = KeyUtils.get_key_identifier_by_timestamp(timestamp=self.key_info[DB_KEY_INFO.CREATED_AT])

        current_used_otps = self.key_info[DB_KEY_INFO.OTPS][DB_KEY_INFO.OTPS__USED].keys()
        code_attachment = general.generate_attachment_from_list(
            pin_list=current_used_otps,
            file_name=DetailViewContent.show_used_pin_attachment_name(key_name=key_name),
        )
        await interaction.followup.send(
            content=DetailViewContent.show_used_pin_button_callback_content(
                key_name=key_name,
                current_used_otps=current_used_otps,
            ),
            file=code_attachment,
            ephemeral=True,
        )


class ShowAllPIN(discord.ui.Button):

    def __init__(self, ctx, key_info):

        super().__init__(
            style=discord.ButtonStyle.grey,
            label=DetailViewContent.show_all_pin_button_label,
            emoji=DetailViewContent.show_all_pin_button_emoji,
            row=1,
            custom_id=DetailViewContent.show_all_pin_button_id,
        )
        self.ctx = ctx
        self.key_info = key_info

    async def callback(self, interaction: discord.Interaction):
        await interaction.response.defer()

        key_name = self.key_info[DB_KEY_INFO.NAME]
        identifier = KeyUtils.get_key_identifier_by_timestamp(timestamp=self.key_info[DB_KEY_INFO.CREATED_AT])

        random_seed = self.key_info[DB_KEY_INFO.OTPS][DB_KEY_INFO.OTPS__SEED]
        total_times = self.key_info[DB_KEY_INFO.COUNT]
        all_otps = general.generate_pins_by_seed(seed=random_seed, quantity=total_times)
        code_attachment = general.generate_attachment_from_list(
            pin_list=all_otps,
            file_name=DetailViewContent.show_all_pin_attachment_name(
                key_name=key_name,
                total_times=total_times,
            ),
        )
        await interaction.followup.send(
            content=DetailViewContent.show_all_pin_button_callback_content(
                key_name=key_name,
                all_otps=all_otps,
            ),
            file=code_attachment,
            ephemeral=True,
        )
