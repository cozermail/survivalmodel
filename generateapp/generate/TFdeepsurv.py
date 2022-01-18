#Obtain datasets

import pandas as pd
import json
from generateapp.tfdeepsurv.datasets import survival_df
from generateapp.tfdeepsurv.datasets import survival_stats
from django.conf import settings

def generate(param): 
    new_col = ['Smoking Status', 'Age', 'SBP', 'TC', 'Hb', 'HDL', '24-hour urinary protein', 'Time', 'Event']
    params = pd.DataFrame(columns = new_col, data=param)
    params["Smoking Status"]=(params["Smoking Status"]-0.339325843)/0.701535834
    params["Age"]=(params["Age"]-52.06741573)/12.02612244
    params["SBP"]=(params["SBP"]-137.6449438)/17.7050513674092
    params["TC"]=(params["TC"]-4.72598876404494)/1.53597181816442
    params["Hb"]=(params["Hb"]-113.039101123595)/24.1637793642026
    params["HDL"]=(params["HDL"]-1.15208988764045)/0.405865754940884
    params["24-hour urinary protein"]=(params["24-hour urinary protein"]-4.26793258426966)/4.34121954893472
    # print(params)
    #Dataset statistics
    # from generateapp.tfdeepsurv.datasets import survival_stats
    # specify the colnames of observed status and time in your dataset
    colname_e = 'Event'
    colname_t = 'Time'
    survival_stats(params, t_col=colname_t, e_col=colname_e, plot=False)
    #Survival data transfrom
    #the transformed survival data includes the existing covariates and a new label column. In the new label column, a negative value indicates that this one is a right-censored sample, and a positive value indicates an event occurrence. The new label column 'Y' is simply generated from the time and event columns according to the below equation.
    #Y =  time, if event = 1
    #Y = -time, if event = 0
    #NOTE: In the latest version 2.0, survival data must be transformed by the functionality tfdeepsurv.datasets.survival_df.
    # from generateapp.tfdeepsurv.datasets import survival_df

    surv_test = survival_df(params, t_col=colname_t, e_col=colname_e, label_col="Y")
    # print(surv_test)
    #Model initialization¶
    #NOTE: You can freely change all hyper-parameters during model initialization or training as you want.
    #All hyper-parameters is as follows:
    #nn_config: model parameters configuration
    # ESSENTIAL STEP-1: Pass arguments
    # ESSENTIAL STEP-2: Build Computation Graph
    #Model training
    #You can save your trained model by passing save_model="file_name.ckpt" or load your trained model by passing load_model="file_name.ckpt"
    Y_col = ["Y"]
    X_cols = [c for c in settings.SURV_TRAIN.columns if c not in Y_col]
    # model saving and loading is also supported!
    # read comments of `train()` function if necessary.
    # ESSENTIAL STEP-3: Train Model
    # `num_steps` is 7also an important parameters
    #Model evaluation

    # print("CI on training data:", model.evals(surv_train[X_cols], surv_train[Y_col]))
    # print("CI on test data:", model.evals(surv_test[X_cols], surv_test[Y_col]))

    #concordance_index(y_true, y_pred) concordance_index(data_y.values, preds) preds = - self.predict(data_X)
    #Model prediction includes:
    #predicting hazard ratio or log hazard ratio
    #predicting survival function

    # predict log hazard ratio#

    # predict hazard ratio 预测对数风险比HR
    # print(settings.TRAIN_MODEL.predict(surv_test.loc[0:10, X_cols], output_margin=False))

    # predict survival function预测生存函数
    # settings.TRAIN_MODEL.predict_survival_function(surv_test.loc[0:0, X_cols], plot=False)
    pred_hr2=settings.TRAIN_MODEL.predict(surv_test.loc[0:0, X_cols], output_margin=False)
    # data = pd.DataFrame(settings.TRAIN_MODEL.BSF.iloc[:, 0].values ** pred_hr2, columns=settings.TRAIN_MODEL.BSF.index.values)
    data = pd.DataFrame((1 - settings.TRAIN_MODEL.BSF.iloc[:, 0].values ** pred_hr2) * 100, columns=settings.TRAIN_MODEL.BSF.index.values)

    # pd.set_option('display.width', 300) # 设置字符显示宽度
    # pd.set_option('display.max_rows', None) # 设置显示最大行
    # pd.set_option('display.max_columns', None) # 设置显示最大列，None为显示所有列
    # data.iloc[0,len(data.columns)-18]
    # HR = "低风险" if data.iloc[0,len(data.columns)-18] > settings.THRESHOLD_5HR else "高风险"
    # HR = "低风险" if data.iloc[0,len(data.columns)-18] < ((1 - settings.THRESHOLD_5HR) * 100) else "高风险"

    return {
        # "HR": HR,
        "data": data.iloc[0,1:].to_json()
    }


