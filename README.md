<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Crimson+Pro&family=Literata" rel="stylesheet">

<div align=center>
<img src="images/icon.png" alt="icon.png" width="200" height="200">
<h1>BeReal-Bot</h1>

## Description
Welcome to BeReal-Bot! 👋 This bot is designed to capture authentic moments, just like the BeReal app. Every day, at a random time, you’ll be prompted to share a photo that showcases your true self—no filters, no edits! 📸✨

## How It Works

  **Random Moment:**  
   You’ll receive a notification at a surprise time.

  **Snap a Pic:**  
   You’ll have 2 minutes to take a photo of what you’re doing right at that moment. It’s all about being real!

  **Share & Connect:**  
   After you snap your pic, you can share them with friends and see their moments too. Let’s keep it genuine!

## Remember
It’s not about the likes; it’s about capturing life as it is. So get ready to embrace the spontaneity! 🎉
Feel free to modify any sections as needed!
</div>


<div align=center>
  
## How to install

</div>

Not interested in downloading bot to your computer, you can add bot to your server [here](https://discord.com/oauth2/authorize?client_id=1261134025955868775&permissions=1710833919851760&integration_type=0&scope=bot)

Follow these steps to run the Discord application and add it to your server.
1. If you are *not* an author, fork the repository [here](https://github.com/pedropa140/bereal-bot/fork).
2. Clone the repository.
    ```bash
    git clone https://github.com/pedropa140/bereal-bot
    ```

3. Install Dependencies
   - Make sure your pip version is up-to-date:
      ```bash
      pip install --upgrade pip
      ```
      ```bash
      pip install -r requirements.txt
      ```
3. Create Discord Application <br>
    - Go to [https://discord.com/developers/applications](https://discord.com/developers/applications)
    - Click on **New Application**
    - Give it a name
    - Agree to [Developer Terms and Services](https://discord.com/developers/docs/policies-and-agreements/developer-terms-of-service) and [Developer Policy](https://discord.com/developers/docs/policies-and-agreements/developer-policy)
    - Go to the **Bot** tab
      - Click on **Reset Token** to receive Discord Application Token
      - Go back to the Github clone and create a **.env** file
      - Type
        
        ```bash
        DISCORD_TOKEN = '**REPLACE WITH DISCORD TOKEN THAT YOU JUST COPIED**'
        ```
    - Go to the **OAuth2** tab
      - For **OAuth2 URL Generator**, click on **bot** on the second column
        - For **General Permissions**, click on
          - **Read Messages/View Channels**
          - **Manage Events**
          - **Create Events**
          - **Moderate Members**
          - **View Server Insights**
          - **View Creator Monetization Insights**
  
      
        - For **Text Permissions**, click on
          - **Send Messages**
          - **Create Public Threads**
          - **Create Private Threads**
          - **Send Messages in Threads**
          - **Send TTS Messages**
          - **Manage Messages**
          - **Manage Threads**
          - **Embed Links**
          - **Attach Files**
          - **Read Message History**
          - **Read Message History**
          - **Mention Everyone**
          - **Use External Emojis**
          - **Use External Stickers**
          - **Add Reactions**
          - **Use Stash Commands**
          - **Use Embedded Activities**
  
      
        - For **Voice Permissions**, click on
          - **Use Embedded Activites**
  
            
      - Copy the **Generated URL** and paste it in your web browser.
      - Click on the Discord server you would like to add the bot into.
      - In your server, please create a discussion channel called **#bereal-bot** so the bot can enter messages in. Make the **View Messages** permission for **@everyone** hidden.
      - Create a role called **bereal-user** and make its only permission is to view **#bereal-bot**.
      - Have fun!
        
<div align=center>   
  
## How to run the Birthday-Bot

In a terminal, find the directory where main.py is located and run this command:
</div>

  ```bash
  python main.py
  ```

### Options:
  - **/adduser [FIRST_NAME] [LAST_NAME]**
    - Adds a user to the database.
  - **/removeuser**
    - Removes a user from the database.