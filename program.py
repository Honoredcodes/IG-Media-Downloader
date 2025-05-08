import instaloader
import os
import time
import getpass

# Initialize Instaloader with no metadata
L = instaloader.Instaloader(
    download_comments=False, 
    download_geotags=False, 
    download_video_thumbnails=False, 
    save_metadata=False
)

# Set a custom User-Agent
L.context._session.headers.update({
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
})

your_username = input("Enter your Instagram username: ")
your_password = getpass.getpass("Enter your Instagram password: ")

username = input("Enter the target Instagram profile username: ")

# Define session file
session_file = f"{your_username}_session"

# Define the download directory
script_directory = os.path.dirname(os.path.realpath(__file__))
os.chdir(script_directory)
save_directory = os.path.join(script_directory, "Downloads", username)
os.makedirs(save_directory, exist_ok=True)

# Handle 2FA login
def input_2fa_code():
    two_factor_code = input("Enter the two-factor authentication code: ")
    L.two_factor_login(two_factor_code)
    print("✅ 2FA authentication successful!\n")

# Login with session handling
try:
    if os.path.exists(session_file):
        print("🔄 Loading saved session...\n")
        L.load_session_from_file(your_username, filename=session_file)
    else:
        print("🔑 Logging in...\n")
        try:
            L.login(your_username, your_password)
            print("✅ Login successful! Saving session...\n")
            L.save_session_to_file(filename=session_file)
        except instaloader.TwoFactorAuthRequiredException:
            print("⚠️ Two-factor authentication is required.\n")
            input_2fa_code()
            L.save_session_to_file(filename=session_file)

    # Load target profile
    print(f"📂 Loading profile: {username}\n")
    profile = instaloader.Profile.from_username(L.context, username)
    print(f"📥 Downloading posts from {username}...\n")
    for count, post in enumerate(profile.get_posts(), start=1):
        post_url = f"https://www.instagram.com/p/{post.shortcode}/"
        print(f"📌 [{count}] Downloading: {post_url}\n")
        L.download_post(post, target=save_directory)
         # Randomized delay
        time.sleep(3 + count % 5) 

    print(f"✅ All {count} media from {username} downloaded to: {save_directory}\n")

except instaloader.LoginRequiredException:
    print("❌ Login failed or session expired. Deleting session file and retrying.\n")
    if os.path.exists(session_file):
        os.remove(session_file)
except instaloader.ConnectionException as e:
    print(f"⚠️ Connection error: {e}\n")
    print("Instagram might have restricted access. Try again later.\n")
except instaloader.ProfileNotExistsException:
    print(f"❌ The profile '{username}' does not exist or is private.\n")
except instaloader.AbortDownloadException as e:
    print(f"🚫 Download aborted: {e}\n")
except Exception as e:
    print(f"⚠️ Unexpected error: {e}\n")