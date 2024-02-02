import requests
import msal
from config import AZURE_CLIENT_ID, AZURE_TENANT_ID, AZURE_THUMBPRINT, AZURE_PRIVATE_KEY


class AzureService:

    def __init__(self):
        self.azure_client = msal.ConfidentialClientApplication(
            AZURE_CLIENT_ID,
            authority="https://login.microsoftonline.com/" +
            AZURE_TENANT_ID,
            client_credential={
                "thumbprint": AZURE_THUMBPRINT,
                "private_key": self._get_private_key()
            },
            token_cache=msal.TokenCache(),
        )
        # print(self._get_private_key())

    def _get_private_key(self):
        ssl_key_content = "\n".join(
            AZURE_PRIVATE_KEY.split(" ")[3:-3]
        )
        return f"-----BEGIN PRIVATE KEY----- \n{ssl_key_content} \n-----END PRIVATE KEY-----"

    def _get_access_token(self):
        result = self.azure_client.acquire_token_for_client(
            scopes=["https://graph.microsoft.com/.default"]
        )

        if "access_token" in result:
            return result['access_token']
        else:
            raise Exception("Can not get access token from Azure.")

    def get_dl_data(self, user_principal_name='andy_pan@trendmicro.com'):
        access_token = self._get_access_token()
        graph_data = requests.get(
            f"https://graph.microsoft.com/v1.0/users/{user_principal_name}/transitiveMemberOf?$top=999",
            headers={'Authorization': f'Bearer {access_token}'}
        ).json()

        dl_list = []
        for data in graph_data['value']:
            dl_list.append(data['displayName'])

        return dl_list

    def create_dl(self, dl_name, owner_list, member_list):
        """
        Ref: https://learn.microsoft.com/zh-tw/graph/api/group-post-groups?view=graph-rest-1.0&tabs=http#request-body
        """
        mail_nickname = dl_name.replace(" ", "").lower()

        post_json_data = {
            "description": "This is a group for testing.",
            "displayName": dl_name,
            "groupTypes": [
                "Unified"
            ],
            "mailEnabled": True,
            "mailNickname": mail_nickname,
            "securityEnabled": True,
            "isAssignableToRole": False,
        }
        post_json_data['owners@odata.bind'] = [
            f"https://graph.microsoft.com/v1.0/users/{owner}" for owner in owner_list.split(',')
        ]
        post_json_data['members@odata.bind'] = [
            f"https://graph.microsoft.com/v1.0/users/{member}" for member in member_list.split(',')
        ]

        access_token = self._get_access_token()
        graph_data = requests.post(
            f"https://graph.microsoft.com/v1.0/groups",
            headers={'Authorization': f'Bearer {access_token}'},
            json=post_json_data
        ).json()

        return graph_data
