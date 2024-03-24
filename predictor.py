import joblib
import pandas as pd
from nltk.metrics import jaccard_distance


def tokenize_text(text):
    return set(text.split())


def jaccard_similarity(text1, text2):
    # Рассчитываем меру схожести Жаккара
    set1 = tokenize_text(text1)
    set2 = tokenize_text(text2)
    similarity = 1 - jaccard_distance(set1, set2)
    return similarity


class ScamPredictor:
    def __init__(self):
            # Загрузка модели
        self.kmeans = joblib.load('kmeans_model.joblib')

        # Предположим, у вас есть DataFrame cluster_results с колонками 'cluster_labels' и 'target_labels'
        self.cluster_results = pd.read_csv('cluster_results.csv')

        self.tsne_df = pd.read_csv('tsne_df.csv')

    def predict_proba(self, code):
        similarities = self.cluster_results['source_text'].apply(lambda x: jaccard_similarity(code, x))
        predicted_cluster = self.kmeans.predict([similarities])[0]

        # Получаем вероятности целевого признака из соответствующего кластера
        cluster_data = self.cluster_results[self.cluster_results['cluster_labels'] == predicted_cluster]

        # Считаем количество положительных и отрицательных целевых признаков внутри кластера
        positive_count = (cluster_data['target_labels'] == 1).sum()
        total_count = len(cluster_data)

        # Вычисляем вероятность положительного целевого признака внутри кластера
        probability_positive = positive_count / total_count

        return probability_positive

    def predict(self, code):
        probability = self.predict_proba(code)
        return probability >= 0.5, probability
