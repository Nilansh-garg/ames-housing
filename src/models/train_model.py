import pandas as pd
import os 
import sys
from dataclasses import dataclass

# from catboost import CatBostRegressor
from sklearn.ensemble import (
    AdaBoostRegressor,
    RandomForestRegressor,
    GradientBoostingRegressor
)

from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score

from sklearn.neighbors import KNeighborsRegressor
from sklearn.tree import DecisionTreeRegressor
# from xgboost import XGBRegressor

from src.exception import CustomException
from src.logger import logging

from src import save_object,evaluate_model


@dataclass
class ModelTrainerConfig():
    trainer_model_file_path = os.path.join("../../models", "model.pkl")

class modelTrainer:
    def __init__(self):
        self.model_trainer_config = ModelTrainerConfig()
        
    def initiate_model_trainer(self, train_array, test_array):
        try:
            logging.info("split training and test input data")
            x_train, y_train, x_test,y_test = (
                train_array[:,:-1],
                train_array[:,-1],
                test_array[:,:-1],
                test_array[:,-1]
                
            )
            
            models = {
                "Random Forest" : RandomForestRegressor(n_estimators=100, random_state=42),
                # "Decision Tree": DecisionTreeRegressor(),
                # "Gradient Boosting": GradientBoostingRegressor(),
                # "Linear Regression":LinearRegression(),
                # "K-Neighboors Regressor":KNeighborsRegressor(),
                # "AdaBoost Regressor":AdaBoostRegressor(),
                # "Cat Boosting Regressor": CatBoostREgressor(verbose = False),
                # "XGB Regressor":XGBRegressor()
            }
            
            model_report:dict = evaluate_model(x_train = x_train, y_train = y_train,x_test = x_test, y_test = y_test, models = models)
            
            ## to get the bet model score from dict
            
            best_model_score = max(sorted(model_report.values()))
            
            ## to get best model name from dict
            
            best_model_name = list(model_report.keys())[
                list(model_report.values()).index(best_model_score)
            ]
            
            best_model = models[best_model_name]
            
            if best_model_score<0.6:
                raise CustomException("No best model found")
            
            logging.info(f"best found model on both trainig and testing dataset")
            
            save_object(
                file_path= self.model_trainer_config.trainer_model_file_path,
                obj = best_model
            )
            
            predicted = best_model.predict(x_test)
            
            r2_Score = r2_score(y_test, predicted)
            
            return r2_Score, predicted
                
        except Exception as e:
            raise CustomException(e,sys)    