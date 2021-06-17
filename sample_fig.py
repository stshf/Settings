#基本ライブラリ
import numpy as np
import pandas as pd

#図形描画ライブラリ
import matplotlib.pyplot as plt
from matplotlib.pylab import rcParams

# 統計モデル（最尤推定で使用）
from scipy.optimize import minimize

#サンプルサイズ
N = 500
#乱数固定
np.random.seed(4)
#状態方程式
mu = np.cumsum(np.random.normal(loc=0, scale=0.2, size=N))
#観測値
obs = mu + np.random.normal(loc=0, scale=0.4, size=N)
#異常値
obs[450] = 8.8
obs[400] = 8.9

#データ（numpyのarrayにすること）
data_series = np.array(obs)

def Kf_LocalLevel(y, mu_pre, P_pre, sigma_w, sigma_v):
  #step1: forecast
  mu_forecast = mu_pre
  P_forecast = P_pre + sigma_w
  y_forecast = mu_forecast
  F = P_forecast + sigma_v

  #step2: filtering
  K = P_forecast / (P_forecast + sigma_v)
  y_residual = y - y_forecast
  mu_filter = mu_forecast + K * y_residual
  P_filter = (1-K) * P_forecast

  #store the result
  result = {
      'mu_filter' : mu_filter,
      'P_filter' : P_filter,
      'y_residual' : y_residual,
      'F' : F,
      'K' : K
  }

  return result



def cal_LogLik_LocalLevel(sigma,data_series=data_series):
  data_series = np.array(data_series)

  sigma_w = np.exp(sigma[0])
  sigma_v = np.exp(sigma[1])

  #sample size
  N = len(data_series)

  #状態の推定量
  mu_zero = 0
  mu_filter = np.hstack((mu_zero,np.zeros(N)))

  P_zero = 10000000
  P_filter = np.hstack((P_zero,np.zeros(N)))

  #
  y_residual =  np.zeros(N)
  F =  np.zeros(N)
  K =  np.zeros(N)

  for i in range(0,N):
    result = Kf_LocalLevel(y=data_series[i], 
                           mu_pre=mu_filter[i], 
                           P_pre=P_filter[i],
                           sigma_w=sigma_w, 
                           sigma_v=sigma_v)
    mu_filter[i+1] = result['mu_filter']
    P_filter[i+1] = result['P_filter']
    y_residual[i] = result['y_residual']
    F[i] = result['F']
    K[i] = result['K']

  LogLik = 1/2 * np.sum( np.log(F) + y_residual**2 / F )

  return LogLik



def output_sigma(initial_value=list((1,1))):
  opt_result = minimize(fun=cal_LogLik_LocalLevel, x0=initial_value, method='l-bfgs-b')

  return np.exp(opt_result.x)



def smooth_LocalLevel(mu_filtered, P_filtered, r_post, s_post, F_post, y_residual_post, K_post):
  r = y_residual_post / F_post + (1-K_post) * r_post
  mu_smooth = mu_filtered + P_filtered * r

  s = 1/F_post + (1-K_post)**2 * s_post
  P_smooth = P_filtered - P_filtered**2 * s


  #store the result
  result = {
      'mu_smooth' : mu_smooth,
      'P_smooth' : P_smooth,
      'r' : r,
      's' : s
  }

  return result

#----------過程誤差と観測誤差の推定----------#

#サンプルサイズ
N = len(data_series)

#状態の推定量
mu_zero = 0
mu_filter = np.hstack((mu_zero,np.zeros(N)))

#状態の分散
P_zero = 10000000
P_filter = np.hstack((P_zero,np.zeros(N)))

#観測値の予測残差
y_residual =  np.zeros(N)

#観測値の予測残差の分散
F =  np.zeros(N)

#カルマンゲイン
K =  np.zeros(N)

#過程誤差の分散
sigma_w = 1000

#観測誤差の分散
sigma_v = 10000

#過程誤差の最適な分散
sigma_w = output_sigma()[0]

#観測誤差の最適な分散
sigma_v = output_sigma()[1]



#----------状態の推定----------#
for i in range(0,N):
  result = Kf_LocalLevel(y=data_series[i],
                         mu_pre=mu_filter[i],
                         P_pre=P_filter[i],
                         sigma_w=sigma_w,
                         sigma_v=sigma_v)
  mu_filter[i+1] = result['mu_filter']
  P_filter[i+1] = result['P_filter']
  y_residual[i] = result['y_residual']
  F[i] = result['F']
  K[i] = result['K']



#----------平準化----------#
# 平滑化状態
mu_smooth = np.zeros(N + 1)

# 平滑化状態分散
P_smooth = np.zeros(N + 1)

# 漸化式のパラメタ（初期値は0のままでよい）
r = np.zeros(N)
s = np.zeros(N)

# 最後のデータは、フィルタリングの結果とスムージングの結果が一致する
mu_smooth[-1] = mu_filter[-1]
P_smooth[-1] = P_filter[-1]

# 逆順でループ
for i in range(N-1,-1,-1):
  result = smooth_LocalLevel(
    mu_filter[i],P_filter[i],r[i], s[i], F[i], y_residual[i], K[i]
  )
  mu_smooth[i] = result['mu_smooth']
  P_smooth[i] = result['P_smooth']
  r[i - 1] = result['r']
  s[i - 1] = result['s']

sigma = P_smooth[1:] + F

anomaly_detection = np.zeros(N-1)

for i in range(1,N-1):
  anomaly_detection[i] = (obs[i] - mu_smooth[i-1])*sigma[i]

anomaly_detection = anomaly_detection * 2

from scipy import stats

N = 300

def main():
   data = anomaly_detection[N:]
   # 標本平均
   mean = np.mean(data)
   # 標本分散
   variance = np.var(data)
   # 異常度
   anomaly_scores = []
   anomaly_scores_dict = {}
   for x in data:
       anomaly_score = (x - mean)**2 / variance
       anomaly_scores.append(anomaly_score)
       anomaly_scores_dict.update({anomaly_score: x})
   # カイ二乗分布による1%水準の閾値
   threshold = stats.chi2.interval(0.99, 1.5)[1]

   r = 3
   res = [a / r for a in anomaly_scores]
   threshold /= r

   # 結果の描画
   fig = plt.figure(figsize=(8.0, 6.0))
   plt.plot(obs[N:] + 2, label="Data")
   plt.plot(res, color = "b", label="Anomaly score")
   plt.plot([0,len(anomaly_detection) - N],[threshold, threshold], 'k-', color = "gray", ls = "dashed")
   plt.xlabel("Time")
   #plt.ylabel("Anomaly score")
   plt.legend(loc='upper center', bbox_to_anchor=(0.9, -0.06), ncol=2)

   plt.show()

main()
