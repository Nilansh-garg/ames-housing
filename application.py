from flask import Flask,request,render_template
import numpy as np
import pandas as pd

from sklearn.preprocessing import StandardScaler
from src.models.predict_model import CustomData,PredictPipeline 

application=Flask(__name__)

app=application

## Route for a home page

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/about')
def about():
    return render_template('about.html')


@app.route('/predictdata',methods=['GET','POST'])
def predict_datapoint():
    if request.method=='GET':
        return render_template('home.html')
    else:
        try:
            data=CustomData(
                # CONVERT TO FLOAT/INT HERE before passing
                Overall_Qual=int(request.form.get('Overall_Qual')), # Should be float/int
                Gr_Liv_Area=int(request.form.get('Gr_Liv_Area')),   # Should be float/int
                Garage_Cars=float(request.form.get('Garage_Cars')),   # Should be float/int
                Garage_Area=float(request.form.get('Garage_Area')),   # Should be float/int
                First_Flr_SF=int(request.form.get('First_Flr_SF')), 
                Total_Bsmt_SF=float(request.form.get('Total_Bsmt_SF')),
                Lot_Area=int(request.form.get('Lot_Area')),
                BsmtFin_SF_1=float(request.form.get('BsmtFin_SF_1')),
                Full_Bath=int(request.form.get('Full_Bath')),
                year_since_remod=int(request.form.get('year_since_remod'))
            )
        except ValueError as e:
            # Handle cases where the user enters non-numeric data in a number field
            return render_template('home.html', results=f"Error: Invalid input format. Please ensure all fields are numbers. Detail: {e}")
            
        
        pred_df=data.get_data_as_data_frame()
        print("Prediction Input DataFrame:\n", pred_df)

        predict_pipeline=PredictPipeline()
        results=predict_pipeline.predict(pred_df)
        
        final_result = np.round((results[0]),2)[0]
        
        return render_template('home.html',results=f"{final_result:.2f}")
    

if __name__=="__main__":
    app.run(host="0.0.0.0")        
