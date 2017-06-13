# LTV_Calculation

This utility stores all events of customers in a data structure. Calculates Lifetime Value for each customer and returns top x customers.

Events are new customer, customer updates, site_visit, image_upload and order.

Methods are 
Ingest(e,D) : Stores event e in data structure D

TopxSimpleLTVCutomers(x,D) : Returns top x customers with highest LTV in D

Data structure is python dictionary which has one entry for each customer and of the form below

D : {
      c1 : {lastname: , adr_city:  , adr_state: ,  event_time:  ,
            site_visit : [],
            image : [],
            order : {}      
          }
          .
          .            
    }

site_visit : maintains list of dictionary to store all site_vist events
image      : maintains list of dictionary to store all image upload events
order      : maintains dictionary of orders with key as order_id and value as dictionary of order details


Calculating LTV:
Assuming average customer lifespan = 10 years, LTV can be calculated for each customer as below
LTV = 10 * 52 * order_revenue / site_visited_count * site_visited_count / num_of_weeks
which can be simplified to 
LTV = 10 * 52 * order_revenue / num_of_weeks
where, 
order_revenue => sum of all orders made by that customer 
num_of_weeks  => number of weeks from first site visit to last one

Assumptions:
Customer must exists in D for events like site_visit, image or order
All orders are due to site_visit events

Input:
Text file of events, All events are seperated by ,
each event is a dictionary

Output:
Text file of top 10 customers with their respective SLV in descending order of SLV

Technology:
Python 3

Instructions to Run:
Maintain Folder containing subfolders
      src : contains ltv_calc.py
      input : contains input.txt
      output : empty or with output.txt
      
Go to src subfolder location in command line and just give ltv_calc on command line 
ltv_calc will take input as input.txt from input subfolder and will store output in output.txt in output subfolder


