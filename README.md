# LTV_Calculation

This utility stores all events of customers in a data structure.Calculates Lifetime Value for each customer and returns top x customers.

Events are new customer, customer updates, site_visit, image_upload and order.

Methods are 
Ingest(e,D) : Stores event e in data structure D

TopxSimpleLTVCutomers(x,D) : Retuens top x customers with highest LTV in D

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

LTV = 10 * 52 * revenue/weeks

where revene = sum of all order amounts
weeks        = number of weeks 
