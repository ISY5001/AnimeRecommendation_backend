import requests
import re
import os

def download_and_rename_anime_poster(anime_url, save_folder):
    try:
        # Send an HTTP GET request to the provided URL
        response = requests.get(anime_url)

        # Check if the request was successful (status code 200)
        if response.status_code == 200:
            # Use regular expressions to find the first occurrence of the image URL
            img_url_match = re.search(r'https://cdn\.myanimelist\.net/images/anime/(\d+)/(\d+)\.jpg', response.text)

            if img_url_match:
                img_url = img_url_match.group(0)  # Get the matched URL
                img_filename = f'anime_{img_url_match.group(1)}_{img_url_match.group(2)}.jpg'
                # print("img_filename is ", img_filename)
                img_path = os.path.join(save_folder, img_filename)

                # Download the image and save it with the new filename
                if not os.path.exists(img_path):
                    with open(img_path, "wb") as img_file:
                        headers = {'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML,like Gecko) Chrome/86.0.4240.111 Safari/537.36'}
                        img_file.write(requests.get(img_url, headers=headers,  verify=False).content)

                    return img_filename # do not return img_path
                else:
                    print(f"Image already exists: {img_path}")
                    return img_filename
            else:
                return None  # Image URL not found in the HTML
        else:
            print(f"Failed to fetch the URL. Status code: {response.status_code}")
            return None
    except Exception as e:
        print(f"An error occurred: {str(e)}")
        return None

# Example usage:
anime_url = "https://myanimelist.net/anime/1/Cowboy_Bebop"
save_folder = "./poster_images"  # Change this to your desired folder path
os.makedirs(save_folder, exist_ok=True)
poster_file_name = download_and_rename_anime_poster(anime_url, save_folder)

if poster_file_name:
    print(f"Poster downloaded and saved as: {poster_file_name}")
else:
    print("Poster URL not found or existed.")
