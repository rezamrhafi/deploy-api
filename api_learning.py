from fastapi import FastAPI , HTTPException
import pandas as pd

# create instance/object
app = FastAPI()

@app.get("/")
def root():
    return {"message": "Hello World"}

@app.get("/data")
def get_data():
    df = pd.read_csv('data.csv')
    #convert dataframe to dictionary
    return df.to_dict(orient="records")

@app.get("/data/{id}")
def get_data_by_id(id : int):
    df = pd.read_csv('data.csv')


    #opsi filter -> df[kondisi] atau df.query(kondisi)

    #filter berdasarkan id
    filter = df[df.id == id]

    #condition if/else for filtering
    #if our data is not found or no match data
    if len(filter) == 0:
        raise HTTPException(status_code=404, detail="No Data!")
    else:
        #convert dataframe to dictionary
        return filter.to_dict(orient="records")
    
@app.get("/name/{name}")
def get_data_by_name(name : str):
    df = pd.read_csv('data.csv')


    #opsi filter -> df[kondisi] atau df.query(kondisi)
    # df[name] = df.name

    #filter berdasarkan id
    filter1 = df[df['fullname'].str.lower() == name.lower()]

    #condition if/else for filtering
    #if our data is not found or no match data
    if len(filter1) == 0:
        raise HTTPException(status_code=404, detail="No Data!")
    else:
        #convert dataframe to dictionary
        return filter1.to_dict(orient="records")
    

#define end-point for updating data
@app.post('/input_data/')
def add_data(update_df:dict):
    df = pd.read_csv('data.csv')
    # define new id for new data
    id = len(df) + 1

    #assign new id to column id in new df named update_df 
    update_df['id'] = id

    new_data = pd.DataFrame([update_df])
    df = pd.concat([df, new_data], ignore_index=True)

    # Save updated DataFrame back to CSV
    df.to_csv('data.csv', index=False)

    return df.to_dict(orient='records')