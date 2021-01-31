from __future__ import annotations

import random
import string
from abc import ABC, abstractmethod

import requests

BASE_URL = "http://127.0.0.1:8080/api/v1"


def get_random_string(length):
    return ''.join(random.choice(string.ascii_letters) for x in range(length))


class RandomField(ABC):
    @abstractmethod
    def get_random_value(self):
        pass


class RandomEmail(RandomField):
    def get_random_value(self):
        return get_random_string(8) + "@gmail.com"


class RandomPassword(RandomField):
    def get_random_value(self):
        return get_random_string(8)


class RandomBoolean(RandomField):
    def get_random_value(self):
        return bool(random.getrandbits(1))


class RandomString(RandomField):
    def get_random_value(self):
        return get_random_string(30)


class RandomPostIdGenerator(RandomField):
    def __init__(self, list_action):
        self.list_action = list_action

    def get_random_value(self):
        data = self.list_action.perform_action().json()
        return random.choice([each["id"] for each in data])


class RandomPayloadGenerator:
    generate_ones = False
    __previous = None

    def generate_payload(self):
        if self.generate_ones and self.__previous:
            return self.__previous
        self.__previous = {}
        for field in filter(lambda x: not x.startswith("_") and x not in ("generate_payload", "generate_ones"),
                            self.__dir__()):
            self.__previous[field] = self.__getattribute__(field).get_random_value()
        return self.__previous


class RandomUrlGenerator:
    def __init__(self, base_url: str, generator: RandomPayloadGenerator):
        self.base_url = base_url
        self.generator = generator

    def __str__(self):
        return self.base_url.format(**self.generator.generate_payload())


class SignUpPayload(RandomPayloadGenerator):
    email = RandomEmail()
    password = RandomPassword()


class PostCreationPayload(RandomPayloadGenerator):
    title = RandomString()
    body = RandomString()


class PostRandomLikePayload(RandomPayloadGenerator):
    liked = RandomBoolean()


class PostRandomId(RandomPayloadGenerator):
    def __init__(self, list_action):
        self.id = RandomPostIdGenerator(list_action)


class Executor(ABC):
    @abstractmethod
    def execute(self, *args, **kwargs):
        pass


class WebExecutor(ABC):
    headers = {}

    def __init__(self, bot_identifier: str = "Uidentified Bot"):
        self.bot_identifier = bot_identifier

    def execute(self, request_path, request_method, payload: RandomPayloadGenerator) -> requests.Response:
        kwargs = {
            "method": request_method,
            "url": BASE_URL + str(request_path),
            "headers": self.headers
        }
        if payload:
            kwargs.update({"data": payload.generate_payload()})
        res = requests.request(**kwargs)
        print(f"{self.bot_identifier} | {request_path} | {request_method} | {res.status_code}")
        res.raise_for_status()
        return res

    @classmethod
    def get_authorized_web_executor(cls, auth_headers: dict):
        executor = cls()
        executor.headers.update(auth_headers)
        return executor


class Action(ABC):
    @abstractmethod
    def perform_action(self):
        pass


class WebAction(Action):
    def __init__(self, action_name: str, request_path: [str, RandomUrlGenerator], request_method: str,
                 payload: RandomPayloadGenerator = None):
        self.action_name = action_name
        self.request_path = request_path
        self.request_method = request_method
        self.payload = payload
        self.executor: WebExecutor = None
        self._bot = None

    def perform_action(self):
        if not self.executor:
            raise RuntimeError("WebExecutor wasn't set up for this action")
        return self.executor.execute(self.request_path, self.request_method, self.payload)


class ActionsRegistry:
    def __init__(self, *actions_):
        self.actions = actions_

    def __iter__(self):
        self.n = 0
        return self

    def __next__(self):
        if self.n < len(self.actions):
            i = self.actions[self.n]
            self.n = self.n + 1
            return i
        raise StopIteration


# post_create_action = WebAction("create_post", "/posts/", "POST", PostCreationPayload())
# post_list_action = WebAction("list_posts", "/posts/", "GET")
# post_like_action = WebAction("like_posts", RandomUrlGenerator("/posts/{id}", PostRandomId), "POST",
#                              PostRandomLikePayload())


class Bot:
    sign_up_action = WebAction("sign_up", "/sign-up/", "POST")
    sign_in_action = WebAction("sign_in", "/token/", "POST")

    def _retrieve_auth_data(self):
        creds = SignUpPayload()
        creds.generate_ones = True
        unauthorized_executor = WebExecutor()
        self.sign_up_action.executor = unauthorized_executor
        self.sign_in_action.executor = unauthorized_executor
        self.sign_up_action.payload = creds
        self.sign_up_action.perform_action()
        self.sign_in_action.payload = creds
        res = self.sign_in_action.perform_action().json()
        return {"Authorization": f"Bearer {res['token']}"}

    def __init__(self, bot_name: str, *actions):
        self.name = bot_name
        self.auth_executor = WebExecutor.get_authorized_web_executor(self._retrieve_auth_data())
        self.auth_executor.bot_identifier = self.name
        self.actions = actions

    def __init_actions__(self):
        for each in self.actions:
            each.executor = self.auth_executor

    def run(self):
        print(f"Starting bot {self.name}")
        for each in self.actions:
            each.perform_action()

    @classmethod
    def get_from_conf(cls, name, max_posts_per_user, max_likes_per_user):
        bot = cls(name)
        post_list_action = WebAction("post_list", "/posts/", "GET", None)
        post_list_action.executor = bot.auth_executor
        actions = []
        for _ in range(max_posts_per_user):
            actions.append(WebAction("create_post", "/posts/", "POST", PostCreationPayload()))
        for _ in range(max_likes_per_user):
            actions.append(
                WebAction("like_posts", RandomUrlGenerator("/posts/{id}", PostRandomId(post_list_action)), "PATCH",
                          PostRandomLikePayload()))
        bot.actions = actions
        bot.__init_actions__()
        return bot