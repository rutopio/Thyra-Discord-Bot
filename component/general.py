import discord
from contents.view.component import ComponentViewContent


class BasicViewComponent(discord.ui.View):

    def __init__(self):
        super().__init__(timeout=None)


class AssignRoleSelector(discord.ui.Select):

    def __init__(self, max_value=3):
        super().__init__(
            placeholder=ComponentViewContent.assign_role_selector_placeholder,
            select_type=discord.ComponentType.role_select,
            min_values=0,
            max_values=max_value,
            row=0,
            custom_id=ComponentViewContent.assign_role_selector_id,
        )
        self.selected_options = []

    async def callback(self, interaction: discord.Interaction):
        self.selected_options = interaction.data['values']
        await interaction.response.edit_message(view=self.view)


class RemoveRoleSelector(discord.ui.Select):

    def __init__(self, max_value=3):
        super().__init__(
            placeholder=ComponentViewContent.remove_role_selector_placeholder,
            select_type=discord.ComponentType.role_select,
            min_values=0,
            max_values=max_value,
            row=1,
            custom_id=ComponentViewContent.remove_role_selector_id,
        )
        self.selected_options = []

    async def callback(self, interaction: discord.Interaction):
        self.selected_options = interaction.data['values']
        await interaction.response.edit_message(view=self.view)


class ChannelSelector(discord.ui.Select):

    def __init__(self, confirm_button):
        super().__init__(
            placeholder=ComponentViewContent.channel_selector_placeholder,
            select_type=discord.ComponentType.channel_select,
            channel_types=[discord.ChannelType.text, discord.ChannelType.private],
            row=0,
            custom_id=ComponentViewContent.channel_selector_id,
        )
        self.confirm_button = confirm_button
        self.selected_option = None

    async def callback(self, interaction: discord.Interaction):
        self.selected_option = interaction.data['values'][0]
        self.confirm_button.disabled = False
        await interaction.response.edit_message(view=self.view)


class CancelButton(discord.ui.Button):

    def __init__(self, row=0):
        super().__init__(
            style=discord.ButtonStyle.grey,
            label=ComponentViewContent.cancel_button_label,
            row=row,
            custom_id=ComponentViewContent.cancel_button_id,
        )

    async def callback(self, interaction: discord.Interaction):
        await interaction.response.edit_message(
            view=None,
            content=ComponentViewContent.cancel_button_callback_content,
            embed=None,
        )
