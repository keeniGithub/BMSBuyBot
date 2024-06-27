import paramiko

def download_file_sftp(hostname, port, username, password, remote_filepath, local_filepath):
    try:
        transport = paramiko.Transport((hostname, port))
        transport.connect(username=username, password=password)
        sftp = paramiko.SFTPClient.from_transport(transport)
        
        sftp.get(remote_filepath, local_filepath)
        
        sftp.close()
        transport.close()
        print(f"File {remote_filepath} downloaded successfully to {local_filepath}")
    except Exception as e:
        print(f"Error: {e}")

def upload_file_sftp(hostname, port, username, password, local_filepath, remote_filepath):
    try:
        transport = paramiko.Transport((hostname, port))
        transport.connect(username=username, password=password)
        sftp = paramiko.SFTPClient.from_transport(transport)
        
        sftp.put(local_filepath, remote_filepath)
        
        sftp.close()
        transport.close()
        print(f"File {local_filepath} uploaded successfully to {remote_filepath}")
    except Exception as e:
        print(f"Error: {e}")