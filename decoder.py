import numpy as np
import pandas as pd


class OneHotShotDecoder:
    def decode(self, dataframe):
        df = dataframe
        labels = df.columns
        data_list = []

        for index, row in df.iterrows():
            curr = pd.DataFrame(row).transpose().to_numpy()
            encoded_at_index = curr[0]
            index_arr = np.where(encoded_at_index == 1)[0][0]
            data_list.append({"filename": encoded_at_index[0], "category": labels[index_arr]})
        return pd.DataFrame(data_list)
