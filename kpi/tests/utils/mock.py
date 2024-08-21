# coding: utf-8
import json
import lxml
import os
from mimetypes import guess_type
from tempfile import NamedTemporaryFile
from typing import Optional
from urllib.parse import parse_qs, unquote

from django.conf import settings
from django.core.files import File
from rest_framework import status

from kpi.mixins.audio_transcoding import AudioTranscodingMixin
from kpi.models.asset_snapshot import AssetSnapshot
from kpi.tests.utils.xml import get_form_and_submission_tag_names


def enketo_edit_instance_response(request):
    """
    Simulate Enketo response
    """
    # Decode `x-www-form-urlencoded` data
    body = {k: v[0] for k, v in parse_qs(unquote(request.body)).items()}

    resp_body = {
        'edit_url': (
            f"{settings.ENKETO_URL}/edit/{body['instance_id']}"
        )
    }
    headers = {}
    return status.HTTP_201_CREATED, headers, json.dumps(resp_body)


def enketo_edit_instance_response_with_root_name_validation(request):
    """
    Simulate Enketo response and validate root names
    """
    # Decode `x-www-form-urlencoded` data
    body = {k: v[0] for k, v in parse_qs(unquote(request.body)).items()}

    submission = body['instance']
    snapshot = AssetSnapshot.objects.get(uid=body['form_id'])

    (
        form_root_name,
        submission_root_name,
    ) = get_form_and_submission_tag_names(snapshot.xml, submission)

    assert form_root_name == submission_root_name

    resp_body = {
        'edit_url': (
            f"{settings.ENKETO_URL}/edit/{body['instance_id']}"
        )
    }
    headers = {}
    return status.HTTP_201_CREATED, headers, json.dumps(resp_body)


def enketo_edit_instance_response_with_uuid_validation(request):
    """
    Simulate Enketo response and validate that formhub/uuid and meta/instanceID
    are present and non-empty
    """
    # Decode `x-www-form-urlencoded` data
    body = {k: v[0] for k, v in parse_qs(unquote(request.body)).items()}

    submission = body['instance']
    submission_xml_root = lxml.etree.fromstring(submission)
    assert submission_xml_root.find(
        'formhub/uuid'
    ).text.strip()
    assert submission_xml_root.find(
        'meta/instanceID'
    ).text.strip()

    resp_body = {
        'edit_url': (
            f"{settings.ENKETO_URL}/edit/{body['instance_id']}"
        )
    }
    headers = {}
    return status.HTTP_201_CREATED, headers, json.dumps(resp_body)


def enketo_view_instance_response(request):
    """
    Simulate Enketo response
    """
    # Decode `x-www-form-urlencoded` data
    body = {k: v[0] for k, v in parse_qs(unquote(request.body)).items()}

    resp_body = {
        'view_url': (
            f"{settings.ENKETO_URL}/view/{body['instance_id']}"
        )
    }
    headers = {}
    return status.HTTP_201_CREATED, headers, json.dumps(resp_body)


class MockAttachment(AudioTranscodingMixin):
    """
    Mock object to simulate KobocatAttachment.
    Relationship with ReadOnlyKobocatInstance is ignored but could be implemented
    """
    def __init__(self, pk: int, filename: str, mimetype: str = None, **kwargs):

        self.id = pk  # To mimic Django model instances
        self.pk = pk
        basename = os.path.basename(filename)
        file_ = os.path.join(
            settings.BASE_DIR,
            'kpi',
            'tests',
            basename
        )

        self.media_file = File(open(file_, 'rb'), basename)
        self.media_file.path = file_
        self.media_file_size = os.path.getsize(file_)
        self.content = self.media_file.read()
        self.media_file_basename = basename
        if not mimetype:
            self.mimetype, _ = guess_type(file_)
        else:
            self.mimetype = mimetype

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.media_file.close()

    @property
    def absolute_path(self):
        return self.media_file.path

    def protected_path(self, format_: Optional[str] = None):
        if format_ == 'mp3':
            suffix = f'.mp3'
            with NamedTemporaryFile(suffix=suffix) as f:
                self.content = self.get_transcoded_audio('mp3')
            return f.name
        else:
            return self.absolute_path
