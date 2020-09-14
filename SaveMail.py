from cryptography.fernet import Fernet

import os

def encrypt(message: bytes, key: bytes) -> bytes:
    return Fernet(key).encrypt(message)

def decrypt(token: bytes, key: bytes) -> bytes:
    return Fernet(key).decrypt(token)

def concatUserPass(user,password):
	UserPass = user + "," + password
	return UserPass

def generateFileEncrypt(user,password):
	archiveLock = concatUserPass(user,password)

	key = Fernet.generate_key()

	token = encrypt(archiveLock.encode(), key)


	ArchiveName = os.getcwd() + "\\keepConnect.gen"
	Archive = open(ArchiveName,'w')
	Archive.write(token.decode())
	Archive.write("\n")
	Archive.write(key.decode())
	Archive.close()

def separateUserPass(UserPass):
	UserPass = UserPass.split(',')
	return UserPass[0], UserPass[1]


def openFileEncrypt():
	ArchiveName = os.getcwd() + "\\keepConnect.gen"
	Archive = open(ArchiveName, "r")


	token = []
	for _ in range(2):
		token.append(Archive.readline())

	key = str(token[1]).encode()
	token = str(token[0]).encode()

	UserPass = decrypt(token,key).decode()
	return separateUserPass(UserPass)

if __name__ == "__main__":

	generateFileEncrypt("gatos@gmail.com","perros231")
	user, password = openFileEncrypt()

	print("User = {}\nPassword = {}".format(user,password))

	"""key = Fernet.generate_key()
	print(key.decode())
	message = 'DoCsIsD14z'
	token = encrypt(message.encode(), key)
	print(token)
	print(decrypt(token, key).decode())"""
