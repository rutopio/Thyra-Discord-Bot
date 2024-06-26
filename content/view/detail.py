from utils import general


class DetailViewContent():
    show_unused_pin_button_id = '.detail_show_unused_pins_button'
    show_unused_pin_button_label = 'Show Unused PINs'
    show_unused_pin_button_emoji = '📬'

    show_used_pin_button_id = '.detail_show_used_pins_button'
    show_used_pin_button_label = 'Show Used PINs'
    show_used_pin_button_emoji = '📭'

    show_all_pin_button_id = '.detail_show_all_pins_button'
    show_all_pin_button_label = 'Show All PINs'
    show_all_pin_button_emoji = '📫'

    def show_unused_pin_attachment_name(key_name):
        return f'otp-unused-{key_name}'

    def show_unused_pin_button_callback_content(key_name, current_unused_otps):
        return f'**Unused** One-Time {general.get_plural("PIN", len(current_unused_otps))} (`{len(current_unused_otps)}` totally) for `{key_name}`:'

    def show_used_pin_attachment_name(key_name):
        return f'otp-used-{key_name}'

    def show_used_pin_button_callback_content(key_name, current_used_otps):
        return f'**Used** One-Time {general.get_plural("PIN", len(current_used_otps))} (`{len(current_used_otps)}` totally) for `{key_name}`:'

    def show_all_pin_attachment_name(key_name, total_times):
        return f'otp-(1-{total_times})-{key_name})'

    def show_all_pin_button_callback_content(key_name, all_otps):
        return f'**All** One-Time {general.get_plural("PIN", len(all_otps))} (`{len(all_otps)}` totally) for `{key_name}`:'
