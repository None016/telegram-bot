import aiogram as ai

bot = ai.Bot(token="6158786303:AAGxXgKENOi-AwI7T8Df92aXUH9vLL9ypC0")
bi = ai.Dispatcher(bot)

user_keys = {}


def app_user_keys(user_id):
    user_keys[f"{user_id}"] = [[None, None, None, None, None, None]]  # 0 - key_reg | 1 - name_user | 2 - sex | 3 - old
    # ^^^^^^^^^^ | 4 - photo | 5 - key_input
