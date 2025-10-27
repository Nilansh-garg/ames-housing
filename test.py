from src.models.predict_model import CustomData,PredictPipeline 
import numpy as np
from src.exception import CustomException
from src.logger import logging

logging.info('Starting prediction for a sample data point')


def predict_datapoint():
    data=CustomData(
                # CONVERT TO FLOAT/INT HERE before passing
        Overall_Qual=int(3), 
        Gr_Liv_Area=int(900), 
        Garage_Cars=float(2),   
        Garage_Area=float(700),   
        First_Flr_SF=int(800), 
        Total_Bsmt_SF=float(1000),
        Lot_Area=int(1000),
        BsmtFin_SF_1=float(800),
        Full_Bath=int(3),
        year_since_remod=int(4)
    )
    logging.info('Custom data instance created')
        
    pred_df=data.get_data_as_data_frame()

    logging.info(f"Prediction Input DataFrame:\n{pred_df}")

    predict_pipeline=PredictPipeline()
    results=predict_pipeline.predict(pred_df)
            
    # IMPORTANT: If your model predicts Log(SalePrice), you MUST expm1() the result!
    final_result = np.round((results[0]),2)[0]
    logging.info(f"Prediction results:\n{results}")

    print(f"Final result:\n{final_result}")
    logging.info('Prediction process completed')

predict_datapoint()