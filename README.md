# Bashkort_chatbot
This repository contains files for implementing the Telegram bot @Aralashyu_bot.

collect_comments.py is used for converting the data from http://web-corpora.net/wsgi3/minorlangs/download into 4 files for training and testing the model:

train.en - the first phrases (questions) from the pairs question-answer, is used for training
train.fr - the second phrases (answers) from the pairs question-answer, is used for training
dev.en - the first phrases (questions) from the pairs question-answer, is used for testing
dev.fr - the second phrases (answers) from the pairs question-answer, is used for testing 

translate.py, seq2seq_model.py, data_utils.py are used for training the model. See https://habrahabr.ru/post/317732/. 

bashkort_bot_getUpdates.py - implementing the bot using long polling (the bot can both answer with predefined responses and generate answers). 
bashkort_bot_webhook.py - implementing the bot using webhooks (the bot can both answer with predefined responses and generate answers). 
bashkort_bot_webhook_without_sample_answers.py - implementing the bot using webhooks (the bot can only generate answers).
bashkort_bot_webhook_without_sess.py - implementing the bot using webhooks (the bot can only answer with predefined responses).

TF_session.py is used for generating phrases with the trained model.

Regex.json - the dictionary with regular expressions for searching for phrases of the following types:
* greeting (formal and informal)
* goodbye (formal and informal)
* questions like "how are you?" (formal and informal)
* offensive words
* questions about the bot

Sample_answers.json - the dictionary with predefined responses for the listed types of phrases.
Offensive_words.json - the list with regular expressions for searching for offensive words. It is not presented here because of the ethical norms.

phrases.py constains the phrases used with commands.

! The Tensorflow version should be 0.11.0 (branch r0.11 https://github.com/tensorflow/tensorflow/tree/r0.11)!
