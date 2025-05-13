css = '''
<style>
.chat-container {
    max-width: 800px;
    margin: auto;
    padding-top: 1rem;
}

.chat-message {
    padding: 1.2rem;
    border-radius: 1rem;
    margin-bottom: 1.2rem;
    display: flex;
    align-items: flex-start;
    gap: 1rem;
    box-shadow: 0 2px 8px rgba(0,0,0,0.15);
    transition: all 0.3s ease-in-out;
}

.chat-message.user {
    background-color: #1e1e2f;
    flex-direction: row-reverse;
}

.chat-message.bot {
    background-color: #34495e;
}

.chat-message .avatar {
    flex-shrink: 0;
}

.chat-message .avatar img {
    width: 64px;
    height: 64px;
    border-radius: 50%;
    object-fit: cover;
    border: 2px solid #ffffff33;
}

.chat-message .message {
    flex-grow: 1;
    color: #f5f5f5;
    font-size: 1rem;
    line-height: 1.5;
    word-wrap: break-word;
}
</style>
'''

bot_template = '''
<div class="chat-container">
    <div class="chat-message bot">
        <div class="avatar">
            <img src="https://www.shutterstock.com/image-vector/chat-bot-icon-design-robot-600nw-2476207303.jpg" alt="Bot Avatar" style="max-height: 78px; max-width: 78px; border-radius: 50%; object-fit: cover;">
        </div>
        <div class="message">{{MSG}}</div>
    </div>
</div>
'''

user_template = '''
<div class="chat-container">
    <div class="chat-message user">
        <div class="avatar">
            <img src="https://cdn-icons-png.flaticon.com/512/10012/10012487.png" alt="User Avatar">
        </div>    
        <div class="message">{{MSG}}</div>
    </div>
</div>
'''
