import time

from services import AzureService
from config import DL_PREFIX, OWNER_EMAIL, MEMBER_EMAIL


def main():
    azure_client = AzureService()

    dl_name = f"{DL_PREFIX} {int(time.time())}"
    dl_list = azure_client.create_dl(
        dl_name=dl_name,
        owner_list=OWNER_EMAIL,
        member_list=MEMBER_EMAIL
    )

    print(dl_list)
