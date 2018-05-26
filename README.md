# REST API for Hotel System.

Steps to setup:

1. Clone the repository. ```git clone https://github.com/Anupam-dagar/RESTAPI.git```
2. Change directory to repository. `cd RESTAPI`
3. Run the shell script `run` to setup and run the server locally. `./run`. It will setup a virtual environment, install requirements and run the server.
4. To stop serving the website press `ctrl+c`.
5. If you want to again run the server, use the run script again, it won't setup virtual environment again and install requirements.

To modify the code:

1. Run the setup script. `./run`
2. Stop the server and activate the virtual environment. `source venv/bin/activate`
3. Run the server using `python3 manage.py runserver`.

API Details:

1. To update the details of a room on a given date:  
url: `/api/room/date-of-booking/`  
where date of booking should be in the YYYY-MM-DD format.  
Request Type: `PUT`  
```json
payload = {
    "singleroomaval": integer_value,
    "doubleroomaval": integer_value
}
```
default for both fields is 5.
integer_value should be between 0 and 5.

2. To update the details of room price on a given date:  
url: `/api/price/date-of-booking/`  
where date of booking should be in the YYYY-MM-DD format.  
Request Type: `PUT`  
```json
payload = {
    "pricesingle": integer_value,
    "pricedouble": integer_value
}
```
both fields are decimal field with upto 2 decimal places. More than 2 decimal places will result in an error. Both should be non negative.  
default for both fields is 0.00

3. To get the details of a room on a given date:  
url: `/api/room/date-of-booking/`  
where date of booking should be in the YYYY-MM-DD format.  
Request Type: `GET`  

4. To get the details of price of a room on a given date:  
url: `/api/price/date-of-booking/`  
where date of booking should be in the YYYY-MM-DD format.  
Request Type: `GET`  

5. To do bulk operations (updating values in a range of date):  
url: `/api/bulk/`  
Request Type: `PUT`  
```json
payload = {
    "from_date": YYYY-MM-DD,
    "to_date": YYYY-MM-DD,
    "days": [1-7],
    "room_type": single or double,
    "price": integer_value,
    "availability": 0-5
}
```  
`days` is an array with numbers from 1-7 with each number representing the respective day of the week.  
For example monday and tuesday will be sent as `[1,2]`.  
`room_type` is a string with value either `single` or `double`.  
`price` is a decimal field with upto 2 decimal places. More than 2 decimal places will result in an error. Price should be non negative.  
`availability` must be between 0 to 5 only.