from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import os, re
import numpy as np
from six.moves import xrange  # pylint: disable=redefined-builtin
import tensorflow as tf

import data_utils
import seq2seq_model


learning_rate = 0.5
learning_rate_decay_factor = 0.99
max_gradient_norm = 5.0
batch_size = 64
size = 512
num_layers = 2
en_vocab_size = 40000
fr_vocab_size = 40000
data_dir = "/root/Bashkort_chatbot"
train_dir = "/root/Bashkort_chatbot"
max_train_data_size = 0
steps_per_checkpoint = 200
use_fp16 = False


model = None
en_vocab_path =None
fr_vocab_path =None
sess = None


regUNK = re.compile('(_UNK)+')


# We use a number of buckets and pad to the closest one for efficiency.
# See seq2seq_model.Seq2SeqModel for details of how they work.
_buckets = [(5, 10), (10, 15), (20, 25), (40, 50)]

def create_model(session, forward_only):
    """Create translation model and initialize or load parameters in session."""
    dtype = tf.float16 if use_fp16 else tf.float32
    model = seq2seq_model.Seq2SeqModel(
        en_vocab_size,
        fr_vocab_size,
        _buckets,
        size,
        num_layers,
        max_gradient_norm,
        batch_size,
        learning_rate,
        learning_rate_decay_factor,
        forward_only=forward_only,
        dtype=dtype)
    ckpt = tf.train.get_checkpoint_state(train_dir)
    print(ckpt)
    if ckpt and tf.gfile.Exists(ckpt.model_checkpoint_path):
        print("Reading model parameters from %s" % ckpt.model_checkpoint_path)
        model.saver.restore(session, ckpt.model_checkpoint_path)
    else:
        session.run(tf.initialize_all_variables())
    print("Created sess")
    return model

def generate_answer(sentence):
    global sess
    if sess == None:
        sess = tf.Session()
    global model
    global en_vocab_path
    global fr_vocab_path
    if model == None:
        model = create_model(sess, True)
        model.batch_size = 1  # We decode one sentence at a time.
    # Load vocabularies.
    if en_vocab_path == None:
        en_vocab_path = os.path.join(data_dir,
                                     "vocab%d.en" % en_vocab_size)
    if fr_vocab_path == None:
        fr_vocab_path = os.path.join(data_dir,
                                     "vocab%d.fr" % fr_vocab_size)
    en_vocab, _ = data_utils.initialize_vocabulary(en_vocab_path)
    _, rev_fr_vocab = data_utils.initialize_vocabulary(fr_vocab_path)
    while sentence:
        # Get token-ids for the input sentence.
        token_ids = data_utils.sentence_to_token_ids(tf.compat.as_bytes(sentence), en_vocab)
        # Which bucket does it belong to?
        bucket_id = min([b for b in xrange(len(_buckets))
                             if _buckets[b][0] > len(token_ids)])
        # Get a 1-element batch to feed the sentence to the model.
        encoder_inputs, decoder_inputs, target_weights = model.get_batch(
                {bucket_id: [(token_ids, [])]}, bucket_id)
        # Get output logits for the sentence.
        _, _, output_logits = model.step(sess, encoder_inputs, decoder_inputs,
                                             target_weights, bucket_id, True)
        # This is a greedy decoder - outputs are just argmaxes of output_logits.
        outputs = [int(np.argmax(logit, axis=1)) for logit in output_logits]
        # If there is an EOS symbol in outputs, cut them at that point.
        if data_utils.EOS_ID in outputs:
            outputs = outputs[:outputs.index(data_utils.EOS_ID)]
        return " ".join([tf.compat.as_str(rev_fr_vocab[output]) for output in outputs])


def answer_by_seq2seq(sentence):
    print('Use answer_by_seq2seq')
    reply = generate_answer(sentence)
    print(reply)
    reply = reply.split(' ')
    answer = ''
    for i in range(len(reply) - 2):
        print(str(i))
        if reply[i] != reply[i + 1]:
            answer += reply[i] + ' '
    answer += reply[len(reply) - 1]
    answer = regUNK.sub('', answer)
    if answer == '':
        answer = 'Ғәфү итегеҙ, мин аңламайым.'
    return answer

