import logging

import torch
import torch.nn.functional as F
from ChatBotAI.yt_encoder import YTEncoder
from transformers import GPT2Config, GPT2LMHeadModel, GPT2Tokenizer

FILTER_VALUE = -float('Inf')
MODEL_PATH = './ChatBotAI/model_checkpoint'

logger = logging.getLogger(__name__)


class ChatBotAI:
    def __init__(self, model_path=MODEL_PATH, tokenizer_cls="YTEncoder",
                 tokenizer_path="ChatBotAI/bpe/yt.model", device='cpu'):
        self.model_path = model_path
        self.model_class = GPT2LMHeadModel
        self.config_class = GPT2Config
        logger.info(f'Model path: {self.model_path}')

        # TODO: Train own tokenizer
        self.tokenizer_cls = YTEncoder if tokenizer_cls == "YTEncoder" \
            else GPT2Tokenizer
        logger.info(f'Tokenizer: {self.tokenizer_cls}')

        self.tokenizer_path = tokenizer_path if tokenizer_path \
            else self.model_path

        self.device = device
        self.max_input = 1023

        logger.info(f'Loading tokenizer from {self.tokenizer_path}')
        self.tokenizer = self.tokenizer_cls.from_pretrained(
            self.tokenizer_path)
        self.max_input = min(self.tokenizer.max_len_single_sentence,
                             self.max_input)

        logger.info(f'Loading config from {self.model_path}')
        self.config = self.config_class.from_pretrained(self.model_path)

        logger.info(f'Loading config from {self.model_path}')
        self.model = self.model_class.from_pretrained(self.model_path,
                                                      config=self.config)
        self.model.to(self.device)

        logger.info(f'Model eval')
        self.model.eval()

    def respond(self, context=""):
        self.model.eval()

        context_tokens = self.tokenizer.encode(context)
        out = sample_sequence(
            model=self.model,
            context=context_tokens,
            length=500,
            temperature=1.0,
            top_k=50,
            top_p=0.9,
            device=self.device,
            max_input=self.max_input
        )
        out = out[0, len(context_tokens):].tolist()
        out_text = self.tokenizer.decode(out)
        return out_text


# PROBABLY OBSOLETE CODE:
def top_k_top_p_filtering(logits, top_k=0, top_p=0.0, filter_value=-float('Inf')):
    """ Filter a distribution of logits using top-k and/or nucleus (top-p) filtering
        Args:
            logits: logits distribution shape (vocabulary size)
            top_k > 0: keep only top k tokens with highest probability (top-k filtering).
            top_p > 0.0: keep the top tokens with cumulative probability >= top_p (nucleus filtering).
                Nucleus filtering is described in Holtzman et al. (http://arxiv.org/abs/1904.09751)
        From: https://gist.github.com/thomwolf/1a5a29f6962089e871b94cbd09daf317
    """
    assert logits.dim() == 1  # batch size 1 for now - could be updated for more but the code would be less clear
    top_k = min(top_k, logits.size(-1))  # Safety check
    if top_k > 0:
        # Remove all tokens with a probability less than the last token of the top-k
        indices_to_remove = logits < torch.topk(logits, top_k)[0][..., -1, None]
        logits[indices_to_remove] = filter_value

    if top_p > 0.0:
        sorted_logits, sorted_indices = torch.sort(logits, descending=True)
        cumulative_probs = torch.cumsum(F.softmax(sorted_logits, dim=-1), dim=-1)

        # Remove tokens with cumulative probability above the threshold
        sorted_indices_to_remove = cumulative_probs > top_p
        # Shift the indices to the right to keep also the first token above the threshold
        sorted_indices_to_remove[..., 1:] = sorted_indices_to_remove[..., :-1].clone()
        sorted_indices_to_remove[..., 0] = 0

        indices_to_remove = sorted_indices[sorted_indices_to_remove]
        logits[indices_to_remove] = filter_value
    return logits


def sample_sequence(model, length, context, num_samples=1, temperature=1.0, top_k=0, top_p=0.0,
                    device='cpu', max_input=1023, filter_single=[], filter_double=[]):
    context = torch.tensor(context, dtype=torch.long, device=device)
    context = context.unsqueeze(0).repeat(num_samples, 1)
    generated = context
    with torch.no_grad():
        for _ in range(length):

            inputs = {'input_ids': generated[:, -max_input:]}

            outputs = model(
                **inputs)  # Note: we could also use 'past' with GPT-2/Transfo-XL/XLNet (cached hidden-states)
            next_tokens = torch.zeros(num_samples, dtype=torch.long).to(device)
            for isample in range(num_samples):
                next_token_logits = outputs[0][isample, -1, :] / temperature

                next_token_logits[filter_single] = FILTER_VALUE
                # filter blank line = double \n
                if generated[isample, -1] in filter_double:
                    next_token_logits[generated[isample, -1]] = FILTER_VALUE

                filtered_logits = top_k_top_p_filtering(next_token_logits, top_k=top_k, top_p=top_p)
                next_tokens[isample] = torch.multinomial(F.softmax(filtered_logits, dim=-1), num_samples=1)

            generated = torch.cat((generated, next_tokens.unsqueeze(-1)), dim=1)
    return generated
