# DA353 Internet of Things Course Project
By @ankitaanand28 @Sunanda-K-H @SHIVAM200219
## Crop And Fertilizer Recommendation
A website that allows farmers to get a crop and fertilizer recommendation based on their soil and location details using machine learning models.

## Technologies

- ReactJS
- Flask
- Python
- MongoDB
- MicroPython
- Selenium

## Dataset
- [Fertilizer Prediction Dataset](https://www.kaggle.com/datasets/gdabhishek/fertilizer-prediction)
- [Crop Recommendation Dataset](https://www.kaggle.com/datasets/atharvaingle/crop-recommendation-dataset)

## Deployment 
Running the app

### Starting the Server

1. Navigate to the server directory:

2. Start the server by running the following command:
 

   ```bash
   cd crop-prediction/server
   python server.py
   ```


Open a separate terminal and run the following command from the root directory:

```bash
cd crop-prediction
npm start
```

To automatically extract the latest data entry from the MongoDB server run this file on a separate terminal , ensure you have access to the MongoDB database.

   ```bash
   cd crop-prediction/server
   python selenium_autofill.py
   ```





