import discord

from component.general import BasicViewComponent
from component.detail import ShowAllPIN, ShowUnusedPIN, ShowUsedPIN
from utils import general
from contents.view.detail import DetailViewContent


class DetailView():

    def get_otp_info_view(ctx, key_info):
        this_view = BasicViewComponent()
        show_unused_pin_button = ShowUnusedPIN(ctx=ctx, key_info=key_info)
        show_used_pin_button = ShowUsedPIN(ctx=ctx, key_info=key_info)
        show_all_pin_button = ShowAllPIN(ctx=ctx, key_info=key_info)

        this_view.add_item(show_unused_pin_button)
        this_view.add_item(show_used_pin_button)
        this_view.add_item(show_all_pin_button)

        return this_view
