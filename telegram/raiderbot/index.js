const TelegramBot = require('node-telegram-bot-api');
require('dotenv').config();
const headlines = require('./headlines');
const schedule = require('./schedule');

const token = process.env.TELEGRAM_BOT_ID;
const bot = new TelegramBot(token, { polling: true });

// Ack any message
bot.on('message', msg => {
  // bot.sendMessage(msg.chat.id, 'Received your message');
  console.log(`Received message:`, msg);
});

// Matches "/echo [whatever]"
bot.onText(/\/echo (.+)/, (msg, match) => {
  // 'msg' is the received Message from Telegram
  // 'match' is the result of executing the regexp above on the text content
  // of the message

  const chatId = msg.chat.id;
  const resp = match[1]; // the captured "whatever"

  // send back the matched "whatever" to the chat
  bot.sendMessage(chatId, resp);
});

bot.onText(/\/sch.*/, msg => {
  bot.sendMessage(msg.chat.id, schedule(), { parse_mode: 'HTML' });
});

bot.onText(/\/head|news.*/, msg => {
  bot.sendMessage(msg.chat.id, headlines(), { parse_mode: 'HTML' });
});
