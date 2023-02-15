from mt_model_service.config.config_models import MTModelConfig
import math
import torch
import torch.nn as nn
from mt_model_service import paths
import spacy
from typing import Any, Dict, List

class MTModel:

    def __init__(self, config: MTModelConfig) -> None:
        if torch.cuda.is_available():
            self.device = torch.device('cuda')
        else:
            self.device = torch.device('cpu')
        self.config = config
        self.spacy_src = spacy.load(config.src_lang_spacy_model_name)
        # Load vocabulary
        self.src_vocab = torch.load(paths.SRC_VOCAB_PATH)
        self.tgt_vocab = torch.load(paths.TGT_VOCAB_PATH)
        ntoken = len(self.src_vocab.stoi)
        tgt_ntoken = len(self.tgt_vocab.stoi)

        self.mt_model = TransformerModel(ntoken, tgt_ntoken, config.emsize, config.nhead, config.nhid, config.nlayers)
        self.mt_model.load_state_dict(torch.load(paths.MODEL_PATH))

        self.mt_model = self.mt_model.to(self.device)


    def get_translated_text(self, text: str) -> str:
        """
        :param text:
        :return: translated text
        """
        token_list = self._tokenize_src(text)
        token_id_list = [self.src_vocab.stoi[token] for token in token_list]
        N = len(token_id_list)
        src_mask = [1.] * N
        src = torch.tensor([token_id_list]).permute(1, 0).to(self.device)
        src_mask = torch.tensor([src_mask]).to(self.device)

        output = []
        for i in range(src.shape[1]):
            output.append(self.mt_model.generate(src[:, i:i + 1], src_mask[i:i + 1]))
        output = torch.stack(output).squeeze() # Currently output is [T]
        return self._convert_output_tensor_to_text(output)

    @staticmethod
    def get_word_num(text: str) -> int:
        return len(text.split())

    def _tokenize_src(self, text: str) -> List[str]:
        return [tok.text for tok in self.spacy_src.tokenizer(text)]

    def _convert_output_tensor_to_text(self, output) -> str:
        # output shape: T
        T, = output.shape
        sent = []
        for t in range(T):
            if self.tgt_vocab.itos[output[t]] != '<eos>':
                sent.append(self.tgt_vocab.itos[output[t]])
            else:
                break
        output_text = " ".join(sent)
        return output_text


class TransformerModel(nn.Module):

    def __init__(self, ntoken, tgt_ntoken, ninp, nhead, nhid, nlayers, dropout=0.5):
        super(TransformerModel, self).__init__()
        from torch.nn import TransformerEncoder, TransformerEncoderLayer
        from torch.nn import TransformerDecoder, TransformerDecoderLayer
        self.model_type = 'Transformer'
        self.src_mask = None
        self.pos_encoder = PositionalEncoding(ninp, dropout)

        self.encoder_embed = nn.Embedding(ntoken, ninp)
        encoder_layers = TransformerEncoderLayer(ninp, nhead, nhid, dropout)
        self.transformer_encoder = TransformerEncoder(encoder_layers, nlayers)

        self.decoder_embed = nn.Embedding(tgt_ntoken, ninp)
        decoder_layers = TransformerDecoderLayer(ninp, nhead, nhid, dropout)
        self.transformer_decoder = TransformerDecoder(decoder_layers, nlayers)
        self.decoder_out = nn.Linear(ninp, tgt_ntoken)

        self.ninp = ninp

        self.init_weights()

    def _generate_square_subsequent_mask(self, sz):
        mask = (torch.triu(torch.ones(sz, sz)) == 1).transpose(0, 1)
        mask = mask.float().masked_fill(mask == 0, float('-inf')).masked_fill(mask == 1, float(0.0))
        return mask

    def init_weights(self):
        initrange = 0.1
        self.encoder_embed.weight.data.uniform_(-initrange, initrange)
        self.decoder_embed.weight.data.uniform_(-initrange, initrange)
        self.decoder_out.bias.data.zero_()
        self.decoder_out.weight.data.uniform_(-initrange, initrange)

    def generate(self, src, src_key_pad_mask):
        # src: [T, B]
        # src_key_pad_mask: [B, T]
        batch_size = src.shape[1]
        src = self.encoder_embed(src) * math.sqrt(self.ninp)
        src = self.pos_encoder(src)
        enc_output = self.transformer_encoder(src, src_key_padding_mask=src_key_pad_mask)

        # TODO need some modifications here with the hard-coded value
        device = src.device
        max_len = 80
        # <sos> is 2 and <eos> is 3
        eos = 3
        sos = 2
        dec_inp = sos * torch.ones((max_len, batch_size)).long().to(device)
        dec_inp_mask = self._generate_square_subsequent_mask(len(dec_inp)).to(device)

        output = eos * torch.ones((max_len, batch_size)).long().to(device)
        stop = torch.zeros((batch_size)).bool().to(device)

        for t in range(max_len):
            x = dec_inp
            x = self.decoder_embed(x) * math.sqrt(self.ninp)
            x = self.pos_encoder(x)
            dec_out = self.transformer_decoder(x, enc_output, tgt_mask=dec_inp_mask, memory_key_padding_mask=src_key_pad_mask)
            logits = self.decoder_out(dec_out)
            #logits = dec_out
            _, topi = logits.topk(1)
            topi_t = topi[t].squeeze().long()
            output[t] = topi_t

            # Stop if all sentences reache eos
            stop_t = (topi_t == eos)
            stop = stop | stop_t
            if torch.all(stop):
                break

            if t == max_len - 1:
                break
            dec_inp[t+1] = topi_t.detach()
        return output

class PositionalEncoding(nn.Module):

    def __init__(self, d_model, dropout=0.1, max_len=5000):
        super(PositionalEncoding, self).__init__()
        self.dropout = nn.Dropout(p=dropout)

        pe = torch.zeros(max_len, d_model)
        position = torch.arange(0, max_len, dtype=torch.float).unsqueeze(1)
        div_term = torch.exp(torch.arange(0, d_model, 2).float() * (-math.log(10000.0) / d_model))
        pe[:, 0::2] = torch.sin(position * div_term)
        pe[:, 1::2] = torch.cos(position * div_term)
        pe = pe.unsqueeze(0).transpose(0, 1)
        self.register_buffer('pe', pe)

    def forward(self, x):
        x = x + self.pe[:x.size(0), :]
        return self.dropout(x)

if __name__ == "__main__":
    config = MTModelConfig.parse_file(paths.SERVICE_CONFIG_PATH)
    mt_model = MTModel(config)
    text = "This is really good."
    text = "We had a really hard time."
    output = mt_model.get_translated_text(text)
    print(f"text: {text}")
    print(f"translated text: {output}")
    word_num = MTModel.get_word_num(text)
    print(f"word num: {word_num}")
    print(f"config int: {mt_model.config.int_place_holder}")
