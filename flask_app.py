from flask import Flask, render_template, request

# some connfigurations
cipher_table = []
base = 32
tblSize = 128 - base;

# creating the cipher table
for index in range(tblSize):
    curr_list = range(index, index + tblSize)

    # fixing the list
    curr_list = map(lambda x: chr(base + (x % tblSize)), curr_list)

    # adding the new list to the table
    cipher_table.append(curr_list)


# encrypting the message by key
def encrypt_msg(key, msg):
    
    encrypted_msg = ""

    # fixing newline issues
    key = key.replace('\r\n', '\n')
    msg = msg.replace('\r\n', '\n')

    # converting msg to list
    msg_list = list(msg)

    # creating a list of locations for each key's letter alphabet
    key_chars = map(lambda x: ord(x) - base, list(key))

    # encrypting the message
    for loc in range(len(msg_list)):

        # ignoring new lines
        if(msg_list[loc] == '\n'):
            encrypted_msg += '\n'
        else:
            # current character in message
            curr_char = msg_list[loc]
            
            # finding the location of the fitting encrpyed character in alphbet line
            char = ord(curr_char) - base

            # the alphabet to encrypt based on the key current char
            alphabet = key_chars[loc % len(key_chars)]

            # adding the encrypted char to the message
            encrypted_msg += cipher_table[alphabet][char]
        
    # adujsting encrypted text to web display
    return encrypted_msg.replace('\n', '\r\n')


# decrypting the message by key
def decrypt_msg(key, msg):
    
    decrypted_msg = ""

    # fixing newline issues
    key = key.replace('\r\n', '\n')
    msg = msg.replace('\r\n', '\n')

    # converting msg to list
    msg_list = list(msg)

    # creating a list of locations for each key's letter alphabet
    key_chars = map(lambda x: ord(x) - base, list(key))

    # decrypting the message
    for loc in range(len(msg_list)):
        
        if(msg_list[loc] == '\n'):
            decrypted_msg += '\n'
        else:
            # the current character to decrypt
            curr_char = msg_list[loc]

            # the alphabet to encrypt based on the key current char
            alphabet = key_chars[loc % len(key_chars)]

            # decrypting the char to the original message
            decrypted_msg += chr(base + cipher_table[alphabet].index(curr_char))
    
    # adujsting decrypted text to web display
    return decrypted_msg.replace('\n', '\r\n')


app = Flask(__name__, static_folder='static', static_url_path='/static')

# handle the encryption request
def encrypt_user_msg(key, msg):
    ans = encrypt_msg(key, msg)
    return render_template('msg_encrypted.html', key=key, org_msg=msg, enc_msg=ans)

# handle the decryption request
def decrypt_user_msg(key, msg):
    ans = decrypt_msg(key, msg)
    return render_template('msg_decrypted.html', key=key, org_msg=msg, dec_msg=ans)


@app.route("/")
def root():
    # return app.send_static_file('index.html')
    return render_template('index.html')

@app.errorhandler(404)
def page_not_found(error):
    return render_template('404.html')

@app.route('/code', methods=['POST', 'GET'])
def code():
    error = None
    if (request.method == 'POST'):
        # 0 - encrypt | 1 - decrypt
        act = request.form['act']

        # converting both key & message to ASCII
        key = request.form['key'].encode('ascii', 'ignore')
        msg = request.form['msg'].encode('ascii', 'ignore')
    
        # assuming the input validation preformed on the HTML page
        if act == '0':
            return encrypt_user_msg(key, msg)
        else:
            return decrypt_user_msg(key, msg)

    else:
        error = 'There was a problem with your input, please try again.'
        # the code below is executed if the request method
        # was GET or the credentials were invalid
        return render_template('error.html', error=error)


if __name__ == "__main__":
    app.run()

