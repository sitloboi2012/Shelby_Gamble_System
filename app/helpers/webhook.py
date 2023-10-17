# -*- coding: utf-8 -*-
"""Webhook stuff"""


class Webhook:
    def __init__(self):
        import requests

        self.session = requests.Session()

        self.customization = {}
        self.webhook_api = None

        self._embed_properties = (
            'title',
            'type',
            'description',
            'url',
            'timestamp',
            'color',
            'footer',
            'image',
            'thumbnail',
            'video',
            'provider',
            'author',
            'fields',
        )

    def send(self, *, webhook_api=None, body=None, embed=None, is_raw=False):
        """The full body of a webhook call looks like this
        {
            'content': 'hi',
            'username': 'abc',
            'embeds': [
                {'title': 'embed1'},
                {'title': 'embed2'}
            ]
        }

        When we only want to send an embed however, it still have to be sent in that form

        References:
        https://discordapp.com/developers/docs/resources/webhook#execute-webhook
        https://discordapp.com/developers/docs/resources/channel#embed-object

        Arguments:
            webhook_api {[type]} -- [description]
            body {[type]} -- [description]
        """
        _api = webhook_api or self.webhook_api

        if not _api:
            return 'You have to either setup api or pass the api to the function.'

        if not body and not embed:
            return 'Cannot send empty message'

        if embed:
            body = body or {}
            body['embeds'] = embed if isinstance(embed, list) else [embed]

        _body = body if is_raw else self._customize(body) #type: ignore
        response = self.session.post(_api, json=_body)

        if response.status_code not in (200, 204):
            self.session.post(
                _api,
                json=self._customize(
                    {
                        'content': f"<@128376038605586432> **{response.status_code}** - ```json\n{response.text}'"[
                            :2045
                        ]
                        + '```'
                    }
                ),
            )

        return response

    def customize(self, **kwargs):
        """[summary]"""
        for key, value in kwargs.items():
            if key in self.__dict__:
                setattr(self, key, value)
            else:
                self.customization[key] = value

    def _customize(self, body: dict) -> dict:
        """[summary]
        For references:
        https://discordapp.com/developers/docs/resources/webhook#execute-webhook
        https://discordapp.com/developers/docs/resources/channel#embed-object

        Arguments:
            body {[type]} -- [description]
        """
        _body = dict(body)

        for key in ('username', 'avatar_url'):
            if key not in _body and key in self.customization:
                _body[key] = self.customization[key]

        if 'embeds' in _body:
            for embed in _body['embeds']:
                for key in self._embed_properties:
                    if key not in embed and key in self.customization:
                        embed[key] = self.customization[key]

        return _body
