import streamlit as st
import requests
from bs4 import BeautifulSoup
import streamlit.components.v1 as components

# Helper function to extract retweeted image
def get_retweeted_image(tweet_url):
    response = requests.get(tweet_url)
    soup = BeautifulSoup(response.content, "html.parser")
    
    # Look for the image within the retweet
    image_tag = soup.find("img", {"alt": "Image"})
    if image_tag:
        image_url = image_tag["src"]
        return image_url
    return None

# Streamlit app
st.title("Twitter Retweeted Image Screenshot")

# Input field for Tweet URL
tweet_url = st.text_input("Enter the Twitter link")

if tweet_url:
    image_url = get_retweeted_image(tweet_url)
    
    if image_url:
        st.image(image_url, caption="Retweeted Image", use_column_width=True)
        
        # HTML/JavaScript block
        components.html(f"""
        <html>
        <body>
            <div id="tweet-container" style="max-width: 500px; margin: auto;">
                <img id="tweet-image" src="{image_url}" style="width:100%; border: 1px solid black;" />
            </div>
            <button id="capture-btn" style="margin-top: 20px;">Capture Screenshot</button>
            <script src="https://html2canvas.hertzen.com/dist/html2canvas.min.js"></script>
            <script>
                document.getElementById("capture-btn").addEventListener("click", function() {{
                    html2canvas(document.getElementById("tweet-container")).then(canvas => {{
                        var imgData = canvas.toDataURL("image/png");
                        var link = document.createElement('a');
                        link.href = imgData;
                        link.download = 'retweet_screenshot.png';
                        document.body.appendChild(link);
                        link.click();
                        document.body.removeChild(link);
                    }});
                }});
            </script>
        </body>
        </html>
        """, height=600)
    else:
        st.error("No retweeted image found in this tweet.")
