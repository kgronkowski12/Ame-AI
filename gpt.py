import g4f
from g4f.cookies import set_cookies

g4f.debug.logging = True # enable logging
g4f.check_version = False # Disable automatic version checking




messag = []
messag.append({"role": "System", "content": "You are an Assistant. All the messages with the role 'Assistant' were sent by you before. Respond to user's request. (Only write your response, without 'Assistant:' or any other starting string)"})
while True:
    print(messag)
    print()
    question = input("> ")
    #messag.append({"role": "User", "content": question})
    # streamed completion
    response = g4f.ChatCompletion.create(
        #model="gpt-3.5-turbo",
        model="gemini",
        cookies = g4f.get_cookies(".google.com"),
        messages=messag,
        stream=True,
    )

    resp = ""
    print()
    for message in response:
        print(message, flush=True, end='')
        resp+=message+" "
    messag.append({"role": "Assistant", "content": resp})


