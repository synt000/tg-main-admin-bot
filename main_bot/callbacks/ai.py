from modules.ai.telegram_ai import TelegramAI

def report_command(biz_id):
    return TelegramAI.handle_report(biz_id)

def insight_command(biz_id):
    return TelegramAI.handle_insight(biz_id)

def recommend_command(biz_id):
    return TelegramAI.handle_recommend(biz_id)
