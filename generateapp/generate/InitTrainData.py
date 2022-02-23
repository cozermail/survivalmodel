#Obtain datasets

import pandas as pd

from generateapp.tfdeepsurv.datasets import survival_df
from generateapp.tfdeepsurv.datasets import survival_stats
from generateapp.tfdeepsurv import dsnn
import csv
import os

survTrain = {}
trainModel = {}
def initTrain(): 
    train_data_url = os.path.dirname(os.path.dirname(os.path.abspath(__file__))).replace('\\', '/') + '/data/train.csv'
    new_col = ['Smoking Status', 'Age', 'SBP', 'TC', 'Hb', 'HDL', '24-hour urinary protein', 'Time', 'Event']
    train_data = pd.read_csv(train_data_url, names = new_col, header=0)
    # test_data = pd.read_csv('C:/Users/Administrator/Desktop/文档/临时项目/预测模型-任晶晶/data/test.csv', names = new_col, header=0)
    train_data["Smoking Status"]=(train_data["Smoking Status"]-0.339325842696629)/0.701535833637939
    train_data["Age"]=(train_data["Age"]-52.0674157303371)/12.0261224418172
    train_data["SBP"]=(train_data["SBP"]-137.644943820225)/17.7050513674092
    train_data["TC"]=(train_data["TC"]-4.72598876404494)/1.53597181816442
    train_data["Hb"]=(train_data["Hb"]-113.039101123595)/24.1637793642026
    train_data["HDL"]=(train_data["HDL"]-1.15208988764045)/0.405865754940884
    train_data["24-hour urinary protein"]=(train_data["24-hour urinary protein"]-4.26793258426966)/4.34121954893472

    
    # print(train_data)
    train_data.head()
    #Dataset statistics
    # from generateapp.tfdeepsurv.datasets import survival_stats
    # specify the colnames of observed status and time in your dataset
    colname_e = 'Event'
    colname_t = 'Time'
    survival_stats(train_data, t_col=colname_t, e_col=colname_e, plot=False)
    #Survival data transfrom
    #the transformed survival data includes the existing covariates and a new label column. In the new label column, a negative value indicates that this one is a right-censored sample, and a positive value indicates an event occurrence. The new label column 'Y' is simply generated from the time and event columns according to the below equation.
    #Y =  time, if event = 1
    #Y = -time, if event = 0
    #NOTE: In the latest version 2.0, survival data must be transformed by the functionality tfdeepsurv.datasets.survival_df.
    # from generateapp.tfdeepsurv.datasets import survival_df
    global survTrain
    survTrain = survival_df(train_data, t_col=colname_t, e_col=colname_e, label_col="Y")

    # columns 't' and 'e' are packed into an new column 'Y'
    survTrain.head()
    #Model initialization¶
    #NOTE: You can freely change all hyper-parameters during model initialization or training as you want.
    #All hyper-parameters is as follows:
    #nn_config: model parameters configuration
    #hidden_layers_nodes: hidden layers configuration
    #num_steps: training steps
    #Hyperparameters tuning can refer to README in directory byopt of this project.
    # from generateapp.tfdeepsurv import dsnn
    # Number of features in your dataset
    input_nodes =len(survTrain.columns) - 1
    # Specify your neural network structure
    hidden_layers_nodes = [7, 4, 1]
    # the arguments of dsnn can be obtained by Bayesian Hyperparameters Tuning.
    # It would affect your model performance largely!
    nn_config = {
        "learning_rate": 0.1,
        "learning_rate_decay": 1,
        "activation": 'tanh',
        "L1_reg": 0.000095882328054111 ,
        "L2_reg": 0.000937799605135647,
        "optimizer": 'adam',#adam
        "dropout_keep_prob":0.9,
        "seed": 1
    }
    # ESSENTIAL STEP-1: Pass arguments
    global trainModel
    trainModel = dsnn(input_nodes,hidden_layers_nodes,nn_config)
    # ESSENTIAL STEP-2: Build Computation Graph
    trainModel.build_graph()
    #Model training
    #You can save your trained model by passing save_model="file_name.ckpt" or load your trained model by passing load_model="file_name.ckpt"
    Y_col = ["Y"]
    X_cols = [c for c in survTrain.columns if c not in Y_col]
    # model saving and loading is also supported!
    # read comments of `train()` function if necessary.
    # ESSENTIAL STEP-3: Train Model
    # `num_steps` is 7also an important parameters
    watch_list = trainModel.train(
        survTrain[X_cols], survTrain[Y_col],
        num_steps=2400,
        num_skip_steps=100,
        plot=True,
        #load_model="model.ckpt"
    )

    #训练集
    pred_hr1 = trainModel.predict(survTrain.loc[0:623, X_cols], output_margin=False)
    survf1 = pd.DataFrame(trainModel.BSF.iloc[:, 0].values ** pred_hr1, columns = trainModel.BSF.index.values)
    # survf1.to_csv("C:\\Users\\Administrator\\Desktop\\survf1.csv")

def getSurvTrain():
    return survTrain

def getTrainModel():
    return trainModel