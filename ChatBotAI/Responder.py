import logging
import zipfile

import requests
from google_drive_downloader import GoogleDriveDownloader as gdd
import threading

import torch
import torch.nn.functional as F
from ChatBotAI.yt_encoder import YTEncoder
from transformers import GPT2Config, GPT2LMHeadModel, GPT2Tokenizer

FILTER_VALUE = -float('Inf')
URL_ZIP_MODEL = "https://drive.google.com/open?id=1FR72Ib40V0nXxfH__x91NWGsy13hzcs5"
ID_GOOGLE_FILE = "1FR72Ib40V0nXxfH__x91NWGsy13hzcs5"
ZIP_NAME = "./ChatBotAI/model_checkpoint.zip"
DIR_NAME = './ChatBotAI/model_checkpoint'

logger = logging.getLogger(__name__)


class ChatBotAI:
    def __init__(self, model_path="", tokenizer_class="YTEncoder",
                 tokenizer_name="ChatBotAI/bpe/yt.model", device='cpu'):
        # assert model_path != "", "model_path is empty."
        self.model = None
        self.config = None
        self.tokenizer = None

        if model_path == "":
            logger.info("Downloading model...")
            # gdd.download_file_from_google_drive(file_id=ID_GOOGLE_FILE,
            #                                     dest_path=f'./{ZIP_NAME}')
            #
            # with zipfile.ZipFile(ZIP_NAME, 'r') as zip_ref:
            #     zip_ref.extractall(DIR_NAME)
            #     model_path = DIR_NAME
            ThreadingExample(ID_GOOGLE_FILE, ZIP_NAME, DIR_NAME)
            logger.info("Download completed!")


        self.model_path = DIR_NAME

        self.model_class = GPT2LMHeadModel
        self.config_class = GPT2Config

        # TODO:
        # Train own tokenizer
        self.tokenizer_class = YTEncoder if tokenizer_class == "YTEncoder" else GPT2Tokenizer
        self.tokenizer_name = tokenizer_name if tokenizer_name else self.model_path

        self.device = device
        self.max_input = 1023

    def load_model(self):
        self.tokenizer = self.tokenizer_class.from_pretrained(self.tokenizer_name)
        self.max_input = min(self.tokenizer.max_len_single_sentence, self.max_input)
        self.config = self.config_class.from_pretrained(self.model_path)

        self.model = self.model_class.from_pretrained(self.model_path, config=self.config)
        self.model.to(self.device)
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


def download_file_from_google_drive(id, destination):
    URL = "https://docs.google.com/uc?export=download"
    session = requests.Session()
    response = session.get(URL, params={'id': id}, stream=True)
    token = get_confirm_token(response)
    if token:
        params = {'id': id, 'confirm': token}
        response = session.get(URL, params=params, stream=True)
    save_response_content(response, destination)


def get_confirm_token(response):
    for key, value in response.cookies.items():
        if key.startswith('download_warning'):
            return value
    return None


def save_response_content(response, destination):
    CHUNK_SIZE = 3276
    with open(destination, "wb") as f:
        for chunk in response.iter_content(CHUNK_SIZE):
            if chunk:  # filter out keep-alive new chunks
                f.write(chunk)


class ThreadingExample(object):
    """ Threading example class
    The run() method will be started and it will run in the background
    until the application exits.
    """
    def __init__(self, id_google="", dest_path_zip="", dest_path=""):
        self.id_google = id_google
        self.dest_path_zip = dest_path_zip
        self.dest_path = dest_path

        thread = threading.Thread(target=self.run, args=())
        thread.daemon = True                            # Daemonize thread
        thread.start()                                  # Start the execution

    def run(self):
        """ Method that runs forever """
        download_file_from_google_drive(self.id_google, self.dest_path_zip)
        with zipfile.ZipFile(self.dest_path_zip, 'r') as zip_ref:
            zip_ref.extractall(self.dest_path)

# if __name__=="__main__":
#     chatbot = ChatBotAI()
#     chatbot.load_model()
