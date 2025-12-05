# loader.py
import pandas as pd

def load_spotify_dataset(path='dataset.csv'):
  df = pd.read_csv(path)

  # remove linhas sem o campo de popularidade
  df = df.dropna(subset=['popularity'])

  dataset = []

  for _, row in df.iterrows():
    dados = {
      'track_name': row['track_name'],
      'artist_name': row['artists'],
      'genre': row['track_genre']
    }

    dataset.append({'popularity': int(row['popularity']), **dados})

  return dataset

# print(len(load_spotify_dataset()))