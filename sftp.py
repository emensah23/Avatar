import sys

# Try to import pysftp, but don't fail the whole program if it's incompatible
try:
    import pysftp
    _HAVE_PYSFTP = True
    _PYSFTP_IMPORT_ERROR = None
except Exception as e:
    pysftp = None
    _HAVE_PYSFTP = False
    _PYSFTP_IMPORT_ERROR = e

#this file is expected to be modifed once for every single chromebook in our BCI lab
class fileTransfer:
    def __init__(self, host='', username='', private_key='', private_key_pass='', ignore_host_key=False):
        self.host = host  # change
        self.username = username  # change
        self.private_key = private_key  # change
        self.private_key_pass = private_key_pass  # change
        self.port = 22
        # Delay connecting until explicitly requested; store None if pysftp unavailable
        self.serverconn = None
        if _HAVE_PYSFTP:
            self.serverconn = self.connect(ignore_host_key)

    def connect(self, ignore_host_key):
        """Connects to the sftp server and returns the sftp connection object"""
        if not _HAVE_PYSFTP:
            raise ImportError(
                "pysftp is not available or failed to import: %s.\n" 
                "Install a compatible version of pysftp/paramiko or update the code to use paramiko directly." % _PYSFTP_IMPORT_ERROR
            )

        try:
            cnopts = None

            if ignore_host_key:
                cnopts = pysftp.CnOpts()
                cnopts.hostkeys = None

            # Get the sftp connection object
            serverconn = pysftp.Connection(
                host=self.host,
                username=self.username,
                private_key=self.private_key,  # make secret
                private_key_pass=self.private_key_pass,  # make secret
                port=self.port,
                cnopts=cnopts
            )
            if (serverconn):
                print("Connected to host...")
            return serverconn
        except Exception as err:
            print(err)
            raise Exception(err)

    def transfer(self, src, target):
        """Recursivily places files in the target dir, copies everything inside of src dir"""
        try:
            print(f"Transfering files to {self.host} ...")
            self.serverconn.put_r(str(src), str(target))
            print("Files Successfully Transfered!")
            print(
                f"Src files placed in Dir: {self.serverconn.listdir(target)}")

        except Exception as err:
            raise Exception(err)


def main():
    svrcon = fileTransfer()
    src = sys.argv[1]
    target = sys.argv[2]
    svrcon.transfer(str(src), (target))


if __name__ == '__main__':
    main()
