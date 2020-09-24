from random import sample
from tqdm import tqdm
from utils.utils import load_json, dump_json
from utils.tokenizer import StanfordTokenizer
from config import config


def get_tqdm_text(pid, length):
    if pid is None:
        tqdm_text = "# iter"
    else:
        tqdm_text = "#" + "{}".format(pid).zfill(length)
    return tqdm_text


def preprocess(path, pid=None):
    data = load_json(path)
    list_data = []
    for i in data:
        list_data += i["paragraphs"]
    data = list_data
    data = sample(data, config.num_sample)

    count = 0
    tokenizer = StanfordTokenizer()
    examples = []

    tqdm_text = get_tqdm_text(pid, 3)
    for j in tqdm(data, desc=tqdm_text, position=pid):
        c = j["context"].replace("''", '" ').replace("``", '" ')#.lower()

        tc = tokenizer.tokenize(c)
        if len(tc) > config.max_len:
            continue

        if isinstance(tokenizer, StanfordTokenizer):
            c_idx = tokenizer.character_level_idx()
        else:
            c_idx = convert_idx(tc)

        y1s, y2s = [], []
        answer_texts = [] 

        qas_sorted = sorted(j["qas"], key=lambda x: x["answers"][0]["answer_start"])
        for k in qas_sorted:
            # q = k["question"].replace("''", '" ').replace("``", '" ').lower() # we don't use question here
            ans = k["answers"][0]
            a_s = ans["answer_start"]
            a = ans["text"].replace("''", '" ').replace("``", '" ')#.lower()
            a_e = a_s + len(a)
            answer_span = []

            for idx, span in enumerate(c_idx):
                if not (a_e <= span[0] or a_s >= span[1]):
                    answer_span.append(idx)
            
            assert len(answer_span) > 0, "Didn't find answer span"
            # y1s.append(answer_span[0])
            # y2s.append(answer_span[-1])
            answer_texts.append((a, answer_span[0], answer_span[-1]))
            count += 1

        examples.append({
            "context_tokens": " ".join(tc), 
            "answers": answer_texts
            # "ans_starts": y1s, 
            # "ans_ends": y2s
            })

    print(count / len(data))
    return examples


def process_squad():
    raw_path = "data/sources/dev.json"
    # save_path = "data/processed/dev.json"

    samples = preprocess(raw_path)

    dump_json(config.processed_path, samples)
    print(len(samples))


if __name__ == "__main__":
    process_squad()