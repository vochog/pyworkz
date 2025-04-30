import requests
from bs4 import BeautifulSoup

def download_tiktok_video(video_url):
    session = requests.Session()

    # Step 1: Post to SnapTik
    response = session.post(
        "https://snaptik.app/action.php",
        data={"url": video_url}
    )

    if response.status_code != 200:
        print("Failed to access SnapTik.")
        return

    soup = BeautifulSoup(response.text, "html.parser")
    links = soup.find_all("a", class_="abutton is-success is-download")

    if not links:
        print("No downloadable links found.")
        return

    # Download the first download link
    download_link = links[0]["href"]
    print(f"Downloading from: {download_link}")

    video_data = session.get(download_link).content

    with open("tiktok_video.mp4", "wb") as f:
        f.write(video_data)

    print("Download completed: tiktok_video.mp4")

# Example usage
tiktok_url = input("Enter TikTok video URL: ")
download_tiktok_video(tiktok_url)