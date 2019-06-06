import surprise
import pandas as pd
from surprise import Dataset, accuracy, Reader
from surprise.model_selection import GridSearchCV
import logging
import pickle
from surprise.model_selection import cross_validate
from surprise import NormalPredictor, BaselineOnly, SVD, SVDpp, SlopeOne, NMF, KNNBaseline,KNNBasic, KNNWithMeans, KNNWithZScore, CoClustering

grid_new = pickle.load( open( "grid_new.pkl", "rb" ) )

logging.basicConfig(filename='benchmark.log',level=logging.DEBUG)


reader = Reader(rating_scale=(0, 5))
data = Dataset.load_from_df(grid_new[['user_name', 'game_genres', 'scaled_score']], reader)

benchmark = []
# Iterate over all algorithms
for algorithm in [SVD(), SVDpp(), SlopeOne(), NMF(), NormalPredictor(), KNNBaseline(), KNNBasic(), KNNWithMeans(), KNNWithZScore(), BaselineOnly(), CoClustering()]:


    # Perform cross validation
    results = cross_validate(algorithm, data, measures=['RMSE'], cv=3, verbose=False)

    # Get results & append algorithm name
    tmp = pd.DataFrame.from_dict(results).mean(axis=0)
    tmp = tmp.append(pd.Series([str(algorithm).split(' ')[0].split('.')[-1]], index=['Algorithm']))
    benchmark.append(tmp)
    logging.debug(algorithm)


benchmark_df = pd.DataFrame(benchmark).set_index('Algorithm').sort_values('test_rmse')

pickle.dump(benchmark_df, open("benchmark_df.pkl", "wb" ) )
