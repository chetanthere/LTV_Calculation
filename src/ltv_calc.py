import ast
import operator
from collections import OrderedDict
import datetime
from datetime import timedelta


def ingest(e,D):

    # Check event type
    if e['type'] == 'CUSTOMER':

        val_struct = {'event_time': None, 'last_name': '', 'adr_city': '', 'adr_state': '',
                      'site_visit': [],
                      'image': [],
                      'order': {}}

        if e['verb'] == 'NEW':
            # Checking whether customer already exists
            if e['key'] in D:
                raise ValueError('Customer already exists for  NEW CUSTOMER')

            else:
                # Update val_struct
                if 'last_name' in e:
                    val_struct['last_name'] = e['last_name']

                if 'adr_city' in e:
                    val_struct['adr_city'] = e['adr_city']

                if 'adr_state' in e:
                    val_struct['adr_state'] = e['adr_state']

                val_struct['event_time'] = e['event_time']

                # Add New customer into event_database D
                D[e['key']] = val_struct

        elif e['verb'] == 'UPDATE':
            # Checking whether customer already exists
            if e['key'] in D:
                # Not storing event_time of CUSTOMER UPDATES
                if 'last_name' in e:
                    D[e['key']]['last_name'] = e['last_name']

                if 'adr_city' in e:
                    D[e['key']]['adr_city'] = e['adr_city']

                if 'adr_state' in e:
                    D[e['key']]['adr_state'] = e['adr_state']

            else:
                raise ValueError('Customer is not exists for  UPDATE CUSTOMER')

        else:
            raise ValueError('Wrong CUSTOMER Event Verb')


    if e['type'] == 'SITE_VISIT':

        if e['verb'] == 'NEW':
            # Check whether customer already exists
            # Assuming SITE_VISIT are only for existing customers
            if e['customer_id'] in D:
                # Update SITE_VISIT for current customer in D
                temp_dict = {}
                temp_dict['page_id'] = e['key']
                temp_dict['event_time'] = e['event_time']
                if 'tags' in e:
                    temp_dict['tags'] = e['tags']
                D[e['customer_id']]['site_visit'].append(temp_dict)

            else:
                raise ValueError('Customer does not exist for SITE_VISIT event')

        else:
            raise ValueError('Wrong SITE_VISIT Event Verb')


    if e['type'] == 'IMAGE':

        if e['verb'] == 'UPLOAD':
            # Check whether customer already exists
            if e['customer_id'] in D:
                # Update IMAGE for current customer in D
                temp_dict = {}
                temp_dict['image_id'] = e['key']
                temp_dict['event_time'] = e['event_time']
                if 'camera_make' in e:
                    temp_dict['camera_make'] = e['camera_make']
                if 'camera_model' in e:
                    temp_dict['camera_model'] = e['camera_model']
                D[e['customer_id']]['image'].append(temp_dict)

            else:
                raise ValueError('Customer does not exist for IMAGE event')

        else:
            raise ValueError('Wrong IMAGE Event Verb')


    if e['type'] == 'ORDER':

        if e['verb'] == 'NEW':
            # Check whether customer already exists
            if e['customer_id'] in D:
                # Add New ORDER for current customer in D
                # Not checking for order's existence if it's already there it will update
                temp_dict = {}
                temp_dict['event_time'] = e['event_time']
                temp_dict['total_amount'] = e['total_amount']
                D[e['customer_id']]['order'][e['key']] = temp_dict

            else:
                raise ValueError('Customer does not exist for NEW ORDER event')

        elif e['verb'] == 'UPDATE':
            # Check whether customer already exists
            if e['customer_id'] in D:
                # Update ORDER for current customer in D
                # Not checking for order's existence if it's not there it will be added
                temp_dict = {}
                temp_dict['event_time'] = e['event_time']
                temp_dict['total_amount'] = e['total_amount']
                D[e['customer_id']]['order'][e['key']] = temp_dict
            else:
                raise ValueError('Customer does not exist for UPDATE ORDER event')

        else:
            raise ValueError('Wrong ORDER Event Verb')


def TopXSimpleLTVCustomers(x,D):

    # Calculating SLV for each customer in D
    slv_dict = {}
    for customer in D:
        order_revenue = 0

        for key, value in D[customer]['order'].items():
            try:
                order_revenue += float(value['total_amount'].split(' ')[0])
            except:
                pass

        #Find out number of weeks of site visited for that particulat customer
        # Assumption here is event can come in any order so site visit events may not be in sorted order of event_time

        # Formula here is SLV = 10 * 52 * order_revenue / site_visited_count * site_visited_count / num_of_weeks
        # Therefore SLV = 10 * 52 * order_revenue / num_of_weeks

        num_of_weeks = 0
        min_sv_event_time = 99991231
        max_sv_event_time = 00000000

        if D[customer]['site_visit']:
            for sv in D[customer]['site_visit']:
                sv_event_time = sv['event_time'][:10]
                sv_event_time = sv_event_time.split('-')
                sv_event_time = int(''.join(sv_event_time))

                if sv_event_time < min_sv_event_time:
                    min_sv_event_time = sv_event_time

                if sv_event_time > max_sv_event_time:
                    max_sv_event_time = sv_event_time

            min_date = str(min_sv_event_time)
            max_date = str(max_sv_event_time)

            d1 = datetime.date(int(min_date[0:4]), int(min_date[4:6]), int(min_date[6:]))
            d2 = datetime.date(int(max_date[0:4]), int(max_date[4:6]), int(max_date[6:]))

            monday1 = (d1 - timedelta(days=d1.weekday()))
            monday2 = (d2 - timedelta(days=d2.weekday()))

            num_of_weeks = ( (monday2 - monday1).days / 7 ) + 1

        if num_of_weeks > 0:
            slv_dict[customer] = 10 * 52 * order_revenue / num_of_weeks
        else:
            slv_dict[customer] = 0

    slv_dict_sort = OrderedDict(sorted(slv_dict.items(),key=operator.itemgetter(1),reverse=True))

   
    max_slv_list = []
    i = 1
    for k,v in slv_dict_sort.items():
        if i <= x:
            max_slv_list.append({k:v})
        else:
            break
        i += 1

    with open('../output/output.txt','w',encoding='utf-8') as out_file:
        for slv_val in max_slv_list:
            out_file.write(str(slv_val) + '\n')


if __name__ == '__main__':

    event_database = {}

    with open('../input/input.txt',encoding='utf-8') as inp_file:

        file_str = inp_file.read()
        try:
            file_str_list = ast.literal_eval(file_str)
        except:
            raise ValueError('Events are not recorded properly in input file, Expected : String of dictionaries')


        for event in file_str_list:
            ingest(event,event_database)

    TopXSimpleLTVCustomers(10, event_database)


