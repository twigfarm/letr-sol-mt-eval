from data import Dataset
from sentence_transformers import SentenceTransformer, losses

import yaml

def train(config):
    print("Model Importing...")
    model = SentenceTransformer('sentence-transformers/stsb-xlm-r-multilingual')
    print("Model Import Completed!")

    dataset = Dataset(config['data_path'])
    ratio = config['split_ratio']

    dataloader = dataset._get_dataloader(ratio)
    loss = losses.CosineSimilarityLoss(model)
    evaluator = dataset._get_evaluator(ratio)

    model.fit(train_objectives=[(dataloader, loss)],
              epochs=config['epochs'],
              output_path=config['model_path'],
              warmup_steps=100,
              save_best_model=True,
              evaluator=evaluator,
              evaluation_steps=100)


if __name__ == '__main__':
    if "models" not in os.listdir():
        os.mkdir("models")

    with open("config/config.yml") as f:
        config = yaml.load(f, Loader=yaml.FullLoader)
    train(config)

