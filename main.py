from sentence_transformers import SentenceTransformer, util
import yaml
import pandas as pd

def calculate_scores(model, sent1List, sent2List):
  embed1 = model.encode(sent1List, convert_to_tensor=True)
  embed2 = model.encode(sent2List, convert_to_tensor=True)
  cosine_scores = util.cos_sim(embed1, embed2)
  return [cosine_scores[i][i].item() for i in range(len(cosine_scores))]

def main(config):
    model = SentenceTransformer(config['model_path'])
    df = pd.read_excel(config['user_data_path'])
    sent1 = df['source'].tolist()
    sent2 = df['target'].tolist()
    df['scores'] = calculate_scores(model, sent1, sent2)
    df.to_excel('data/result.xlsx', index=None)
    print("Scoring Completed!")

if __name__ == '__main__':
    with open("config/config.yml") as f:
        config = yaml.load(f, Loader=yaml.FullLoader)
    main(config)
