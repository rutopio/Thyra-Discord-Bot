import discord

from content.embed.general import GeneralEmbedContent
from constant.constants import CONSTANT


class GeneralEmbed():

    def get_invalid_usage_limit_embed():
        return discord.Embed(
            title=GeneralEmbedContent.invalid_usage_limit_embed_title(),
            description=GeneralEmbedContent.invalid_usage_limit_embed_description(),
            color=CONSTANT.EMBED_COLOR,
        )

    def get_invalid_otp_number_embed(value):
        return discord.Embed(
            title=GeneralEmbedContent.invalid_otp_number_embed_title(),
            description=GeneralEmbedContent.invalid_otp_number_embed_description(value=value),
            color=CONSTANT.EMBED_COLOR,
        )

    def get_invalid_value_embed(value):
        return discord.Embed(
            title=GeneralEmbedContent.invalid_value_embed_title(),
            description=GeneralEmbedContent.invalid_value_embed_description(value=value),
            color=CONSTANT.EMBED_COLOR,
        )

    def get_new_usage_limit_too_small_embed(num_used_users, new_times_value):
        return discord.Embed(
            title=GeneralEmbedContent.new_usage_limit_too_small_embed_title(),
            description=GeneralEmbedContent.new_usage_limit_too_small_embed_description(
                num_used_users=num_used_users,
                new_times_value=new_times_value,
            ),
            color=CONSTANT.EMBED_COLOR,
        )

    def get_name_too_long_embed(key_name):
        return discord.Embed(
            title=GeneralEmbedContent.name_too_long_embed_title(),
            description=GeneralEmbedContent.name_too_long_embed_description(key_name=key_name),
            color=CONSTANT.EMBED_COLOR,
        )

    def get_key_is_full_embed():
        return discord.Embed(
            title=GeneralEmbedContent.key_is_full_embed_title(),
            description=GeneralEmbedContent.key_is_full_embed_description(),
            color=CONSTANT.EMBED_COLOR,
        )

    def get_usage_limit_too_many_embed(number):
        return discord.Embed(
            title=GeneralEmbedContent.usage_limit_too_many_embed_title(),
            description=GeneralEmbedContent.usage_limit_too_many_embed_description(number=number),
            color=CONSTANT.EMBED_COLOR,
        )

    def get_otp_too_many_embed(number):
        return discord.Embed(
            title=GeneralEmbedContent.otp_too_many_embed_title(),
            description=GeneralEmbedContent.otp_too_many_embed_description(number=number),
            color=CONSTANT.EMBED_COLOR,
        )

    def get_edited_otp_too_many_embed(num_current_pins, num_additional_pins):
        return discord.Embed(
            title=GeneralEmbedContent.otp_too_many_embed_title(),
            description=GeneralEmbedContent.edited_otp_too_many_embed_description(
                num_current_pins=num_current_pins,
                num_additional_pins=num_additional_pins,
            ),
            color=CONSTANT.EMBED_COLOR,
        )

    def get_key_not_found_embed(key_name):
        return discord.Embed(
            title=GeneralEmbedContent.key_not_found_embed_title(key_name=key_name),
            description=GeneralEmbedContent.key_not_found_embed_description(),
            color=CONSTANT.EMBED_COLOR,
        )

    def get_same_key_name_exist_embed(key_name):
        return discord.Embed(
            title=GeneralEmbedContent.same_key_name_exist_embed_title(key_name=key_name),
            description=GeneralEmbedContent.same_key_name_exist_embed_description(),
            color=CONSTANT.EMBED_COLOR,
        )
