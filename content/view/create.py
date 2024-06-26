from constant.key_type_name import KEY_TYPE_NAME
from utils import general


class CreateViewContent():
    create_key_confirm_button_id = '.create_key_confirm_button'
    create_key_confirm_button_label = 'Create Key'
    create_key_confirm_button_emoji = '➕'

    none_string = '-'

    def regular_key_type_description():
        return KEY_TYPE_NAME.REGULAR_KEY_WITH_EMOJI

    def limited_key_type_description(times):
        return f'{KEY_TYPE_NAME.LIMITED_KEY_WITH_EMOJI} (**{times}** {general.get_plural("time", times)})'

    def protected_key_type_description(times):
        return f'{KEY_TYPE_NAME.PROTECTED_KEY_WITH_EMOJI} with **{times}** One-Time {general.get_plural("PIN", times)}'

    def otp_attachment_name(key_name, times):
        return f'otp-(1-{times})-{key_name}'

    def otp_attachment_embed_title(key_name, times):
        return f'`{times}` One-Time {general.get_plural("PIN", times)} (`#1`~`#{times}`) for `{key_name}`.\nYou can access {general.get_plural("PIN", times)} by `/detail <key_name>` commands later.'

    def otp_attachment_field_title(times):
        return f'One-Time {general.get_plural("PIN", times)} (one per line)'

    def otp_attachment_field_description(times):
        return f'Available One-Time {general.get_plural("PIN", times)} please refer to the attachment below.\nEach code consists of 6 digits with numbers or capital letters.'

    def regular_key_string():
        return f'- **{KEY_TYPE_NAME.REGULAR_KEY}**\n- Each Key can be used an **unlimited** number of times.'

    def limited_key_string(times):
        return f'- **{KEY_TYPE_NAME.LIMITED_KEY}**\n- This Key can only be used **{times}** {general.get_plural("time", times)}.'

    def protected_key_string(times):
        return f'- **{KEY_TYPE_NAME.PROTECTED_KEY}**\n- With **{times}** One-Time {general.get_plural("PIN", times)}. Each One-Time PIN can only be used once.\n- {general.get_plural("PIN", times)} will be automatically generated after creating successfully.'
