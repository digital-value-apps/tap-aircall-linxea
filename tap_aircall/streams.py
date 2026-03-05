"""Stream type classes for tap-aircall."""

from __future__ import annotations

import typing as t
from pathlib import Path

from singer_sdk import typing as th
from singer_sdk.typing import (
    IntegerType,
    StringType,
    DateTimeType,
    ObjectType,
    Property,
    PropertiesList,
    ArrayType,
    BooleanType,
)

from tap_aircall.client import AircallStream


class CallsStream(AircallStream):
    name = "calls"
    path = "/calls"
    primary_keys: t.ClassVar[list[str]] = ["id"]
    replication_key = "started_at"
    records_jsonpath = "$.calls[*]"

    def get_url_params(self, context, next_page_token):
        params = super().get_url_params(context, next_page_token)
        params["fetch_call_timeline"] = "true"
        return params

    schema = PropertiesList(
        Property("id", IntegerType),
        Property("direct_link", StringType),
        Property("started_at", IntegerType),
        Property("answered_at", IntegerType),
        Property("ended_at", IntegerType),
        Property("duration", IntegerType),
        Property("status", StringType),
        Property("direction", StringType),
        Property("raw_digits", StringType),
        Property("asset", StringType),
        Property("recording", StringType),
        Property("voicemail", StringType),
        Property("archived", BooleanType),
        Property("missed_call_reason", StringType),
        Property("cost", StringType),
        Property("number", ObjectType(Property("id", IntegerType))),
        Property("user", ObjectType(Property("id", IntegerType))),
        Property("contact", ObjectType(Property("id", IntegerType))),
        Property("assigned_to", ObjectType(Property("id", IntegerType))),
        Property("transferred_by", ObjectType(Property("id", IntegerType))),
        Property("transferred_to", ObjectType(Property("id", IntegerType))),
        Property("tags", ArrayType(ObjectType(Property("id", IntegerType)))),
        # --- New fields below ---
        Property("sid", StringType),
        Property("recording_short_url", StringType),
        Property("voicemail_short_url", StringType),
        Property(
            "teams",
            ArrayType(
                ObjectType(
                    Property("id", IntegerType),
                    Property("name", StringType),
                    Property("direct_link", StringType),
                )
            ),
        ),
        Property(
            "comments",
            ArrayType(
                ObjectType(
                    Property("id", IntegerType),
                    Property("content", StringType),
                    Property("posted_at", IntegerType),
                    Property(
                        "posted_by",
                        ObjectType(
                            Property("id", IntegerType),
                            Property("name", StringType),
                        ),
                    ),
                )
            ),
        ),
        Property(
            "participants",
            ArrayType(
                ObjectType(
                    Property("id", IntegerType),
                    Property("type", StringType),
                    Property("name", StringType),
                    Property("phone_number", StringType),
                    Property("direct_link", StringType),
                )
            ),
        ),
        Property(
            "ivr_options_selected",
            ArrayType(
                ObjectType(
                    Property("id", StringType),
                    Property("title", StringType),
                    Property("key", StringType),
                    Property("branch", StringType),
                    Property("created_at", StringType),
                    Property("transition_started_at", StringType),
                    Property("transition_ended_at", StringType),
                )
            ),
        ),
    ).to_dict()


class UsersStream(AircallStream):
    name = "users"
    path = "/users"
    primary_keys: t.ClassVar[list[str]] = ["id"]
    records_jsonpath = "$.users[*]"
    schema = PropertiesList(
        Property("id", IntegerType),
        Property("direct_link", StringType),
        Property("name", StringType),
        Property("email", StringType),
        Property("created_at", DateTimeType),
        Property("available", BooleanType),
        Property("availability_status", StringType),
        Property(
            "numbers", ArrayType(ObjectType(Property("id", IntegerType)))
        ),
        Property("time_zone", StringType),
        Property("language", StringType),
        Property("wrap_up_time", IntegerType),
        # --- New fields below ---
        Property("substatus", StringType),
        Property("extension", StringType),
        Property("default_number_id", IntegerType),
    ).to_dict()


class NumbersStream(AircallStream):
    name = "numbers"
    path = "/numbers"
    primary_keys: t.ClassVar[list[str]] = ["id"]
    records_jsonpath = "$.numbers[*]"
    schema = PropertiesList(
        Property("id", IntegerType),
        Property("direct_link", StringType),
        Property("name", StringType),
        Property("digits", StringType),
        Property("created_at", DateTimeType),
        Property("country", StringType),
        Property("time_zone", StringType),
        Property("open", BooleanType),
        Property("availability_status", StringType),
        Property("is_ivr", BooleanType),
        Property("priority", IntegerType),
        # --- New fields below ---
        Property("e164_digits", StringType),
        Property("live_recording_activated", BooleanType),
        Property(
            "users", ArrayType(ObjectType(Property("id", IntegerType)))
        ),
        Property(
            "messages",
            ObjectType(
                Property("welcome", StringType),
                Property("waiting", StringType),
                Property("ringing_tone", StringType),
                Property("unanswered_call", StringType),
                Property("after_hours", StringType),
                Property("ivr", StringType),
                Property("voicemail", StringType),
                Property("closed", StringType),
                Property("callback_later", StringType),
                Property("callback_unavailable", StringType),
            ),
        ),
    ).to_dict()


class ContactsStream(AircallStream):
    name = "contacts"
    path = "/contacts"
    primary_keys: t.ClassVar[list[str]] = ["id"]
    records_jsonpath = "$.contacts[*]"
    schema = PropertiesList(
        Property("id", IntegerType),
        Property("direct_link", StringType),
        Property("first_name", StringType),
        Property("last_name", StringType),
        Property("company_name", StringType),
        Property("description", StringType),
        Property("information", StringType),
        Property("is_shared", BooleanType),
        # --- New fields below ---
        Property("created_at", IntegerType),
        Property("updated_at", IntegerType),
        Property(
            "phone_numbers",
            ArrayType(
                ObjectType(
                    Property("id", IntegerType),
                    Property("label", StringType),
                    Property("value", StringType),
                )
            ),
        ),
        Property(
            "emails",
            ArrayType(
                ObjectType(
                    Property("id", IntegerType),
                    Property("label", StringType),
                    Property("value", StringType),
                )
            ),
        ),
    ).to_dict()


class TagsStream(AircallStream):
    name = "tags"
    path = "/tags"
    primary_keys: t.ClassVar[list[str]] = ["id"]
    records_jsonpath = "$.tags[*]"
    schema = PropertiesList(
        Property("id", IntegerType),
        Property("direct_link", StringType),
        Property("name", StringType),
        Property("color", StringType),
        Property("description", StringType),
    ).to_dict()
