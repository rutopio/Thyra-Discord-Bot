import discord
from content.view.welcome import WelcomeViewContent
from utils.verifier import Verifier
from utils import general


class WelcomeView(discord.ui.View):

    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(
        label=WelcomeViewContent.welcome_view_button_label,
        custom_id=WelcomeViewContent.welcome_view_button_id,
        style=discord.ButtonStyle.grey,
        emoji=WelcomeViewContent.welcome_view_button_emoji,
    )
    async def button_callback(self, button, interaction: discord.Interaction):
        await interaction.response.send_modal(UserKeyInputModal(title=WelcomeViewContent.welcome_view_modal_title))


class UserKeyInputModal(discord.ui.Modal):

    def __init__(self, custom_id=WelcomeViewContent.welcome_view_modal_id, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.add_item(
            discord.ui.InputText(
                label=WelcomeViewContent.welcome_view_modal_key_input_label,
                placeholder=WelcomeViewContent.welcome_view_modal_key_input_placeholder,
                custom_id=WelcomeViewContent.welcome_view_modal_key_input_id,
                max_length=100,
            ))
        self.add_item(
            discord.ui.InputText(
                label=WelcomeViewContent.welcome_view_modal_pin_input_label,
                custom_id=WelcomeViewContent.welcome_view_modal_pin_input_id,
                required=False,
                max_length=10,
                placeholder=WelcomeViewContent.welcome_view_modal_pin_input_placeholder,
            ))

    async def callback(self, interaction: discord.Interaction):
        user_key = str(self.children[0].value)
        user_pin = str(self.children[1].value)
        is_verified, final_embed = await Verifier(
            interaction=interaction,
            guild=interaction.guild,
            user=interaction.user,
            key_name=user_key,
            pin=user_pin,
        ).get_auth_embed()
        await interaction.response.send_message(embed=final_embed, ephemeral=True)
        if is_verified:
            await general.update_server_dashboard(guild=interaction.guild)
