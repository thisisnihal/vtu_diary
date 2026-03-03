# vtu internship diary fill automatation using playwright

1. Create python environment and activate it  
2. Install dependencies.  
```
pip install -r requirements.txt 
```  
3. create `.env` file and copy the varibales from `.env.example`  

4. Edit work hour in `config.py` if needed.  

5. Run the server  
```
python server.py
```

6. Select start date and end date (I prefer 1 month at a time)  

7. Select holidays to avoid generating content for those days (It should sound legitimate :-\ )  

8. Review content once (check dates and content) and Save it.  
(It will save a json file like `2025-10-08_2025-11-30_internship_details.json`)  
You are free to modify the content.  

9. Select the same file for automation  

10. Hit Run Automation
