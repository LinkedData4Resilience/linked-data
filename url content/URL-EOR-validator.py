

import csv
import json
import time

import requests
num_url = 0
num_validated_url = 0
num_403_url = 0
num_404_url = 0

with open("datasets\enriched_original_EOR-2023-04-30.json") as fjson:
    data = json.load(fjson)

    with open("EOR_url_count.csv", "w", newline="") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["URL", "Response", "Request Duration"])
# Initialize an event ID counter
# with open("EOR_url_count.csv", "w", newline="") as csvfile:
#     writer = csv.writer(csvfile)
#     writer.writerow(["URL", "Response", "Request Duration"])

        # Loop through the features in the JSON file
        for feature in data['features']:
            # print ('event id ', event_id)
    
            if feature["properties"].get("country") == "Ukraine":
                if feature['properties'].get('url'):
                                        social_media_content_url = feature["properties"]['url']
                                        num_url += 1

                                            
                                        num_validated_url +=1
                                            

                                        request_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
                                        try:
                                            start_time = time.time()
                                            response = requests.get(social_media_content_url, timeout=5)
                                            if 200 <= response.status_code <= 299:
                                                num_validated_url += 1
                                            elif response.status_code == 403:
                                                num_403_url += 1
                                            elif response.status_code == 404:
                                                num_404_url += 1
                                            
                                            request_duration = time.time() - start_time
                                            writer.writerow([social_media_content_url, response.status_code, request_duration])
                                        except requests.Timeout:
                                            writer.writerow([social_media_content_url, "Timeout Error", None])
                                        except Exception as e:
                                            writer.writerow([social_media_content_url, str(e), None])

print ('count URL: ', num_url)
print ('valid URL: ', num_validated_url)
print ('403 URL: ', num_403_url)
print ('404 URL: ', num_404_url)