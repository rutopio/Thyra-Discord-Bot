import discord

# from embed import create_embed
from component.general import BasicViewComponent, AssignRoleSelector, RemoveRoleSelector, CancelButton
from component.create import CreateKeyConfirmButton

from content.view.create import CreateViewContent
from embed.create import CreateEmbed

from constant.usage_limits import USAGE_LIMIT
from constant.enum.key_type import KEY_TYPE


class CreateView():

    def get_creating_embed_and_view(ctx, key_name, key_type, times=-1):

        key_type_dict = {
            KEY_TYPE.REGULAR_KEY: CreateViewContent.regular_key_string(),
            KEY_TYPE.LIMITED_KEY: CreateViewContent.limited_key_string(times=times),
            KEY_TYPE.PROTECTED_KEY: CreateViewContent.protected_key_string(times=times),
        }
        key_type_description = key_type_dict[key_type]
        this_embed = CreateEmbed.get_creating_embed(
            key_name=key_name,
            type_description=key_type_description,
        )

        this_view = BasicViewComponent()

        max_selectable = USAGE_LIMIT.MAX_NUMBER_OF_SELECTABLE_ROLES()
        assign_roles_selector = AssignRoleSelector(max_value=max_selectable)
        remove_roles_selector = RemoveRoleSelector(max_value=max_selectable)

        confirm_button = CreateKeyConfirmButton(
            key_name=key_name,
            assign_roles_selector=assign_roles_selector,
            remove_roles_selector=remove_roles_selector,
            key_type=key_type,
            times=times,
        )
        canceled_button = CancelButton(row=2)

        this_view.add_item(assign_roles_selector)
        this_view.add_item(remove_roles_selector)
        this_view.add_item(confirm_button)
        this_view.add_item(canceled_button)

        return this_embed, this_view
