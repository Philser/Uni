#!/usr/bin/env python

import sys, socket

def create_error_page(conn, err_string):
    conn.send('HTTP/1.1 200 OK\r\n')
    conn.send('Connection: close\r\n')
    conn.send('Content-Type: text/html\r\n\r\n')
    conn.send('<html><head><title>ERROR</title></head>\r\n')
    conn.send('<body><h1>Error</h1><hr/><p>%s</p></body></html>'%(err_string))
    conn.close()

def handleRequest(conn):
    data = conn.recv(1024).decode("utf-8")

    head, body = data.split('\r\n\r\n')
    header = {}
    values = {}

    lines = head.split('\r\n')
    requestLine = lines[0]
    for line in lines[1:]:
        key, value = line.split(': ')
        header[key] = value
        
    kontostand = 100
    amount = 0.0
    # Request was a POST, send 303
    if requestLine.startswith('POST'):
        if body:
            pairs = body.split('&')
            for pair in pairs:
                key, value = pair.split('=')
                values[key] = value

        if 'amount' in values:
            try:
                amount = float(values['amount'])
            except:
                create_error_page(conn, "%s ist kein Fliesskommawert"%(values['amount']))
                return
            if 'Cookie' in header:
                cookieFields = header['Cookie'].replace('Cookie: ', '')
                cookieFields = cookieFields.split(';')
                for cookieField in cookieFields:
                    if cookieField.startswith('Kontostand'):
                        kontostand = float(cookieField.split('=')[1])
            kontostand -= amount
        # Send 303 Header to get Client to send GET
        conn.send(b'HTTP/1.1 303 See other\r\n')
        conn.send(b'Location: http://localhost:42422\r\n')
        conn.send(b'Set-Cookie: Kontostand=%5.2f;\r\n' % (kontostand))
        conn.send(b'Set-Cookie: Amount=%5.2f\r\n\r\n' % (amount))
        conn.close()
    elif requestLine.startswith('GET'):
        # Send Web Page
        conn.send(b'HTTP/1.1 200 OK\r\n')
        conn.send(b'Connection: close\r\n')
        conn.send(b'Content-Type: text/html; charset=utf-8\r\n\r\n')

        conn.send(b'<html><head><title>Konto</title></head>\r\n')
        conn.send(b'<body><h1>Konto</h1><hr/>\r\n')
        # Read values from cookie, set to 0 if not found
        # TODO: best practice?
        if 'Cookie' in header:
            amount = 0.0
            kontostand = 0.0
            cookieVal = header['Cookie'].replace('Cookie: ', '')
            cookieFields = cookieVal.split(';')
            for cookieField in cookieFields:
                if cookieField.strip().startswith('Amount'):
                    amount = float(cookieField.split('=')[1])
                elif cookieField.startswith('Kontostand'):
                    kontostand = float(cookieField.split('=')[1])
            conn.send(('<p>Überwiesen = %5.2f</p>\r\n'%(amount)).encode())
            conn.send(('<p>Neuer Kontostand = %5.2f</p>\r\n'%(kontostand)).encode())
        else:
            conn.send(('<p>Kontostand = 100</p>\r\n').encode())   
        conn.send(b'<form method="POST">\r\n')
        conn.send('<p>Betrag zum Überweisen: <input type="text" name="amount"/></p>\r\n'.encode())
        conn.send(b'<p><input type="submit" value="Abschicken"/></p>\r\n')
        conn.send(b'</form>\r\n')
        conn.send(b'</body></html>\r\n')
        conn.close()
    return

KONTOSTANDFILE = 'konto.txt'

# empty string == INADDR_ANY
TCP_IP = ''
TCP_PORT = 42422
print("Starting Server...")
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
s.bind((TCP_IP, TCP_PORT))
s.listen(1)
print("Started")

while 1:
    conn, addr = s.accept()
    print("Incoming Connection")
    handleRequest(conn)
