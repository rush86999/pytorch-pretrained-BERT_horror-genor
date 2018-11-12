import re
from IPython.display import HTML, display

b4='(\<span[^\>]+\>)?'
after='(\<\/span\>)?'

replace_list = [
    # punctuation
    ['\s{}\,'.format(b4), r'\1,'],
    ['\s{}\.'.format(b4), r'\1.'],
    ['\s{}\:'.format(b4), r'\1:'],
    ['\s{}\;'.format(b4), r'\1;'],
    ['\s{}\!'.format(b4), r'\1!'],
    ['\s{}\?'.format(b4), r'\1?'],
    ["\s{}\'{}\s?".format(b4,after), r"\1'\2"],
    ["\s{}\-{}\s".format(b4,after), r"\1-\2"],
    ["\“{}\s".format(after), r"“\1"],
    ["\s{}\”".format(b4), r"\1”"],
    ["\s{}\’".format(b4), r"\1’"],
    
    # tokenization
    ['\s?{}\#\#'.format(b4), r'\1'],    
#     ['\[CLS\]\s?', ''],
#     ['\s?\[SEP\]\s?', ''],
    ["\[\s?PAD\s?\]\s?", r""],
    ["\s?\¿\s?", r""],
#     [UNK]
#     [MASK]
#     [CLS]
    # TODO ideally I need to be able to do these with of without span tags
]

def clean_decoded(tokens):
    s = ' '.join(tokens)
    for a, b in replace_list:
        p = re.search(a, s)
        s = re.sub(a, b, s)
    return s



def html_clean_decoded_logits(input_ids, logits, input_mask, label_weights):
    """Format model outputs as html, with masked elements in red, with opacity indicating confidence."""
    log_probs = nn.LogSoftmax(-1)(logits).detach()
    prediction_idxs = log_probs.argmax(-1)
    # join masked an non masked
    y = input_ids *  (1 - label_weights) + prediction_idxs * label_weights
    yd = [decoder[hh.item()] for hh in y]
    html_yd = []
    for i in range(len(yd)):
        if not label_weights[i]:
            html_yd.append(yd[i])
        else:
            prob = log_probs[i][prediction_idxs[i]].exp()
            prob = prob/2 + 0.5
            html_yd.append('<span style="color: rgba(255,0,0,{})">{}</span>'.format(prob, yd[i]))
    return clean_decoded(html_yd)

def html_clean_decoded(tokens, input_mask, label_weights):
    """Format model outputs as html, with masked elements in red, with opacity indicating confidence."""
    yd = [decoder[hh.item()] for hh in tokens]
    html_yd = []
    for i in range(len(yd)):
        if not label_weights[i]:
            html_yd.append(yd[i])
        else:
            prob = 1
            html_yd.append('<span style="color: rgba(255,0,0,{})">{}</span>'.format(prob, yd[i]))
    return clean_decoded(html_yd)
