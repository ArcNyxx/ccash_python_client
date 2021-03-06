#!/bin/python3
# ccash_python_client - ccash python client
# Copyright (C) 2021 FearlessDoggo21
# see LICENCE for licensing information

from requests import get, post, delete, patch, Response
from .inc import User


class CCash:
    '''The CCash client class'''
    def __init__(self, domain: str, timeout=20):
        self.timeout = timeout
        if domain[-1] != '/':
            domain += '/'

        try:
            properties = get(
                domain + "api/properties", timeout=self.timeout
            ).json()
        except Exception as error:
            print("\x1b[1m\x1b[31mThe server is most likely not running.\x1b[m")
            raise error

        self.version = properties["version"]
        self.log_max = properties["max_log"]
        self.ret_del = properties.get("return_on_del", "")

        self.domain = domain + "api/v" + str(self.version)


    def close(self, admin: User) -> Response:
        '''Safely closes the server and saves its current state.'''
        return post(
            self.domain + "/admin/shutdown",
            timeout=self.timeout,
            headers={
                "Accept": "*/*",
                "Authorization": admin.auth_encode()
            }
        )


    def new_user(self, user: User) -> Response:
        '''Creates a new user without an initial balance.'''
        return post(
            self.domain + "/user/register",
            timeout=self.timeout,
            headers={"Accept": "*/*"},
            json=user.to_dict()
        )


    def admin_new_user(self, admin: User, user: User,
            amount: int) -> Response:
        '''Creates a new user with an initial balance.'''
        return post(
            self.domain + "/admin/user/register",
            timeout=self.timeout,
            headers={
                "Accept": "*/*",
                "Authorization": admin.auth_encode()
            },
            json={"name": user.name, "amount": amount, 
                    "pass": user.passwd}
        )


    def del_user(self, user: User) -> Response:
        '''Deletes a user.'''
        return delete(
            self.domain + "/user/delete",
            timeout=self.timeout,
            headers={
                "Accept": "*/*",
                "Authorization": user.auth_encode()
            }
        )


    def admin_del_user(self, admin: User, name: str) -> Response:
        '''Deletes a user via the admin password.'''
        return delete(
            self.domain + "/admin/user/delete",
            timeout=self.timeout,
            headers={
                "Accept": "*/*",
                "Authorization": admin.auth_encode()
            },
            json={"name": name}
        )


    def user_exists(self, name: str) -> Response:
        '''Confirms if a user exists.'''
        return get(
            self.domain + f"/user/exists?name={name}",
            timeout=self.timeout,
            headers={"Accept": "*/*"}
        )


    def verify_passwd(self, user: User) -> Response:
        '''Confirms a users password.  
        If a `False` value returned, the user may not exist.'''
        return post(
            self.domain + "/user/verify_password",
            timeout=self.timeout,
            headers={
                "Accept": "*/*",
                "Authorization": user.auth_encode()
            }
        )


    def verify_admin(self, admin: User) -> Response:
        '''Confirms the admin account.'''
        return post(
            self.domain + "/admin/verify_account",
            timeout=self.timeout,
            headers={
                "Accept": "*/*",
                "Authorization": admin.auth_encode()
            }
        )


    def change_passwd(self, user: User, passwd: str) -> Response:
        '''Changes a user password.'''
        return patch(
            self.domain + "/user/change_password",
            timeout=self.timeout,
            headers={
                "Accept": "*/*",
                "Authorization": user.auth_encode()
            },
            json={"pass": passwd}
        )


    def admin_change_passwd(self, admin: User, name: str, \
            passwd: str) -> Response:
        '''Changes a user password via the admin password.'''
        return patch(
            self.domain + "/admin/user/change_password",
            timeout=self.timeout,
            headers={
                "Accept": "*/*",
                "Authorization": admin.auth_encode()
            },
            json={"name": name, "pass": passwd}
        )


    def get_bal(self, name: str) -> Response:
        '''Gets the balance of a user.  
        Returns 0 if the user does not exist.'''
        return get(
            self.domain + f"/user/balance?name={name}",
            timeout=self.timeout,
            headers={"Accept": "*/*"}
        )


    def set_bal(self, admin: User, name: str, balance: int) -> \
            Response:
        '''Sets the balance of a user.'''
        return patch(
            self.domain + "/admin/set_balance",
            timeout=self.timeout,
            headers={
                "Accept": "*/*",
                "Authorization": admin.auth_encode()
            },
            json={"name": name, "amount": balance}
        )


    def impact_bal(self, admin: User, name: str, amount: int) -> \
            Response:
        '''Offsets the balance of a user.'''
        return post(
            self.domain + "/admin/impact_balance",
            timeout=self.timeout,
            headers={
                "Accept": "*/*",
                "Authorization": admin.auth_encode()
            },
            json={"name": name, "amount": amount}
        )


    def get_logs(self, user: User) -> Response:
        '''Returns the logged transactions of a user.'''
        return get(
            self.domain + "/user/log",
            timeout = self.timeout,
            headers={
                "Accept": "*/*",
                "Authorization": user.auth_encode()
            }
        )


    def send(self, user: User, name: str, amount: str) -> Response:
        '''Sends an amount to another user.'''
        return post(
            self.domain + "/user/transfer",
            timeout=self.timeout,
            headers={
                "Accept": "*/*",
                "Authorization": user.auth_encode()
            },
            json={"name": name, "amount": amount}
        )


    def prune(self, admin: User, time: int, amount: int) -> Response:
        '''Deletes all users older than time and which have less
        money than amount.'''
        return post(
            self.domain + "/admin/prune_users",
            timeout=self.timeout,
            headers={
                "Accept": "*/*",
                "Authorization": admin.auth_encode()
            },
            json={"time": time, "amount": amount}
        )
