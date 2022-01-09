import pandas as pd
import yaml

from sentence_transformers import InputExample, evaluation
from torch.utils.data import DataLoader


class Dataset:
    def __init__(self, data_path):
        self.source = []
        self.target = []
        self.score = []

        self._load_data(data_path)
        self.size = len(self.source)

    def _load_data(self, data_path):
        df = pd.read_excel(data_path)
        self.source = df['source'].tolist()
        self.target = df['target'].tolist()
        self.score = df['score'].tolist()
        assert len(self.source) == len(self.target) == len(self.score)

    def __len__(self):
        return len(self.source)

    def split_data_idx(self, ratio):
        test_size = int(self.size * ratio)
        train_size = self.size - test_size
        print(self.size, train_size, test_size)
        return train_size

    def _create_input_examples(self):
        input_examples = []
        for idx in range(self.size):
            sent1 = self.source[idx]
            sent2 = self.target[idx]
            score = self.score[idx]
            example = InputExample(texts=[sent1, sent2], label=score)
            input_examples.append(example)
        return input_examples

    def _get_dataloader(self, ratio):
        split_size = self.split_data_idx(ratio)
        data = self._create_input_examples()
        return DataLoader(data[:split_size], shuffle=True, batch_size=16)

    def _get_evaluator(self, ratio):
        split_size = self.split_data_idx(ratio)
        source = self.source[split_size:]
        target = self.target[split_size:]
        score = self.score[split_size:]
        return evaluation.EmbeddingSimilarityEvaluator(source, target, score)




# DATA_PATH = config["data_path"]
# print(DATA_PATH)
# a = Dataset(DATA_PATH)
# b = a._get_dataloader(0.4)
# print(b)

# df = pd.read_excel(DATA_PATH)
# df = df.sample(frac=1).reset_index(drop=True)
# print(df.columns)

