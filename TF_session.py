from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import os, re
import numpy as np
from six.moves import xrange  # pylint: disable=redefined-builtin
import tensorflow as tf

import data_utils
import seq2seq_model

model = None
en_vocab_path =None
fr_vocab_path =None
sess = None

#tf.app.flags.DEFINE_float("learning_rate", 0.5, " Learning rate.")
#tf.app.flags.DEFINE_float("max_gradient_norm", 5.0,
#                          "Clip gradients to this norm.")
#tf.app.flags.DEFINE_integer("batch_size", 64,
#                            "Batch size to use during training.")
#tf.app.flags.DEFINE_integer("size", 512, "Size of each model layer.")
#tf.app.flags.DEFINE_integer("num_layers", 2, "Number of layers in the model.")
#tf.app.flags.DEFINE_integer("en_vocab_size", 40000, "English vocabulary size.")
#tf.app.flags.DEFINE_integer("fr_vocab_size", 40000, "French vocabulary size.")
#tf.app.flags.DEFINE_string("data_dir", "/root/Bashkort_chatbot", "Data directory")
#tf.app.flags.DEFINE_string("train_dir", "/root/Bashkort_chatbot", "Training directory.")
#tf.app.flags.DEFINE_integer("max_train_data_size", 0,
#                            "Limit on the size of training data (0: no limit).")
#tf.app.flags.DEFINE_integer("steps_per_checkpoint", 200,
#                            "How many training steps to do per checkpoint.")
#tf.app.flags.DEFINE_boolean("decode", False,
#                            "Set to True for interactive decoding.")
#tf.app.flags.DEFINE_boolean("self_test", False,
#                            "Run a self-test if this is set to True.")
#tf.app.flags.DEFINE_boolean("use_fp16", False,
#                            "Train using fp16 instead of fp32.")

#FLAGS = tf.app.flags.FLAGS

learning_rate = 0.5
learning_rate_decay_factor = 0.99
max_gradient_norm = 5.0
batch_size = 64
size = 1024
num_layers = 3
en_vocab_size = 40000
fr_vocab_size = 40000
data_dir = "/home/rsa-key-20170514/bot"
train_dir = "/home/rsa-key-20170514/bot"
max_train_data_size = 0
steps_per_checkpoint = 200
use_fp16 = False


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
    print("Created model with fresh parameters.")
    session.run(tf.initialize_all_variables())
  print("created sess")
  return model

def TF_session(sentence):
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
#    with tf.Session() as sess:
        # Create model and load parameters.
#        model = create_model(sess, True)
#        model.batch_size = 1  # We decode one sentence at a time.

        # Load vocabularies.
#        en_vocab_path = os.path.join(data_dir,
#                                     "vocab%d.en" % en_vocab_size)
#        fr_vocab_path = os.path.join(data_dir,
#                                     "vocab%d.fr" % fr_vocab_size)
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
    print('use send_answer_by_seq2seq')
    regUNK = re.compile('_UNK')
    reply = TF_session(sentence)
#    sess = tf.Session()
    # Create model and load parameters.
#    model = create_model(sess, True)
#    model.batch_size = 1  # We decode one sentence at a time.

    # Load vocabularies.
#    en_vocab_path = os.path.join(data_dir,
#                                     "vocab%d.en" % en_vocab_size)
#    fr_vocab_path = os.path.join(data_dir,
#                                     "vocab%d.fr" % fr_vocab_size)
#    en_vocab, _ = data_utils.initialize_vocabulary(en_vocab_path)
#    _, rev_fr_vocab = data_utils.initialize_vocabulary(fr_vocab_path)
#    print ("prepared vocab")
#    while sentence:
#        print("started sentence")
            # Get token-ids for the input sentence.
#        token_ids = data_utils.sentence_to_token_ids(tf.compat.as_bytes(sentence), en_vocab)
            # Which bucket does it belong to?
#        bucket_id = min([b for b in xrange(len(_buckets))
#                             if _buckets[b][0] > len(token_ids)])
#            # Get a 1-element batch to feed the sentence to the model.
#        encoder_inputs, decoder_inputs, target_weights = model.get_batch(
#                {bucket_id: [(token_ids, [])]}, bucket_id)
            # Get output logits for the sentence.
#        _, _, output_logits = model.step(sess, encoder_inputs, decoder_inputs,
#                                             target_weights, bucket_id, True)
            # This is a greedy decoder - outputs are just argmaxes of output_logits.
#        outputs = [int(np.argmax(logit, axis=1)) for logit in output_logits]
            # If there is an EOS symbol in outputs, cut them at that point.
#        if data_utils.EOS_ID in outputs:
#            outputs = outputs[:outputs.index(data_utils.EOS_ID)]
#        reply = " ".join([tf.compat.as_str(rev_fr_vocab[output]) for output in outputs])
    print(reply)
#    del sess
    reply = regUNK.sub('Ғәфү итегеҙ, мин аңламайым.',reply)
    return reply

