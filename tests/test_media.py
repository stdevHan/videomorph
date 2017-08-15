#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# File _name: test_media.py
#
#   VideoMorph - A PyQt5 frontend to ffmpeg and avconv.
#   Copyright 2015-2016 VideoMorph Development Team

#   Licensed under the Apache License, Version 2.0 (the "License");
#   you may not use this file except in compliance with the License.
#   You may obtain a copy of the License at

#       http://www.apache.org/licenses/LICENSE-2.0

#   Unless required by applicable law or agreed to in writing, software
#   distributed under the License is distributed on an "AS IS" BASIS,
#   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#   See the License for the specific language governing permissions and
#   limitations under the License.

"""This module provides tests for media.py module."""

import nose

from videomorph.converter import media
from videomorph.converter import profile
from videomorph.converter import ConversionProfile
from videomorph.converter import ConversionLib


conv_lib = ConversionLib()


# Set of tests for media._MediaFile class
def test_get_name():
    """Test get_name."""
    media_file = _get_media_file_obj()
    assert media_file.get_name() == 'Dad'
    # Another way to do this
    nose.tools.assert_equal(media_file.get_name(), 'Dad')

    # With extension
    assert media_file.get_name(with_extension=True) == 'Dad.mpg'


def test_get_info_with_ffprobe():
    """Test get_info_with_ffprobe."""
    media_file = _get_media_file_obj()

    nose.tools.assert_almost_equal(
        float(media_file.get_info('format_duration')),
        120.72)
    # nose.tools.assert_almost_equal(float(media_file.get_info('file_size')),
    #                                21227416.0)
    # nose.tools.assert_equal(media_file.get_info('format_name'),
    #                         'mpeg')
    # nose.tools.assert_equal(media_file.get_info('format_long_name'),
    #                         'MPEG-PS (MPEG-2 Program Stream)')


# def test_get_info_with_avprobe():
#     media_file = _get_media_file_obj(prober='avprobe')
#
#     nose.tools.assert_almost_equal(float(
#                                    media_file.get_info('format_duration')),
#                                    120.68)
#     nose.tools.assert_almost_equal(float(media_file.get_info('file_size')),
#                                    21227416.0)
#     nose.tools.assert_equal(media_file.get_info('format_name'),
#                             'mpeg')
#     nose.tools.assert_equal(media_file.get_info('format_long_name'),
#                             'MPEG-PS (MPEG-2 Program Stream)')


def test_get_conversion_cmd():
    """Test get_conversion_cmd."""
    media_file = _get_media_file_obj()
    assert media_file.build_conversion_cmd(
        output_dir='.',
        target_quality='DVD Fullscreen (4:3)') == ['-i', 'Dad.mpg', '-f',
                                                   'dvd', '-target',
                                                   'ntsc-dvd', '-vcodec',
                                                   'mpeg2video', '-r',
                                                   '29.97', '-s', '352x480',
                                                   '-aspect', '4:3', '-b:v',
                                                   '4000k', '-mbd', 'rd',
                                                   '-cmp', '2', '-subcmp',
                                                   '2', '-acodec', 'mp2',
                                                   '-b:a', '192k', '-ar',
                                                   '48000', '-ac', '2',
                                                   '-threads', '3', '-y',
                                                   './[DVDF]-Dad.mpg']


def test_profile():
    """Test profile."""
    media_file = _get_media_file_obj()
    assert isinstance(media_file._profile,
                      profile.ConversionProfile)


# Set of tests for media.MediaList class
def test_add_file():
    """Test _add_file."""
    media_file = _get_media_file_obj()
    media_list = _get_media_list_obj(empty=True)

    # testing...
    media_list._add_file(media_file)

    assert len(media_list) == 1
    assert isinstance(media_list[0], media._MediaFile)
    assert media_file is media_list[0]


@nose.tools.raises(media.InvalidMetadataError)
def test_add_file_invalid_metadata():
    """Test _add_file invalid metadata."""
    media_file = _get_media_file_obj()
    media_list = _get_media_list_obj(empty=True)

    media_file.info['format_duration'] = 'wrong'
    media_list._add_file(media_file)
    media_file.info['format_duration'] = 0
    media_list._add_file(media_file)


def test_add_file_twice():
    """Testing adding the same file two times."""
    media_file = _get_media_file_obj()
    media_list = _get_media_list_obj(empty=True)

    # test adding the same file twice
    media_list._add_file(media_file)
    media_list._add_file(media_file)
    assert media_list.length == 1


def test_clear():
    """Test clear."""
    media_list = _get_media_list_obj()

    # Be sure there is one element in the list
    nose.tools.assert_equal(len(media_list), 1)

    media_list.clear()
    nose.tools.assert_equal(len(media_list), 0)


def test_delete_file():
    """Test delete_file."""
    media_list = _get_media_list_obj()

    # Be sure there is one element in the list
    assert len(media_list) == 1

    media_list.delete_file(position=0)
    assert len(media_list) == 0


def test_get_file():
    """Test get_file."""
    media_list = _get_media_list_obj()

    file = media_list.get_file(position=0)
    assert isinstance(file, media._MediaFile)
    assert file is media_list[0]


def test_get_file_name():
    """Test get_file_name."""
    media_list = _get_media_list_obj()
    media_list.position = 0
    name = media_list.running_file.get_name()
    assert name == 'Dad'

    name = media_list.running_file.get_name(with_extension=True)
    assert name == 'Dad.mpg'

    name = media_list.get_file_name(position=0)
    assert name == 'Dad'

    name = media_list.get_file_name(position=0, with_extension=True)
    assert name == 'Dad.mpg'


def test_get_file_path():
    """Test get_file_path."""
    media_list = _get_media_list_obj()

    assert media_list.get_file_path(position=0) == 'Dad.mpg'


def test_lenght():
    """Test lenght."""
    media_list = _get_media_list_obj()

    nose.tools.assert_equal(media_list.length, 1)


def test_duration():
    """Test duration."""
    media_list = _get_media_list_obj()

    # with ffprobe
    nose.tools.assert_almost_equal(media_list.duration, 120.72)


# Helper functions
def _get_media_file_obj(file_path='Dad.mpg'):
    """Helper function to crate a valid file object."""
    profile = ConversionProfile(prober=conv_lib.prober,
                                quality='DVD Fullscreen (4:3)')
    profile.set_xml_root()
    return media._MediaFile(
        file_path,
        profile=profile)


def _get_media_list_obj(empty=False):
    """Helper function to crate a valid media list object."""
    media_list = media.MediaList()

    if not empty:
        media_list._add_file(_get_media_file_obj())

    return media_list


if __name__ == '__main__':
    nose.main()
