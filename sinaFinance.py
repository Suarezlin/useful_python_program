import requests
from bs4 import BeautifulSoup
import time
import matplotlib.pyplot as plt
import tensorflow as tf
import numpy as np


class SinaFinance:
    def __init__(self):
        self.search_url = 'http://biz.finance.sina.com.cn/suggest/lookup_n.php?country=&q={}&name={}&t=keyword&c=all&k={}&range=all&col=1_7&from=channel'
        self.trend_url = 'http://vip.stock.finance.sina.com.cn/quotes_service/view/CN_TransListV2.php?symbol={}&rn={}'

    def searchFromCode(self, code):
        search_url = self.search_url.format(code, code, code)
        search = requests.get(search_url)
        search.encoding = 'gb2312'
        search_text = search.text
        search_soup = BeautifulSoup(search_text, 'html.parser')
        list = search_soup.select('.list')[0]
        search_result = list.select('a')[0]['href']
        return search_result

    def getStockTrend(self, code):
        trend_url = self.trend_url.format(code, time.time())
        trend = requests.get(trend_url).text.split(';')[1:-2]
        data = []
        for item in trend:
            item = float(item.split(',')[2][2:-1])
            data.append(item)
        return data

    def func(x, p):
        """
        数据拟合所用的函数: A*sin(2*pi*k*x + theta)
        """
        A, k, theta = p
        return A * np.sin(2 * np.pi * k * x + theta)

    def drewGraph(self, data):
        y = np.array(data)
        index = y.shape[0]
        x = np.arange(1, index + 1, 1)
        features = [tf.contrib.layers.real_valued_column("x", dimension=1)]
        estimator = tf.contrib.learn.LinearRegressor(feature_columns=features)
        input_fn = tf.contrib.learn.io.numpy_input_fn({"x": x}, y, batch_size=4674,
                                                      num_epochs=10000)
        estimator.fit(input_fn=input_fn, steps=10000)
        print(estimator.evaluate(input_fn=input_fn))
        predict = list(estimator.predict(input_fn=input_fn))
        plt.figure(figsize=(60, 5))
        plt.plot(x, y, 'b')
        plt.plot(predict, 'r')
        plt.show()


if __name__ == '__main__':
    sinafinance = SinaFinance()
    data = sinafinance.getStockTrend('sz000651')
    sinafinance.drewGraph(data)
