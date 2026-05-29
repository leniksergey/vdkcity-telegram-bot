from telegram import Update
from telegram.ext import ContextTypes

async def rules(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = """📋 *Правила проживания*

✅ Заселение: с 15:00
✅ Выезд: до 12:00
✅ Паспорт при заезде

❌ *Строго запрещено:*
• Курение (включая вейп)
• Животные
• Вечеринки и громкая музыка
• Вандализм и порча имущества

💰 Штраф за нарушение — от 5000₽
Особенно внимательно относимся к компаниям подростков."""
    await update.message.reply_text(text, parse_mode="Markdown")