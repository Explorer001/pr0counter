import requests
import time
import threading

FIRST_DONATION_ID = 2447473
URL_API = "http://pr0gramm.com/api"
POST = "/items/info?itemId="
FLAG_NEW = "&flags=7"
CONFIDENCE_THRESHOLD = 0.1
THREAD_SUMS = []

def main():
    global FIRST_DONATION_ID, THREAD_SUMS
    num_threads = 4
    thread_add = num_threads
    
    threads = []
    post_id = FIRST_DONATION_ID

    THREAD_SUMS = [0] * num_threads

    for i in range(num_threads):
        t = threading.Thread(target=sum_worker, args=(post_id+i, i, thread_add))
        threads.append(t)
        t.start()

    donations = 0

    for thread in threads:
        thread.join()

    print(str(sum(THREAD_SUMS))+"€")

def sum_worker(start_id, thread_id, id_add, limit=0):
    global URL_API, POST, FLAG_NEW, CONFIDENCE_THRESHOLD, THREAD_SUMS
    
    print("Thread " + str(thread_id) + " started!")

    request_url = URL_API + POST

    #variables for limit
    limit_reached = False
    limit_id = start_id + limit

    donation_sum = 0
    
    post_id = start_id

    empty_tag_count = 0
    empty_tag_threshold = 10

    while not limit_reached:

        #send http request
        response = requests.get(request_url + str(post_id))
    
        if response.status_code != 200:
            print(response)
            print("ZOMG!")
        else:
            #transform response in json and get tags
            data = response.json()
            tags = data["tags"]
            
            for tag in tags:
                tag_message = tag["tag"]
                tag_confidence = tag["confidence"]
                if "€" in tag_message and tag_confidence > CONFIDENCE_THRESHOLD:
                    try:
                        donation_amount = float(tag_message.replace("€", ""))
                        donation_sum += donation_amount
                        print(tag_message + " | " + str(post_id) + " | " + str(donation_sum) + " | " + str(thread_id))
                        break
                    except:
                        continue

            if len(tags) == 0:
                empty_tag_count += 1
            else:
                empty_tag_count = 0

        if post_id > limit_id and limit != 0:
            limit_reached = True

        if empty_tag_count > empty_tag_threshold:
            limit_reached = True

        post_id += id_add

        time.sleep(0.1)

    THREAD_SUMS[thread_id] = donation_sum

main()
#sum_worker(2459586, 1, 1)
