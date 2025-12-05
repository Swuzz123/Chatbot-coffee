from database.ingestion import ingest_data

if __name__ == '__main__':
  try:
    data = '/home/nmtri2110/Workspace/CoffeeAssistant/data/coffee_house_data.csv'
    ingest_data(data)
    
    print("Succesfully ingest data!")
  except Exception as e:
    print("Failed to ingest data, reason {e}")